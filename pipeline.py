import os
import streamlit as st
import whisper
from transformers import pipeline as hf_pipeline
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client once at top of pipeline.py
# We handle the case where the API key is not set or is the placeholder value
api_key = os.getenv("GROQ_API_KEY")
if not api_key or api_key == "your_existing_groq_key_here":
    client = None
else:
    try:
        client = Groq(api_key=api_key)
    except Exception:
        client = None

@st.cache_resource
def load_whisper_model():
    """Loads the Whisper 'small' model."""
    try:
        return whisper.load_model("small")
    except Exception as e:
        st.error(f"Failed to load Whisper model: {str(e)}\nCheck internet connection for first run.")
        raise e

@st.cache_resource
def load_sentiment_pipeline():
    """Loads the RoBERTa sentiment model on CPU."""
    try:
        return hf_pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            truncation=True,
            max_length=512,
            device=-1
        )
    except Exception as e:
        st.error(f"Failed to load Sentiment model: {str(e)}\nCheck internet connection for first run.")
        raise e

@st.cache_resource
def load_intent_pipeline():
    """Loads the MiniLM intent model on CPU."""
    try:
        return hf_pipeline(
            "zero-shot-classification",
            model="typeform/distilbert-base-uncased-mnli",
            device=-1
        )
    except Exception as e:
        st.error(f"Failed to load Intent model: {str(e)}\nCheck internet connection for first run.")
        raise e

def transcribe_audio(file_path: str) -> list[dict]:
    """Transcribes audio and returns a list of segment dictionaries."""
    try:
        model = load_whisper_model()
        result = model.transcribe(
            file_path,
            word_timestamps=False,
            verbose=False,
            condition_on_previous_text=False,  # Prevents hallucination snowballing between segments
            no_speech_threshold=0.6,           # Whisper skips segments it's >60% sure are silence
            language="en"                      # Remove this line if audio is not always English
        )

        data_list = []
        for segment in [s for s in result.get("segments", []) if s.get("no_speech_prob", 0.0) < 0.6]:
            text = segment.get("text", "").strip()
            if not text:
                continue
                
            # Do not split segments further unless a segment exceeds 100 words
            words = text.split()
            if len(words) > 100:
                chunk_size = 100
                for i in range(0, len(words), chunk_size):
                    chunk_text = " ".join(words[i:i + chunk_size])
                    data_list.append({
                        "text": chunk_text,
                        "start": segment.get("start", 0.0),
                        "end": segment.get("end", 0.0)
                    })
            else:
                data_list.append({
                    "text": text,
                    "start": segment.get("start", 0.0),
                    "end": segment.get("end", 0.0)
                })
        return data_list
    except Exception as e:
        st.error(f"Whisper transcription failed: {str(e)}")
        return []

def analyse_sentiment(data: list[dict]) -> list[dict]:
    """Adds sentiment and sentiment_score to each segment."""
    try:
        sentiment_model = load_sentiment_pipeline()
    except Exception:
        for segment in data:
            segment["sentiment"] = "error"
            segment["sentiment_score"] = 0.0
        return data

    label_map = {
        "LABEL_0": "Negative",
        "LABEL_1": "Neutral",
        "LABEL_2": "Positive",
        "negative": "Negative",
        "neutral": "Neutral",
        "positive": "Positive"
    }

    for segment in data:
        try:
            text = segment.get("text", "")
            # Filter segments under 3 words
            if len(text.split()) < 3:
                segment["sentiment"] = "skip"
                segment["sentiment_score"] = 0.0
                continue
                
            result = sentiment_model(text)[0]
            label = result.get("label", "")
            score = result.get("score", 0.0)
            
            segment["sentiment"] = label_map.get(label, "Unknown")
            segment["sentiment_score"] = round(score, 4)
        except Exception:
            segment["sentiment"] = "error"
            segment["sentiment_score"] = 0.0
            
    return data

def detect_intent(data: list[dict]) -> list[dict]:
    """Adds intent to each segment."""
    try:
        intent_model = load_intent_pipeline()
    except Exception:
        for segment in data:
            segment["intent"] = "error"
        return data

    candidate_labels = [
        "billing query", "technical support", "cancellation request", 
        "upgrade request", "general inquiry", "complaint"
    ]

    for segment in data:
        try:
            if segment.get("sentiment") == "skip":
                segment["intent"] = "skip"
                continue
                
            text = segment.get("text", "")
            result = intent_model(text, candidate_labels)
            top_label = result['labels'][0]
            top_score = result['scores'][0]
            
            if top_score < 0.4:
                segment["intent"] = "unclear"
            else:
                segment["intent"] = top_label
        except Exception:
            segment["intent"] = "error"
            
    return data

def generate_summary(transcript_text: str) -> str:
    """Generates a Groq summary from the plain text transcript."""
    if client is None:
        return "Summary unavailable (Groq API key missing or invalid)"
        
    system_prompt = (
        "You are summarising a customer service call transcript.\n"
        "Reply in exactly 3 bullet points:\n"
        "1. What the caller wanted\n"
        "2. How the conversation went\n"
        "3. What the outcome or next step was\n"
        "Be concise. Maximum 2 sentences per bullet point."
    )
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript_text}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception:
        return "Summary unavailable"

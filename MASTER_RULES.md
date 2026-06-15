# MASTER PROJECT RULES — Voice Sentiment Analytics Pipeline

NON-NEGOTIABLE — every line of code must adhere to this document.
If a rule conflicts with a suggestion from any source including the LLM, this document wins. No exceptions.

=== TECH STACK — FIXED, NO SUBSTITUTIONS ===

Language:         Python 3.10+
UI:               Streamlit — no Flask, no FastAPI, no Gradio
Speech-to-Text:   openai-whisper (local, model size: small)
Sentiment Model:  cardiffnlp/twitter-roberta-base-sentiment-latest (via HuggingFace transformers, runs locally)
Intent Model:     cross-encoder/nli-MiniLM2-L6-H64 (via HuggingFace transformers, runs locally)
LLM Summary:      Groq API — model: llama-3.3-70b-versatile
Graphing:         Plotly (via streamlit plotly chart)
Env management:   python-dotenv
API keys:         Groq only — existing key from previous project works

DO NOT use:
— OpenAI API (not needed, Groq replaces it)
— Flask or FastAPI (Streamlit handles everything)
— facebook/bart-large-mnli (too heavy, crashes 7GB RAM)
— Any cloud ML APIs for sentiment or intent (defeats the purpose)
— Threading or async anywhere in the pipeline
— Any model size above "small" for Whisper
— CUDA or GPU specific code (Windows CPU only machine)

=== FILE STRUCTURE — FIXED ===

app.py            — Streamlit UI only, zero ML logic here
pipeline.py       — all ML functions, zero Streamlit imports here
utils.py          — text cleaning and formatting helpers only
requirements.txt  — all dependencies listed below
.env              — API keys only, never commit to GitHub
README.md         — demo gif, what it does, how to run locally

No additional files to be created without explicit instruction.
No renaming of these files.

=== REQUIREMENTS.TXT — EXACT, NO ADDITIONS ===

openai-whisper
transformers
torch
streamlit
plotly
groq
python-dotenv

=== .ENV FILE — EXACT FORMAT ===

GROQ_API_KEY=your_existing_groq_key_here

No other keys needed. No OpenAI key. No HuggingFace token needed for these models as they are public.

=== ARCHITECTURE RULES ===

1. All models load ONCE at app startup using @st.cache_resource decorator
   — Never load models inside a button click or function called repeatedly
   — Reason: RoBERTa and BART take 30-60 seconds to load, reloading on every click will freeze the app completely

2. Pipeline runs in this exact order, no skipping, no reordering:
   Audio file
   → Whisper transcription → List of segments with timestamps
   → RoBERTa sentiment → sentiment + score added to each segment
   → BART intent → intent added to each segment
   → Plotly graph built from segment data
   → Groq summary from plain text transcript
   → Streamlit displays everything

3. All data passed between pipeline steps must follow this exact shape:
   [
     {
       "text": "sentence here",
       "start": 0.0,
       "end": 2.4,
       "sentiment": "POSITIVE",
       "sentiment_score": 0.94,
       "intent": "billing query"
     }
   ]
   — Every pipeline function receives this list
   — Every pipeline function returns this list with new fields added
   — Never remove fields, never rename fields, only add new ones
   — This shape is used from Whisper output all the way to Streamlit display

=== MODEL RULES ===

4. Whisper
   — Model size: "small" — non-negotiable
   — Parameters: word_timestamps=False, verbose=False
   — Whisper returns segments, treat each segment as one unit
   — Do not split segments further unless a segment exceeds 100 words
   — Output must be converted to the data shape in rule 3 immediately after transcription before passing to next step

5. RoBERTa sentiment
   — Model: "cardiffnlp/twitter-roberta-base-sentiment-latest"
   — Load via:
     pipeline("sentiment-analysis",
     model="cardiffnlp/twitter-roberta-base-sentiment-latest",
     truncation=True,
     max_length=512,
     device=-1)
   — device=-1 forces CPU, mandatory on this machine
   — Label mapping, apply this every time without exception:
     LABEL_0 = Negative
     LABEL_1 = Neutral
     LABEL_2 = Positive
   — Run on each segment individually, never pass full transcript at once
   — If segment is under 3 words set sentiment="skip", score=0.0 and move on without calling the model

6. Intent classification
   — Model: "cross-encoder/nli-MiniLM2-L6-H64"
   — Load via:
     pipeline("zero-shot-classification",
     model="cross-encoder/nli-MiniLM2-L6-H64",
     device=-1)
   — device=-1 mandatory
   — Candidate labels, use exactly these, no changes:
     ["billing query", "technical support", "cancellation request", "upgrade request", "general inquiry", "complaint"]
   — Take only the top scoring label
   — If top label score is below 0.4 set intent="unclear"
   — If segment sentiment is "skip" also set intent="skip", do not call the model

7. Groq summary
   — Client initialised once at top of pipeline.py:
     client = Groq(api_key=os.getenv("GROQ_API_KEY"))
   — Model: "llama-3.3-70b-versatile"
   — Max tokens: 200
   — Input: plain text transcript only, not the full data structure
   — System prompt, use exactly this:
     "You are summarising a customer service call transcript.
     Reply in exactly 3 bullet points:
     1. What the caller wanted
     2. How the conversation went
     3. What the outcome or next step was
     Be concise. Maximum 2 sentences per bullet point."
   — Call structure:
     response = client.chat.completions.create(
       model="llama-3.3-70b-versatile",
       messages=[{"role": "user", "content": transcript_text}],
       max_tokens=200
     )
     summary = response.choices[0].message.content
   — Wrap in try/except, on failure return "Summary unavailable"
   — Never crash the app due to Groq failure

=== STREAMLIT UI RULES ===

8. Page component order, exact, no reordering:
   — Page title: "Voice Call Sentiment Analyser" (Note: overridden by Custom UI Rules below)
   — One line description under title
   — File uploader: accepts .mp3 .wav .m4a only
   — Process button: "Analyse Call"
   — Progress indicators while processing
   — Results section:
       a. Transcript table — columns: Time, Text, Sentiment, Score, Intent
       b. Sentiment timeline graph (plotly)
       c. Intent breakdown (plotly pie or bar chart)
       d. Groq summary
       e. Download CSV button

9. Progress messages, show these in order during processing:
   — "Transcribing audio with Whisper..."
   — "Analysing sentiment..."
   — "Detecting intent..."
   — "Generating summary with Groq..."
   — Use st.status() wrapper if available in installed Streamlit version, otherwise use st.spinner()

10. File handling:
    — Save uploaded file using tempfile.NamedTemporaryFile
    — Pass the temp file path to Whisper, not the file object
    — Delete temp file immediately after Whisper finishes
    — Use suffix matching the uploaded file extension

=== ERROR HANDLING RULES ===

11. Each pipeline step has its own try/except, isolated from others:
    — Whisper failure: display error, stop pipeline, do not continue
    — RoBERTa failure on one segment: set sentiment="error", continue to next segment, do not stop entire pipeline
    — Intent failure on one segment: set intent="error", continue
    — Groq failure: display "Summary unavailable", pipeline still shows transcript and graph

12. Input validation before pipeline starts:
    — File is None: show "Please upload an audio file"
    — File size is 0: show "Uploaded file is empty"
    — File over 25MB: show warning "Large file, processing may be slow" but continue anyway

13. Model loading failure:
    — If any model fails to load show exact error message
    — Tell user to check internet connection for first run download
    — Do not show a blank screen or silent failure ever

=== PERFORMANCE RULES ===

14. First run behaviour:
    — Models download automatically to ~/.cache/huggingface
    — Total download size approximately 600MB first run
    — Show message: "First run: downloading ML models (~600MB), this will take a few minutes and won't happen again"
    — After first run all models load from cache, no internet needed

15. Segment filtering:
    — Skip sentiment and intent for any segment under 3 words
    — Set both to "skip" and move on
    — Do not call any model on these segments

16. Sequential processing only:
    — No threading
    — No asyncio
    — No multiprocessing
    — Process one segment at a time through sentiment then intent
    — Reason: parallel inference on 7GB RAM CPU machine will crash

=== CODE STYLE RULES ===

17. pipeline.py structure:
    — One function per pipeline step
    — Function names: transcribe_audio(), analyse_sentiment(), detect_intent(), generate_summary()
    — Each function takes the data list, returns the data list
    — Models passed as parameters not loaded inside functions

18. app.py structure:
    — Import functions from pipeline.py only
    — No ML logic whatsoever in app.py
    — All Streamlit components in one main() function
    — Call main() at bottom with if __name__ == "__main__"

19. utils.py structure:
    — clean_text(text) — removes special characters
    — format_timestamp(seconds) — converts float seconds to MM:SS
    — segments_to_csv(segments) — converts data list to CSV string
    — No imports from pipeline.py or app.py

20. General code rules:
    — No global variables except model objects loaded at startup
    — Every function has a docstring, one line is enough
    — No hardcoded strings except in utils.py and the prompts in rule 7
    — No print statements in final code, use st.write for debug output
    — All API keys via os.getenv() only

=== CUSTOM UI RULES (OVERRIDES FOR UI BEHAVIOR) ===

21. Approvals and Explanations: Whenever a command or anything is asked of approval by the user, the assistant MUST clearly explain what is happening, what command is being run, and why approval is being asked.

22. See `UI_WORKFLOW.md` for exact UI visual aesthetics, layouts, and animations required for the Emotion Tracker landing page, loading page, and results page.

import streamlit as st
import tempfile
import os
import random
import plotly.express as px
import pandas as pd
import re
from utils import segments_to_csv
from test_scripts import TEST_SCRIPTS

# Page Config
st.set_page_config(page_title="Call Analyser", page_icon="📞", layout="wide")

# Custom CSS for aesthetics and animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');

    /* Global Typography & Colors */
    [data-testid="stAppViewContainer"] {
        background-color: #F8F5FC;
        background-image: radial-gradient(#D2C5EB 2px, transparent 2px);
        background-size: 30px 30px;
    }
    
    p, span, div, label, li {
        font-family: 'VT323', monospace !important;
        font-size: 1.3rem !important;
        color: #392A48 !important;
    }

    /* Restore Streamlit Material Icons */
    .material-icons, .material-symbols-rounded, [class*="icon"], [data-testid="stIconMaterial"] {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
    }

    h1, h2, h3 {
        font-family: 'Press Start 2P', cursive !important;
        color: #392A48 !important;
        text-shadow: 3px 3px #D2C5EB;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    /* Hide Streamlit Header Anchor Links */
    h1 a, h2 a, h3 a, h4 a, h5 a, h6 a, [data-testid="stHeaderActionElements"] {
        display: none !important;
    }

    .main-title {
        font-family: 'Press Start 2P', cursive !important;
        color: #392A48 !important;
        font-size: 2.6rem !important;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem 0;
        text-shadow: 4px 4px #D2C5EB;
        border-bottom: 4px dashed #392A48;
        text-transform: uppercase;
    }

    /* Pixel Art Buttons */
    .stButton > button {
        font-family: 'Press Start 2P', cursive !important;
        font-size: 0.9rem !important;
        background-color: #E4DAF5;
        color: #392A48 !important;
        border: 4px solid #392A48;
        box-shadow: 6px 6px 0px 0px #9B7EBD;
        border-radius: 0;
        padding: 0.5rem 1rem;
        transition: all 0.1s;
    }
    
    .stButton > button:hover {
        transform: translate(2px, 2px);
        box-shadow: 4px 4px 0px 0px #9B7EBD;
        color: #392A48 !important;
        border-color: #392A48;
        background-color: #D2C5EB;
    }

    .stButton > button:active {
        transform: translate(6px, 6px);
        box-shadow: 0px 0px 0px 0px #9B7EBD;
        background-color: #9B7EBD;
    }

    /* Inputs & Containers */
    .stFileUploader, [data-testid="stFileUploader"], [data-testid="stAudioInput"] {
        border: 4px solid #392A48 !important;
        background-color: #FFFFFF !important;
        box-shadow: 6px 6px 0px 0px #9B7EBD !important;
        border-radius: 0 !important;
        margin-bottom: 1rem !important;
    }
    
    /* Hide broken material icons inside inputs */
    [data-testid="stFileUploader"] [data-testid="stIconMaterial"],
    [data-testid="stFileUploader"] .material-symbols-rounded,
    [data-testid="stFileUploader"] .material-icons,
    [data-testid="stAudioInput"] [data-testid="stIconMaterial"],
    [data-testid="stAudioInput"] .material-symbols-rounded,
    [data-testid="stAudioInput"] .material-icons {
        display: none !important;
    }


    .stRadio > label {
        font-family: 'Press Start 2P', cursive !important;
        font-size: 1rem !important;
    }

    /* Test Script Box */
    .test-script-box {
        border: 4px solid #392A48;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 6px 6px 0px 0px #9B7EBD;
        background-color: #FFFFFF;
    }

    /* Typewriter container styled like a retro screen */
    .typewriter-container {
        font-family: 'VT323', monospace;
        font-size: 1.5rem;
        background: #FFFFFF;
        padding: 20px;
        border: 4px solid #392A48;
        box-shadow: 8px 8px 0px 0px #9B7EBD;
        color: #392A48;
        width: 100%;
        margin-bottom: 2rem;
        border-radius: 0;
        line-height: 1.5;
    }
    
    /* Alerts and Info Boxes */
    .stAlert {
        border: 4px solid #392A48 !important;
        background-color: #FFFFFF !important;
        color: #392A48 !important;
        box-shadow: 6px 6px 0px 0px #9B7EBD !important;
        border-radius: 0 !important;
    }
    
    .stAlert p {
        font-size: 1.2rem !important;
    }

    /* DataFrames and Tables */
    [data-testid="stDataFrame"] {
        border: 4px solid #392A48;
        box-shadow: 6px 6px 0px 0px #9B7EBD;
    }

    /* Status Widget */
    [data-testid="stStatusWidget"] {
        border: 4px solid #392A48;
        background-color: #FFFFFF;
        box-shadow: 6px 6px 0px 0px #9B7EBD;
        border-radius: 0;
    }
    
    /* Hide some default Streamlit elements that ruin the retro vibe */
    header { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

def main():
    if "view" not in st.session_state:
        st.session_state.view = "landing"
    
    if st.session_state.view == "landing":
        
        # Check if models are cached roughly
        hf_cache = os.path.expanduser("~/.cache/huggingface")
        if not os.path.exists(hf_cache) or len(os.listdir(hf_cache)) == 0:
            st.info("First run: downloading ML models (~600MB), this will take a few minutes and won't happen again")

        col1, col2, col3 = st.columns([1, 8, 1])
        with col2:
            st.markdown('<div class="main-title">Call Analyser</div>', unsafe_allow_html=True)
            if "show_script" not in st.session_state:
                st.session_state.show_script = False

            def toggle_script_on():
                st.session_state.show_script = True
                st.session_state.test_script = random.choice(TEST_SCRIPTS)

            def toggle_script_off():
                st.session_state.show_script = False

            def refresh_script():
                st.session_state.test_script = random.choice(TEST_SCRIPTS)

            if not st.session_state.show_script:
                st.button("Generate Test Script", on_click=toggle_script_on)
            else:
                col_gen1, col_gen2, col_gen_space = st.columns([3, 2, 7])
                with col_gen1:
                    st.button("Generate Test Script", use_container_width=True, key="btn_close", on_click=toggle_script_off)
                with col_gen2:
                    st.button("Refresh", use_container_width=True, on_click=refresh_script)
                        
                if "test_script" in st.session_state:
                    st.markdown(f'<div class="test-script-box">{st.session_state.test_script}</div>', unsafe_allow_html=True)

            input_method = st.radio("Choose input method", ["Upload File", "Record Audio"], horizontal=True)
            
            if input_method == "Upload File":
                uploaded_file = st.file_uploader(" ", type=['mp3', 'wav', 'm4a'], label_visibility="collapsed")
            else:
                uploaded_file = st.audio_input(" ", label_visibility="collapsed")
            
            st.write("") # Spacer
            if st.button("Analyse", use_container_width=True):
                if uploaded_file is None:
                    st.error("Please provide an audio file or recording")
                elif uploaded_file.size == 0:
                    st.error("Audio data is empty")
                else:
                    if uploaded_file.size > 25 * 1024 * 1024:
                        st.warning("Large file, processing may be slow")
                    st.session_state.uploaded_file = uploaded_file
                    st.session_state.view = "loading"
                    st.rerun()

    elif st.session_state.view == "loading":
        col1, col2, col3 = st.columns([1, 8, 1])
        with col2:
            st.markdown('<div class="main-title">Call Analyser</div>', unsafe_allow_html=True)
        
        # Lazy load the heavy ML pipeline only when needed
        from pipeline import transcribe_audio, analyse_sentiment, detect_intent, generate_summary
        
        uploaded_file = st.session_state.uploaded_file
        ext = os.path.splitext(uploaded_file.name)[1]
        
        failed = False
        # Use st.status per rule 9
        with st.status("Initializing...", expanded=True) as status:
            temp_path = None
            try:
                # Save file temporarily
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
                temp_file.write(uploaded_file.read())
                temp_file.close()
                temp_path = temp_file.name
                
                st.write("Transcribing audio with Whisper...")
                segments = transcribe_audio(temp_path)
                
                if not segments:
                    status.update(label="Transcription Failed", state="error")
                    failed = True
                else:
                    st.write("Analysing sentiment...")
                    segments = analyse_sentiment(segments)
                    
                    st.write("Detecting intent...")
                    segments = detect_intent(segments)
                    
                    st.write("Generating summary with Groq...")
                    full_text = " ".join([seg["text"] for seg in segments])
                    summary = generate_summary(full_text)
                    
                    status.update(label="Analysis Complete", state="complete")
                    
                    st.session_state.segments = segments
                    st.session_state.summary = summary
                    st.session_state.view = "results"
                
            except Exception as e:
                status.update(label="Pipeline Failed", state="error")
                st.error(f"Error: {str(e)}")
                failed = True
            finally:
                if temp_path and os.path.exists(temp_path):
                    try:
                        os.unlink(temp_path)
                    except:
                        pass
            
                if failed:
                    st.write("")
                    if st.button("Try Again", use_container_width=True):
                        st.session_state.view = "landing"
                        st.rerun()
        
        if st.session_state.view == "results":
            st.rerun()

    elif st.session_state.view == "results":
        st.markdown('<div class="main-title" style="font-size: 3rem; margin-bottom: 1rem;">Call Report</div>', unsafe_allow_html=True)
        
        summary_text = st.session_state.summary
        # Force a double line break before numbers (1. ) or bullets (* ) to ensure they start on a new line
        summary_text = re.sub(r'(?<!^)(?<!\n)(\d+\.\s)', r'\n\n\1', summary_text)
        summary_text = re.sub(r'(?<!^)(?<!\n)([-*]\s)', r'\n\n\1', summary_text)
        
        # Split by actual newline character and convert to HTML line breaks
        formatted_summary = "<br/><br/>".join([line.strip() for line in summary_text.split('\n') if line.strip() != ""])
        st.markdown(f'<div class="typewriter-container">{formatted_summary}</div>', unsafe_allow_html=True)
        
        st.write("---")
        
        segments = st.session_state.segments
        if segments:
            df = pd.DataFrame(segments)
            
            st.subheader("Transcript")
            display_df = df.copy()
            display_df['Time'] = display_df['start'].apply(lambda x: f"{x:.1f}s") + " - " + display_df['end'].apply(lambda x: f"{x:.1f}s")
            table_df = display_df[['Time', 'text', 'sentiment', 'sentiment_score', 'intent']]
            table_df.columns = ['Time', 'Text', 'Sentiment', 'Score', 'Intent']
            st.dataframe(table_df, use_container_width=True)
            
            csv_str = segments_to_csv(segments)
            st.download_button("Download Transcript (CSV)", data=csv_str, file_name="transcript.csv", mime="text/csv")
            
            st.write("---")
            st.subheader("Sentiment Timeline")
            sent_val = {"Positive": 1, "Neutral": 0, "Negative": -1, "Unknown": 0, "skip": 0, "error": 0}
            df['SentNum'] = df['sentiment'].map(sent_val)
            fig_sent = px.line(df, x='start', y='SentNum', hover_data=['text', 'sentiment'], 
                               labels={'start': 'Time (s)', 'SentNum': 'Sentiment'})
            fig_sent.update_layout(
                plot_bgcolor='#FFFFFF',
                paper_bgcolor='#FFFFFF',
                font_family='VT323',
                font_color='#392A48',
                title_font_family='Press Start 2P',
                xaxis=dict(
                    showgrid=True, gridcolor='#E4DAF5', gridwidth=2, zerolinecolor='#392A48',
                    showline=True, linewidth=2, linecolor='#392A48', tickfont=dict(color='#392A48', family='VT323', size=14),
                    title_font=dict(color='#392A48', family='Press Start 2P', size=10),
                    title_standoff=20
                ),
                yaxis=dict(
                    showgrid=True, gridcolor='#E4DAF5', gridwidth=2, zerolinecolor='#392A48',
                    tickmode='array', tickvals=[-1, 0, 1], ticktext=['-1 (Negative)', '0 (Neutral)', '1 (Positive)'],
                    range=[-1.2, 1.2],
                    showline=True, linewidth=2, linecolor='#392A48', tickfont=dict(color='#392A48', family='VT323', size=14),
                    title_font=dict(color='#392A48', family='Press Start 2P', size=10),
                    title_standoff=20
                ),
                margin=dict(l=80, r=40, t=40, b=80)
            )
            fig_sent.update_traces(line_color='#9B7EBD', line_width=4, marker=dict(size=8, color='#392A48'))
            
            # Apply border to plotly chart via CSS mapping wrapper
            st.markdown('<div style="border: 4px solid #392A48; box-shadow: 6px 6px 0px 0px #9B7EBD; margin-bottom: 2rem;">', unsafe_allow_html=True)
            st.plotly_chart(fig_sent, use_container_width=True, theme=None)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.subheader("Intent Breakdown")
            valid_intents = df[~df['intent'].isin(['skip', 'error', 'unclear'])]['intent']
            if not valid_intents.empty:
                intent_counts = valid_intents.value_counts().reset_index()
                intent_counts.columns = ['Intent', 'Count']
                fig_intent = px.pie(intent_counts, values='Count', names='Intent')
                fig_intent.update_layout(
                    paper_bgcolor='#FFFFFF',
                    font_family='VT323',
                    font_color='#392A48',
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                fig_intent.update_traces(
                    marker=dict(colors=['#9B7EBD', '#D2C5EB', '#392A48', '#E4DAF5'], 
                                line=dict(color='#392A48', width=3))
                )
                st.markdown('<div style="border: 4px solid #392A48; box-shadow: 6px 6px 0px 0px #9B7EBD; margin-bottom: 2rem;">', unsafe_allow_html=True)
                st.plotly_chart(fig_intent, use_container_width=True, theme=None)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No specific intents recognised with high confidence.")
            
        st.write("")
        if st.button("Analyse Another File"):
            st.session_state.view = "landing"
            st.rerun()

if __name__ == "__main__":
    main()

# User Interface (UI) Workflow and Aesthetics

## 1. Landing Page
- **Main Title**: "Emotion Tracker" displayed in the center of the screen.
  - **Aesthetics**: Glowing and bouncing/floaty text to give a vibe of calmness.
  - **Animation**: Text should appear to come from slightly up and fade in.
- **Subtitle**: "mp3 to emotions ?" displayed below the main title in a smaller font.
  - **Animation**: Appears from slightly up.
- **Upload Button**: A file uploader or button with the text "mp3 to emotions ?".
  - Accepts ONLY `.mp3`, `.wav`, `.m4a`.
- **Layout**: Everything must be auto-aligned to the center of the screen and adjust to the size and amount of text accordingly.

## 2. Loading / Processing Page
- **Trigger**: Activated immediately after the user uploads an audio file.
- **Progressive Loading Bar**: 
  - **Visuals**: One rectangle appearing after another, sliding like a card deck from behind.
  - **Status Text**: Shows a very brief explanation of the current step (e.g., "Transcribing...", "Analyzing Sentiment...") so the user knows what's going on without being confused.
- **Completion Text**: At the end of the loading process, a disconnected text appears saying: "ur file is done processing".

## 3. Results Page
- **Transition**: Automatically moves to this page after the completion text.
- **Intro Text**: The text "the mp3 file provided conveys ..." appears (coming from slightly up).
- **Actual Result**: 
  - The final analysis/summary is displayed in a designated box.
  - **Animation**: The text inside the result box must appear in a typing style, but fast enough to not frustrate the user.
- **Additional Results**: (As per Master Rules)
  - Transcript table (Time, Text, Sentiment, Score, Intent)
  - Sentiment timeline graph (Plotly)
  - Intent breakdown (Plotly)
  - Download CSV button

## General Styling Rules
- **Animations**: All text (except the loading bar) should have an entrance animation where it comes from slightly up and fades in.
- **Alignment**: Auto-center everything dynamically based on screen size.
- **Implementation Note**: Since we are strictly using Streamlit, these animations and specific visual effects will need to be implemented via custom CSS and HTML injected into the Streamlit app using `st.markdown("<style>...</style>", unsafe_allow_html=True)`.

import streamlit as st
import speech_recognition as sr
import pandas as pd
import time
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import io
import json
import datetime

# Download NLTK resources if needed
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

# Initialize session state
if 'transcription_history' not in st.session_state:
    st.session_state.transcription_history = []
if 'commands' not in st.session_state:
    st.session_state.commands = []

# Function for speech recognition
def transcribe_speech(api_choice="google", wit_api_key=None, ibm_api_key=None, ibm_url=None):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        status_placeholder.markdown("🎤 **Listening...**")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    try:
        status_placeholder.markdown("🔍 **Processing...**")
        
        if api_choice == "google":
            text = recognizer.recognize_google(audio)
            api_name = "Google Speech Recognition"
            
        elif api_choice == "sphinx":
            text = recognizer.recognize_sphinx(audio)
            api_name = "CMU Sphinx (Offline)"
            
        elif api_choice == "wit":
            if not wit_api_key:
                raise ValueError("Wit.ai API key is required.")
            text = recognizer.recognize_wit(audio, key=wit_api_key)
            api_name = "Wit.ai"
            
        elif api_choice == "ibm":
            if not ibm_api_key or not ibm_url:
                raise ValueError("IBM Watson API key and URL are required.")
            text = recognizer.recognize_ibm(audio, ibm_api_key, ibm_url)
            api_name = "IBM Watson"
            
        else:
            raise ValueError("Invalid API choice. Options: google, sphinx, wit, ibm")
            
        status_placeholder.markdown("✅ **Done!**")
        return text, api_name
        
    except sr.UnknownValueError:
        status_placeholder.markdown("❌ **Error: Could not understand audio**")
        return "Sorry, I couldn't understand the audio.", None
        
    except sr.RequestError as e:
        status_placeholder.markdown(f"❌ **Error: {e}**")
        return f"API request failed: {e}", None
        
    except Exception as e:
        status_placeholder.markdown(f"❌ **Error: {e}**")
        return str(e), None

# Command processor
def process_command(text):
    text = text.lower()
    
    # Define commands
    commands = {
        "time": lambda: f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}",
        "date": lambda: f"Today is {datetime.datetime.now().strftime('%Y-%m-%d')}",
        "hello": lambda: "Hello! How can I help you?",
        "help": lambda: "Available commands: time, date, hello, help, clear, sentiment",
        "clear": lambda: "clear_history"
    }
    
    # Check for commands
    for cmd, func in commands.items():
        if cmd in text:
            result = func()
            if result == "clear_history":
                st.session_state.transcription_history = []
                return "History cleared!"
            return result
            
    # If no command matched
    return None

# Sentiment analysis function
def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    
    # Determine sentiment label
    if sentiment['compound'] >= 0.05:
        label = "Positive"
    elif sentiment['compound'] <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
        
    return {
        'label': label,
        'score': sentiment['compound'],
        'details': sentiment
    }

# Function to create sentiment visualization
def create_sentiment_chart():
    if len(st.session_state.transcription_history) < 2:
        return None
        
    # Extract sentiment data
    sentiments = [entry.get('sentiment', {}).get('score', 0) 
                 for entry in st.session_state.transcription_history 
                 if 'sentiment' in entry]
    
    if not sentiments:
        return None
        
    # Create plot
    fig, ax = plt.subplots()
    ax.plot(range(len(sentiments)), sentiments, marker='o')
    ax.axhline(y=0, color='r', linestyle='-', alpha=0.3)
    ax.set_ylim(-1.1, 1.1)
    ax.set_title('Sentiment Trend')
    ax.set_xlabel('Transcription #')
    ax.set_ylabel('Sentiment Score')
    
    # Convert plot to image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf

# Streamlit app
def main():
    st.set_page_config(page_title="Speech Recognition App", page_icon="🎤", layout="wide")
    
    st.title("🎤 Voice Assistant & Speech Recognition")
    st.subheader("Convert speech to text and execute voice commands")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Transcribe", "History", "About"])
    
    # Tab 1: Transcription
    with tab1:
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("### Speech Recognition")
            
            # API selection
            api_options = ["google", "sphinx", "wit", "ibm"]
            api_choice = st.selectbox("Choose API", api_options)
            
            # API keys input
            wit_key = None
            ibm_key = None
            ibm_url = None
            
            if api_choice == "wit":
                wit_key = st.text_input("Wit.ai API Key", type="password")
            elif api_choice == "ibm":
                ibm_key = st.text_input("IBM Watson API Key", type="password")
                ibm_url = st.text_input("IBM Watson URL")
                
            # Status display
            global status_placeholder
            status_placeholder = st.empty()
            
            # Start button
            if st.button("🎤 Start Listening"):
                transcription, api_name = transcribe_speech(api_choice, wit_key, ibm_key, ibm_url)
                
                if transcription and api_name:
                    # Display transcription
                    st.markdown(f"### Transcription:")
                    st.write(transcription)
                    
                    # Process for command
                    command_result = process_command(transcription)
                    
                    # Add to history
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Analyze sentiment
                    sentiment_result = analyze_sentiment(transcription)
                    
                    # Save to history
                    entry = {
                        'timestamp': timestamp,
                        'text': transcription,
                        'api': api_name,
                        'sentiment': sentiment_result
                    }
                    
                    if command_result:
                        entry['command_result'] = command_result
                        st.success(f"Command executed: {command_result}")
                    
                    st.session_state.transcription_history.append(entry)
                    
                    # Show sentiment
                    st.markdown("### Sentiment Analysis:")
                    sentiment_color = {
                        "Positive": "green",
                        "Neutral": "blue",
                        "Negative": "red"
                    }
                    st.markdown(f"<span style='color:{sentiment_color[sentiment_result['label']]}'>{sentiment_result['label']}</span> (Score: {sentiment_result['score']:.2f})", unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Voice Commands")
            st.info("""
            Say any of these commands:
            - "time" - Get current time
            - "date" - Get today's date
            - "hello" - Greeting
            - "help" - List commands
            - "clear" - Clear history
            - "sentiment" - Analyze sentiment
            """)
            
            st.markdown("### Tips")
            st.warning("""
            For best results:
            - Speak clearly
            - Reduce background noise
            - Use a good microphone
            - Start with "OK" or "Hey" for better command recognition
            """)
    
    # Tab 2: History
    with tab2:
        st.markdown("### Transcription History")
        
        # Export options
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            if st.button("Export History (JSON)") and st.session_state.transcription_history:
                json_data = json.dumps(st.session_state.transcription_history, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name="transcription_history.json",
                    mime="application/json"
                )
        
        with col_exp2:
            if st.button("Clear History"):
                st.session_state.transcription_history = []
                st.success("History cleared!")
        
        # Display history
        if st.session_state.transcription_history:
            # Create sentiment chart
            sentiment_img = create_sentiment_chart()
            if sentiment_img:
                st.markdown("### Sentiment Trend")
                st.image(sentiment_img)
            
            st.markdown("### Recent Transcriptions")
            for i, entry in enumerate(reversed(st.session_state.transcription_history)):
                # Limit to 10 most recent entries
                if i >= 10:
                    break
                    
                with st.expander(f"{entry['timestamp']} - {entry['text'][:50]}..."):
                    st.markdown(f"**Time:** {entry['timestamp']}")
                    st.markdown(f"**API:** {entry['api']}")
                    st.markdown(f"**Text:** {entry['text']}")
                    
                    if 'sentiment' in entry:
                        sentiment = entry['sentiment']
                        st.markdown(f"**Sentiment:** {sentiment['label']} (Score: {sentiment['score']:.2f})")
                    
                    if 'command_result' in entry:
                        st.markdown(f"**Command Result:** {entry['command_result']}")
        else:
            st.info("No transcription history yet.")
    
    # Tab 3: About
    with tab3:
        st.markdown("### About This App")
        st.write("""
        This speech recognition app is powered by multiple speech-to-text APIs including Google Speech 
        Recognition, CMU Sphinx, Wit.ai, and IBM Watson. The app provides a user-friendly interface for 
        transcribing speech, executing voice commands, and analyzing sentiment.
        
        **Features:**
        - Multiple speech recognition API support
        - Voice command execution
        - Sentiment analysis
        - Transcription history
        - Export functionality
        
        **Use Cases:**
        - Accessibility tool for those who prefer speaking over typing
        - Meeting transcription
        - Voice-controlled applications
        - Sentiment analysis of spoken content
        
        **Future Development:**
        - Custom wake word detection
        - More advanced commands
        - Multiple language support
        - Real-time transcription
        """)
        
        st.markdown("### Required Packages")
        st.code("""
        pip install streamlit
        pip install SpeechRecognition
        pip install nltk
        pip install pandas
        pip install matplotlib
        pip install pyaudio
        """)

if __name__ == "__main__":
    main()
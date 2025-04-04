# Speech Recognition Voice Assistant

A feature-rich Streamlit application for speech recognition with sentiment analysis, voice commands, and interactive visualizations.

![Speech Recognition App](https://github.com/Feezysr/speech-recognition-app/raw/main/screenshot.png)

## 📋 Features

### Speech Recognition
- **Multiple API Support**:
  - Google Speech Recognition (default, no API key required)
  - CMU Sphinx (works offline)
  - Wit.ai (requires API key)
  - IBM Watson (requires API key and URL)
- **Real-time Transcription**: Convert speech to text with a single click

### Voice Commands
- **Built-in Commands**:
  - Get current time (`"time"`)
  - Display today's date (`"date"`)
  - Respond to greetings (`"hello"`)
  - List available commands (`"help"`)
  - Clear history (`"clear"`)
  - Analyze sentiment (`"sentiment"`)
- **Natural Language Processing**: Commands can be embedded within sentences

### Sentiment Analysis
- **Real-time Analysis**: Instant feedback on the emotional tone of speech
- **Visual Classification**: Color-coded results (Positive: green, Neutral: blue, Negative: red)
- **Detailed Scores**: Compound, positive, negative, and neutral scores displayed
- **Trend Visualization**: Track sentiment changes over time

### History Management
- **Comprehensive Logging**: Timestamps, transcriptions, API used, sentiment scores, and command results
- **Export Functionality**: Save history as JSON file
- **Interactive Interface**: Expandable entries for detailed information
- **Data Visualization**: Sentiment trend charts

## 🚀 Installation

### Prerequisites
- Python 3.7+
- Git (for cloning the repository)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Feezysr/speech-recognition-app.git
   cd speech-recognition-app
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   # For Windows
   python -m venv venv
   venv\Scripts\activate

   # For macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install PyAudio**:
   ```bash
   # Windows
   pip install pyaudio

   # macOS
   brew install portaudio
   pip install pyaudio

   # Linux
   sudo apt-get install python3-pyaudio
   ```

## 💻 Usage

1. **Run the application**:
   ```bash
   streamlit run app.py
   ```

2. **Access the web interface**:
   The application will open automatically in your browser, or you can visit:
   ```
   http://localhost:8501
   ```

3. **Select an API**:
   - Google (default)
   - Sphinx (offline)
   - Wit.ai (requires API key)
   - IBM Watson (requires API key and URL)

4. **Start listening**:
   Click the "Start Listening" button and speak clearly into your microphone.

5. **Use voice commands**:
   Try saying "What's the time?" or "Show me today's date" to test command functionality.

## 📱 User Interface

### Tab 1: Transcribe
- Speech recognition controls
- API selection
- Real-time status indicators
- Voice command reference
- Tips for optimal performance

### Tab 2: History
- Sentiment trend visualization
- Export options (JSON)
- Clear history functionality
- Recent transcriptions with detailed information

### Tab 3: About
- Application overview
- Feature list
- Use cases
- Development roadmap
- Installation instructions

## 🔧 Technical Details

### Dependencies
- **streamlit**: Web application framework
- **SpeechRecognition**: Interface to multiple speech recognition APIs
- **nltk**: Natural language processing for sentiment analysis
- **pandas**: Data manipulation and storage
- **matplotlib**: Data visualization
- **pyaudio**: Audio input interface

### Code Structure
- **Speech Recognition Function**: Handles different API interfaces
- **Command Processor**: Parses text for commands
- **Sentiment Analysis**: Uses NLTK's VADER model
- **Visualization Engine**: Creates charts from historical data
- **Streamlit UI**: Organizes the application layout

## 🛣️ Roadmap

### Planned Features
- Custom wake word detection
- Support for additional languages
- Continuous listening mode
- Cloud storage integration
- User profiles and preferences
- Advanced command customization
- Text-to-speech response capabilities

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

Hafiz - [@Feezysr](https://github.com/Feezysr)

Project Link: [https://github.com/Feezysr/speech-recognition-app](https://github.com/Feezysr/speech-recognition-app)

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/) - For the amazing web app framework
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) - For the speech recognition capabilities
- [NLTK](https://www.nltk.org/) - For sentiment analysis tools

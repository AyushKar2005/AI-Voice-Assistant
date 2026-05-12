# J.A.R.V.I.S - AI Voice Assistant

J.A.R.V.I.S is a desktop-based AI Voice Assistant inspired by the concept of intelligent virtual assistants.  
Built using Python and PyQt5, the project combines voice recognition, task automation, chatbot interaction, and a modern GUI into a single application.

The assistant can listen to commands, respond through speech, perform web searches, open applications, and automate basic desktop tasks in real time.

---

## Features

- Real-time voice recognition
- AI-based conversational responses
- Text-to-speech interaction
- Modern PyQt5 graphical interface
- Web search automation
- Open applications and websites
- Live date and time updates
- Music and media controls
- Multi-threaded execution
- Dynamic status updates
- Microphone enable/disable controls
- File-based communication system

---

## Tech Stack

### Language
- Python

### Libraries and Frameworks
- PyQt5
- SpeechRecognition
- pyttsx3
- pywhatkit
- wikipedia
- threading
- datetime
- os
- webbrowser

---

## Project Architecture

```text
User Voice Input
        ↓
Speech Recognition
        ↓
Command Processing
        ↓
Automation / Chatbot Engine
        ↓
Speech Output + GUI Updates
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/jarvis-ai-assistant.git
```

### Move to Project Directory

```bash
cd jarvis-ai-assistant
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Project

```bash
python main.py
```

---

## Project Structure

```text
JARVIS-AI/
│
├── gui/
│   ├── main_gui.py
│   └── assets/
│
├── engine/
│   ├── speech_recognition.py
│   ├── text_to_speech.py
│   ├── automation.py
│   └── chatbot.py
│
├── data/
│   └── status_files/
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Core Functionalities

### Voice Interaction
The assistant continuously listens for commands and processes them in real time.

### Automation
Can open applications, websites, and perform desktop-level tasks automatically.

### Smart Search
Supports searching information from Google, YouTube, and Wikipedia.

### Conversational Responses
Provides chatbot-like responses for smoother interaction.

### GUI System
Interactive interface built using PyQt5 for better user experience.

---

## Example Commands

```text
Open YouTube
Search machine learning on Google
Play music
Open VS Code
What is the time?
Tell me about artificial intelligence
```

---

## Future Improvements

- LLM integration
- Face recognition
- Cloud synchronization
- Smart home integration
- Persistent memory system
- Advanced animations and UI improvements

---

## Learning Outcomes

This project helped in understanding:

- GUI development using PyQt5
- Speech recognition systems
- Multi-threading in Python
- Automation workflows
- Human-computer interaction
- Real-time desktop application development

---

## Contributing

Contributions and suggestions are welcome.

```bash
Fork → Clone → Create Branch → Commit → Push → Pull Request
```

---

## License

This project is licensed under the MIT License.

---

## Author

Ayush Kar

B.Tech CSE Student  
AI Enthusiast | Full Stack Developer

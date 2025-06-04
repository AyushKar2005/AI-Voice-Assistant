from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget,
    QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton,
    QFrame, QLabel, QSizePolicy
)
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values
import os
import sys

# Create necessary directories first
current_dir = os.path.dirname(os.path.abspath(__file__))
Files_dir = os.path.join(current_dir, "Files")
Graphics_dir = os.path.join(current_dir, "Graphics")

# Create directories if they don't exist
os.makedirs(Files_dir, exist_ok=True)
os.makedirs(Graphics_dir, exist_ok=True)

env_path = os.path.join(current_dir, "..", ".env")
env_vars = dotenv_values(env_path)
Assistantname = env_vars.get("Assistantname")

old_chat_message = ""
TempDirPath = Files_dir
GraphicsDirPath = Graphics_dir

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = [
        "how", "what", "where", "when", "who", "why", "which",
        "whose", "whom", "can you", "what's", "where's", "who's",
        "when's", "why's", "how's", "could you", "would you",
        "should you", "is it possible to", "are you able to",
        "do you know how to"
    ]
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + " ?"
        else:
            new_query += " ?"
    else:
        if query_words[-1][-1] in ['.','?','!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()

def SetMicrophoneStatus(Command):
    mic_file = os.path.join(TempDirPath, "Mic.data")
    with open(mic_file, "w", encoding='utf-8') as f:
        f.write(Command)

def GetMicrophoneStatus():
    mic_file = os.path.join(TempDirPath, "Mic.data")
    with open(mic_file, "r", encoding='utf-8') as f:
        Status = f.read()
        return Status
    
def SetAssistantStatus(Status):
    status_file = os.path.join(TempDirPath, "Status.data")
    with open(status_file, "w", encoding='utf-8') as f:
        f.write(Status)

def GetAssistantStatus():
    status_file = os.path.join(TempDirPath, "Status.data")
    with open(status_file, "r", encoding='utf-8') as f:
        Status = f.read()
        return Status
    
def MicButtonInitialized():
    SetMicrophoneStatus("False")

def MicButtonClosed():
    SetMicrophoneStatus("True")

def GraphicsDirectoryPath(f):
    return os.path.join(GraphicsDirPath, f)
    
def TempDirectoryPath(f):
    return os.path.join(TempDirPath, f)

def showTextToScreen(Text):
    response_file = os.path.join(TempDirPath, "Responses.data")
    with open(response_file, "w", encoding='utf-8') as f:
        f.write(Text)

class ChatSection(QWidget):
    def __init__(self):
        super(ChatSection, self).__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10, 40, 40, 100)
        layout.setSpacing(-100)
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)
        self.setStyleSheet("background-color:black;")
        layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
        layout.setStretch(1, 1)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        text_color = QColor(Qt.red)
        text_color_text = QTextCharFormat()
        text_color_text.setForeground(text_color)
        self.chat_text_edit.setCurrentCharFormat(text_color_text)
        
        # Initialize files if they don't exist
        for file in ["Responses.data", "Status.data", "Mic.data"]:
            file_path = os.path.join(TempDirPath, file)
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding='utf-8') as f:
                    if file == "Mic.data":
                        f.write("False")
                    else:
                        f.write("")

        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border:none;")
        gif_path = GraphicsDirectoryPath('Jarvis.gif')
        if os.path.exists(gif_path):
            movie = QMovie(gif_path)
            max_gif_size_W = 480
            max_gif_size_H = 270
            movie.setScaledSize(QSize(max_gif_size_W, max_gif_size_H))
            self.gif_label.setMovie(movie)
            movie.start()
        else:
            print(f"GIF not found at: {gif_path}")
        layout.addWidget(self.gif_label)
        
        self.label = QLabel("")
        self.label.setStyleSheet("color:white; font-size:16px; margin-right: 195px; border:none;margin-top:-30px;")
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)
        layout.setSpacing(-10)
        
        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)
        
        self.chat_text_edit.viewport().installEventFilter(self)
        self.setStyleSheet(""" 
              QScrollBar:vertical{
              border:none;
              background:black;
              width:10px;
              margin: 0px 0px 0px 0px;
              }
              QScrollBar::handle:vertical{
               background:white;
              min-height:20px;
              }
                QScrollBar::add-line:vertical{
                background: black;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
                height:10px;}

                QScrollBar::sub-line:vertical{
                background: black;
                subcontrol-position: top;
                subcontrol-origin: margin;
                height:10px;}

                QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{
                    border:none;
                    background: none;
                    color:none;
                }
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{
                    background:none;
                }
              """)

    def loadMessages(self):
        global old_chat_message
        response_file = os.path.join(TempDirPath, "Responses.data")
        
        try:
            with open(response_file, "r", encoding='utf-8') as f:
                messages = f.read()

                if messages is None:
                    pass
                elif len(messages) <= 1:
                    pass
                elif str(old_chat_message) == str(messages):
                    pass
                else:
                    self.addMessage(message=messages, color='White')
                    old_chat_message = messages
        except FileNotFoundError:
            pass

    def SpeechRecogText(self):
        status_file = os.path.join(TempDirPath, "Status.data")
        try:
            with open(status_file, "r", encoding='utf-8') as file:
                messages = file.read()
                self.label.setText(messages)
        except FileNotFoundError:
            pass

    def load_icon(self, path, width=60, height=60):
        if os.path.exists(path):
            pixmap = QPixmap(path)
            new_pixmap = pixmap.scaled(width, height)
            self.icon_label.setPixmap(new_pixmap)
        else:
            print(f"Icon not found at: {path}")

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath('Mic_on.png'), 60, 60)
            MicButtonInitialized()
        else:
            self.load_icon(GraphicsDirectoryPath('Mic_off.png'), 60, 60)
            MicButtonClosed()
        self.toggled = not self.toggled

    def addMessage(self, message, color):
        cursor = self.chat_text_edit.textCursor()
        format = QTextCharFormat()
        formatm = QTextBlockFormat()
        formatm.setTopMargin(10)
        formatm.setLeftMargin(10)
        format.setForeground(QColor(color))
        cursor.setCharFormat(format)
        cursor.setBlockFormat(formatm)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)

class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        gif_label = QLabel()
        gif_path = GraphicsDirectoryPath('Jarvis.gif')
        if os.path.exists(gif_path):
            movie = QMovie(gif_path)
            max_gif_size_H = int(screen_width/16*9)
            movie.setScaledSize(QSize(screen_width, max_gif_size_H))
            gif_label.setMovie(movie)
            movie.start()
        else:
            print(f"GIF not found at: {gif_path}")
            
        gif_label.setAlignment(Qt.AlignCenter)
        gif_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.icon_label = QLabel()
        icon_path = GraphicsDirectoryPath('Mic_on.png')
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            new_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.icon_label.setPixmap(new_pixmap)
        else:
            print(f"Icon not found at: {icon_path}")
            
        self.icon_label.setFixedSize(150, 150)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.toggled = True
        
        # Initialize files if they don't exist
        for file in ["Responses.data", "Status.data", "Mic.data"]:
            file_path = os.path.join(TempDirPath, file)
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding='utf-8') as f:
                    if file == "Mic.data":
                        f.write("False")
                    else:
                        f.write("")

        self.toggle_icon()
        self.icon_label.mousePressEvent = self.toggle_icon
        
        self.label = QLabel("")
        self.label.setStyleSheet("color:white; font-size:16px;margin-bottom:0;")
        
        content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        content_layout.setContentsMargins(0, 0, 0, 150)
        
        self.setLayout(content_layout)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        self.setStyleSheet("background-color:black;")
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)

    def SpeechRecogText(self):
        status_file = os.path.join(TempDirPath, "Status.data")
        try:
            with open(status_file, "r", encoding='utf-8') as file:
                messages = file.read()
                self.label.setText(messages)
        except FileNotFoundError:
            pass

    def load_icon(self, path, width=60, height=60):
        if os.path.exists(path):
            pixmap = QPixmap(path)
            new_pixmap = pixmap.scaled(width, height)
            self.icon_label.setPixmap(new_pixmap)
        else:
            print(f"Icon not found at: {path}")

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath('Mic_on.png'), 60, 60)
            MicButtonInitialized()
        else:
            self.load_icon(GraphicsDirectoryPath('Mic_off.png'), 60, 60)
            MicButtonClosed()
        self.toggled = not self.toggled

class MessageScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        
        layout = QVBoxLayout()
        label = QLabel("")
        layout.addWidget(label)
        
        chat_section = ChatSection()
        layout.addWidget(chat_section)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color:black;")
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)

class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.initUI()
        self.current_screen = None
        self.stacked_widget = stacked_widget

    def initUI(self):
        self.setFixedHeight(50)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignRight)
        
        # Home button
        home_button = QPushButton()
        home_icon_path = GraphicsDirectoryPath('Home.png')
        if os.path.exists(home_icon_path):
            home_icon = QIcon(home_icon_path)
            home_button.setIcon(home_icon)
        home_button.setText("Home")
        home_button.setStyleSheet("height:40px; line-height:40px; background-color:white;color:black")
        
        # Message button
        message_button = QPushButton()
        message_icon_path = GraphicsDirectoryPath('Chats.png')
        if os.path.exists(message_icon_path):
            message_icon = QIcon(message_icon_path)
            message_button.setIcon(message_icon)
        message_button.setText("Chat")
        message_button.setStyleSheet("height:40px; line-height:40px; background-color:white;color:black")
        
        # Minimize button
        minimize_button = QPushButton()
        minimize_icon_path = GraphicsDirectoryPath('Minimize2.png')
        if os.path.exists(minimize_icon_path):
            minimize_icon = QIcon(minimize_icon_path)
            minimize_button.setIcon(minimize_icon)
        minimize_button.setStyleSheet("background-color:white")
        minimize_button.clicked.connect(self.minimizeWindow)
        
        # Maximize button
        self.maximize_button = QPushButton()
        maximize_icon_path = GraphicsDirectoryPath('Maximize.png')
        if os.path.exists(maximize_icon_path):
            self.maximize_icon = QIcon(maximize_icon_path)
            self.maximize_button.setIcon(self.maximize_icon)
        self.restore_icon_path = GraphicsDirectoryPath('Minimize.png')
        if os.path.exists(self.restore_icon_path):
            self.restore_icon = QIcon(self.restore_icon_path)
        self.maximize_button.setFlat(True)
        self.maximize_button.setStyleSheet("background-color:white")
        self.maximize_button.clicked.connect(self.maximizeWindow)
        
        # Close button
        close_button = QPushButton()
        close_icon_path = GraphicsDirectoryPath('Close.png')
        if os.path.exists(close_icon_path):
            close_icon = QIcon(close_icon_path)
            close_button.setIcon(close_icon)
        close_button.setStyleSheet("background-color:white")
        close_button.clicked.connect(self.closeWindow)
        
        line_frame = QFrame()
        line_frame.setFixedHeight(1)
        line_frame.setFrameShape(QFrame.HLine)
        line_frame.setFrameShadow(QFrame.Sunken)
        line_frame.setStyleSheet("border-color:black;")
        
        title_label = QLabel(f"{str(Assistantname).capitalize()} AI  ")
        title_label.setStyleSheet("color:black; font-size:18px;background-color:white")
        
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        
        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch(1)
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)
        layout.addWidget(line_frame)
        
        self.draggable = True
        self.offset = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)
        super().paintEvent(event)

    def minimizeWindow(self):
        self.parent().showMinimized()

    def maximizeWindow(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            if hasattr(self, 'maximize_icon'):
                self.maximize_button.setIcon(self.maximize_icon)
        else:
            self.parent().showMaximized()
            if hasattr(self, 'restore_icon'):
                self.maximize_button.setIcon(self.restore_icon)

    def closeWindow(self):
        self.parent().close()

    def mousePressEvent(self, event):
        if self.draggable:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable and self.offset:
            new_pos = event.globalPos() - self.offset
            self.parent().move(new_pos)

    def showMessageScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()

        message_screen = MessageScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(message_screen)
        self.current_screen = message_screen
        
    def showInitialScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()

        initial_screen = InitialScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(initial_screen)
            self.current_screen = initial_screen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        
        # Create necessary files if they don't exist
        for file in ["Responses.data", "Status.data", "Mic.data"]:
            file_path = os.path.join(TempDirPath, file)
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding='utf-8') as f:
                    if file == "Mic.data":
                        f.write("False")
                    else:
                        f.write("")

        stacked_widget = QStackedWidget(self)
        initial_screen = InitialScreen()
        message_screen = MessageScreen()
        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen)
        
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setStyleSheet("background-color:black;")
        
        top_bar = CustomTopBar(self, stacked_widget)
        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    GraphicalUserInterface()
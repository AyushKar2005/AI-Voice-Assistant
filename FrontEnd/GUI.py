from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget,
    QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton,
    QFrame, QLabel, QSizePolicy
)
from PyQt5.QtCore import QEasingCurve
from PyQt5.QtGui import QPainter, QPen, QColor


from PyQt5.QtGui import (QIcon, QPainter, QMovie, QColor, QTextCharFormat, 
                         QFont, QPixmap, QTextBlockFormat, QRadialGradient,
                         QConicalGradient, QLinearGradient)
from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation, pyqtProperty, QPointF
from dotenv import dotenv_values
import os
import sys
import math
import random


current_dir = os.path.dirname(os.path.abspath(__file__))
Files_dir = os.path.join(current_dir, "Files")
Graphics_dir = os.path.join(current_dir, "Graphics")


os.makedirs(Files_dir, exist_ok=True)
os.makedirs(Graphics_dir, exist_ok=True)

env_path = os.path.join(current_dir, "..", ".env")
env_vars = dotenv_values(env_path)
Assistantname = env_vars.get("Assistantname")

old_chat_message = ""
TempDirPath = Files_dir
GraphicsDirPath = Graphics_dir

class JarvisAnimation(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(480, 270)
        self.setAlignment(Qt.AlignCenter)
        self._amplitude = 0
        self._pulse = 0
        self.active_color = QColor(0, 162, 232) 
        self.idle_color = QColor(100, 100, 100, 150) 
        self.current_color = self.idle_color
        self.arcs = 8
        self.max_radius = 100
        self.min_radius = 30
        self.center = QPointF(self.width()/2, self.height()/2)
        
        
        self.color_anim = QPropertyAnimation(self, b"color")
        self.color_anim.setDuration(500)
        self.color_anim.setEasingCurve(QEasingCurve.OutQuad)
        
        
        self.amplitude_anim = QPropertyAnimation(self, b"amplitude")
        self.amplitude_anim.setDuration(200)
        
        
        self.pulse_anim = QPropertyAnimation(self, b"pulse")
        self.pulse_anim.setDuration(1000)
        self.pulse_anim.setLoopCount(-1)  
        self.pulse_anim.setStartValue(0)
        self.pulse_anim.setEndValue(100)
        self.pulse_anim.start()
        

        self.dot_gradient = QRadialGradient(self.center, 15)
        self.dot_gradient.setColorAt(0, QColor(0, 162, 232, 200))
        self.dot_gradient.setColorAt(1, QColor(0, 162, 232, 0))

    def getAmplitude(self):
        return self._amplitude
    
    def resizeEvent(self, event):
        self.center = QPointF(self.width()/2, self.height()/2)

        self.dot_gradient = QRadialGradient(self.center, 15)
        self.dot_gradient.setColorAt(0, QColor(0, 162, 232, 200))
        self.dot_gradient.setColorAt(1, QColor(0, 162, 232, 0))
        super().resizeEvent(event)

    def setAmplitude(self, value):
        self._amplitude = min(max(value, 0), 100)
        self.update()

    amplitude = pyqtProperty(int, getAmplitude, setAmplitude)

    def getPulse(self):
        return self._pulse

    def setPulse(self, value):
        self._pulse = value
        self.update()

    pulse = pyqtProperty(int, getPulse, setPulse)

    def getColor(self):
        return self.current_color

    def setColor(self, color):
        self.current_color = color
        self.update()

    color = pyqtProperty(QColor, getColor, setColor)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        

        for i in range(3, 0, -1):
            radius = self.min_radius + (self.max_radius - self.min_radius) * (i/3)
            alpha = 50 - i*15
            color = QColor(self.current_color)
            color.setAlpha(alpha)
            painter.setPen(QPen(color, 1, Qt.SolidLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(self.center, radius, radius)
        
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.dot_gradient)
        painter.drawEllipse(self.center, 15, 15)
        
        
        painter.setPen(QPen(self.current_color, 2, Qt.SolidLine))
        painter.setBrush(Qt.NoBrush)
        
        arc_length = 30  
        spacing = 5      
        start_angle = self._pulse * 3.6  
        
        for i in range(self.arcs):
            radius = self.min_radius + (self.max_radius - self.min_radius) * (self._amplitude/100)
            angle = start_angle + i * (arc_length + spacing)
            
            
            gradient = QConicalGradient(self.center, angle)
            gradient.setColorAt(0, QColor(0, 162, 232, 200))
            gradient.setColorAt(0.5, QColor(255, 255, 255, 255))
            gradient.setColorAt(1, QColor(0, 162, 232, 200))
            
            pen = QPen(gradient, 2)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            
            
            variance = random.randint(-5, 5)
            painter.drawArc(
                int(self.center.x() - radius), 
                int(self.center.y() - radius), 
                int(radius * 2), 
                int(radius * 2), 
                int(angle * 16), 
                int((arc_length + variance) * 16)
            )

    def activate(self):
        self.color_anim.stop()
        self.color_anim.setStartValue(self.current_color)
        self.color_anim.setEndValue(self.active_color)
        self.color_anim.start()
        
        
        self.amplitude_anim.stop()
        self.amplitude_anim.setStartValue(self._amplitude)
        self.amplitude_anim.setEndValue(random.randint(60, 100))
        self.amplitude_anim.start()

    def deactivate(self):
        self.color_anim.stop()
        self.color_anim.setStartValue(self.current_color)
        self.color_anim.setEndValue(self.idle_color)
        self.color_anim.start()
        
        self.amplitude_anim.stop()
        self.amplitude_anim.setStartValue(self._amplitude)
        self.amplitude_anim.setEndValue(0)
        self.amplitude_anim.start()

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
    try:
        with open(mic_file, "r", encoding='utf-8') as f:
            Status = f.read()
            return Status
    except:
        return "False"
    
def SetAssistantStatus(Status):
    status_file = os.path.join(TempDirPath, "Status.data")
    with open(status_file, "w", encoding='utf-8') as f:
        f.write(Status)

def GetAssistantStatus():
    status_file = os.path.join(TempDirPath, "Status.data")
    try:
        with open(status_file, "r", encoding='utf-8') as f:
            Status = f.read()
            return Status
    except:
        return ""
    
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
        
        text_color = QColor(0, 162, 232)  
        text_color_text = QTextCharFormat()
        text_color_text.setForeground(text_color)
        self.chat_text_edit.setCurrentCharFormat(text_color_text)
        
        
        for file in ["Responses.data", "Status.data", "Mic.data"]:
            file_path = os.path.join(TempDirPath, file)
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding='utf-8') as f:
                    if file == "Mic.data":
                        f.write("False")
                    else:
                        f.write("")

        
        self.jarvis_animation = JarvisAnimation()
        self.jarvis_animation.setStyleSheet("border:none;")
        layout.addWidget(self.jarvis_animation)
        
        self.label = QLabel("")
        self.label.setStyleSheet("color:#00a2e8; font-size:16px; margin-right: 195px; border:none;margin-top:-30px;")
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)
        layout.setSpacing(-10)
        
        font = QFont()
        font.setPointSize(13)
        font.setFamily("Arial")
        font.setWeight(QFont.Bold)
        self.chat_text_edit.setFont(font)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.timeout.connect(self.updateMicStatus)
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
               background:#00a2e8;
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
                    self.addMessage(message=messages, color='#00a2e8')
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

    def updateMicStatus(self):
        mic_status = GetMicrophoneStatus()
        if mic_status.strip().lower() == "true":
            self.jarvis_animation.activate()
        else:
            self.jarvis_animation.deactivate()

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
        

        self.jarvis_animation = JarvisAnimation()
        self.jarvis_animation.setFixedSize(screen_width, int(screen_width/16*9))
        content_layout.addWidget(self.jarvis_animation, alignment=Qt.AlignCenter)
            
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(150, 150)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.toggled = True
        

        for file in ["Responses.data", "Status.data", "Mic.data"]:
            file_path = os.path.join(TempDirPath, file)
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding='utf-8') as f:
                    if file == "Mic.data":
                        f.write("False")
                    else:
                        f.write("")

        self.updateMicIcon()
        self.icon_label.mousePressEvent = self.toggle_icon
        
        self.label = QLabel("")
        self.label.setStyleSheet("color:#00a2e8; font-size:16px;margin-bottom:0;")
        
        content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        content_layout.setContentsMargins(0, 0, 0, 150)
        
        self.setLayout(content_layout)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        self.setStyleSheet("background-color:black;")
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.timeout.connect(self.updateMicStatus)
        self.timer.start(5)

    def SpeechRecogText(self):
        status_file = os.path.join(TempDirPath, "Status.data")
        try:
            with open(status_file, "r", encoding='utf-8') as file:
                messages = file.read()
                self.label.setText(messages)
        except FileNotFoundError:
            pass

    def updateMicStatus(self):
        mic_status = GetMicrophoneStatus()
        if mic_status.strip().lower() == "true":
            self.jarvis_animation.activate()
        else:
            self.jarvis_animation.deactivate()
        self.updateMicIcon()

    def updateMicIcon(self):
        mic_status = GetMicrophoneStatus()
        if mic_status.strip().lower() == "true":
            icon_path = GraphicsDirectoryPath('Mic_on.png')
            self.toggled = False
        else:
            icon_path = GraphicsDirectoryPath('Mic_off.png')
            self.toggled = True
            
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            new_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        if self.toggled:
            MicButtonClosed()
        else:
            MicButtonInitialized()
        self.toggled = not self.toggled
        self.updateMicIcon()

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
        
        
        home_button = QPushButton()
        home_icon_path = GraphicsDirectoryPath('Home.png')
        if os.path.exists(home_icon_path):
            home_icon = QIcon(home_icon_path)
            home_button.setIcon(home_icon)
        home_button.setText("Home")
        home_button.setStyleSheet("""
            height:40px; 
            line-height:40px; 
            background-color:#111111;
            color:#00a2e8;
            border:1px solid #00a2e8;
            border-radius:5px;
            padding:5px;
            font-weight:bold;
        """)
        
        
        message_button = QPushButton()
        message_icon_path = GraphicsDirectoryPath('Chats.png')
        if os.path.exists(message_icon_path):
            message_icon = QIcon(message_icon_path)
            message_button.setIcon(message_icon)
        message_button.setText("Chat")
        message_button.setStyleSheet("""
            height:40px; 
            line-height:40px; 
            background-color:#111111;
            color:#00a2e8;
            border:1px solid #00a2e8;
            border-radius:5px;
            padding:5px;
            font-weight:bold;
        """)
        
        
        minimize_button = QPushButton()
        minimize_icon_path = GraphicsDirectoryPath('Minimize2.png')
        if os.path.exists(minimize_icon_path):
            minimize_icon = QIcon(minimize_icon_path)
            minimize_button.setIcon(minimize_icon)
        minimize_button.setStyleSheet("""
            background-color:#111111;
            border:1px solid #00a2e8;
            border-radius:5px;
        """)
        minimize_button.clicked.connect(self.minimizeWindow)
        
        
        self.maximize_button = QPushButton()
        maximize_icon_path = GraphicsDirectoryPath('Maximize.png')
        if os.path.exists(maximize_icon_path):
            self.maximize_icon = QIcon(maximize_icon_path)
            self.maximize_button.setIcon(self.maximize_icon)
        self.restore_icon_path = GraphicsDirectoryPath('Minimize.png')
        if os.path.exists(self.restore_icon_path):
            self.restore_icon = QIcon(self.restore_icon_path)
        self.maximize_button.setFlat(True)
        self.maximize_button.setStyleSheet("""
            background-color:#111111;
            border:1px solid #00a2e8;
            border-radius:5px;
        """)
        self.maximize_button.clicked.connect(self.maximizeWindow)
        
        
        close_button = QPushButton()
        close_icon_path = GraphicsDirectoryPath('Close.png')
        if os.path.exists(close_icon_path):
            close_icon = QIcon(close_icon_path)
            close_button.setIcon(close_icon)
        close_button.setStyleSheet("""
            background-color:#111111;
            border:1px solid #00a2e8;
            border-radius:5px;
        """)
        close_button.clicked.connect(self.closeWindow)
        
        title_label = QLabel(f"{str(Assistantname).capitalize()} AI  ")
        title_label.setStyleSheet("""
            color:#00a2e8; 
            font-size:18px;
            background-color:transparent;
            font-weight:bold;
        """)
        
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
        
        self.draggable = True
        self.offset = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(20, 20, 20))
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
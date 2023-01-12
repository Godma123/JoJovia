import sys
import pygame
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QGridLayout, QGroupBox, QLabel, QRadioButton, QPushButton, QVBoxLayout, QWidget)
import random

class QuizApp(QWidget):
    def __init__(self):
        self.is_muted = False
        super().__init__()
        self.setWindowTitle("Jojo Bizarre Adventure Quiz")
        self.difficulty = "Easy"
        self.question_index = 0
        self.score = 0
        self.questions = {
            "Easy": [
                {
                    "question": "What is Jotaro's Stand?",
                    "options": ["Hermit Purple", "The World", "Star Platinum", "Killer Queen"],
                    "answer": "Star Platinum"
                },
                {
                    "question": "What is the name of Jotaro's grandfather?",
                    "options": ["Jotaro", "Jonathan", "Joseph", "Josuke"],
                    "answer": "Joseph"
                }
            ],
            "Medium": [
                {
                    "question": "What is the name of Jotaro's mother?",
                    "options": ["Holly", "Mary", "Jane", "Jolyne"],
                    "answer": "Holly"
                },
                {
                    "question": "What is Jotaro's epithet?",
                    "options": ["The Hand", "Jotaro", "Star Platinum", "Jotaro Kujo"],
                    "answer": "Jotaro Kujo"
                }
            ],
            "Hard": [
                {
                    "question": "What does Jotaro's Stand do?",
                    "options": ["Heal others", "Stop time", "Create illusions", "Create air blasts"],
                    "answer": "Stop time"
                },
            ],
            "Impossible": [
                {
                    "question": "What is Jotaro's stand's real name?",
                    "options": ["Hermit Purple", "The World", "Star Platinum: The World", "Killer Queen"],
                    "answer": "Star Platinum"
                },
            ]
        }
        self.create_intro_box()
        self.create_question_box()
        self.create_answer_box()
        self.create_score_box()
        
        
        self.mute_button = QPushButton("Mute Audio")
        
        self.mute_button.clicked.connect(self.mute_music)

        self.question_box.hide()
        self.answer_box.hide()
        self.score_box.hide()
        
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.intro_box)
        layout.addWidget(self.question_box)
        layout.addWidget(self.answer_box)
        layout.addWidget(self.score_box)
        
        
        self.setLayout(layout)
        self.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
            }
            QRadioButton {
                font-size: 18px;
            }
            QPushButton {
                font-size: 18px;
                color: white;
                background-color: blue;
                padding: 10px;
                border-radius: 10px;
            }
            QPushButton:pressed {
                background-color: darkblue;
            }
            QPushButton.selected {
                background-color: #0b3d91;
            }
        """)

        # Background music setup
        pygame.init()
        
        pygame.mixer.music.load("C:\\Users\\Kennedy\\Desktop\\JOJOQUIZAPP\\diotheme.mp3")
        pygame.mixer.music.play(-1)

        self.show()
        
    def hide_widgets(self):
        self.intro_box.hide()
        self.question_box.hide()
        self.answer_box.hide()
        self.score_box.hide()

    def set_easy(self):
        self.difficulty = "Easy"
        self.question_index = 0
        self.score = 0
        self.hide_widgets()
        self.question_box.show()
        self.answer_box.show()
        self.score_box.show()
        self.update_question()
        
    def set_medium(self):
        self.difficulty = "Medium"
        self.question_index = 0
        self.score = 0
        self.hide_widgets()
        self.question_box.show()
        self.answer_box.show()
        self.score_box.show()
        self.update_question()
        
    def set_hard(self):
        self.difficulty = "Hard"
        self.question_index = 0
        self.score = 0
        self.hide_widgets()
        self.question_box.show()
        self.answer_box.show()
        self.score_box.show()
        self.update_question()
        
    def set_impossible(self):
        self.difficulty = "Impossible"
        self.question_index = 0
        self.score = 0
        self.hide_widgets()
        self.question_box.show()
        self.answer_box.show()
        self.score_box.show()
        self.update_question()


        

    def start_quiz(self):
        self.intro_box.setVisible(False)
        self.question_box.setVisible(True)
        self.answer_box.setVisible(True)
        self.score_box.setVisible(True)
        self.update_question()


    def create_intro_box(self):
        intro_box = QGroupBox("Welcome to the Jojo Bizarre Adventure Quiz")
        layout = QVBoxLayout()

        self.easy_button = QPushButton("Easy")
        self.easy_button.clicked.connect(self.set_easy)
        self.easy_button.clicked.connect(self.easy_button.setChecked)

        self.medium_button = QPushButton("Medium")
        self.medium_button.clicked.connect(self.set_medium)
        self.medium_button.clicked.connect(self.medium_button.setChecked)

        self.hard_button = QPushButton("Hard")
        self.hard_button.clicked.connect(self.set_hard)
        self.hard_button.clicked.connect(self.hard_button.setChecked)

        self.impossible_button = QPushButton("Impossible")
        self.impossible_button.clicked.connect(self.set_impossible)
        self.impossible_button.clicked.connect(self.impossible_button.setChecked)

        layout.addWidget(self.easy_button)
        layout.addWidget(self.medium_button)
        layout.addWidget(self.hard_button)
        layout.addWidget(self.impossible_button)

        intro_box.setLayout(layout)
        self.intro_box = intro_box
                

    def create_question_box(self):
        self.question_box = QGroupBox()
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignCenter)
        self.options = [QRadioButton() for i in range(4)]
        for option in self.options:
            option.setAutoExclusive(False)
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.check_answer)
        layout = QGridLayout()
        layout.addWidget(self.question_label, 0, 0, 1, 2)
        
        
        self.question_box.setLayout(layout)
        self.question_box.hide()

    def create_answer_box(self):
        self.answer_box = QGroupBox("Answer")
        layout = QVBoxLayout()

        # Create radio buttons for the options
        self.options = []
        for i in range(4):
            option = QRadioButton()
            self.options.append(option)
            layout.addWidget(option)

        # Create submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.check_answer)
        layout.addWidget(self.submit_button)

        self.answer_box.setLayout(layout)

    def create_score_box(self):
        self.score_box = QGroupBox("Score")
        layout = QVBoxLayout()

        # Create label to display the score
        self.score_label = QLabel()
        layout.addWidget(self.score_label)

        self.score_box.setLayout(layout)


    def update_question(self):
        if self.question_index >= len(self.questions[self.difficulty]):
            self.end_quiz()
            return
        current_question = self.questions[self.difficulty][self.question_index]
        self.question_label.setText(current_question["question"])
        for i, option in enumerate(current_question["options"]):
            self.options[i].setText(option)
            self.options[i].setChecked(False)
        self.answer = current_question["answer"]

    def check_answer(self):
        for i, option in enumerate(self.options):
            if option.isChecked():
                if option.text() == self.answer:
                    self.score += 1
                    self.correct_sound.play()
                else:
                    self.wrong_sound.play()
                break
        self.question_index += 1
        self.next_question()

    def end_quiz(self):
        self.question_box.hide()
        self.score_label.setText(f"Your score is: {self.score}/{len(self.questions[self.difficulty])}")
        self.score_box.show()
        
    def mute_music(self):
        if self.is_muted:
            pygame.mixer.music.unpause()
            self.is_muted = False
            self.mute_button.setText("Mute Audio")
        else:
            pygame.mixer.music.pause()
            self.is_muted = True
            self.mute_button.setText("Unmute Audio")
            


        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    quiz_app = QuizApp()
    sys.exit(app.exec_())


    
        











       

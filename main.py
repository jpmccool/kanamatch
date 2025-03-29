import sys

from PySide6.QtGui import QIcon

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout, QHBoxLayout,
    QGroupBox,
    QCheckBox,
    QRadioButton,
    QSpinBox,
    QPushButton,
)

import kanadict
from game import MultipleChoiceGameWindow

class MainWindow (QMainWindow) :
    def __init__(self) :
        super().__init__()
        
        self.setWindowTitle("Kana Match")
        self.setWindowIcon(QIcon("icon.png"))

        self.topLabel        = QLabel("Choose your kana quiz:")
        self.kanaGroup       = QGroupBox("Script")
        self.hiraganaCheck   = QCheckBox("Hiragana")
        self.katakanaCheck   = QCheckBox("Katakana")
        self.setGroup        = QGroupBox("Include")
        self.basicCheck      = QCheckBox("Basic kana")
        self.diacriticCheck  = QCheckBox("Diacritics ( \" / º )")
        self.digraphCheck    = QCheckBox("Digraphs (yōon)")
        self.optionsGroup    = QGroupBox("Options")
        self.multipleRadio   = QRadioButton("Multiple choice")
        self.multipleSpin    = QSpinBox()
        self.multipleLabel   = QLabel("choices (max. 10)")
        self.inputRadio      = QRadioButton("Rōmaji input")
        self.hardCheck       = QCheckBox("No second chances (hard)") 
        self.startButton     = QPushButton("Start!")
        
        # TODO: Set previously selected options, or options from saved preferences, or sensible default options, in that order
        # TODO: Add a button to let the user save the current options, but only if they make sense
        self.hiraganaCheck.setChecked(True)   # This is a sensible default
        self.basicCheck.setChecked(True)      # This is a sensible default
        self.diacriticCheck.setChecked(False) # This is a sensible default
        self.digraphCheck.setChecked(False)   # This is a sensible default        
        self.multipleRadio.setChecked(True)   # This is a sensible default
        self.multipleSpin.setRange(2, 10)     # There must be at least two options for the quiz to be considered multiple choice
        self.multipleSpin.setValue(4)         # This is a sensible default
        self.startButton.clicked.connect(self.launch_game)
        
        self.layout_widgets()
                
    def layout_widgets (self) :
        
        kanaBox = QVBoxLayout()
        kanaBox.addStretch(1)
        kanaBox.addWidget(self.hiraganaCheck)
        kanaBox.addWidget(self.katakanaCheck)
        self.kanaGroup.setLayout(kanaBox)
        
        setBox = QVBoxLayout()
        setBox.addStretch(1)
        setBox.addWidget(self.basicCheck)
        setBox.addWidget(self.diacriticCheck)
        setBox.addWidget(self.digraphCheck)
        self.setGroup.setLayout(setBox)

        optionsBox = QVBoxLayout()
        optionsBox.addStretch(1)
        optionsBox.addWidget(self.multipleRadio)
        multipleBox = QHBoxLayout()        
        multipleBox.addWidget(self.multipleSpin)
        multipleBox.addWidget(self.multipleLabel)
        optionsBox.addLayout(multipleBox)
        optionsBox.addWidget(self.inputRadio)
        optionsBox.addWidget(self.hardCheck)        
        self.optionsGroup.setLayout(optionsBox)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.topLabel)
        mainLayout.addWidget(self.kanaGroup)
        mainLayout.addWidget(self.setGroup)
        mainLayout.addWidget(self.optionsGroup)
        mainLayout.addWidget(self.startButton)

        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)
    
    def launch_game (self) :
        hiragana  = self.hiraganaCheck.isChecked()
        katakana  = self.katakanaCheck.isChecked()
        basic     = self.basicCheck.isChecked()
        diacritic = self.diacriticCheck.isChecked()
        digraph   = self.digraphCheck.isChecked()
        if hiragana is katakana is False :
            print("Bad state: script not selected")
            return
        if basic is diacritic is digraph is False :
            print("Bad state: character subset not selected")
            return
        deck = (kanadict.hiragana if hiragana else set()) | (kanadict.katakana if katakana else set())
        if not basic :
            deck -= kanadict.basic
        if not diacritic :
            deck -= kanadict.diacritic
        if not digraph :
            deck -= kanadict.digraph
        
        self.game = MultipleChoiceGameWindow(deck, self.hardCheck.isChecked(), self.multipleSpin.value())
        self.game.show()
        
    
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()


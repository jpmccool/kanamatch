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

        topLabel             = QLabel("Choose your kana quiz:")
        kanaGroup            = QGroupBox("Script")
        self.hiraganaCheck   = QCheckBox("Hiragana")
        self.katakanaCheck   = QCheckBox("Katakana")
        setGroup             = QGroupBox("Include")
        self.basicCheck      = QCheckBox("Basic kana")
        self.diacriticCheck  = QCheckBox("Diacritics ( \" / º )")
        self.digraphCheck    = QCheckBox("Digraphs (yōon)")
        optionsGroup         = QGroupBox("Options")
        multipleRadio        = QRadioButton("Multiple choice")
        self.multipleSpin    = QSpinBox()
        multipleLabel        = QLabel("choices (max. 10)")
        inputRadio           = QRadioButton("Rōmaji input")
        self.hardCheck       = QCheckBox("No second chances (hard)") 
        startButton          = QPushButton("Start!")
        
        # TODO: Set previously selected options, or options from saved preferences, or sensible default options, in that order
        # TODO: Add a button to let the user save the current options, but only if they make sense
        self.hiraganaCheck.setChecked(True)   # This is a sensible default
        self.basicCheck.setChecked(True)      # This is a sensible default
        self.diacriticCheck.setChecked(False) # This is a sensible default
        self.digraphCheck.setChecked(False)   # This is a sensible default        
        multipleRadio.setChecked(True)  # This is a sensible default
        self.multipleSpin.setRange(2, 10)    # There must be at least two options for the quiz to be considered multiple choice
        self.multipleSpin.setValue(4)        # This is a sensible default
        startButton.clicked.connect(self.launch_game)
                
        kanaBox = QVBoxLayout()
        kanaBox.addStretch(1)
        kanaBox.addWidget(self.hiraganaCheck)
        kanaBox.addWidget(self.katakanaCheck)
        kanaGroup.setLayout(kanaBox)
        
        setBox = QVBoxLayout()
        setBox.addStretch(1)
        setBox.addWidget(self.basicCheck)
        setBox.addWidget(self.diacriticCheck)
        setBox.addWidget(self.digraphCheck)
        setGroup.setLayout(setBox)

        optionsBox = QVBoxLayout()
        optionsBox.addStretch(1)
        optionsBox.addWidget(multipleRadio)
        multipleBox = QHBoxLayout()        
        multipleBox.addWidget(self.multipleSpin)
        multipleBox.addWidget(multipleLabel)
        optionsBox.addLayout(multipleBox)
        optionsBox.addWidget(inputRadio)
        optionsBox.addWidget(self.hardCheck)        
        optionsGroup.setLayout(optionsBox)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(topLabel)
        mainLayout.addWidget(kanaGroup)
        mainLayout.addWidget(setGroup)
        mainLayout.addWidget(optionsGroup)
        mainLayout.addWidget(startButton)

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


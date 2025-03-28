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

class MainWindow (QMainWindow) :
    def __init__(self) :
        super().__init__()
        
        self.setWindowTitle("Kana Match")
        self.setWindowIcon(QIcon("icon.png"))

        topLabel        = QLabel("Choose your kana quiz:")
        kanaGroup       = QGroupBox("Script")
        self.hiraganaCheck   = QCheckBox("Hiragana")
        self.katakanaCheck   = QCheckBox("Katakana")
        setGroup        = QGroupBox("Include")
        self.basicCheck      = QCheckBox("Basic kana")
        self.diacriticCheck  = QCheckBox("Diacritics ( \" / º )")
        self.digraphCheck    = QCheckBox("Digraphs (yōon)")
        optionsGroup    = QGroupBox("Options")
        multipleRadio   = QRadioButton("Multiple choice")
        multipleSpin    = QSpinBox()
        multipleLabel   = QLabel("choices (max. 10)")
        inputRadio      = QRadioButton("Rōmaji input")
        hardCheck       = QCheckBox("No second chances (hard)") 
        startButton     = QPushButton("Start!")
        
        # TODO: Set previously selected options, or options from saved preferences, or sensible default options, in that order
        # TODO: Add a button to let the user save the current options, but only if they make sense
        self.hiraganaCheck.setChecked(True)  # This is a sensible default
        self.basicCheck.setChecked(True)     # This is a sensible default
        self.diacriticCheck.setChecked(True) # This is a sensible default
        self.digraphCheck.setChecked(True)   # This is a sensible default        
        multipleRadio.setChecked(True)  # This is a sensible default
        multipleSpin.setRange(2, 10)    # There must be at least two options for the quiz to be considered multiple choice
        multipleSpin.setValue(4)        # This is a sensible default
        startButton.clicked.connect(self.print_deck)
                
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
        multipleBox.addWidget(multipleSpin)
        multipleBox.addWidget(multipleLabel)
        optionsBox.addLayout(multipleBox)
        optionsBox.addWidget(inputRadio)
        optionsBox.addWidget(hardCheck)        
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
    
    def print_deck (self) :
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
        print(deck)
    
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()


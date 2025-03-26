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

class MainWindow (QMainWindow) :
    def __init__(self) :
        super().__init__()
        
        self.setWindowTitle("Kana Match")
        self.setWindowIcon(QIcon("icon.png"))

        topLabel        = QLabel("Choose your kana quiz:")
        kanaGroup       = QGroupBox("Kana")
        hiraganaCheck   = QCheckBox("Hiragana")
        katakanaCheck   = QCheckBox("Katakana")
        setGroup        = QGroupBox("Sets")
        basicCheck      = QCheckBox("Basic Kana")
        diacriticCheck  = QCheckBox("Diacritics ( \" / º )")
        digraphCheck    = QCheckBox("Digraphs (yōon)")
        optionsGroup    = QGroupBox("Options")
        
        multipleRadio   = QRadioButton("Multiple choice")
        multipleSpin    = QSpinBox()
        multipleLabel   = QLabel("choices (max. 10)")
        inputRadio      = QRadioButton("Rōmaji input")
        hardCheck       = QCheckBox("No second chances (hard)") 
        startButton     = QPushButton("Start!")
        
        # TODO: Set previously selected options, or options from saved preferences, or sensible default options, in that order
        # TODO: Add a button to let the user save the current options, but only if they make sense
        hiraganaCheck.setChecked(True)  # This is a sensible default
        basicCheck.setChecked(True)     # This is a sensible default        
        multipleRadio.setChecked(True)  # This is a sensible default
        multipleSpin.setRange(2, 10)     # There must be at least two options for the quiz to be considered multiple choice
        multipleSpin.setValue(4)        # This is a sensible default
        
        #startButton.clicked.connect(self.begin_quiz())
        
        kanaBox = QVBoxLayout()
        kanaBox.addStretch(1)
        kanaBox.addWidget(hiraganaCheck)
        kanaBox.addWidget(katakanaCheck)
        kanaGroup.setLayout(kanaBox)
        
        setBox = QVBoxLayout()
        setBox.addStretch(1)
        setBox.addWidget(basicCheck)
        setBox.addWidget(diacriticCheck)
        setBox.addWidget(digraphCheck)
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

    def toggleCheck (self) :
        print("toggled")
    
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()


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
from game import DirectInputGameWindow

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
        self.sizeGroup       = QGroupBox()
        self.sizeLabel       = QLabel()
        self.formatGroup     = QGroupBox("Format")
        self.multipleRadio   = QRadioButton("Multiple choice")
        self.multipleSpin    = QSpinBox()
        self.multipleLabel   = QLabel("choices (max. 10)")
        self.inputRadio      = QRadioButton("Rōmaji input")
        self.optionsGroup    = QGroupBox("Options")
        self.passCheck       = QCheckBox("Allow passes")
        self.hardCheck       = QCheckBox("No second chances (hard)")
        self.startButton     = QPushButton("Start!")
        
        # Sensible defaults
        self.hiraganaCheck.setChecked(True)
        self.basicCheck.setChecked(True)
        self.diacriticCheck.setChecked(False)
        self.digraphCheck.setChecked(False)        
        self.multipleRadio.setChecked(True)
        self.multipleSpin.setRange(2, 10)
        self.multipleSpin.setValue(4)
        
        # Connect widget signals
        self.hiraganaCheck.stateChanged.connect(self.update_deck)
        self.katakanaCheck.stateChanged.connect(self.update_deck)
        self.basicCheck.stateChanged.connect(self.update_deck)
        self.diacriticCheck.stateChanged.connect(self.update_deck)
        self.digraphCheck.stateChanged.connect(self.update_deck)
        self.startButton.clicked.connect(self.launch_game)
        
        self.layout_widgets()
        
        # Update the deck size
        self.update_deck()
    
        
    def update_deck (self) :
        hiragana  = self.hiraganaCheck.isChecked()
        katakana  = self.katakanaCheck.isChecked()
        basic     = self.basicCheck.isChecked()
        diacritic = self.diacriticCheck.isChecked()
        digraph   = self.digraphCheck.isChecked()
        if hiragana is katakana is False :
            size = 0
        elif basic is diacritic is digraph is False :
            size = 0
        else :
            self.deck = (kanadict.hiragana if hiragana else set()) | (kanadict.katakana if katakana else set())
            if not basic :
                self.deck -= kanadict.basic
            if not diacritic :
                self.deck -= kanadict.diacritic
            if not digraph :
                self.deck -= kanadict.digraph
            size = len(self.deck)
        if size == 0 :
            self.sizeLabel.setText("No cards selected")
            self.startButton.setEnabled(False)
        else :
            self.sizeLabel.setText(str(size) + " cards selected")
            self.startButton.setEnabled(True)
                
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
        
        sizeBox = QVBoxLayout()
        sizeBox.addStretch(1)
        sizeBox.addWidget(self.sizeLabel)
        self.sizeGroup.setLayout(sizeBox)
        
        formatBox = QVBoxLayout()
        formatBox.addStretch(1)
        formatBox.addWidget(self.multipleRadio)
        multipleBox = QHBoxLayout()
        multipleBox.addWidget(self.multipleSpin)
        multipleBox.addWidget(self.multipleLabel)
        formatBox.addLayout(multipleBox)
        formatBox.addWidget(self.inputRadio)
        self.formatGroup.setLayout(formatBox)

        optionsBox = QVBoxLayout()
        optionsBox.addStretch(1)
        optionsBox.addWidget(self.passCheck)
        optionsBox.addWidget(self.hardCheck)        
        self.optionsGroup.setLayout(optionsBox)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.topLabel)
        mainLayout.addWidget(self.kanaGroup)
        mainLayout.addWidget(self.setGroup)
        mainLayout.addWidget(self.sizeGroup)
        mainLayout.addWidget(self.formatGroup)
        mainLayout.addWidget(self.optionsGroup)
        mainLayout.addWidget(self.startButton)

        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)
        
    def launch_game (self) :
        
        isHard = self.hardCheck.isChecked()
        passEnabled = self.passCheck.isChecked()
        
        if self.multipleRadio.isChecked() :
            self.game = MultipleChoiceGameWindow(self.deck, isHard, passEnabled, self.multipleSpin.value())
        elif self.inputRadio.isChecked() :
            self.game = DirectInputGameWindow(self.deck, isHard, passEnabled)
            
        self.game.show()

    # Prevent the window from being resized by fixing the size to the current size
    # This must be done *after* showing the window, or the dimensions of self.size() are wrong!
    def show (self) :
        super().show()
        self.setFixedSize(self.size())
        
    
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()


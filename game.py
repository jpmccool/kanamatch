import sys, random

from PySide6.QtGui import (
    QIcon,
    QPixmap,
)

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout, QHBoxLayout,
    QPushButton,
)

import kanadict

class GameWindow (QMainWindow) :
    def __init__(self, deck) :
        super().__init__()
        
        self.setWindowTitle("Quiz Progress: 0%")
        self.setWindowIcon(QIcon("icon.png"))
        
        self.deck = deck
        self.tags = deck.copy()
        self.cardLabel = QLabel(self)
        self.inputLayout = QHBoxLayout()
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.cardLabel)
        mainLayout.addLayout(self.inputLayout)
        
        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)
        
    def draw_card (self) :
        card = self.deck.pop()
        self.cardLabel.setPixmap(QPixmap("./kana/" + card + ".png"))
        return card
    

class MultipleChoiceGameWindow (GameWindow) :
    def __init__ (self, deck, choices, hardMode) :
        super().__init__(deck)
        self.draw(choices, hardMode)
    
    def draw (self, choices, hardMode) :
        curr_card = self.draw_card()
        self.tags.remove(curr_card)
        # TODO: also remove any tags from self.tags with conflicting labels
        hand = random.sample(self.tags, choices - 1)
        hand.append(curr_card)
        hand = random.sample(hand, choices)
        for card in hand :
            button = QPushButton(kanadict.kana[card][1])
            if card is curr_card :
                button.clicked.connect(self.printOK)
            else :
                button.clicked.connect(self.printNG)
            self.inputLayout.addWidget(button)
        self.tags.add(curr_card)
        # TODO: Also add back in any cards taken out in the TODO above
            
    def printOK (self) :
        print("CORRECT!")
    def printNG (self) :
        print("Wrong answer!")

    
if __name__ == '__main__' :
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    app.exec()


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
    def __init__(self, deck, isHard) :
        super().__init__()
        
        self.setWindowIcon(QIcon("icon.png"))
        
        self.deck = deck    # The deck of flash cards to draw
        self.isHard = isHard
        
        self.score = 0
        self.n_cards = len(self.deck)
        
        self.cardLabel = QLabel(self)
        self.inputLayout = QHBoxLayout()
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.cardLabel)
        mainLayout.addLayout(self.inputLayout)
        
        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)
        
    def draw (self) :
        self.setWindowTitle("Quiz Progress: " + str(round(100 * (1 - (len(self.deck) / self.n_cards)))) + "%")
        card = self.deck.pop()
        self.cardLabel.setPixmap(QPixmap("./kana/" + card + ".png"))
        return card
    
    def end (self) : # TODO: Make a much more satisfying ending
        print("Complete!")
        print("Final score:", self.score)
        self.setWindowTitle("Quiz Complete!")
        # TODO: Replace graphic in label with a report of how the user did on their quiz
        # TODO: The above will require a bit more data collection on successes/failures in subclasses
        # TODO: Clear all widgets in the inputLayer, replace with a button that says "Close Results" that closes the window
    

class MultipleChoiceGameWindow (GameWindow) :
    def __init__ (self, deck, isHard, choices) :
        super().__init__(deck, isHard)
        self.tags = [*self.deck]
        self.choices = choices
        self.draw()
    
    def draw (self) :
        curr_card = super().draw()
        
        while self.inputLayout.count() > 0 :
            button = self.inputLayout.takeAt(0)
            if button.widget() is True :
                button.widget().deleteLater()
        
        
        self.tags.remove(curr_card)
        # TODO: also remove any tags from self.tags with conflicting labels
        hand = random.sample(self.tags, self.choices - 1)
        hand.append(curr_card)
        hand = random.sample(hand, self.choices)
        
        for card in hand :
            button = QPushButton(kanadict.kana[card][1]) # TODO: Set the label to include alternate acceptable answers, e.g. he / e, o / wo, etc.
            if card is curr_card :
                button.clicked.connect(self.success)
            else :
                button.clicked.connect(self.failure)
            self.inputLayout.addWidget(button)
        self.tags.append(curr_card)
        # TODO: Also add back in any cards taken out in the TODO above
            
    def success (self) :
        self.score += 1
        self.next()
    
    def failure (self) :
        self.score -= 1
        if self.isHard :
            self.next()
        else :
            self.sender().setEnabled(False)
    
    def next (self) :
        if len(self.deck) > 0 :
            self.draw()
        else : # End condition reached
            self.end()
    
    
    

    
if __name__ == '__main__' :
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    app.exec()


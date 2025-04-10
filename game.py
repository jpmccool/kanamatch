import sys, random

from PySide6.QtCore import (
    Qt,
)

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
    def __init__(self, deck, isHard, passEnabled) :
        super().__init__()
        
        self.setWindowIcon(QIcon("icon.png"))
        
        self.deck = deck    # The deck of flash cards to draw
        self.isHard = isHard
        self.passEnabled = passEnabled
        
        self.score = 0
        self.n_cards = len(self.deck)
        self.correct_responses = 0
        self.incorrect_responses = 0
        self.passes = 0
        
        self.cardLabel = QLabel()
        self.cardLabel.setAlignment(Qt.AlignHCenter)
        self.inputLayout = QHBoxLayout()
        
        self.layout_widgets()
    
    def layout_widgets (self) :
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.cardLabel, Qt.AlignHCenter)
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
    def __init__ (self, deck, isHard, passEnabled, choices) :
        super().__init__(deck, isHard, passEnabled)
        self.tags = [*self.deck]
        self.choices = choices
        self.draw()
    
    def draw (self) :
        # Draw a card
        curr_card = super().draw()
        # Clear the inputLayout of old buttons, if any
        while self.inputLayout.count() > 0 :
            button = self.inputLayout.takeAt(0)
            if button.widget() is True :
                button.widget().deleteLater()
        # Remove the current card from the list of tags temporarily to avoid false buttons
        self.tags.remove(curr_card)
        # TODO: also remove any tags from self.tags with conflicting labels, temporarily: ji and (d)ji, zu and (d)zu, ha/wa and wa, he/e and e, wo/o and o
        # Build a hand of random tags for the 'wrong' options and shuffle in the one correct tag (curr_card)
        hand = random.sample(self.tags, self.choices - 1)
        hand.append(curr_card)
        hand = random.sample(hand, self.choices)
        # For each card in the hand, add a new button with the appropriate label to the inputLayout
        for card in hand :
            button = QPushButton(kanadict.kana[card][1]) # TODO: Set the label to include alternate acceptable answers, e.g. he / e, o / wo, etc.
            if card is curr_card :
                button.clicked.connect(self.success)
            else :
                button.clicked.connect(self.failure)
            self.inputLayout.addWidget(button)
        # If passing is an option, add a pass button
        if self.passEnabled :
            button = QPushButton("Pass")
            button.clicked.connect(self.pass_on)
            self.inputLayout.addWidget(button)
        # Add the current card back to the list of tags so that it can appear as a wrong answer later (or you'll run out of tags at the end!)
        self.tags.append(curr_card)
        # TODO: Also add back in any cards taken out in the TODO above
    
    # One point for a correct guess, then move on to the next card
    def success (self) :
        self.score += 1
        self.correct_responses += 1
        self.next()
    
    # Minus one point for a wrong guess, then either move on to the next card (isHard) or grey out the button (otherwise)
    def failure (self) :
        self.score -= 1
        self.incorrect_responses += 1
        if self.isHard :
            self.next()
        else :
            self.sender().setEnabled(False)
    
    # No points added or deducted for passing, then move on to the next card
    def pass_on (self) :
        self.passes += 1
        self.next()
    
    # Draw the next card, or end the game if the deck is empty
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


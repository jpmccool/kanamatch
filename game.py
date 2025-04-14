import sys, random

from PySide6.QtCore import (
    Qt,
)

from PySide6.QtGui import (
    QIcon,
    QPixmap,
)

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit
)

import kanadict

class GameWindow (QMainWindow) :
    def __init__(self, deck, isHard, passEnabled) :
        super().__init__()
        
        self.setWindowIcon(QIcon("icon.png"))
        
        # Copy the provided deck into a list and shuffle it
        self.deck = [*deck]
        random.shuffle(self.deck)
        
        self.isHard = isHard
        self.passEnabled = passEnabled
        
        self.score = 0
        self.correct = 0
        self.incorrect = 0
        self.passes = 0
        
        self.next_card = 0
        
        self.cardLabel = QLabel()
        self.cardLabel.setAlignment(Qt.AlignHCenter)
        self.inputLayout = QHBoxLayout()
        
        self.layout_widgets()
    
    # Lay out widgets
    def layout_widgets (self) :
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.cardLabel, Qt.AlignHCenter)
        self.mainLayout.addLayout(self.inputLayout)
        centralWidget = QWidget()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)
    
    # Draw a card from the deck and display it
    def draw (self) :
        self.setWindowTitle("Quiz Progress: " + str( round(100 * self.next_card / len(self.deck)) ) + "%")
        card = self.deck[self.next_card]
        self.next_card += 1
        self.cardLabel.setPixmap(QPixmap("./kana/" + card + ".png"))
        return card
    
    # End the game and display a report
    def end (self) :
        self.clear_layout(self.mainLayout)
        self.setWindowTitle("Quiz Complete!")
        report  = "<h1>Quiz Complete!</h1><br /><br />"
        report += "<p><b>Here's how you did...</b></p>"
        report += "<table>"
        report += "<tr><td style=\"text-align: right;\">" + str(self.correct) + " </td><td> responses were <b>correct</b></td></tr>"
        report += "<tr><td style=\"text-align: right;\">" + str(self.incorrect) + " </td><td> responses were <b>incorrect</b></td></tr>"
        if self.passEnabled :
            report += "<tr><td style=\"text-align: right;\">" + str(self.passes) + " </td><td> cards were <b>passed over</b></td></tr>"
        report += "</table>"
        report += "<p>Total score: <b>" + str(self.score) + "</b></p>"
        reportLabel = QLabel(report)
        reportLabel.setTextFormat(Qt.RichText)
        reportLabel.setWordWrap(True)
        self.mainLayout.addWidget(reportLabel)
        closeButton = QPushButton("Close")
        closeButton.clicked.connect(self.close_window)
        self.mainLayout.addWidget(closeButton)
        
    # Useful for cleaning up layouts
    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clear_layout(child.layout())
    
    # Close the game window
    def close_window (self) :
        self.close()
        self.destroy()

class MultipleChoiceGameWindow (GameWindow) :
    
    def __init__ (self, deck, isHard, passEnabled, choices) :
        super().__init__(deck, isHard, passEnabled)
        self.tags = [*self.deck]
        self.choices = choices
        self.draw()
    
    def draw (self) :
        # Draw a card
        curr_card = super().draw()
        # Clear the inputLayout of old buttons
        self.clear_layout(self.inputLayout)
        # Remove the current card from the list of tags temporarily to avoid false buttons
        self.tags.remove(curr_card)
        # TODO: also remove any tags from self.tags with conflicting labels, temporarily: ji and (d)ji, zu and (d)zu, ha/wa and wa, he/e and e, wo/o and o
        # Build a hand of random tags for the 'wrong' options and shuffle in the one correct tag (curr_card)
        random.shuffle(self.tags)        
        hand = self.tags[:self.choices - 1]
        hand.append(curr_card)
        random.shuffle(hand)
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
        self.correct += 1
        self.next()
    
    # Minus one point for a wrong guess, then either move on to the next card (isHard) or grey out the button (otherwise)
    def failure (self) :
        self.score -= 1
        self.incorrect += 1
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
        if self.next_card < len(self.deck) :
            self.draw()
        else : # End condition reached
            self.end()
    

    
class DirectInputGameWindow (GameWindow) :
    
    def __init__ (self, deck, isHard, passEnabled) :
        super().__init__(deck, isHard, passEnabled)
        self.inputLine = QLineEdit()
        self.inputLine.setAlignment(Qt.AlignRight)
        self.inputLine.returnPressed.connect(self.submit)
        self.submitButton = QPushButton("Submit")
        self.submitButton.clicked.connect(self.submit)
        if passEnabled :
            self.passButton = QPushButton("Pass")
            self.passButton.clicked.connect(self.pass_on)
            self.inputLayout.addWidget(self.passButton)
        self.inputLayout.addWidget(self.inputLine)
        self.inputLayout.addWidget(self.submitButton)
        self.draw()
    
    def draw (self) :
        # Draw a card and set the current correct response
        curr_card = super().draw()
        self.correct_response = kanadict.kana[curr_card][1]
        # Clear the input line of old text
        self.inputLine.clear()
        self.inputLine.setFocus()
    
    def submit (self) :
        response = self.inputLine.text()
        # Correct response is a success
        if response == self.correct_response :
            self.success()
        # Incorrect response is a failure
        else :
            self.failure()
            
    # One point for a correct guess, then move on to the next card
    def success (self) :
        self.score += 1
        self.correct += 1
        self.next()
    
    # Minus one point for a wrong guess, then either move on to the next card (isHard) or don't
    def failure (self) :
        self.score -= 1
        self.incorrect += 1
        if self.isHard :
            self.next()
        else :
            # TODO: Should indicate that the user should try again
            pass
    
    # No points added or deducted for passing, then move on to the next card
    def pass_on (self) :
        self.passes += 1
        self.next()
    
    # Draw the next card, or end the game if the deck is empty
    def next (self) :
        if self.next_card < len(self.deck) :
            self.draw()
        else : # End condition reached
            self.end()
    

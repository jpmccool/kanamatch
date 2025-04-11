# kanamatch

A simple Japanese kana flash-card matching game


## About

Kana Match is a simple flash-card matching game that tests your knowledge of the Japanese hiragana and katakana syllabaries and their Hepburn romanizations.

Two game modes are offered: multiple choice (easier) and direct input of rōmaji (harder).

You can set up your quiz with a pass option to avoid losing points, or really test yourself with No Second Chances mode, where you only get one shot at a correct response to each card.


## Development

The program is written in Python using the PySide6 (QT) GUI framework, and should be compatible with Windows, Mac, & Linux.

UPDATE (2025-04-11): Kana Match is now in beta! Basic quizzes are fully playable. Please try it out!

Please don't hesistate to contact the author or file a bug report on GitHub if you find any bugs. Feature requests are also welcome!

Have fun!

Kana Match is still in development. Please check back for updates soon!


## Installation

Copy the code from this repository and run the main program:

```
python3 main.py
```

If PySide6 is not installed on your system, you can add it quickly as a Python pip:

```
python3 -m pip install pyside6
```

On Linux systems, if you encounter this error:
```
qt.qpa.plugin: From 6.5.0, xcb-cursor0 or libxcb-cursor0 is needed to load the Qt xcb platform plugin.
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
```
install the system package 'libxcb-cursor0':
```
sudo apt install libxcb-cursor0
```


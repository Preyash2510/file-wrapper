import os
from threading import Thread

# PyQt6 imports for the app
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import \
    QWidget, \
    QTabWidget, \
    QLabel, QDialog, QScrollArea, QVBoxLayout

import styles   # Component Styles
from Error import Wrapper_Error # Error Window

"""
    This class wraps all the files or directory to width given to it.
    It will also creates a window where all the windowed output is shown, using tabs.
"""


class Wrapper:
    def __init__(self, window, data, index):
        self.error = 0
        self.width = 0
        self.window = window
        self.f = []                     # Wrap output to File
        self.w = []                     # Wrap output to Window
        self.d = []                     # Wrap Directory
        self.col_num = 0

        self.separate(data, index)

    """
        This method separates the data to its specific transfer list
    """
    def separate(self, d, index):
        # For each index to wrap from the data list
        for i in index:
            if d[i]['type'] == 'file' and d[i]['transfer'] == 'File':
                self.f.append(d[i])
            elif d[i]['type'] == 'file' and d[i]['transfer'] == 'Window':
                self.w.append(d[i])
            else:
                self.d.append(d[i])

    # Wraps the files and outputs it to file
    def wrap_to_file(self):
        for d in self.f:
            # Open the file in the list and read it
            with open(d['path'], 'r') as file:
                path = os.path.dirname(os.path.abspath(d['path']))
                out_file = open((path + os.sep + 'wrap.' + d['name']), 'w')

                # read the file
                self.wrap_read(in_file=file, func=out_file.write)
                out_file.close()

    # Wraps the files and outputs it to Window
    def wrap_to_window(self):
        # Create Window with TabView
        w = QDialog(self.window)
        w.setFixedSize(600, 600)
        w.setWindowTitle('Wrapped Files')

        tabs = QTabWidget(w)
        tabs.setFixedSize(600, 600)
        i = 0

        for d in self.w:
            tabs.addTab(Tab(d['path']), d['name'])
            # Open the file in the list and read it
            with open(d['path'], 'r') as file:
                tab = tabs.widget(i)
                self.wrap_read(in_file=file, func=tab.write)

            i += 1

        w.show()

    # Wraps the Directories:- Each Directory file wraps it to a 'wrap.filename.txt' files
    def wrap_dir(self):
        for d in self.d:
            for filename in os.listdir(d['path']):
                if filename.endswith('.txt'):
                    path = os.path.abspath(d['path']) + os.sep + filename
                    with open(path, 'r') as file:
                        out_file = open((d['path'] + os.sep + 'wrap.' + filename), 'w')

                        self.wrap_read(in_file=file, func=out_file.write)

                        out_file.close()

    # Start the Wrapping process using Threads
    def start(self, width, dialog):
        dialog.close()
        self.width = width

        f_th = Thread(target=self.wrap_to_file)  # File Wrap Thread
        d_th = Thread(target=self.wrap_dir)      # Directory Wrap Thread

        f_th.start()
        d_th.start()
        self.wrap_to_window()                    # Wrap output to Window

        f_th.join()
        d_th.join()

        # If there are words that are bigger then wrap width then show error
        if self.error != 0:
            Wrapper_Error(self.window,
                          "There are {0} words larger than wrap width provide".
                          format(self.error)
                          )

    # Read the file character by character and send it to write to its particular function
    def wrap_read(self, in_file, func):
        self.col_num = 0
        is_Word = False
        paragraph = False
        newLine = 0
        word = ''
        while c := in_file.read(1):
            if not c:
                self.wrap_write(word, func)
                break

            if c.isspace():
                if is_Word:
                    is_Word = False
                    self.wrap_write(word, func)
                    word = ''

                if c == '\n':
                    is_Word = False
                    newLine += 1
                    if newLine > 1 and not paragraph:
                        newLine = 0
                        paragraph = True
                        word = '\n\n'
                        self.wrap_write(word, func)
                        word = ''
                else:
                    continue

            else:
                newLine = 0
                paragraph = False
                is_Word = True
                word += c

        if word:
            self.wrap_write(word, func)
            word = ''

    # Write to file using function that is passed
    def wrap_write(self, word, func):
        if len(word) > self.width:
            if word:
                func('\n')
            self.error += 1
        else:
            if not self.col_num == 0:
                self.col_num += 1

                if (self.col_num + len(word)) > self.width and word != '\n\n':
                    func('\n')
                    self.col_num = 0
                else:
                    func(' ')

            if word == '\n\n':
                self.col_num = 0
            else:
                self.col_num += len(word)

        func(word)


"""
    This class is used as tab for the Tab View with it own write method to write to QLabel
"""


class Tab(QWidget):
    def __init__(self, name):
        super(Tab, self).__init__()
        sc_name = QScrollArea(self)
        sc_name.setWidgetResizable(True)
        sc_name.setMinimumWidth(593)
        sc_name.setMinimumHeight(25)
        sc_name.setStyleSheet(styles.SCROLL)
        wid_n = QWidget(sc_name)
        lay_n = QVBoxLayout(wid_n)
        sc_name.setWidget(wid_n)

        self.name = QLabel(wid_n)
        self.name.setText(name)
        self.name.setFixedSize(550, 25)
        self.name.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        lay_n.addWidget(self.name)

        font = self.name.font()
        font.setBold(True)
        font.setUnderline(True)
        self.name.setFont(font)
        self.name.setWordWrap(True)

        sc_data = QScrollArea(self)
        sc_data.setWidgetResizable(True)
        sc_data.setMinimumWidth(593)
        sc_data.setMinimumHeight(510)
        sc_data.setStyleSheet(styles.SCROLL)
        wid_d = QWidget(sc_data)
        lay_d = QVBoxLayout(wid_d)
        sc_data.setWidget(wid_d)
        sc_data.move(0, 50)

        self.data = QLabel(wid_d)
        self.data.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        d_font = self.data.font()
        d_font.setFamily('Consolas')
        self.data.setFont(d_font)
        self.data.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        lay_d.addWidget(self.data)

    # Append to QLabel
    def write(self, word):
        prev = self.data.text()
        self.data.setText(prev + word)


import os
import sys

# PyQt6 imports for the app
from PyQt6 import QtCore as Qt

from PyQt6.QtWidgets import \
    QApplication, \
    QWidget, \
    QPushButton, \
    QLabel, \
    QComboBox, \
    QTableWidget, \
    QFileDialog, \
    QDialog, \
    QTableWidgetItem, \
    QHBoxLayout, \
    QAbstractItemView, \
    QCheckBox, \
    QLineEdit

from PyQt6.QtGui import \
    QIcon, \
    QPixmap

import styles as st  # Component Styles
import Wrapper  # Wrapper to wrap files
from Error import Wrapper_Error  # Error Window
"""
    Class for  the Main window: Inherits from QWidgets
    Components: 
        QTableWidget:
            -> Displays all the files and directories chosen from the computer
            -> AlLows to select files and directories using QCheckBoxes:
                -> When selected put the row index into an array
        
        QPushButtons:
            -> Add:
                -> Opens a Dialog to choose the file type (Files or Directory)
                -> Adds the Selected file and directory to the table
            -> Deselect:
                -> Unchecks all the CheckBoxes from the table
            -> Wrap:
                -> Input a wrap Column size the files and directory
                -> Start the wrap process by initializing the Wrapper Class
            -> Clear:
                -> Removes all the rows from the Table
"""


class Window(QWidget):
    i = 0
    data = []
    index = []

    # Initialize the Main Window
    def __init__(self):
        super().__init__()
        self.setWindowTitle('File Wrapper')
        self.setWindowIcon(QIcon('images/gift.png'))
        self.setFixedSize(900, 700)
        self.setStyleSheet('background-color: white')
        self.__gui()

    # Add necessary Component Table, Button
    def __gui(self):
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Check', 'Names', 'Type', 'Transfer To'])
        col_size = int(self.width() / 2)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, col_size - 50)
        self.table.setColumnWidth(2, 50)
        self.table.setColumnWidth(3, col_size - 50)
        self.table.setStyleSheet(st.TABLE)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setFixedSize(self.width(), self.height() - 100)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.table.setFocusPolicy(Qt.Qt.FocusPolicy.NoFocus)

        # Deselects all the Checkboxes in Table
        deselect = QPushButton(self)
        deselect.setText('Deselect')
        deselect.setStyleSheet(st.BUTTON_DESELECT)
        deselect.setFixedSize(175, 50)
        deselect.move(int((self.width() / 4) - 175), self.height() - 75)
        deselect.clicked.connect(lambda: self.deselect())

        # Adds Files and Directory
        add = QPushButton(self)
        add.setText('ADD')
        add.setStyleSheet(st.BUTTON_ADD)
        add.setFixedSize(200, 60)
        add.move(int((self.width() / 2) - 210), self.height() - 80)
        add.clicked.connect(lambda: self.select_file_mode())

        # Wraps the selection
        run = QPushButton(self)
        run.setText('Wrap')
        run.setStyleSheet(st.BUTTON_RUN)
        run.setFixedSize(200, 60)
        run.move(int((self.width() / 2) + 10), self.height() - 80)
        run.clicked.connect(lambda: self._wrap())

        # Clears the Table
        clear = QPushButton(self)
        clear.setText('Clear')
        clear.setStyleSheet(st.BUTTON_CLEAR)
        clear.setFixedSize(175, 50)
        clear.move(int((self.width() / 4) + 450), self.height() - 75)
        clear.clicked.connect(lambda: self.clear())

    # Deselect the Checkboxes in the Table
    def deselect(self):
        for i in range(self.table.rowCount()):
            c = self.table.cellWidget(i, 0).layout().itemAt(0).widget()
            if c.isChecked():
                self.table.selectRow(i)
                c.setChecked(False)
        self.index.clear()

    # Ask for File type using a Dialog Box
    def select_file_mode(self):
        dia = QDialog(self)
        dia.setFixedSize(300, 100)
        dia.setWindowTitle('Select a File Type')
        dia.setWindowFlag(Qt.Qt.WindowType.FramelessWindowHint)
        dia.setStyleSheet("""
            QDialog {
                background-color: white;
                border: 2px solid gray; 
                border-radius: 15px;
            }
        """)

        com = QComboBox(dia)
        com.setFixedSize(150, 30)
        com.addItems(['File', 'Directory'])
        com.setStyleSheet(st.COMBOBOX)
        com.move(int((dia.width() / 2) - 75), 20)

        ok = QPushButton(dia, text='Ok')
        ok.setStyleSheet(st.BUTTON_OK)
        ok.setFixedSize(100, 30)
        ok.move(int(dia.width() / 2) - 110, dia.height() - 35)
        ok.clicked.connect(lambda: self.file_choose(dia, com.itemText(com.currentIndex())))

        cancel = QPushButton(dia, text='Cancel')
        cancel.setStyleSheet(st.BUTTON_CANCEL)
        cancel.setFixedSize(100, 30)
        cancel.move(int(dia.width() / 2) + 10, dia.height() - 35)
        cancel.clicked.connect(lambda: dia.close())

        dia.show()

    # Open the File Dialog box to choose files or directory
    def file_choose(self, dia, file_type):
        dia.close()
        fileDialog = QFileDialog(self)
        if file_type == 'File':
            fileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
            names = fileDialog.getOpenFileNames(self,
                                                'Select Files',
                                                '.',
                                                'Text files (*.txt)'
                                                )[0]
            if names:
                self.add_files(names)

        elif file_type == 'Directory':
            fileDialog.setFileMode(QFileDialog.FileMode.Directory)
            name = fileDialog.getExistingDirectory(self,
                                                   'Select Directory',
                                                   '.',
                                                   QFileDialog.Option.ShowDirsOnly |
                                                   QFileDialog.Option.DontResolveSymlinks)
            if name:
                self.add_dir(name)
        else:
            pass

    # Add the Files to the Table and the data list
    def add_files(self, names):
        for i in range(len(names)):
            self.data.append({
                'path': names[i],
                'name': names[i].split('/')[-1],
                'type': 'file',
                'transfer': None
            })

            self.add_to_table(row_data=self.data[-1])

    # Add the Directory to the Table and the data list
    def add_dir(self, name):
        self.data.append({
            'path': name,
            'name': name.split('/')[-1],
            'type': 'directory',
            'transfer': None
        })

        self.add_to_table(row_data=self.data[-1])

    # Add the file or directory to table in a row
    # Row: checkbox | name | type | transfer type
    def add_to_table(self, row_data=None):
        if row_data is None:
            row_data = {}

        row = self.table.rowCount()
        self.table.insertRow(row)

        # Add Checkbox to Row and center it
        c_widget = QWidget()
        c_layout = QHBoxLayout(c_widget)

        check = QCheckBox()
        check.clicked.connect(lambda: self.__checkbox_click(row))

        c_layout.addWidget(check)
        c_layout.setAlignment(Qt.Qt.AlignmentFlag.AlignCenter)
        c_layout.setContentsMargins(0, 0, 0, 0)
        c_widget.setLayout(c_layout)
        self.table.setCellWidget(row, 0, c_widget)

        # Add Name of the file or the path
        label = self.__set_name(row_data)
        self.table.setItem(row, 1, label)

        # Add the type icon
        self.table.setCellWidget(row, 2, self.__set_icon(row_data['type']))

        # Add the Combo box to select the transfer type
        b_widget = QWidget()
        b_layout = QHBoxLayout(b_widget)
        b_layout.addWidget(self.__set_combo_box(row))
        b_layout.setAlignment(Qt.Qt.AlignmentFlag.AlignCenter)
        b_layout.setContentsMargins(0, 0, 0, 0)
        b_widget.setLayout(b_layout)

        self.table.setCellWidget(row, 3, b_widget)

    # Add the Name of the file if in the same directory
    # else add the absolute path to the file
    @staticmethod
    def __set_name(row_data):
        rtn = QTableWidgetItem()
        if row_data['path'].split('/')[-2] == os.getcwd().split(os.sep)[-1]:
            rtn.setText(f'. / {row_data["name"]}')
        else:
            rtn.setText(row_data['path'])

        rtn.setTextAlignment(Qt.Qt.AlignmentFlag.AlignCenter)
        return rtn

    # Add the icon according to type of file
    @staticmethod
    def __set_icon(file_type):
        i_widget = QWidget()
        i_layout = QHBoxLayout(i_widget)
        icon = QLabel()

        if file_type == 'file':
            pix = QPixmap('images/file-alt-solid.svg')
        else:
            pix = QPixmap('images/folder-solid.svg')

        icon.setPixmap(pix.scaled(20, 20, Qt.Qt.AspectRatioMode.KeepAspectRatio))
        i_layout.addWidget(icon)
        i_layout.setAlignment(Qt.Qt.AlignmentFlag.AlignCenter)
        i_layout.setContentsMargins(0, 0, 0, 0)
        i_widget.setLayout(i_layout)

        return i_widget

    # Set the combo box
    def __set_combo_box(self, row):
        com = QComboBox(self.table)
        com.setFixedSize(self.table.columnWidth(3) - 100, 28)
        com.addItems(['-', 'Window', 'File'])
        com.setStyleSheet(st.COMBOBOX)
        com.currentIndexChanged.connect(lambda:
                                        self.__change_combo_box(row,
                                                                com.itemText(
                                                                    com.currentIndex()
                                                                )
                                                                )
                                        )
        com.setCurrentIndex(1)

        # If the file type is directory the disable the Combo box
        if self.data[row]['type'] == 'directory':
            com.setCurrentIndex(2)
            com.setDisabled(True)

        return com

    # Event method called when combox box selection is changed
    # Add the selected value to the data[row] dict 'transfer' value
    def __change_combo_box(self, row, item):
        self.data[row]['transfer'] = item

    # Event method called when checkbox is clicked
    # Adds the the index to a array
    def __checkbox_click(self, row):
        self.table.selectRow(row)
        if row in self.index:
            self.index.remove(row)
        else:
            self.index.append(row)

    # Starts the file wrapping process by call Wrapper class
    def _wrap(self):
        if not self.data:
            Wrapper_Error(self, 'Please add Files or Directory')
        elif not self.index:
            Wrapper_Error(self, 'Please checks Files or Directory to be wrapped')
        else:
            wrap = Wrapper.Wrapper(self, self.data, self.index)

            # Choose a column width for the wrap
            dia = QDialog(self)
            dia.setFixedSize(300, 100)
            dia.setWindowTitle('Select a Wrap Width')

            inp = QLineEdit(dia)
            inp.setFixedSize(150, 30)
            inp.setAlignment(Qt.Qt.AlignmentFlag.AlignCenter)
            inp.setStyleSheet("""
                        QLineEdit {
                            border: 1px solid black;
                            border-radius: 5px;
                        }
                    """)
            inp.move(int((dia.width() / 2) - 75), 20)

            ok = QPushButton(dia, text='Ok')
            ok.setStyleSheet(st.BUTTON_OK)
            ok.setFixedSize(100, 30)
            ok.move(int(dia.width() / 2) - 110, dia.height() - 35)
            # Start the process
            ok.clicked.connect(lambda: wrap.start(int(inp.text()), dia))

            cancel = QPushButton(dia, text='Cancel')
            cancel.setStyleSheet(st.BUTTON_CANCEL)
            cancel.setFixedSize(100, 30)
            cancel.move(int(dia.width() / 2) + 10, dia.height() - 35)
            cancel.clicked.connect(lambda: dia.close())

            dia.show()

    # Remove everything from the Table
    def clear(self):
        r = self.table.rowCount()
        for i in range(r):
            self.table.removeRow(0)
        self.data.clear()
        self.index.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


# Style for ComboBox
COMBOBOX = """
    QComboBox {
        border: 1px solid gray;
        border-radius: 5px;
    }
    
    QComboBox::drop-down {
        border: 0;
        width: 30px;
        height: 29px;
    }
    
    QComboBox::down-arrow {
        image: url(images/chevron-circle-down-solid.svg);
        width: 15px;
        height: 15px;
    }
    
    QComboBox:on {
        border-bottom-right-radius: 0px;
        border-bottom-left-radius: 0px;
    }
    
    QComboBox::down-arrow:on {
        image: url(images/minus-circle-solid.svg);
        width: 15px;
        height: 15px;
    }
    
    QComboBox QAbstractListView {
        background-color: transparent;
    }
"""

# Style for Add button
BUTTON_ADD = """
    QPushButton {
        border: 2px solid white;
        border-radius: 5px;
        background-color: rgb(255, 92, 92);
        color: white;
        font-size: 25px;
        font-family: Helvetica;
        font-weight: bold;
    }
    
    QPushButton::pressed {
        border-color: rgb(255, 92, 92);
        background-color: white;
        color: rgb(255, 92, 92);
    }
"""

# Style for run button
BUTTON_RUN = """
    QPushButton {
        border: 2px solid white;
        border-radius: 5px;
        background-color: rgb(82, 199, 93);
        color: white;
        font-size: 25px;
        font-family: Helvetica;
        font-weight: bold;
    }

    QPushButton::pressed {
        border-color: rgb(82, 199, 93);
        background-color: white;
        color: rgb(82, 199, 93);
    }
"""

# Style for Ok button (Dialog)
BUTTON_OK = """
    QPushButton {
        border: 2px solid white;
        border-radius: 5px;
        background-color: rgb(92, 111, 255);
        color: white;
        font-size: 14px;
        font-family: Helvetica;
        font-weight: bold;
    }

    QPushButton::pressed {
        border-color: rgb(92, 111, 255);
        background-color: white;
        color: rgb(92, 111, 255);
    }
"""

# Style for Cancel button (Dialog)
BUTTON_CANCEL = """
    QPushButton {
        border: 2px solid white;
        border-radius: 5px;
        background-color: rgb(255, 179, 92);
        color: white;
        font-size: 14px;
        font-family: Helvetica;
        font-weight: bold;
    }

    QPushButton::pressed {
        border-color: rgb(255, 179, 92);
        background-color: white;
        color: rgb(255, 179, 92);
    }
"""

# Style for the Deselect button
BUTTON_DESELECT = """
    QPushButton {
        border: 2px solid white;
        border-radius: 25px;
        background-color: rgb(92, 111, 255);
        color: white;
        font-size: 20px;
        font-family: Helvetica;
        font-weight: bold;
    }

    QPushButton::pressed {
        border-color: rgb(255, 179, 92);
        background-color: white;
        color: rgb(255, 179, 92);
    }
"""

# Style for Clear button
BUTTON_CLEAR = """
    QPushButton {
        border: 2px solid white;
        border-radius: 25px;
        background-color: rgb(255, 179, 92);
        color: white;
        font-size: 20px;
        font-family: Helvetica;
        font-weight: bold;
    }

    QPushButton::pressed {
        border-color: rgb(255, 179, 92);
        background-color: white;
        color: rgb(255, 179, 92);
    }
"""

# Style for the Table
TABLE = """
    QTableView {
        border: 0;
    }
    
    QTableView::item {
        height: 32px;
        border-radius: 5px;
        border: 1px solid white;
    }
    
    QTableView::item:selected{
        background-color: lightgray;
    }
"""

# Style for the ScrollView in the Wrapper Window
SCROLL = """
    QScrollArea {
        border: 0;
    }

    QScrollBar:horizontal {
      border: 0;
      height: 8px;
      margin: 0 0 0 0;
    }
    
    QScrollBar::handle:horizontal {
      background-color: lightgray;
      border: 0px solid black;
      border-radius: 4px;
      min-width: 2px;
    }
    
    QScrollBar::add-line:horizontal {
        border: 0;
        width: 0;
    }
    
    QScrollBar::sub-line:horizontal {
        border: 0;
        width: 0;
    }
    
    QScrollBar:vertical {
      border: 0;
      width: 8px;
      margin: 0 0 0 0;
    }
    
    QScrollBar::handle:vertical {
      background-color: lightgray;
      border: 0px solid black;
      border-radius: 4px;
      min-height: 2px;
    }
    
     QScrollBar::add-line:vertical {
        border: 0;
        height: 0;
    }
    
    QScrollBar::sub-line:vertical {
        border: 0;
        height: 0;
    }
"""
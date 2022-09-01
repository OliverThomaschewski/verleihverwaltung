from datetime import date, timedelta

import math
from pickle import NONE
import random
import sqlite3


from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import pandas as pd
import numpy as np


class Expenses(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.expensesLayout = QVBoxLayout(self)
        self.expensesItemsLayout = QHBoxLayout()

        self.expCal = QCalendarWidget()
        self.expCal.setFixedSize(200, 200)
        self.newTypeButton = QPushButton("Neuer Typ")
        self.newTypeButton.setFixedWidth(200)
        self.newTypeButton.clicked.connect(self.addType)
        self.typeComboBox = QComboBox()
        self.typeComboBox.setFixedWidth(200)
        self.typeComboBox.setPlaceholderText("Typ wählen")
        self.typeComboBox.activated.connect(self.setCursor)

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        query = f"""SELECT bezeichnung FROM ausgabentyp"""
        data = conn.execute(query).fetchall()
        conn.close()

        self.typeComboBox.addItems([i[0] for i in data])

        self.priceLineEdit = QLineEdit()
        self.priceLineEdit.setFixedWidth(200)
        self.priceLineEdit.returnPressed.connect(self.saveExp)
        self.saveButton = QPushButton("Speichern")
        self.saveButton.clicked.connect(self.saveExp)
        self.saveButton.setFixedWidth(200)

        self.linesLayout = QVBoxLayout()

        self.linesLayout.addWidget(self.newTypeButton)
        self.linesLayout.addWidget(self.typeComboBox)
        self.linesLayout.addWidget(self.priceLineEdit)
        self.linesLayout.addWidget(self.saveButton)

        self.expensesItemsLayout.addWidget(self.expCal)
        self.expensesItemsLayout.addLayout(self.linesLayout)

        self.expensesLayout.addLayout(self.expensesItemsLayout)

    def addType(self):
        item, ok = QInputDialog.getText(self, "Neuer Typ", "Typ: ")
        print(item)
        if ok:
            conn = sqlite3.connect("db\\verleihverwaltung.db")
            query = f"""INSERT INTO ausgabentyp VALUES ('{item}')"""
            conn.execute(query)
            conn.commit()
            conn.close()
            self.typeComboBox.addItem(item)

    def saveExp(self):
        datum = self.expCal.selectedDate().toString("yyyy-MM-dd")
        ausgabentyp = self.typeComboBox.currentText()
        betrag = self.convertToFloat(self.priceLineEdit.text())

        print(datum)

        print(betrag)

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        query = f"""INSERT INTO ausgaben (ausgabentyp, datum, betrag) VALUES ('{ausgabentyp}', '{datum}', {betrag})"""
        conn.execute(query)
        conn.commit()
        conn.close()

        self.priceLineEdit.setText("")

    def setCursor(self):
        self.priceLineEdit.setFocus()

    def convertToFloat(self, betrag):

        try:
            betrag = float(betrag)
        except:
            betrag = betrag.replace(",", ".")

        finally:
            return betrag
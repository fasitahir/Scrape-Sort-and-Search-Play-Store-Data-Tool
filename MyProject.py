import sys
import time
import typing
from PyQt5.uic import loadUi
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import csv
import pandas as pds
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableView
from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt
sys.path.append('D:\\FasiTahir\\DSA\\Mid Project\\Sorting')
from Sorting import DataSorter
from Searching import DataSearcher
from Searching import multiColumnSearch
import Scraping

class ScrapingThread(QThread):
    def __init__(self):
        super(ScrapingThread, self).__init__()

    def run(self):
        Scraping.start_scraping()

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow,self).__init__()

        loadUi("D:\\FasiTahir\\DSA\\Mid Project\\GUI\\GUI.ui",self)
        
        self.ExitButton.clicked.connect(self.closeApp)
        self.multiLevelSearch.clicked.connect(self.showMultiColSearchUI)
        self.MultiLevelSorting.clicked.connect(self.showMultiLevelSortUI)
        self.SearchWinBtn.clicked.connect(self.showSearchUI)
        self.Refresh.clicked.connect(self.RefreshTable)
        self.load_table()

        self.startScrapping.clicked.connect(self.start_scraping)
        self.pauseButton.clicked.connect(self.pause_scraping)
        self.resumeButton.clicked.connect(self.resume_scraping)
        self.stopButton.clicked.connect(self.stop_scraping)
        self.scraping_thread = ScrapingThread()

        self.SortBtn.clicked.connect(self.SortColumn)


        self.multiColWindow = None  # Initialize the instance variable
        self.multiLevelSortWindow = None
        self.searchWindow = None
    # This is a helping Function to load the content of the table after every event.
    
    def load_table(self):
        with open('ScrapedData.csv', "r",encoding="utf-8") as fileInput:
            roww = 0
            data = list(csv.reader(fileInput))
            model = TableModel(data)
            self.tableView.setModel(model)
        
    def closeApp(self):
        self.close()
    
    def showMultiColSearchUI(self):
        if not self.multiColWindow:  # Only create the window if it doesn't exist
            self.multiColWindow = MultiColumnSearchUi()  # Create a new instance of the MultiColumnUi window
        self.multiColWindow.show()  # Show the new window
    
    def showMultiLevelSortUI(self):
        if not self.multiLevelSortWindow:  # Only create the window if it doesn't exist
            self.multiLevelSortWindow = MultiLevelSortUi()  # Create a new instance of the multiLevelSortWindow
        self.multiLevelSortWindow.show()  # Show the new window
    
    def showSearchUI(self):
        if not self.searchWindow:  # Only create the window if it doesn't exist
            self.searchWindow = SearchUi()  # Create a new instance of the multiLevelSortWindow
        self.searchWindow.show()  # Show the new window

    def RefreshTable(self):
        self.load_table()

    '.................................Sort Single Column.........................'
    def SortColumn(self):

        runTime = 0

        columnName = self.SelectColumn.currentText()
        iscolumnName = False
        
        orderOfSort = self.SelectOrder.currentText()
        isorderOfSort = False

        algoName = self.SelectAlgorithm.currentText()
        isAlgorithmName = False

        if columnName != "Select Column":
            iscolumnName = True
        

        if  orderOfSort != "Order":
            if orderOfSort == "Ascending":
                orderOfSort = "ascending"
            elif orderOfSort == "Decending":
                orderOfSort = "descending"
            isorderOfSort = True


        if  algoName != "Select Algorithm":
            isAlgorithmName = True
        

        if iscolumnName and isorderOfSort and isAlgorithmName:
            if ((columnName != "Reviews" and columnName != "Downloads") and 
                (algoName == "CountingSort" or algoName == "RadixSort" or algoName == "PigeonHoleSort")):
                QMessageBox.information(self, "Error", "This algorithm only works for integers")
            else:
                try:

                    runTime = DataSorter.dataSorter(algoName, columnName, orderOfSort)
                    self.load_table()
                except Exception as e:
                    QMessageBox.information(self,"Exception Error",f"An error occurred: {str(e)}")

        else:
            QMessageBox.information(self, "Error", "Fill All the information")

        self.RunTime.setText(str(runTime) + ' milli seconds')
    
    def start_scraping(self):
        if not self.scraping_thread.isRunning():
            try:
                self.scraping_thread.start()
            except Exception as e:
                QMessageBox.information(self, "Scraping Error", f"An error occurred while starting scraping: {str(e)}")


    def pause_scraping(self):
        Scraping.pause_scraping()

    def resume_scraping(self):
        Scraping.resume_scraping()

    def stop_scraping(self):
        try:
            Scraping.stop_scraping()
        except Exception as e:
            print(str(e))
'.................................Searching Multi Column....................................'    
class MultiColumnSearchUi(QWidget):
    def __init__(self):
        super(MultiColumnSearchUi, self).__init__()
        loadUi("D:\\FasiTahir\\DSA\\Mid Project\\GUI\\Multi-Column-Search Window.ui", self)
        self.ExitButton.clicked.connect(self.closeWindow)
        self.SearchButton.clicked.connect(self.MultiColumnSearch)
        self.SearchButton.clicked.connect(self.showSearchResult)
        # Initialize the checked columns list
        self.checked_order = []

        # Connect the checkbox state change to the update_checked_order method
        self.Name.stateChanged.connect(self.update_checked_order)
        self.Price.stateChanged.connect(self.update_checked_order)
        self.Category.stateChanged.connect(self.update_checked_order)
        self.Downloads.stateChanged.connect(self.update_checked_order)
        self.Company.stateChanged.connect(self.update_checked_order)
        self.Rating.stateChanged.connect(self.update_checked_order)
        self.UpdatedDate.stateChanged.connect(self.update_checked_order)
        self.Reviews.stateChanged.connect(self.update_checked_order)

        # Creating a dictionary to map Check Box Names with column names
        self.columnNameMapping = {
            "Name": "Name",
            "Price": "Price",
            "Category": "Category",
            "Downloads": "Downloads",
            "Company": "Company",
            "Rating": "Rating",
            "UpdatedDate": "Updated Date",
            "Reviews": "Reviews",
        }
    
    def showSearchResult(self):
        try:
            if not hasattr(self, 'searchResultWindow'):  # Only create the window if it doesn't exist
                self.searchResultWindow = SearchResultUi()  # Create a new instance of the SearchResultUi window
            self.searchResultWindow.show()  # Show the new window
        except Exception as e:
            QMessageBox.information(self, "Error", str(e))

    def update_checked_order(self, state):
        checkbox = self.sender()  # Get signal from Checkbox
        if state == Qt.Checked:
            self.checked_order.append(checkbox.text())
        elif state == Qt.Unchecked:
            if checkbox.text() in self.checked_order:
                self.checked_order.remove(checkbox.text())

    def MultiColumnSearch(self):
        listOfColumns = []
        flag = False

        if not self.checked_order:
            QMessageBox.information(self, "Error", "Please check at least one of the check boxes")
            return
        else:
            flag = True
            for column in self.checked_order:
                mapped_column = self.columnNameMapping.get(column, column)
                listOfColumns.append(mapped_column)

        filter = self.SelectFilter.currentText()
        isFilter = False

        if filter != "Select Filter":
            isFilter = True

        searchText = self.SearchBar.toPlainText()
        searchTerms = []
        isSearchText = False

        try:
            if searchText:
                if ',' in searchText:
                    searchTerms = searchText.split(',')
                    isSearchText = True
                else:
                    QMessageBox.information(self, "Error", "Please Enter the search text in the format separated by commas")
                    return
            else:
                QMessageBox.information(self, "Error", "Please Enter the search text")
                return
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        if flag and isFilter and isSearchText:
            try:
                multiColumnSearch.MultiColumnSearch(searchTerms, listOfColumns, filter)
                QMessageBox.information(self, "Message", "Data Has been Searched")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        else:
            QMessageBox.information(self, "Error", "Please fill all the information correctly")

    def closeWindow(self):
        self.close()  # Close the MultiColumnSearchUi window

'.................................Sorting Multi Level Column....................................'

class MultiLevelSortUi(QWidget):
    def __init__(self):
        super(MultiLevelSortUi, self).__init__()
        loadUi("D:\\FasiTahir\\DSA\\Mid Project\\GUI\\Multi-Level-Sort Window.ui", self)

        # Create a list to store the order of checked items
        self.checked_order = []

        # Creating a dictionary to map Check Box Names with column names
        self.columnNameMapping = {
            "Name": "Name",
            "Price": "Price",
            "Category": "Category",
            "Downloads": "Downloads",
            "Company": "Company",
            "Ratings": "Rating",
            "UpdatedDate": "Updated Date",  
            "Reviews": "Reviews",
        }

        # Connect the checkbox state change to the update_checked_order method
        self.Name.stateChanged.connect(self.update_checked_order)
        self.Price.stateChanged.connect(self.update_checked_order)
        self.Category.stateChanged.connect(self.update_checked_order)
        self.Downloads.stateChanged.connect(self.update_checked_order)
        self.Company.stateChanged.connect(self.update_checked_order)
        self.Ratings.stateChanged.connect(self.update_checked_order)
        self.UpdatedDate.stateChanged.connect(self.update_checked_order)
        self.Reviews.stateChanged.connect(self.update_checked_order)

        self.ExitButton.clicked.connect(self.closeWindow)
        self.SortButton.clicked.connect(self.MultiLevelSort)

    def update_checked_order(self, state):
        checkbox = self.sender()  # Get the checkbox that emitted the signal
        if state == Qt.Checked:
            self.checked_order.append(checkbox.text())
        elif state == Qt.Unchecked:
            if checkbox.text() in self.checked_order:
                self.checked_order.remove(checkbox.text())



    def MultiLevelSort(self):
        if not self.checked_order:
            QMessageBox.information(self, "Error", "Please check at least one of the check boxes")
            return

        try:
            listOfColumns = []
            for column in self.checked_order:
                mapped_column = self.columnNameMapping.get(column, column)
                listOfColumns.append(mapped_column)

            DataSorter.MultiColumnSort(listOfColumns)

            QMessageBox.information(self, "Message", "Data Has been Sorted")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def closeWindow(self):
        self.close()  

'.................................Searching Single Column....................................'

class SearchUi(QWidget):
    def __init__(self):
        super(SearchUi, self).__init__()
        loadUi("D:\\FasiTahir\\DSA\\Mid Project\\GUI\\SearchUI.ui", self)  # Load the UI for SearchUi     
        self.ExitButton.clicked.connect(self.closeWindow)
        self.SearchButton.clicked.connect(self.SearchColumn)
        try:
            self.SearchButton.clicked.connect(self.showSearchResult)
        except Exception as e:
            print(str(e))
    
    def showSearchResult(self):
        try:

            if not hasattr(self, 'searchResultWindow'):  # Only create the window if it doesn't exist
                self.searchResultWindow = SearchResultUi()  # Create a new instance of the SearchResultUi window
            self.searchResultWindow.show()  # Show the new window
        except Exception as e:
            QMessageBox.information(self, "Error", str(e))
        
    def SearchColumn(self):
        columnName = self.SelectColumn.currentText()
        isColumnName = False

        filter = self.SelectFilter.currentText()
        isFilter = False

        searchText = self.SearchBar.toPlainText()
        isSearchText = False

        if columnName != "Select Column":
            isColumnName =True

        if filter != "Select Filter":
            isFilter =True
            if filter == "Contain":
                filter = "contains"
            
            elif filter == "Start With":
                filter = "starts_with"

            elif filter == "End With":
                filter = "ends_with"
        
        if searchText != None and searchText != "":
            isSearchText = True
        
        if isColumnName and isFilter and isSearchText:
            try:
                DataSearcher.linear_search(columnName, searchText, filter)
                QMessageBox.information(self, "Result", "Your data has been searched")
            except Exception as e:
                print(str(e))
        else:
            QMessageBox.information(self, "Error", "Please select the correct data")

    def closeWindow(self):
        self.close()             

import csv

class SearchResultUi(QWidget):
    def __init__(self):
        super(SearchResultUi, self).__init__()
        loadUi("D:\\FasiTahir\\DSA\\Mid Project\\GUI\\Searched_Data.ui", self)
        self.ExitButton.clicked.connect(self.closeWindow)
        self.load_table()

    def load_table(self):
        with open('SearchedResult.csv', "r", encoding="utf-8") as fileInput:
            data = list(csv.reader(fileInput))
            model = TableModel(data)
            self.tableView.setModel(model)

    def closeWindow(self):
        self.close()


class TableModel(QAbstractTableModel):
    def __init__(self,data):
        super().__init__()
        self._data = data

    def set(self, data):
        self._data = data

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        elif role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            return self._data[row][col]
        else:
            return QVariant()

    def headerData(self, p_int, Qt_Orientation, role=None):
        return self._data[0]


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())        
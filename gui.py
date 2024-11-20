from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QComboBox, QWidget, QTableWidget, QTableWidgetItem,
    QDialog, QDialogButtonBox, QFileDialog, QAction
)
from PyQt5.QtCore import Qt
from finance_management import Finance_Manager, Amount
from process_management import Process_Manager
from excel import export_results_to_excel, export_transactions, load_transactions
from typing import NoReturn

class GUI(QMainWindow):
    def __init__(self, finance_manager: Finance_Manager, process_manager: Process_Manager):
        super().__init__()
        self.finance_manager = finance_manager
        self.process_manager = process_manager
        self.setWindowTitle('Personal Finance Manager')
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget(self)
        self.central_widget.setStyleSheet('''
            QPushButton {
                background-color: #5293fa;
                color: white;
                font-size: 16px;
                border-radius: 8px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #7287e0;
            }
            QMainWindow>QWidget {
                background-color: #c4e6ff;
            }
            ''')
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.render_UI()

    def render_UI(self) -> NoReturn:
        '''Initialize UI components.'''
        self.render_Menu_bar()
        self.render_Transaction_Table()
        self.render_transaction_Form()

    
    def render_Menu_bar(self) -> NoReturn:
        self.menu_bar = self.menuBar()

        self.file_menu = self.menu_bar.addMenu('File')

        load_transactions_button = QAction('Open/Load transactions from Excel file', self)
        load_transactions_button.triggered.connect(self.load_transactions)

        export_transactions_button = QAction('Save/Export transactions to Excel file', self)
        export_transactions_button.triggered.connect(self.export_transactions)

        self.file_menu.addActions([
            load_transactions_button,
            export_transactions_button
        ])

        self.plot_menu = self.menu_bar.addMenu('Plot Finances')

        plot_broad_button = QAction('Plot Broad Finances [Pie Chart]', self)
        plot_broad_button.triggered.connect(self.plot_broad_finances)

        plot_income_button = QAction('Plot Income [Pie Chart]', self)
        plot_income_button.triggered.connect(self.plot_income)

        plot_expenses_button = QAction('Plot Expenses [Pie Chart]', self)
        plot_expenses_button.triggered.connect(self.plot_expenses)

        plot_assets_button = QAction('Plot Assets(Savings+Investments) [Pie Chart]', self)
        plot_assets_button.triggered.connect(self.plot_assets)

        self.plot_menu.addActions([
            plot_broad_button,
            plot_income_button,
            plot_expenses_button,
            plot_assets_button
        ])


        self.report_menu = self.menu_bar.addMenu('Financial Report')

        get_report_button = QAction('View Report', self)
        get_report_button.triggered.connect(self.get_report)
        
        export_report_button = QAction('Export Report to Excel file', self)
        export_report_button.triggered.connect(self.export_report_to_excel)
        
        self.report_menu.addActions([
            get_report_button,
            export_report_button
        ])


        self.help_menu = self.menu_bar.addMenu('Help')

        edit_button = QAction('How to edit a transaction', self)
        edit_button.triggered.connect(self.help_with_edits)

        self.help_menu.addActions([
            edit_button
        ])

        self.menu_bar.setStyleSheet('''
            QMenuBar {
                background-color: #7287e0;        
                color: black;
                font-size: 16px;
                padding: 5px 10px;
            }
            QMenu {
                background-color: #c4e6ff;
                color: black;
                font-size: 16px;
                border-radius: 8px;
                border-width: 5px;
                border-color: black;
                padding: 5px 10px;
            }
        ''')
    
    def render_Transaction_Table(self) -> NoReturn:
        self.transactions_title = QLabel('<h2>Transactions</h2>')
        self.layout.addWidget(self.transactions_title)

        self.transaction_table = QTableWidget(0, 5)
        self.transaction_table.setHorizontalHeaderLabels(['Amount', 'Name', 'Type', 'Edit', 'Delete'])
        self.transaction_table.setStyleSheet('QPushButton { color: black; background-color: white; }')
        self.layout.addWidget(self.transaction_table)

    def render_transaction_Form(self) -> NoReturn:
        form_layout = QHBoxLayout()

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText('Amount')
        form_layout.addWidget(self.amount_input)

        self.type_input = QComboBox()
        self.type_input.addItems(['Income', 'Expense', 'Investment'])
        form_layout.addWidget(self.type_input)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Name')
        form_layout.addWidget(self.name_input)

        self.add_button = QPushButton('Add Transaction')
        self.add_button.clicked.connect(self.add_transaction)
        form_layout.addWidget(self.add_button)

        self.transaction_form = QWidget()
        self.transaction_form.setLayout(form_layout)
        self.transaction_form.setStyleSheet('''
            QPushButton, QComboBox, QLineEdit {
                color: black;
                font-size: 16px;
                border-radius: 8px;
                padding: 10px 20px;
            }
                                            
            QComboBox {
                background-color: white;
            }

            QPushButton {
                background-color: #5293fa;
                color: white;
            }

            QPushButton:hover {
                background-color: #7287e0;
            }
        ''')
        self.layout.addWidget(self.transaction_form)

    def add_transaction(self, amount: Amount|None = None, name: str|None = None, transaction_type: str|None = None) -> NoReturn:
        if amount == None or name == None or transaction_type == None:
            if not self.verify_form_is_filled(): return
            amount           = Amount(self.amount_input.text().replace(',', ''))
            name             = self.name_input.text()
            transaction_type = self.type_input.currentText()
        
        self.finance_manager.add_transaction(name, transaction_type, amount)
        row = self.transaction_table.rowCount()
        self.transaction_table.insertRow(row)
        self.transaction_table.setItem(row, 0, QTableWidgetItem(str(amount)))
        self.transaction_table.setItem(row, 1, QTableWidgetItem(name))
        self.transaction_table.setItem(row, 2, QTableWidgetItem(transaction_type))
        edit_button = QPushButton('Edit')
        edit_button.clicked.connect(lambda: self.edit_transaction(row))
        self.transaction_table.setCellWidget(row, 3, edit_button)
        delete_button = QPushButton('Delete')
        delete_button.clicked.connect(lambda: self.delete_transaction(row))
        self.transaction_table.setCellWidget(row, 4, delete_button)

    def edit_transaction(self, row: int) -> NoReturn:
        if not self.verify_form_is_filled():
            self.help_with_edits()
            return
        amount           = Amount(self.amount_input.text().replace(',', ''))
        name             = self.name_input.text()
        transaction_type = self.type_input.currentText()
        amount           = Amount(self.amount_input.text().replace(',', ''))
        name             = self.name_input.text()
        transaction_type = self.type_input.currentText()
        self.finance_manager.add_transaction(name, transaction_type, amount)
        self.transaction_table.setItem(row, 0, QTableWidgetItem(str(amount)))
        self.transaction_table.setItem(row, 1, QTableWidgetItem(name))
        self.transaction_table.setItem(row, 2, QTableWidgetItem(transaction_type))
        edit_button = QPushButton('Edit')
        edit_button.clicked.connect(lambda: self.edit_transaction(row))
        self.transaction_table.setCellWidget(row, 3, edit_button)
        delete_button = QPushButton('Delete')
        delete_button.clicked.connect(lambda: self.delete_transaction(row))
        self.transaction_table.setCellWidget(row, 4, delete_button)
        
    def delete_transaction(self, row: int) -> NoReturn:
        self.transaction_table.removeRow(row)
        for i in range(row, self.transaction_table.rowCount()):
            edit_button = QPushButton('Edit')
            edit_button.clicked.connect(lambda: self.edit_transaction(i))
            self.transaction_table.setCellWidget(i, 3, edit_button)
            delete_button = QPushButton('Delete')
            delete_button.clicked.connect(lambda: self.delete_transaction(i))
            self.transaction_table.setCellWidget(i, 4, delete_button)
    
    def help_with_edits(self) -> NoReturn:
        Help_Window('Making Edits', '1. Make to fill the details of the edit in the transaction form below.\n2. Click on edit button next to the transaction you want to edit.')

    def verify_form_is_filled(self) -> bool:
        is_blank =  (self.amount_input.text().replace(',', '') == '') or (self.name_input.text() == '')
        return not is_blank

    def plot_broad_finances(self) -> NoReturn:
        self.finance_manager.process_transactions()
        target = self.finance_manager.plot_broad_finances()
        self.process_manager.new_process(target)
    
    def plot_income(self) -> NoReturn:
        self.finance_manager.process_transactions()
        target = self.finance_manager.plot_income()
        self.process_manager.new_process(target)

    def plot_expenses(self) -> NoReturn:
        self.finance_manager.process_transactions()
        target = self.finance_manager.plot_expenses()
        self.process_manager.new_process(target)
    
    def plot_assets(self) -> NoReturn:
        self.finance_manager.process_transactions()
        target = self.finance_manager.plot_assets()
        self.process_manager.new_process(target)

    def get_report(self) -> NoReturn:
        self.finance_manager.process_transactions()
        self.report_window = Report_Window(self.finance_manager.report)
        self.report_window.show()

    def export_report_to_excel(self) -> NoReturn:
        self.finance_manager.process_transactions()
        export_results_to_excel(self.load_file())
    
    def export_transactions(self) -> NoReturn:
        export_transactions(self.load_file(), self.finance_manager.transactions)
    
    def load_transactions(self) -> NoReturn:
        transactions = load_transactions(self.load_file())
        for transaction in transactions:
            self.add_transaction(name=transaction[0], transaction_type=transaction[1], amount=transaction[2])
        
    def load_file(self) -> str:
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            'Open Excel File',
            '',
            'Excel Files (*.xlsx *.xls)' 
        )
        return file_path
        

class Report_Window(QWidget):
    def __init__(self, report: dict[str, dict[str, Amount]]):
        super().__init__()
        self.report = report
        self.setWindowTitle('Financial Report')
        self.setGeometry(100, 100, 1200, 800)

        self.layout = QHBoxLayout()

        self.render_UI()

        self.setLayout(self.layout)
    
    def render_UI(self) -> NoReturn:
        income_layout = QVBoxLayout()
        self.income_title = QLabel('<h2>Income</h2>')
        income_layout.addWidget(self.income_title)
        self.income_table = QTableWidget(len(list(self.report['Income'].keys())), 2)
        self.income_table.setHorizontalHeaderLabels(['Name', 'Amount'])
        income_layout.addWidget(self.income_table)
        self.layout.addLayout(income_layout)

        for row, name in enumerate(self.report['Income'].keys()):
            self.income_table.setItem(row, 0, QTableWidgetItem(name))
            self.income_table.setItem(row, 1, QTableWidgetItem(str(self.report['Income'][name])))

        expense_layout = QVBoxLayout()
        self.expense_title = QLabel('<h2>Expenses</h2>')
        expense_layout.addWidget(self.expense_title)
        self.expense_table = QTableWidget(len(list(self.report['Expense'].keys())), 2)
        self.expense_table.setHorizontalHeaderLabels(['Name', 'Amount'])
        expense_layout.addWidget(self.expense_table)
        self.layout.addLayout(expense_layout)

        for row, name in enumerate(self.report['Expense'].keys()):
            self.expense_table.setItem(row, 0, QTableWidgetItem(name))
            self.expense_table.setItem(row, 1, QTableWidgetItem(str(self.report['Expense'][name])))

        assets_layout = QVBoxLayout()
        self.assets_title = QLabel('<h2>Assets(Savings + Investment)</h2>')
        assets_layout.addWidget(self.assets_title)
        self.assets_table = QTableWidget(len(list(self.report['Investment'].keys())), 2)
        self.assets_table.setHorizontalHeaderLabels(['Name', 'Amount'])
        assets_layout.addWidget(self.assets_table)
        self.layout.addLayout(assets_layout)

        for row, name in enumerate(self.report['Investment'].keys()):
            self.assets_table.setItem(row, 0, QTableWidgetItem(name))
            self.assets_table.setItem(row, 1, QTableWidgetItem(str(self.report['Investment'][name])))

class Help_Window(QDialog):
    def __init__(self, title: str, help_message: str):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(500, 100, 400, 400)

        self.setStyleSheet('''
            QDialog{
                background-color: #c4e6ff;
            }
            QLabel {
                font-size: 20px;
            }
            QPushButton {
                background-color: #5293fa;
                color: white;
                font-size: 20px;
                border-radius: 8px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #7287e0;
            }
        ''')

        self.layout: QVBoxLayout = QVBoxLayout()

        self.message = QLabel(help_message.replace('\n', '<br>'))
        self.layout.addWidget(self.message)

        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.close)
        self.layout.addWidget(self.ok_button)

        self.setLayout(self.layout)
        self.exec_()
    

def run_GUI(argv: list[str], finance_manager: Finance_Manager, process_manager: Process_Manager) -> NoReturn:
    app = QApplication(argv)
    window = GUI(finance_manager, process_manager)
    window.show()
    return app.exec_()
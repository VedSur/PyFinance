from typing import NoReturn
import matplotlib.pyplot as plt
from process_management import Process_Manager

currency_symbols: dict[str, str] = {
    'INR': '₹',
    'USD': '$'
}
currency_symbol = currency_symbols['INR']

class Amount(float): pass

class Finance_Manager:
    X:      int = 100
    Y:      int = 100
    HEIGHT: int = 400 
    WIDTH:  int = 500

    def __init__(self):
        self.income:   dict[str, Amount] = {}
        self.expenses: dict[str, Amount] = {}
        self.investment:   dict[str, Amount] = {}
        self.report: dict[str, dict[str, Amount]] = {
            'Income': self.income,
            'Expense': self.expenses,
            'Investment': self.investment
        }
        self.transactions: list[tuple[str, str, Amount]] = []

    def add_transaction(self, name: str, transaction_type: str, amount: Amount) -> NoReturn:
        self.transactions.append((name, transaction_type, amount))

    def edit_transaction(self, index: int, name: str, transaction_type: str, amount: Amount) -> NoReturn:
        self.transactions[index] = (name, transaction_type, amount)

    def process_transactions(self) -> NoReturn:
        self.reset()
        for transaction in self.transactions:
            self.process_transaction(transaction[0], transaction[1], transaction[2])
        self.investment['Savings'] = self.net_income() - self.net_expenses() + self.net_asset_value()

    def process_transaction(self, name: str, transaction_type: str, amount: Amount) -> NoReturn:
        self.verify_transaction_type(transaction_type)
        self.report[transaction_type][name] = amount
        return self
            
    def get_report(self) -> dict[str, dict[str, Amount]]:
        return self.report

    def verify_transaction_type(self, transaction_type: str) -> NoReturn:
        if transaction_type not in ['Income', 'Expense', 'Investment']:
            raise ValueError(f'Invalid Transaction Type: {transaction_type}')
        
    def net_income(self) -> Amount:
        return sum(amount for amount in self.income.values())
    
    def net_expenses(self) -> Amount:
        return sum(amount for amount in self.expenses.values())
    
    def net_asset_value(self) -> Amount:
        return sum(amount for amount in self.investment.values())
    
    def plot_broad_finances(self) -> NoReturn:
        X, Y, HEIGHT, WIDTH = Finance_Manager.X, Finance_Manager.Y, Finance_Manager.HEIGHT, Finance_Manager.WIDTH
        net_income      = self.net_income()
        net_expenses    = self.net_expenses()
        net_asset_value = self.net_asset_value()
        sizes  = [net_expenses/net_income*100, net_asset_value/net_income*100]
        labels = [f'Expenses({currency_symbol}{net_expenses})', f'Savings and Investments({currency_symbol}{net_asset_value})']
        colors = ['red', 'blue']
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.title('Broad Finance Chart')
        plt.get_current_fig_manager().window.setGeometry(X, Y, WIDTH, HEIGHT)
        plt.show()

    def plot_expenses(self) -> NoReturn:
        X, Y, HEIGHT, WIDTH = Finance_Manager.X, Finance_Manager.Y, Finance_Manager.HEIGHT, Finance_Manager.WIDTH
        net_expenses    = self.net_expenses()
        sizes  = [expense/net_expenses*100 for expense in self.expenses.values()]
        labels = [f'{label}({currency_symbol}{self.expenses[label]})' for label in self.expenses.keys()]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.title('Expenses Chart')
        plt.get_current_fig_manager().window.setGeometry(X, Y, WIDTH, HEIGHT)
        plt.show()
    
    def plot_income(self) -> NoReturn:
        X, Y, HEIGHT, WIDTH = Finance_Manager.X, Finance_Manager.Y, Finance_Manager.HEIGHT, Finance_Manager.WIDTH
        net_income    = self.net_income()
        sizes  = [income/net_income*100 for income in self.income.values()]
        labels = [f'{label}({currency_symbol}{self.income[label]})' for label in self.income.keys()]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.title('Income Chart')
        plt.get_current_fig_manager().window.setGeometry(X, Y, WIDTH, HEIGHT)
        plt.show()

    def plot_assets(self) -> NoReturn:
        X, Y, HEIGHT, WIDTH = Finance_Manager.X, Finance_Manager.Y, Finance_Manager.HEIGHT, Finance_Manager.WIDTH
        net_asset_value    = self.net_asset_value()
        sizes  = [investment/net_asset_value*100 for investment in self.investment.values()]
        labels = [f'{label}({currency_symbol}{self.investment[label]})' for label in self.investment.keys()]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.title('Assets Chart')
        plt.get_current_fig_manager().window.setGeometry(X, Y, WIDTH, HEIGHT)
        plt.show()

    def reset(self) -> NoReturn:
        self.income = {}
        self.expenses = {}
        self.investment = {}
        self.report = {
            'Income': self.income,
            'Expense': self.expenses,
            'Investment': self.investment
        }
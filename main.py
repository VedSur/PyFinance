import sys
from finance_management import Finance_Manager
from process_management import Process_Manager
from gui import run_GUI
from typing import NoReturn

def main() -> NoReturn:
    finance_manager = Finance_Manager()
    process_manager = Process_Manager()
    run_GUI(sys.argv, finance_manager, process_manager)

if __name__ == '__main__':
    main()
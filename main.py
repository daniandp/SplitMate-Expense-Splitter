import ttkbootstrap as tb
from expenses_db import ExpenseDB
from logic import ExpenseLogic
from gui import ExpenseGUI


# Main file responsibility: Initialize and inject dependencies

if __name__ == "__main__":
    
    #Initialize Database object and Logic object
    db = ExpenseDB()
    logic = ExpenseLogic(db)
    
    # Launch the graphical interface
    app_window = tb.Window(themename="superhero")
    
    # Initialize GUI object and pass the root window, db, and logic
    gui = ExpenseGUI(app_window, db, logic)
    
    # Keep the app running
    app_window.mainloop()
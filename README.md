# SplitMate-Expense-Splitter

Forget the calculators and post-trip headaches! **SplitMate** is a desktop application designed for friend groups, roommates, or families who need an easy way to keep track of shared expenses. 

You just log who paid for what, and SplitMate handles the heavy math. It calculates exactly who owes whom.

## Setup & Requirements

To run this project on your computer, you'll need to have Python installed. It also uses a couple of libraries for the GUI and the PDF reporting feature. 

Open your terminal and install the dependencies by running this command:
`pip install ttkbootstrap reportlab`

To launch the application, simply run:
`python main.py`

## 💡 How to use SplitMate step-by-step

**1. Add the Group Members**
In the left panel, type the names of everyone sharing the expenses and click "Add Member". If you make a mistake, you can just select a name from the list and hit "Delete Member".

**2. Add Expenses**
In the right panel, write down what the money was spent on (e.g., "Dinner in Toronto"), how much it cost, and select who paid the bill from the dropdown menu. Click "Save Expense". You can add as many expenses as you need! If you need to fix an amount or description later, just select the expense from the list and use the "Edit" button.

**3. Work the magic (Debt Settlements)**
Whenever you need to split the expenses, go to the bottom section and click **"Calculate Split"**. **SplitMate** will analyze all the expenses and give you a clear, direct summary of exactly who needs to transfer money to whom so everyone is even.

**4. Export your report**
If you want to send the final math to the group chat as a friendly reminder, click **"Generate PDF Report"**. The app will automatically create a file called `SplitMate_Report.pdf` with the official summary.

Pay on time and save a mate!
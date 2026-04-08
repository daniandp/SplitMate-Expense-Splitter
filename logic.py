from reportlab.pdfgen import canvas

# Logic file responsibility: Handle business logic, calculations and PDF generation with ReportLab

class ExpenseLogic:
    def __init__(self, db):
        # Database object to access data for calculations and report generation
        self.db = db

    def calculate_debts(self):
        # Fetch current data from the database
        members = self.db.get_members()
        expenses = self.db.get_expenses()

        # Ensure we have data to calculate
        if len(members) == 0:
            return ["No members in the group yet."]
        if len(expenses) == 0:
            return ["No expenses recorded yet."]

        # Calculate the total spent across all expenses
        total_spent = 0
        for exp in expenses:
            total_spent = total_spent + exp[2] # The amount is in the 3rd column of the expenses query result

        # Calculate the equal share per person
        per_person = total_spent / len(members)

        # Dictionary to track how much each person actually paid
        paid_amounts = {}
        for m in members:
            paid_amounts[m[1]] = 0.0 # Initialize all members with 0.0

        for exp in expenses:
            payer_name = exp[3] # The payer's name is in the 4th column of the expenses query result
            paid_amounts[payer_name] = paid_amounts[payer_name] + exp[2]

        # Calculate individual balances (What they paid minus what they should pay)
        balances = {}
        for name in paid_amounts:
            balances[name] = paid_amounts[name] - per_person

        # Separate members into Debtors (owe money) and Creditors (receive money)
        debtors = [] 
        creditors = []

        for name in balances:
            if balances[name] < -0.01: # Negative balance means they underpaid
                debtors.append([name, abs(balances[name])])
            elif balances[name] > 0.01: # Positive balance means they overpaid
                creditors.append([name, balances[name]])

        # Match debtors to creditors
        results = []
        for d in debtors:
            debtor_name = d[0]
            amount_owed = d[1]

            for c in creditors:
                creditor_name = c[0]
                amount_to_receive = c[1]

                if amount_owed == 0 or amount_to_receive == 0:
                    continue

                # Determine the payment amount (the smaller of the two values)
                if amount_owed <= amount_to_receive:
                    payment = amount_owed
                else:
                    payment = amount_to_receive

                # Record the transaction
                results.append(f"{debtor_name} owes {creditor_name} ${payment:.2f}")

                # Update remaining balances for the current iteration
                d[1] = d[1] - payment
                c[1] = c[1] - payment
                amount_owed = d[1] 

        if not results:
            return ["Everyone is settled up!"]
        
        results.append("")
        results.append("-" * 60)
        results.append("Pay on time and save a mate!")

        return results

    # Generates a PDF report using ReportLab
    def generate_pdf_report(self, debts_list):
        try:
            c = canvas.Canvas("SplitMate_Report.pdf")
            c.drawString(100, 800, "SplitMate - Settlement Report")
            c.drawString(100, 780, "-" * 60)

            # Print each debt line
            y_position = 750
            for debt in debts_list:
                c.drawString(100, y_position, debt)
                y_position = y_position - 20

            c.save()
            return True
        except Exception as e:
            print("PDF Error:", e)
            return False
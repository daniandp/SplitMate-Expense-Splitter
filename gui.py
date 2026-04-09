import tkinter as tk
import ttkbootstrap as tb
from tkinter import messagebox, simpledialog
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# GUI file responsibility: Manage user interface and events

class ExpenseGUI:
    def __init__(self, root, db, logic):
        self.root = root
        self.db = db
        self.logic = logic

        # Window's app configuration
        self.root.title("SplitMate - Your Friendly Expense Splitter")
        self.root.geometry("1100x1200")

        self.root.iconbitmap(resource_path('logo.ico'))

        self.main_container = tb.Frame(self.root, padding=30)
        self.main_container.pack(fill="both", expand=True)

        self.top_frame = tb.Frame(self.main_container)
        self.top_frame.pack(fill="x", expand=True, anchor="center")

        self.left_frame = tb.Frame(self.top_frame, padding=10)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=30)

        self.right_frame = tb.Frame(self.top_frame, padding=10)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=30)

        self.bottom_frame = tb.Frame(self.main_container, padding=10)
        self.bottom_frame.pack(side="bottom", fill="x")
        
        # Initialize the UI components
        self.setup_members()
        self.setup_expenses()
        self.setup_results()

        # Populate the UI with existing database data on startup
        self.refresh_members()
        self.refresh_expenses()

    def setup_members(self):
        # --- Members Management ---
        tb.Label(self.left_frame, text="1. Group Members", font=("Helvetica", 14, "bold")).pack(pady=10)
        
        self.member_var = tb.StringVar() 
        tb.Entry(self.left_frame, textvariable=self.member_var).pack(fill="x", pady=5, ipady=4)
        
        tb.Button(self.left_frame, text="Add Member", bootstyle="primary", command=self.add_member).pack(pady=5)
        
        self.members_listbox = tk.Listbox(self.left_frame, height=6, bg="#2b3e50", fg="white", selectbackground="#4e5d6c", font=("Helvetica", 10))
        self.members_listbox.pack(fill="x", pady=5)
        
        tb.Button(self.left_frame, text="Delete Member", bootstyle="secondary", command=self.delete_member).pack(pady=5)

    def setup_expenses(self):
        # --- Expense Management ---
        tb.Label(self.right_frame, text="2. Add Expense", font=("Helvetica", 14, "bold")).pack(pady=10)
        
        tb.Label(self.right_frame, text="Description:").pack(anchor="w")
        self.desc_var = tb.StringVar()
        tb.Entry(self.right_frame, textvariable=self.desc_var).pack(fill="x", pady=2, ipady=4)

        tb.Label(self.right_frame, text="Amount ($):").pack(anchor="w")
        self.amount_var = tb.StringVar()
        tb.Entry(self.right_frame, textvariable=self.amount_var).pack(fill="x", pady=2, ipady=4)

        tb.Label(self.right_frame, text="Who Paid?").pack(anchor="w")
        self.payer_var = tb.StringVar()
        self.payer_combo = tb.Combobox(self.right_frame, textvariable=self.payer_var, state="readonly", font=("Helvetica", 11))
        self.payer_combo.pack(fill="x", pady=2, ipady=4)

        tb.Button(self.right_frame, text="Save Expense", bootstyle="info", command=self.add_expense).pack(pady=10)

        self.expenses_listbox = tk.Listbox(self.right_frame, height=6, bg="#2b3e50", fg="white", selectbackground="#4e5d6c", font=("Helvetica", 10))
        self.expenses_listbox.pack(fill="x", pady=5)

        btn_frame = tb.Frame(self.right_frame)
        btn_frame.pack(fill="x")
        tb.Button(btn_frame, text="Edit", bootstyle="primary-outline", command=self.edit_expense).pack(side="left", padx=5)
        tb.Button(btn_frame, text="Delete", bootstyle="secondary", command=self.delete_expense).pack(side="left", padx=5)
    
    def setup_results(self):
        # --- Results and Export ---
        tb.Label(self.bottom_frame, text="3. Debt Settlements", font=("Helvetica", 14, "bold")).pack(pady=10)
        
        self.result_text = tb.Text(self.bottom_frame, height=5, state="disabled", bg="#2b3e50", fg="white", font=("Helvetica", 11), padx=15, pady=15)
        self.result_text.pack(fill="x", pady=5)

        btn_frame = tb.Frame(self.bottom_frame)
        btn_frame.pack(pady=10)
        tb.Button(btn_frame, text="Calculate Split", bootstyle="primary", command=self.show_calculations).pack(side="left", padx=10)
        tb.Button(btn_frame, text="Generate PDF Report", bootstyle="info", command=self.export_pdf).pack(side="left", padx=10)

    # --- Data Binding Methods ---
    def refresh_members(self):
        self.members_listbox.delete(0, 'end')
        members = self.db.get_members()
        self.member_map = {} 
        combo_values = []
        for m in members:
            member_id = m[0]
            member_name = m[1]
            self.member_map[member_name] = member_id 
            self.members_listbox.insert('end', f" {member_name}")
            combo_values.append(member_name) 
            self.payer_combo['values'] = combo_values

    def refresh_expenses(self):
        self.expenses_listbox.delete(0, 'end')
        expenses = self.db.get_expenses()
        
        self.expense_id_list = [] 
        for exp in expenses:
            self.expense_id_list.append(exp[0])
            display_text = f" {exp[1]} | ${exp[2]:.2f} | Paid by: {exp[3]}"
            self.expenses_listbox.insert('end', display_text)

    # --- Controller Actions ---
    def add_member(self):
        name = self.member_var.get().strip()
        # Input validation
        if name == "":
            messagebox.showerror("Error", "Name cannot be empty.")
            return
            
        if self.db.add_member(name):
            self.member_var.set("") # Clear input
            self.refresh_members()
        else:
            messagebox.showerror("Error", "Member name already exists.")

    def delete_member(self):
        selected = self.members_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select a member to delete.")
            return
            
        member_name = self.members_listbox.get(selected[0]).strip()
        member_id = self.member_map[member_name]
        
        self.db.delete_member(member_id)
        self.refresh_members()
        self.refresh_expenses()

    def add_expense(self):
        desc = self.desc_var.get().strip()
        amount_str = self.amount_var.get().strip()
        payer_name = self.payer_var.get()

        if desc == "" or amount_str == "" or payer_name == "":
            messagebox.showerror("Error", "Please fill all fields.")
            return

        try:
            amount = float(amount_str) 
        except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number.")
            return

        payer_id = self.member_map[payer_name]

        self.db.add_expense(desc, amount, payer_id)
        
        # Clear input fields after adding expense
        self.desc_var.set("")
        self.amount_var.set("")
        self.payer_var.set("")
        self.refresh_expenses()

    def delete_expense(self):
        selected = self.expenses_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select an expense to delete.")
            return
        
        index = selected[0]
        expense_id = self.expense_id_list[index]
        
        self.db.delete_expense(expense_id)
        self.refresh_expenses()

    def edit_expense(self):
        selected = self.expenses_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select an expense to edit.")
            return
            
        index = selected[0]
        expense_id = self.expense_id_list[index]
        
        new_desc = simpledialog.askstring("Edit Expense", "Enter new description:")
        if new_desc:
            new_amount = simpledialog.askfloat("Edit Expense", "Enter new amount:")
            if new_amount is not None:
                self.db.update_expense(expense_id, new_desc, new_amount)
                self.refresh_expenses()

    def show_calculations(self):
        debts = self.logic.calculate_debts()
        
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, "end")
        for debt in debts:
            self.result_text.insert("end", debt + "\n")
        self.result_text.config(state="disabled")

    def export_pdf(self):
        debts = self.logic.calculate_debts()
        if self.logic.generate_pdf_report(debts):
            messagebox.showinfo("Success", "Report saved as SplitMate_Report.pdf")
        else:
            messagebox.showerror("Error", "Could not generate PDF.")
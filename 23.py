import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os

# Using a generic data file name
DATA_FILE = "piggy_bank_data.json"

class PiggyBankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Piggy Bank Tracker 🐷")
        self.root.geometry("400x550")
        self.root.configure(bg="#f0f7f4")
        self.root.resizable(False, False)

        # Core variables
        self.balance = 0.0
        self.history = []
        self.load_data()

        # --- Title ---
        title_label = tk.Label(root, text="Piggy Bank 🐷", font=("Segoe UI", 22, "bold"), fg="#2d6a4f", bg="#f0f7f4")
        title_label.pack(pady=10)

        # --- Balance Display ---
        self.balance_frame = tk.Frame(root, bg="#d8f3dc", bd=2, relief="groove")
        self.balance_frame.pack(pady=10, fill="x", padx=30)
        
        # This label displays the actual total money
        self.balance_label = tk.Label(self.balance_frame, text=f"${self.balance:.2f}", font=("Segoe UI", 32, "bold"), fg="#1b4332", bg="#d8f3dc")
        self.balance_label.pack(pady=10)

        # --- Input Fields ---
        input_frame = tk.Frame(root, bg="#f0f7f4")
        input_frame.pack(pady=10, fill="x", padx=30)

        tk.Label(input_frame, text="How much money?", font=("Segoe UI", 11, "bold"), fg="#495057", bg="#f0f7f4").grid(row=0, column=0, sticky="w", pady=2)
        self.amount_entry = tk.Entry(input_frame, font=("Segoe UI", 12), width=12, justify="center")
        self.amount_entry.grid(row=1, column=0, padx=5, pady=5)

        tk.Label(input_frame, text="For what? (e.g. Chores)", font=("Segoe UI", 11, "bold"), fg="#495057", bg="#f0f7f4").grid(row=0, column=1, sticky="w", pady=2)
        self.label_entry = tk.Entry(input_frame, font=("Segoe UI", 12), width=18)
        self.label_entry.grid(row=1, column=1, padx=5, pady=5)

        # --- Action Buttons ---
        btn_frame = tk.Frame(root, bg="#f0f7f4")
        btn_frame.pack(pady=5)

        # Clicking these runs the math modification function
        add_btn = tk.Button(btn_frame, text="💰 Add Money", font=("Segoe UI", 11, "bold"), bg="#52b788", fg="white", bd=0, padx=15, pady=5, command=lambda: self.modify_money("add"))
        add_btn.grid(row=0, column=0, padx=10)

        spend_btn = tk.Button(btn_frame, text="🍦 Spend Money", font=("Segoe UI", 11, "bold"), bg="#e63946", fg="white", bd=0, padx=15, pady=5, command=lambda: self.modify_money("spend"))
        spend_btn.grid(row=0, column=1, padx=10)

        # --- Journal Log ---
        tk.Label(root, text="📜 Piggy Bank Journal", font=("Segoe UI", 12, "bold"), fg="#495057", bg="#f0f7f4").pack(anchor="w", padx=35, pady=(15, 2))
        
        history_frame = tk.Frame(root, bg="white")
        history_frame.pack(fill="both", expand=True, padx=30, pady=5)

        scrollbar = tk.Scrollbar(history_frame, orient="vertical")
        self.history_listbox = tk.Listbox(history_frame, font=("Courier", 10), bd=0, yscrollcommand=scrollbar.set)
        
        scrollbar.config(command=self.history_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_listbox.pack(side="left", fill="both", expand=True)

        # --- Reset Trigger ---
        reset_btn = tk.Button(root, text="Reset Piggy Bank", font=("Segoe UI", 9, "underline"), fg="#adb5bd", bg="#f0f7f4", bd=0, activebackground="#f0f7f4", command=self.clear_data)
        reset_btn.pack(pady=10)

        # Initial UI refresh
        self.update_ui()

    def modify_money(self, transaction_type):
        try:
            # Grabs the text from the entry box and turns it into a decimal number
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Oops!", "Please type a valid number greater than 0!")
            return

        label = self.label_entry.get().strip()
        if not label:
            label = "Saved Money" if transaction_type == "add" else "Spent Money"

        timestamp = datetime.now().strftime("%m/%d %H:%M")

        # The actual math equations
        if transaction_type == "add":
            self.balance += amount
            log_text = f"[{timestamp}] +${amount:6.2f} : {label}"
        else:
            self.balance -= amount
            log_text = f"[{timestamp}] -${amount:6.2f} : {label}"

        # Save to array
        self.history.insert(0, log_text)
        
        # Save straight to local offline file
        self.save_data()

        # Clear text input entries so they are ready for next time
        self.amount_entry.delete(0, tk.END)
        self.label_entry.delete(0, tk.END)

        # Trigger full screen display update
        self.update_ui()

    def update_ui(self):
        # Update the big green total money box instantly
        self.balance_label.config(text=f"${self.balance:.2f}")
        
        # Clear old items out of the listbox and reprint the new history order
        self.history_listbox.delete(0, tk.END)
        for record in self.history:
            self.history_listbox.insert(tk.END, record)
            if "-" in record:
                self.history_listbox.itemconfig(tk.END, {'fg': '#e63946'})
            else:
                self.history_listbox.itemconfig(tk.END, {'fg': '#2d6a4f'})

    def save_data(self):
        try:
            data = {"balance": self.balance, "history": self.history}
            with open(DATA_FILE, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Save error: {e}")

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                    self.balance = float(data.get("balance", 0.0))
                    self.history = data.get("history", [])
            except:
                self.balance = 0.0
                self.history = []

    def clear_data(self):
        if messagebox.askyesno("Reset", "Are you sure you want to empty your piggy bank?"):
            if os.path.exists(DATA_FILE):
                try:
                    os.remove(DATA_FILE)
                except:
                    pass
            self.balance = 0.0
            self.history = []
            self.update_ui()

if __name__ == "__main__":
    root = tk.Tk()
    app = PiggyBankApp(root)
    root.mainloop()
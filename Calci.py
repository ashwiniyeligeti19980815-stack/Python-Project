import tkinter as tk
from tkinter import messagebox
import math

class ProCalci:
    def __init__(self, root):
        self.root = root
        self.root.title("Calci Pro")
        self.root.geometry("380x550")
        self.root.configure(bg="#1e272e") # Dark Theme

        self.equation = ""
        self.history_data = [] # Stores all calculations

        # --- Display ---
        self.display = tk.Entry(root, font=("Arial", 30), borderwidth=0, justify='right', 
                                bg="#1e272e", fg="white", insertbackground="white")
        self.display.pack(fill="both", padx=20, pady=40)
        self.display.focus_set()

        # --- Button Frame ---
        self.btn_frame = tk.Frame(root, bg="#1e272e")
        self.btn_frame.pack(expand=True, fill="both", padx=10)

        # Keyboard Bindings
        self.root.bind('<Key>', self.key_input)
        self.root.bind('<Return>', lambda e: self.calculate())
        self.root.bind('<BackSpace>', lambda e: self.backspace())

        self.create_buttons()

        # --- Bottom History Button ---
        self.hist_btn = tk.Button(root, text="VIEW HISTORY LOG", bg="#2980b9", fg="white",
                                  font=("Arial", 10, "bold"), relief="flat", pady=12,
                                  command=self.open_history_window)
        self.hist_btn.pack(fill="x", side="bottom")

    def create_buttons(self):
        buttons = [
            'sin', 'cos', 'tan', 'C',
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        row, col = 0, 0
        for btn in buttons:
            # Theme: Grey for numbers, Blue for functions, Green for equals
            if btn.isdigit() or btn == ".": bg = "#7f8c8d"
            elif btn == "=": bg = "#27ae60"
            else: bg = "#2980b9"

            b = tk.Button(self.btn_frame, text=btn, font=("Arial", 14, "bold"), 
                          bg=bg, fg="white", relief="flat", 
                          command=lambda x=btn: self.on_click(x))
            b.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)
            
            col += 1
            if col > 3:
                col = 0
                row += 1

        for i in range(4): self.btn_frame.columnconfigure(i, weight=1)
        for i in range(5): self.btn_frame.rowconfigure(i, weight=1)

    def on_click(self, char):
        if char == "=": self.calculate()
        elif char == "C": self.clear()
        elif char in ['sin', 'cos', 'tan']: self.sci_op(char)
        else:
            self.equation += str(char)
            self.update_display()

    def key_input(self, event):
        if event.char.isdigit() or event.char in "+-*/.":
            self.equation += event.char
            self.update_display()

    def backspace(self):
        self.equation = self.equation[:-1]
        self.update_display()

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.equation)

    def clear(self):
        self.equation = ""
        self.update_display()

    def sci_op(self, func):
        try:
            val = float(self.display.get())
            if func == 'sin': res = math.sin(math.radians(val))
            elif func == 'cos': res = math.cos(math.radians(val))
            elif func == 'tan': res = math.tan(math.radians(val))
            
            result_str = str(round(res, 4))
            self.history_data.append(f"{func}({val}) = {result_str}")
            self.equation = result_str
            self.update_display()
        except:
            messagebox.showerror("Error", "Enter a valid number first")

    def calculate(self):
        try:
            res = str(eval(self.equation))
            self.history_data.append(f"{self.equation} = {res}")
            self.equation = res
            self.update_display()
        except:
            messagebox.showerror("Error", "Invalid Math")
            self.equation = ""

    def open_history_window(self):
        # Create a new top-level window
        history_win = tk.Toplevel(self.root)
        history_win.title("Calculation History")
        history_win.geometry("300x400")
        history_win.configure(bg="#2f3640")

        header = tk.Label(history_win, text="Recent History", bg="#2f3640", 
                          fg="white", font=("Arial", 12, "bold"), pady=10)
        header.pack()

        # Listbox to show the data
        listbox = tk.Listbox(history_win, bg="#353b48", fg="white", 
                             font=("Arial", 10), borderwidth=0, highlightthickness=0)
        listbox.pack(fill="both", expand=True, padx=10, pady=10)

        # Add items from our list to the listbox
        for item in reversed(self.history_data): # Show newest first
            listbox.insert(tk.END, f" • {item}")

        # Close button for the popup
        close_btn = tk.Button(history_win, text="CLOSE", command=history_win.destroy, 
                              bg="#e74c3c", fg="white", relief="flat")
        close_btn.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProCalci(root)
    root.mainloop()
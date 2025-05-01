from pydoc import text
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv

# --- Login Window Class
class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        # print("--> Inside LoginWindow __init__") # Keep prints for debugging if needed
        super().__init__(parent)
        self.parent_app = parent

        self.title("Login")
        self.resizable(False, False)

        frame = ttk.Frame(self, padding="15")
        frame.grid(row=0, column=0, sticky="nsew")

        username_label = ttk.Label(frame, text="Username:")
        username_label.grid(row=0, column=0, sticky="w", pady=5, padx=5)

        self.username_entry = ttk.Entry(frame)
        self.username_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        password_label = ttk.Label(frame, text="Password:")
        password_label.grid(row=1, column=0, sticky="w", pady=5, padx=5)

        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        login_button = ttk.Button(frame, text="Login", command=self.perform_login)
        login_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.error_label = ttk.Label(frame, text="") # Error label with default styling
        self.error_label.grid(row=3, column=0, columnspan=2, sticky="ew")

        self.username_entry.bind("<Return>", lambda event=None: login_button.invoke())
        self.password_entry.bind("<Return>", lambda event=None: login_button.invoke())
      


    def perform_login(self):
        # print("--> Attempting login...") # Keep prints for debugging if needed
        username = self.username_entry.get()
        password = self.password_entry.get()

        valid_username = "admin"
        valid_password = "password"

        if username == valid_username and password == valid_password:
            # print("--> Login successful. Destroying LoginWindow and showing main app.") # Keep prints if needed
            self.destroy()
            self.parent_app.show_main_window()
        else:
            # print("--> Login failed.") # Keep prints if needed
            self.error_label.config(text="Invalid username or password", foreground="red") # Optionally set error color
            self.password_entry.delete(0, tk.END)

#  Main Application Class 
class Application(tk.Tk):
    def __init__(self):
        # print("--> Inside Application __init__ (Creating root window)") # Keep prints if needed
        super().__init__()
        self.title("Inventory App")

        # print("--> Withdrawing main window...") # Keep prints if needed
        self.withdraw() # Hide the main window initially

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        frame = InputForm(self) # InputForm is created here
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
       


    def show_main_window(self):
      
        self.deiconify()

# --- InputForm Class
class InputForm(ttk.Frame):
    def __init__(self, parent):
       
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.entry = ttk.Entry(self)
        self.entry.grid(row=0, column=0, sticky="ew")
       
        self.entry.bind("<Return>", self.add_to_list)

        
        self.entry_btn = ttk.Button(self, text="Add Line", command=self.add_to_list)
        self.entry_btn.grid(row=0, column=1)

        self.entry_btn5 = ttk.Button(self, text="Remove Line", command=self.remove_to_list)
        self.entry_btn5.grid(row=0, column=2)

        self.entry_btn2 = ttk.Button(self, text="Clear", command=self.clear_list)
        self.entry_btn2.grid(row=0, column=3)

        self.entry_btn3 = ttk.Button(self, text="Save", command=lambda: save_list(self, self.text_list))
        self.entry_btn3.grid(row=0, column=4)

        self.entry_btn4 = ttk.Button(self, text="Load", command=lambda: load_list(self, self.text_list))
        self.entry_btn4.grid(row=0, column=5)

        self.text_list = tk.Listbox(self)
        self.text_list.grid(row=1, column=0, columnspan=6, sticky="nsew")
       

    
    def add_to_list(self, _event=None):
        
        text = self.entry.get()
        if text:
            self.text_list.insert(tk.END, text)
            self.entry.delete(0, tk.END)

    def clear_list(self):
        
        self.text_list.delete(0, tk.END)
    
    def remove_to_list(self):
        selected_indices = self.text_list.curselection()
        for i in reversed(selected_indices):
            self.text_list.delete(i)


# --- Load/Save Functions ---
def load_list(parent_window, listbox_widget):
    """Opens file dialog, loads CSV into listbox widget."""
    # print("--> Attempting to load list...") # Keep prints if needed
    try:
        file_path = filedialog.askopenfilename(
            parent=parent_window,
            title="Select a CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not file_path:
            # print("--> Load cancelled.") # Keep prints if needed
            return False, "cancelled"

        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            listbox_widget.delete(0, tk.END)
            for row in reader:
                if row and row[0].strip():
                    listbox_widget.insert(tk.END, row[0])
        # print("--> List loaded successfully.") # Keep prints if needed
        return True, file_path
    except FileNotFoundError:
        print("--> Error loading CSV: File not found")
        return False, "not_found"
    except Exception as e:
        print(f"--> An error occurred while loading from CSV: {str(e)}")
        return False, str(e)

def save_list(parent_window, listbox_widget):
    """Opens file dialog, saves listbox content to CSV."""
    # print("--> Attempting to save list...") # Keep prints if needed
    try:
        file_path = filedialog.asksaveasfilename(
            parent=parent_window,
            title="Save Inventory As",
            initialfile="inventory.csv",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not file_path:
            # print("--> Save cancelled.") # Keep prints if needed
            return False, "cancelled"

        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            inventory_items = listbox_widget.get(0, tk.END)

            for item in inventory_items:
                if isinstance(item, str) and item.strip():
                    writer.writerow([item.strip()])
        # print("--> List saved successfully.") # Keep prints if needed
        return True, file_path
    except Exception as e:
        print(f"--> An error occurred while saving to CSV: {str(e)}")
        return False, str(e)


# --- Main Function ---
def main():
    
    app = Application()
    # print("--> Application instance created.") # Keep prints if needed

    login_window = LoginWindow(app)
   

    login_window.protocol("WM_DELETE_WINDOW", app.quit)
    

    
    app.mainloop() 
    


if __name__ == "__main__":
   
    main()

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv

class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
      super().__init__(parent)
    self.parent_app = parent

def main():
    app = Application()
    app.mainloop()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple App")

        self.columnconfigure(0, weight=1)
        # Removed the second column configuration as only one frame is used
        self.rowconfigure(0, weight=1)

        frame = InputForm(self)
        # Adjusted column span to 1 as only one frame is used
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)


class InputForm(ttk.Frame):
    def __init__(self, parent):
       
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1) # Row for the listbox

        self.entry = ttk.Entry(self)
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", self.add_to_list)

        self.entry_btn = ttk.Button(self, text="Add", command=self.add_to_list)
        self.entry_btn.grid(row=0, column=1)

        self.entry_btn2 = ttk.Button(self, text="Clear", command=self.clear_list)
        self.entry_btn2.grid(row=0, column=2)

        # Use self.text_list directly as the widget reference
        self.entry_btn3 = ttk.Button(self, text="Save", command=lambda: save_list(self, self.text_list))
        self.entry_btn3.grid(row=0, column=3)

        self.entry_btn4 = ttk.Button(self, text="Load", command=lambda: load_list(self, self.text_list))
        self.entry_btn4.grid(row=0, column=4)

        self.text_list = tk.Listbox(self)
        self.text_list.grid(row=1, column=0, columnspan=5, sticky="nsew") # Listbox in row 1

    def add_to_list(self, _event=None):
        text = self.entry.get()
        if text:
            self.text_list.insert(tk.END, text)
            self.entry.delete(0, tk.END)

    def clear_list(self):
        self.text_list.delete(0, tk.END)

def load_list(parent_window, listbox_widget): 
    """Opens file dialog, loads CSV into listbox widget."""
    try:
        file_path = filedialog.askopenfilename(
            parent=parent_window,
            title="Select a CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not file_path:
            return False, "cancelled"

        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            
            listbox_widget.delete(0, tk.END)
            for row in reader:
                
                if row and row[0].strip():
                     
                    listbox_widget.insert(tk.END, row[0])

        return True, file_path
    except FileNotFoundError:
        print("An error occurred while loading from CSV: File not found")
        return False, "not_found"
    except Exception as e:
        print(f"An error occurred while loading from CSV: {str(e)}")
        return False, str(e)

def save_list(parent_window, listbox_widget): 
    """Opens file dialog, saves listbox content to CSV."""
    try:
        file_path = filedialog.asksaveasfilename(
            parent=parent_window,
            title="Save Inventory As",
            initialfile="inventory.csv",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not file_path:
            return False, "cancelled"

        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
           
            inventory_items = listbox_widget.get(0, tk.END)

            for item in inventory_items:
                 
                if isinstance(item, str) and item.strip():
                    writer.writerow([item.strip()]) 

        return True, file_path
    except Exception as e:
        print(f"An error occurred while saving to CSV: {str(e)}")
        return False, str(e)

if __name__ == "__main__":
    main()
        


#root = tk.Tk()
#root.title("My Simple App")
#root.mainloop()


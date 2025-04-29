import tkinter as tk

root = tk.Tk()
root.title("My Simple App")

def add_to_list(event=None):
    text =entry.get()
    if text:
        text_list.insert(tk.END,text)
        entry.delete(0,tk.END)

def remove_to_list():
    try:
        index = text_list.curselection()[0]
        text_list.delete(index)
        entry.delete(0,tk.END)
    except IndexError:
        pass

root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)

frame2 =tk.Frame(root)
frame2.grid(row=0, column=0, sticky="nsew")


frame2.columnconfigure(0,weight=1)
frame2.rowconfigure(1,weight=1)


entry= tk.Entry(frame2)
entry.grid(row=0,column=0, sticky="ew")

entry.bind("<Return>",add_to_list)



entry_btn=tk.Button(frame2,text="Add", command=add_to_list)
entry_btn.grid(row=0,column=1)

entry_btn=tk.Button(frame2,text="Remove", command=remove_to_list)
entry_btn.grid(row=0,column=2)

text_list =tk.Listbox(frame2)
text_list.grid(row=1,column=0, columnspan=2, sticky="nsew")

entry.bind("<Delete>",remove_to_list)

root.mainloop()
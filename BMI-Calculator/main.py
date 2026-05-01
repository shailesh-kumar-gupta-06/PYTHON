import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime
import matplotlib.pyplot as plt

conn = sqlite3.connect("bmi_app.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    weight REAL,
    height REAL,
    bmi REAL,
    date TEXT
)
""")
conn.commit()

def calculate_bmi(weight, height):
    return weight / (height ** 2)

def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 24.9:
        return "Normal"
    elif bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

def save_data(name, weight, height, bmi):
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO bmi_records (name, weight, height, bmi, date)
    VALUES (?, ?, ?, ?, ?)
    """, (name, weight, height, bmi, date))

    conn.commit()

def fetch_user_data(name):
    cursor.execute("SELECT date, bmi FROM bmi_records WHERE name=?", (name,))
    return cursor.fetchall()

def on_calculate():
    name = entry_name.get().strip()

    try:
        weight = float(entry_weight.get())
        height = float(entry_height.get())

        if not name:
            messagebox.showerror("Error", "Enter your name!")
            return

        if weight <= 0 or height <= 0:
            raise ValueError

        bmi = calculate_bmi(weight, height)
        category = categorize_bmi(bmi)

        result_label.config(
            text=f"BMI: {bmi:.2f} ({category})"
        )

        save_data(name, weight, height, bmi)

    except ValueError:
        messagebox.showerror("Error", "Enter valid positive numbers!")

def show_history():
    name = entry_name.get().strip()

    if not name:
        messagebox.showerror("Error", "Enter your name first!")
        return

    data = fetch_user_data(name)

    if not data:
        messagebox.showinfo("Info", "No history found!")
        return

    history_text = "\n".join([f"{d[0]} → BMI: {d[1]:.2f}" for d in data])
    messagebox.showinfo("BMI History", history_text)

def show_graph():
    name = entry_name.get().strip()

    if not name:
        messagebox.showerror("Error", "Enter your name first!")
        return

    data = fetch_user_data(name)

    if not data:
        messagebox.showinfo("Info", "No data to plot!")
        return

    dates = [d[0] for d in data]
    bmis = [d[1] for d in data]

    plt.figure()
    plt.plot(bmis, marker='o')
    plt.title(f"{name}'s BMI Trend")
    plt.xlabel("Entries")
    plt.ylabel("BMI")
    plt.grid()
    plt.show()

root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("350x350")

tk.Label(root, text="Name").pack(pady=5)
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Weight (kg)").pack(pady=5)
entry_weight = tk.Entry(root)
entry_weight.pack()

tk.Label(root, text="Height (m)").pack(pady=5)
entry_height = tk.Entry(root)
entry_height.pack()

tk.Button(root, text="Calculate BMI", command=on_calculate).pack(pady=10)
tk.Button(root, text="Show History", command=show_history).pack(pady=5)
tk.Button(root, text="Show Graph", command=show_graph).pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=15)

root.mainloop()
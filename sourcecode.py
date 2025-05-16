import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt


# Database Setup
conn = sqlite3.connect('bmi_data.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    weight REAL,
    height REAL,
    bmi REAL
)''')
conn.commit()


# BMI Calculation
def calculate_bmi():
    name = entry_name.get().strip()
        
    if not name:
        messagebox.showerror("Error","Name can not be empty")
        label_result.config(text="")  # Clear previous result
        return  # Stop further execution
            
    if any(char.isdigit() for char in name):
        messagebox.showerror("Invalid Input", "Name should not contain numbers!")
        label_result.config(text="")  # Clear previous result
        return  # Stop further execution
            
    try:
            
        weight = float(entry_weight.get())
        height = float(entry_height.get())

        if height <= 0 or weight <= 0:
            messagebox.showerror("Invalid Input", "Height and Weight must be positive values.")
            return

        bmi = weight / (height ** 2)
        result = f"Your BMI is: {bmi:.2f} - {bmi_category(bmi)}"
        label_result.config(text=result)

        cursor.execute("INSERT INTO users (name, weight, height, bmi) VALUES (?, ?, ?, ?)",
                   (name, weight, height, bmi))
        conn.commit()
        
    except ValueError as ve:
        messagebox.showerror("Invalid Input", "Please enter numeric values for Weight/Height")
        label_result.config(text="")
        
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {str(e)}")
        label_result.config(text="")

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 24.9:
        return "Normal"
    elif bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"


def view_history():
    cursor.execute("SELECT name, bmi FROM users")
    records = cursor.fetchall()

    names = []
    bmis = []

    for record in records:
        name = record[0].strip()
        if name and not any(char.isdigit() for char in name):  # skip empty or numeric names
            names.append(name)
            bmis.append(record[1])

    if not names:
        messagebox.showinfo("No Data", "No valid user data to display!")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(names, bmis, marker='o')
    plt.title("BMI Trend Analysis")
    plt.xlabel("User")
    plt.ylabel("BMI")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# GUI Setup
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("400x400")

tk.Label(root, text="Name:").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Weight (kg):").pack()
entry_weight = tk.Entry(root)
entry_weight.pack()

tk.Label(root, text="Height (m):").pack()
entry_height = tk.Entry(root)
entry_height.pack()

tk.Button(root, text="Calculate BMI", command=calculate_bmi).pack(pady=10)
label_result = tk.Label(root, text="")
label_result.pack()

tk.Button(root, text="View BMI History", command=view_history).pack(pady=10)

root.mainloop()

conn.close()
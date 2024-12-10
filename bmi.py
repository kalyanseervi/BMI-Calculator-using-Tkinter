import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import re

# Initialize the database
def init_db():
    conn = sqlite3.connect("bmi_data.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bmi_records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_name TEXT,
                        email TEXT UNIQUE,
                        gender TEXT,
                        weight REAL,
                        height REAL,
                        bmi REAL,
                        category TEXT,
                        date TEXT)''')
    conn.commit()
    conn.close()

# Calculate BMI and categorize
def calculate_bmi(weight, height):
    try:
        bmi = weight / (height / 100) ** 2
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"
        return round(bmi, 2), category
    except ZeroDivisionError:
        raise ValueError("Height cannot be zero or negative.")

# Save data with error handling
def save_data(username, email, gender, weight, height, bmi, category):
    try:
        conn = sqlite3.connect("bmi_data.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bmi_records (user_name, email, gender, weight, height, bmi, category, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (username, email, gender, weight, height, bmi, category, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "The email already exists. Please use a different email.")
        return False
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred while saving the data: {e}")
        return False

# Display BMI gauge using Plotly
def show_bmi_gauge(bmi):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=bmi,  # Current BMI value
        title={"text": "BMI Gauge"},
        delta={
            'reference': 24.9,  # Reference BMI for normal weight upper bound
            'increasing': {'color': "green"},  # Set color when delta is positive
            'decreasing': {'color': "red"},  # Set color when delta is negative
        },
        gauge={
            'axis': {'range': [None, 40], 'tickcolor': "black", 'tickwidth': 2},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 18.5], 'color': '#ff7f0e'},  # Underweight (red)
                {'range': [18.5, 24.9], 'color': '#2ca02c'},  # Normal (green)
                {'range': [24.9, 29.9], 'color': '#ffcc00'},  # Overweight (yellow)
                {'range': [29.9, 40], 'color': '#d62728'},  # Obese (red)
            ],
        }
    ))
    fig.show()

# Display user records
def view_user_records(email):
    conn = sqlite3.connect("bmi_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, weight, height, bmi, category FROM bmi_records WHERE email = ?", (email,))
    records = cursor.fetchall()
    conn.close()

    if records:
        records_window = tk.Toplevel(root)
        records_window.title(f"Records for {email}")
        records_window.geometry("700x400")

        tree = ttk.Treeview(records_window, columns=("Date", "Weight", "Height", "BMI", "Category"), show="headings")
        tree.heading("Date", text="Date")
        tree.heading("Weight", text="Weight (kg)")
        tree.heading("Height", text="Height (cm)")
        tree.heading("BMI", text="BMI")
        tree.heading("Category", text="Category")
        tree.pack(fill=tk.BOTH, expand=True)

        for record in records:
            tree.insert("", tk.END, values=record)

        tk.Button(records_window, text="Close", command=records_window.destroy, font=("Arial", 12)).pack(pady=10)
    else:
        messagebox.showinfo("No Records", f"No data found for email: {email}")

# Display BMI trends graph
def show_bmi_trends(email):
    conn = sqlite3.connect("bmi_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, bmi FROM bmi_records WHERE email = ?", (email,))
    rows = cursor.fetchall()
    conn.close()

    if rows:
        dates = [row[0] for row in rows]
        bmis = [row[1] for row in rows]

        plt.figure(figsize=(8, 6))
        plt.plot(dates, bmis, marker="o", label="BMI", color="blue")
        plt.title(f"BMI Trends for {email}")
        plt.xlabel("Date")
        plt.ylabel("BMI")
        plt.xticks(rotation=45)
        plt.grid()
        plt.legend()
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showinfo("No Data", "No BMI records found for this email.")

# Validate email format
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

# Submit button action
def calculate_and_save():
    username = entry_name.get().strip()
    email = entry_email.get().strip()
    gender = gender_var.get()
    weight = entry_weight.get().strip()
    height = entry_height.get().strip()

    # Validate inputs
    if not username or not email or not gender or not weight or not height:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    if not is_valid_email(email):
        messagebox.showerror("Invalid Email", "Please enter a valid email address.")
        return

    try:
        weight = float(weight)
        height = float(height)
        if weight <= 0 or height <= 0:
            raise ValueError("Weight and height must be positive values.")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
        return

    # Calculate BMI
    try:
        bmi, category = calculate_bmi(weight, height)
    except ValueError as e:
        messagebox.showerror("Calculation Error", str(e))
        return

    # Save data and display prompt
    success = save_data(username, email, gender, weight, height, bmi, category)
    if success:
        messagebox.showinfo("BMI Calculated", f"Name: {username}\nEmail: {email}\nGender: {gender}\nWeight: {weight} kg\nHeight: {height} cm\nBMI: {bmi}\nCategory: {category}")
        show_bmi_gauge(bmi)

# GUI Design with UI/UX Optimizations
root = tk.Tk()
root.title("BMI Calculator with Gauge")
root.geometry("700x700")
root.config(bg="#f0f0f0")

style = ttk.Style()
style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("TCombobox", font=("Arial", 12))

# Header
tk.Label(root, text="BMI Calculator", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=10)

# Input Frame
frame = ttk.Frame(root, padding=10, style="TFrame")
frame.pack(pady=20)

# User inputs
ttk.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_name = ttk.Entry(frame)
entry_name.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_email = ttk.Entry(frame)
entry_email.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame, text="Gender:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
gender_var = tk.StringVar()
gender_menu = ttk.Combobox(frame, textvariable=gender_var, values=["Male", "Female", "Other"])
gender_menu.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame, text="Weight (kg):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_weight = ttk.Entry(frame)
entry_weight.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(frame, text="Height (cm):").grid(row=4, column=0, padx=5, pady=5, sticky="e")
entry_height = ttk.Entry(frame)
entry_height.grid(row=4, column=1, padx=5, pady=5)

# Buttons
ttk.Button(root, text="Calculate and Save", command=calculate_and_save).pack(pady=10)
ttk.Button(root, text="View Records", command=lambda: view_user_records(entry_email.get().strip())).pack(pady=5)
ttk.Button(root, text="View BMI Trends", command=lambda: show_bmi_trends(entry_email.get().strip())).pack(pady=5)

# Initialize database
init_db()

# Start the main application loop
root.mainloop()

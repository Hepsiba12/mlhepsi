import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import pandas as pd
import plotly.express as px

# Tariffs
tariffs = {
    "Urban": [2.0, 3.0, 5.0],
    "Rural": [1.5, 2.5, 4.0],
    "Industrial": [3.0, 4.0, 6.0]
}

def calculate_bill(units, region="Urban"):
    """Calculate bill based on dynamic slabs for specific regions."""
    slab_rates = tariffs.get(region, tariffs["Urban"])
    if units <= 100:
        return units * slab_rates[0]
    elif units <= 300:
        return 100 * slab_rates[0] + (units - 100) * slab_rates[1]
    else:
        return 100 * slab_rates[0] + 200 * slab_rates[1] + (units - 300) * slab_rates[2]

def visualize_trends(past_usage):
    """Visualize past usage trends."""
    months = [f"Month {i+1}" for i in range(len(past_usage))]
    df = pd.DataFrame({"Months": months, "Usage": past_usage})
    fig = px.line(df, x="Months", y="Usage", title="Electricity Usage Trends")
    fig.show()

# GUI
def calculate():
    try:
        units = int(units_entry.get())
        if units < 0:
            messagebox.showerror("Error", "Units cannot be negative!")
            return

        region = region_combobox.get()
        if region not in tariffs:
            region = "Urban"
        
        bill = calculate_bill(units, region)
        result_label.config(text=f"Estimated Bill: ${bill:.2f}")
        
        # Update past usage
        past_usage.append(units)
        if len(past_usage) > 1:
            visualize_trends(past_usage)

    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter valid units!")

# App setup
root = tk.Tk()
root.title("Electricity Bill Calculator")

# Fullscreen
root.attributes('-fullscreen', True)

# Add a way to exit fullscreen
def exit_fullscreen(event=None):
    root.attributes('-fullscreen', False)

root.bind("<Escape>", exit_fullscreen)

past_usage = []

# Region dropdown
tk.Label(root, text="Select Region:").pack(pady=5)
region_combobox = ttk.Combobox(root, values=["Urban", "Rural", "Industrial"], state="readonly")
region_combobox.pack()
region_combobox.set("Urban")

# Units entry
tk.Label(root, text="Enter Units Consumed:").pack(pady=5)
units_entry = tk.Entry(root)
units_entry.pack()

# Calculate button
calculate_button = tk.Button(root, text="Calculate Bill", command=calculate)
calculate_button.pack(pady=10)

# Result display
result_label = tk.Label(root, text="")
result_label.pack(pady=5)

# Run app
root.mainloop()


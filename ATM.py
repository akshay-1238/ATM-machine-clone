import tkinter as tk
from tkinter import messagebox
import os

# File path for storing balance
balance_file = "balance.txt"

# Functions to read and write balance
def read_balance():
    if os.path.exists(balance_file):
        with open(balance_file, "r") as file:
            return int(file.read().strip())
    else:
        return 10000  # Initial balance if file doesn't exist

def write_balance(balance):
    with open(balance_file, "w") as file:
        file.write(str(balance))

# Initialize balance from file
balance = read_balance()

# GUI setup
root = tk.Tk()
root.title("ATM Service")
root.geometry("300x400")

# Variables
pin = 36128
attempts = 3
entered_pin = tk.StringVar()

# Functions for ATM operations
def check_pin():
    global attempts
    try:
        user_pin = int(entered_pin.get())
        if user_pin == pin:
            messagebox.showinfo("Access Granted", "PIN correct! You can proceed with transactions.")
            show_main_screen()
        else:
            attempts -= 1
            if attempts > 0:
                messagebox.showwarning("Access Denied", f"Incorrect PIN. You have {attempts} attempts left.")
            else:
                messagebox.showerror("Access Denied", "Incorrect PIN entered 3 times. The account is locked.")
                root.quit()  # Close the application after 3 wrong attempts
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid PIN.")

def show_main_screen():
    pin_frame.pack_forget()
    main_frame.pack()

def show_balance():
    # Create a new window to show balance
    balance_window = tk.Toplevel(root)
    balance_window.title("Check Balance")
    balance_window.geometry("200x150")
    
    balance_label = tk.Label(balance_window, text=f"Your balance is: {balance} rupees", font=("Arial", 14))
    balance_label.pack(pady=20)
    
    close_button = tk.Button(balance_window, text="Close", command=balance_window.destroy, font=("Arial", 12))
    close_button.pack(pady=10)

def deposit_money():
    deposit_screen = tk.Toplevel(root)
    deposit_screen.title("Deposit Money")
    deposit_screen.geometry("300x200")
    
    tk.Label(deposit_screen, text="Enter amount to deposit:", font=("Arial", 14)).pack(pady=10)
    amount_var = tk.StringVar()
    tk.Entry(deposit_screen, textvariable=amount_var, font=("Arial", 14)).pack(pady=10)

    def confirm_deposit():
        try:
            deposit_amount = int(amount_var.get())
            global balance
            balance += deposit_amount
            write_balance(balance)
            messagebox.showinfo("Success", f"Deposited {deposit_amount} rupees successfully!")
            deposit_screen.destroy()  # Close deposit window
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")

    tk.Button(deposit_screen, text="Confirm", command=confirm_deposit, font=("Arial", 12)).pack(pady=10)

def withdraw_money():
    withdraw_screen = tk.Toplevel(root)
    withdraw_screen.title("Withdraw Money")
    withdraw_screen.geometry("300x200")
    
    tk.Label(withdraw_screen, text="Enter amount to withdraw:", font=("Arial", 14)).pack(pady=10)
    amount_var = tk.StringVar()
    tk.Entry(withdraw_screen, textvariable=amount_var, font=("Arial", 14)).pack(pady=10)

    def confirm_withdraw():
        try:
            withdraw_amount = int(amount_var.get())
            global balance
            if withdraw_amount <= balance:
                balance -= withdraw_amount
                write_balance(balance)
                messagebox.showinfo("Success", f"Withdrew {withdraw_amount} rupees successfully!")
                withdraw_screen.destroy()  # Close withdraw window
            else:
                messagebox.showerror("Insufficient Funds", "You don't have enough balance.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")

    tk.Button(withdraw_screen, text="Confirm", command=confirm_withdraw, font=("Arial", 12)).pack(pady=10)

def exit_program():
    root.quit()  # Close the main application window

# PIN Entry Screen
pin_frame = tk.Frame(root)
tk.Label(pin_frame, text="WELCOME TO AKSHAY ATM", font=("Arial", 16)).pack(pady=10)
tk.Label(pin_frame, text="Enter PIN:", font=("Arial", 14)).pack(pady=10)
tk.Entry(pin_frame, textvariable=entered_pin, show="*", font=("Arial", 14)).pack(pady=10)
tk.Button(pin_frame, text="Submit", command=check_pin, font=("Arial", 12)).pack(pady=10)
pin_frame.pack()

# Main Transaction Screen
main_frame = tk.Frame(root)
tk.Button(main_frame, text="Check Balance", command=show_balance, font=("Arial", 12)).pack(pady=10)
tk.Button(main_frame, text="Deposit Money", command=deposit_money, font=("Arial", 12)).pack(pady=10)
tk.Button(main_frame, text="Withdraw Money", command=withdraw_money, font=("Arial", 12)).pack(pady=10)

# Exit Button
tk.Button(main_frame, text="Exit", command=exit_program, font=("Arial", 12)).pack(pady=10)

# Start with PIN screen only
main_frame.pack_forget()

root.mainloop()

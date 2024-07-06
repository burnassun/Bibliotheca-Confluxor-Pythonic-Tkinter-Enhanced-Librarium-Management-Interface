import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime, timedelta

# Initializing database
def init_db():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books
                      (id INTEGER PRIMARY KEY, name TEXT, author TEXT, quantity INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY, name TEXT, book_name TEXT, author TEXT, issued_date DATE, return_date DATE, phone TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS returned_books
                      (id INTEGER PRIMARY KEY, name TEXT, book_name TEXT, author TEXT, returned_date DATE)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS wallet
                      (id INTEGER PRIMARY KEY, user_name TEXT, book_name TEXT, amount INTEGER, payment_type TEXT)''')
    conn.commit()
    conn.close()

# Functions to handle different operations
def view_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    
    view_books_window = tk.Toplevel()
    view_books_window.title("View Books")
    for book in books:
        tk.Label(view_books_window, text=f"Name: {book[1]}, Author: {book[2]}, Quantity: {book[3]}", font=("Helvetica", 12)).pack()

def add_book():
    def submit():
        name = name_entry.get()
        author = author_entry.get()
        quantity = int(quantity_entry.get())
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE name=? AND author=?', (name, author))
        book = cursor.fetchone()
        if book:
            cursor.execute('UPDATE books SET quantity = quantity + ? WHERE id = ?', (quantity, book[0]))
        else:
            cursor.execute('INSERT INTO books (name, author, quantity) VALUES (?, ?, ?)', (name, author, quantity))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Book added successfully!")
        add_book_window.destroy()
    
    add_book_window = tk.Toplevel()
    add_book_window.title("Add Book")
    
    tk.Label(add_book_window, text="Name:", font=("Helvetica", 12)).pack()
    name_entry = tk.Entry(add_book_window)
    name_entry.pack()
    
    tk.Label(add_book_window, text="Author:", font=("Helvetica", 12)).pack()
    author_entry = tk.Entry(add_book_window)
    author_entry.pack()
    
    tk.Label(add_book_window, text="Quantity:", font=("Helvetica", 12)).pack()
    quantity_entry = tk.Entry(add_book_window)
    quantity_entry.pack()
    
    tk.Button(add_book_window, text="Submit", command=submit, font=("Helvetica", 12)).pack()

def users():
    def issue_book():
        name = name_entry.get()
        book_name = book_name_entry.get()
        author = author_entry.get()
        phone = phone_entry.get()
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE name=? AND author=?', (book_name, author))
        book = cursor.fetchone()
        if book and book[3] > 0:
            issued_date = datetime.now().date()
            return_date = issued_date + timedelta(days=15)
            cursor.execute('INSERT INTO users (name, book_name, author, issued_date, return_date, phone) VALUES (?, ?, ?, ?, ?, ?)', 
                           (name, book_name, author, issued_date, return_date, phone))
            cursor.execute('UPDATE books SET quantity = quantity - 1 WHERE id = ?', (book[0],))
            conn.commit()
            messagebox.showinfo("Success", "Book issued successfully!")
        else:
            messagebox.showwarning("Warning", "Book not available!")
        conn.close()
        users_window.destroy()
    
    users_window = tk.Toplevel()
    users_window.title("Users")
    
    tk.Label(users_window, text="Name:", font=("Helvetica", 12)).pack()
    name_entry = tk.Entry(users_window)
    name_entry.pack()
    
    tk.Label(users_window, text="Book Name:", font=("Helvetica", 12)).pack()
    book_name_entry = tk.Entry(users_window)
    book_name_entry.pack()
    
    tk.Label(users_window, text="Author:", font=("Helvetica", 12)).pack()
    author_entry = tk.Entry(users_window)
    author_entry.pack()
    
    tk.Label(users_window, text="Phone:", font=("Helvetica", 12)).pack()
    phone_entry = tk.Entry(users_window)
    phone_entry.pack()
    
    tk.Button(users_window, text="Issue Book", command=issue_book, font=("Helvetica", 12)).pack()

def owner_section():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, phone, book_name, return_date FROM users')
    users = cursor.fetchall()
    conn.close()
    
    owner_window = tk.Toplevel()
    owner_window.title("Owner Section")
    for user in users:
        tk.Label(owner_window, text=f"Name: {user[0]}, Phone: {user[1]}, Book: {user[2]}, Return Date: {user[3]}", font=("Helvetica", 12)).pack()

def remove_users():
    def remove_user(user):
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id=?', (user[0],))
        user_info = cursor.fetchone()
        if user_info:
            cursor.execute('DELETE FROM users WHERE id=?', (user_info[0],))
            cursor.execute('UPDATE books SET quantity = quantity + 1 WHERE name=? AND author=?', (user_info[2], user_info[3]))
            cursor.execute('INSERT INTO returned_books (name, book_name, author, returned_date) VALUES (?, ?, ?, ?)',
                           (user_info[1], user_info[2], user_info[3], datetime.now().date()))
            conn.commit()
            messagebox.showinfo("Success", f"User {user_info[1]} removed and book {user_info[2]} returned!")
        conn.close()
        remove_users_window.destroy()

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    
    remove_users_window = tk.Toplevel()
    remove_users_window.title("Remove Users")
    for user in users:
        tk.Button(remove_users_window, text=f"Remove {user[1]} (Book: {user[2]})", command=lambda u=user: remove_user(u), font=("Helvetica", 12)).pack()

def incoming_payments():
    def add_penalty(user):
        def submit_penalty():
            penalty_amount = int(penalty_entry.get())
            payment_type = payment_var.get()
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO wallet (user_name, book_name, amount, payment_type) VALUES (?, ?, ?, ?)', 
                           (user[1], user[2], penalty_amount, payment_type))
            cursor.execute('DELETE FROM returned_books WHERE id = ?', (user[0],))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Penalty of {penalty_amount} added to wallet as {payment_type} payment!")
            penalty_window.destroy()
            incoming_payments_window.destroy()

        penalty_window = tk.Toplevel()
        penalty_window.title("Add Penalty")
        tk.Label(penalty_window, text=f"Add Penalty for {user[1]} (Book: {user[2]})", font=("Helvetica", 12)).pack()
        tk.Label(penalty_window, text="Penalty Amount:", font=("Helvetica", 12)).pack()
        penalty_entry = tk.Entry(penalty_window)
        penalty_entry.pack()

        payment_var = tk.StringVar(value="cash")
        tk.Radiobutton(penalty_window, text="Cash", variable=payment_var, value="cash").pack()
        tk.Radiobutton(penalty_window, text="Online", variable=payment_var, value="online").pack()

        tk.Button(penalty_window, text="Submit", command=submit_penalty, font=("Helvetica", 12)).pack()

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM returned_books')
    returned_users = cursor.fetchall()
    conn.close()
    
    incoming_payments_window = tk.Toplevel()
    incoming_payments_window.title("Incoming Payments")
    for user in returned_users:
        tk.Button(incoming_payments_window, text=f"{user[1]} (Book: {user[2]})", command=lambda u=user: add_penalty(u), font=("Helvetica", 12)).pack()

def wallet():
    def withdraw_all():
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM wallet')
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "All money withdrawn successfully!")
        wallet_window.destroy()

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM wallet')
    payments = cursor.fetchall()
    cursor.execute('SELECT SUM(amount) FROM wallet WHERE payment_type="cash"')
    cash_total = cursor.fetchone()[0] or 0
    cursor.execute('SELECT SUM(amount) FROM wallet WHERE payment_type="online"')
    online_total = cursor.fetchone()[0] or 0
    conn.close()
    
    wallet_window = tk.Toplevel()
    wallet_window.title("Wallet")
    for payment in payments:
        tk.Label(wallet_window, text=f"User: {payment[1]}, Book: {payment[2]}, Amount: {payment[3]}, Payment Type: {payment[4]}", font=("Helvetica", 12)).pack()
    tk.Label(wallet_window, text=f"Total Cash: {cash_total}", font=("Helvetica", 12)).pack()
    tk.Label(wallet_window, text=f"Total Online: {online_total}", font=("Helvetica", 12)).pack()
    tk.Label(wallet_window, text=f"Total Amount: {cash_total + online_total}", font=("Helvetica", 12)).pack()
    tk.Button(wallet_window, text="Withdraw All Money", command=withdraw_all, font=("Helvetica", 12)).pack()

# Initializing main window
root = tk.Tk()
root.title("Library Admin Page")

# Creating buttons for different operations
tk.Button(root, text="View Books", command=view_books, font=("Helvetica", 12)).pack()
tk.Button(root, text="Add Books", command=add_book, font=("Helvetica", 12)).pack()
tk.Button(root, text="Users", command=users, font=("Helvetica", 12)).pack()
tk.Button(root, text="Remove Users", command=remove_users, font=("Helvetica", 12)).pack()
tk.Button(root, text="Owner Section", command=owner_section, font=("Helvetica", 12)).pack()
tk.Button(root, text="Incoming Payments", command=incoming_payments, font=("Helvetica", 12)).pack()
tk.Button(root, text="Wallet", command=wallet, font=("Helvetica", 12)).pack()

init_db()
root.mainloop()

import mysql.connector
from datetime import date
import tkinter as tk
from tkinter import messagebox

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="fireflies",
            database="LIBRARY_MGMT",
            use_unicode = True,
            charset="utf8mb4"
        )
        return connection
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
        return None

def add_book(title, author, year):
    conn = connect_to_db()
    if conn is None:
        return
    cursor = conn.cursor()
    query = "insert into Books (title, author, year) values (%s, %s, %s)"
    values = (title, author, year)
    try:
        cursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Success", f"Book '{title}' added successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to add book: {err}")
    finally:
        cursor.close()
        conn.close()

def search_books(title):
    conn = connect_to_db()
    if conn is None:
        return None
    cursor = conn.cursor()
    query = "Select * from Books where title like %s"
    cursor.execute(query, (f'%{title}%',))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results  # Added return statement

def issue_book(book_id, member_id):
    conn = connect_to_db()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute("select status from Books where book_id = %s", (book_id,))
    book = cursor.fetchone()
    if book and book[0] == 'Available':
        query = "insert into Transactions (book_id, member_id, issue_date) values (%s, %s, %s)"
        cursor.execute(query, (book_id, member_id, date.today()))
        cursor.execute("Update Books set status = 'Issued' where book_id = %s", (book_id,))
        conn.commit()
        messagebox.showinfo("Book issued successfully!")
    else:
        messagebox.showerror("Error", "Book is not available.")
    cursor.close()
    conn.close()

def return_book(book_id):
    conn = connect_to_db()
    if conn is None:
        return
    cursor = conn.cursor()
    query = "Update Books set status = 'Available' where book_id = %s"
    cursor.execute(query, (book_id,))
    conn.commit()
    messagebox.showinfo("Book returned successfully!")
    cursor.close()
    conn.close()

def main_menu():
    root = tk.Tk()
    root.title("Library Management System")
    root.geometry("400x300")

    label = tk.Label(root, text="Library Management System", font=("Arial", 16))
    label.pack(pady=20)

    add_book_btn = tk.Button(root, text="Add Book", width=20, command=add_book_window)
    add_book_btn.pack(pady=5)

    search_book_btn = tk.Button(root, text="Search Books", width=20, command=search_book_window)
    search_book_btn.pack(pady=5)

    exit_btn = tk.Button(root, text="Exit", width=20, command=root.quit)
    exit_btn.pack(pady=5)

    root.mainloop()

def add_book_window():
    window = tk.Toplevel()
    window.title("Add Book")
    window.geometry("300x200")

    tk.Label(window, text="Title").pack(pady=5)
    title_entry = tk.Entry(window)
    title_entry.pack(pady=5)

    tk.Label(window, text="Author").pack(pady=5)
    author_entry = tk.Entry(window)
    author_entry.pack(pady=5)

    tk.Label(window, text="Year").pack(pady=5)
    year_entry = tk.Entry(window)
    year_entry.pack(pady=5)

    def submit():
        title = title_entry.get()
        year = year_entry.get()
        author = author_entry.get()
        if not title or not author or not year.isdigit():  # Validate input
            messagebox.showerror("Input Error", "Please enter valid title, author, and year.")
            return
        add_book(title, author, int(year))  # Convert year to int
        window.destroy()

    submit_btn = tk.Button(window, text="Add Book", command=submit)
    submit_btn.pack(pady=10)

def search_book_window():
    window = tk.Toplevel()
    window.title("Search Books")
    window.geometry("400x300")

    tk.Label(window, text="Search by Title").pack(pady=5)
    title_entry = tk.Entry(window)
    title_entry.pack(pady=5)

    result_label = tk.Label(window, text="")
    result_label.pack(pady=5)

    def search():
        title = title_entry.get()
        results = search_books(title)
        if results:
            result_text = "\n".join([f"ID: {r[0]}, Title: {r[1]}, Author: {r[2]}, Year: {r[3]}" for r in results])
            result_label.config(text=result_text)
        else:
            result_label.config(text="No books found.")

    search_btn = tk.Button(window, text="Search", command=search)
    search_btn.pack(pady=10)

if __name__ == "__main__":
    main_menu()

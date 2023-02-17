 
import sqlite3
from tkinter import *
from tkinter import messagebox

# Connect to the database
conn = sqlite3.connect('ebookstore.db')
c = conn.cursor()

# Create the books table if it does not exist
c.execute('''CREATE TABLE IF NOT EXISTS books
             (id INTEGER PRIMARY KEY,
              title TEXT,
              author TEXT,
              quantity INTEGER)''')

# Define the functions for the bookstore clerk program

# Create function add_book - It requests the user for the book information.
def add_book():
    id = id_entry.get()
    title = title_entry.get()
    author = author_entry.get()
    quantity = quantity_entry.get()

    if id and title and author and quantity:
        # Insert the book information into the database
        c.execute("INSERT INTO books (id, title, author, quantity) VALUES (?, ?, ?, ?)",
                  (id, title, author, quantity))
        conn.commit()

        # Clear the entry fields
        id_entry.delete(0, END)
        title_entry.delete(0, END)
        author_entry.delete(0, END)
        quantity_entry.delete(0, END)

        # Show a message box to confirm the book was added
        messagebox.showinfo("Book Added", "The book has been added to the database.")
    else:
        messagebox.showerror("Missing Information", "Please fill in all fields.")

def update_book():
    # Get the book information from the user
    id = id_entry.get()
    title = title_entry.get()
    author = author_entry.get()
    quantity = quantity_entry.get()

    if id or title or author or quantity:
        # Update the book information in the database
        c.execute("UPDATE books SET title=?, author=?, quantity=? WHERE id=?",
                  (title, author, quantity, id))
        conn.commit()

        # Clear the entry fields
        id_entry.delete(0, END)
        title_entry.delete(0, END)
        author_entry.delete(0, END)
        quantity_entry.delete(0, END)

        # Show a message box to confirm the book was updated
        messagebox.showinfo("Book Updated", "The book has been updated in the database.")
    else:
        messagebox.showerror("Missing Information", "Please fill in at least one field.")

def delete_book():
    # Get the book ID from the user
    id = id_entry.get()

    if id:
        # Delete the book from the database
        c.execute("DELETE FROM books WHERE id=?", (id,))
        conn.commit()

        # Clear the entry fields
        id_entry.delete(0, END)
        title_entry.delete(0, END)
        author_entry.delete(0, END)
        quantity_entry.delete(0, END)

        # Show a message box to confirm the book was deleted
        messagebox.showinfo("Book Deleted", "The book has been deleted from the database.")
    else:
        messagebox.showerror("Missing Information", "Please fill in the ID field.")

def search_book():
    # Get the search string from the user
    search = search_entry.get()

    if search:
        # Search the database for books that match the search string
        c.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
                  ('%' + search + '%', '%' + search + '%'))
        books = c.fetchall()

        # Clear the listbox and insert the search results
        search_results.delete(0, END)
        for book in books:
            search_results.insert(END, book)
    else:
        messagebox.showerror("Missing Information", "Please fill in the search field.")

# Create the GUI for the bookstore clerk program
root = Tk()
root.geometry("400x500")
root.title("Bookstore Clerk")


# Create the labels and entry fields for the book information
id_label = Label(root, text="ID:")
id_label.grid(row=0, column=0)
id_entry = Entry(root)
id_entry.grid(row=0, column=1)

title_label = Label(root, text="Title:")
title_label.grid(row=1, column=0)
title_entry = Entry(root)
title_entry.grid(row=1, column=1)

author_label = Label(root, text="Author:")
author_label.grid(row=2, column=0)
author_entry = Entry(root)
author_entry.grid(row=2, column=1)

quantity_label = Label(root, text="Quantity:")
quantity_label.grid(row=3, column=0)
quantity_entry = Entry(root)
quantity_entry.grid(row=3, column=1)

# Create the buttons for adding, updating, deleting books and searching books
add_button = Button(root, text="Add Book", command=add_book)
add_button.grid(row=5, column=0)

update_button = Button(root, text="Update Book", command=update_book)
update_button.grid(row=5, column=1)

delete_button = Button(root, text="Delete Book", command=delete_book)
delete_button.grid(row=5, column=2)

search_button = Button(root, text="Search", command=search_book)
search_button.grid(row=5, column=3)

# Create the labels and entry field for searching books
search_label = Label(root, text="Search:")
search_label.grid(row=8, column=0)
search_entry = Entry(root)
search_entry.grid(row=8, column=1)

# Create the listbox for displaying search results
search_result_label = Label(root, text="Results:")
search_result_label.grid(row=9, column=1)
search_results = Listbox(root)
search_results.config(width=50, height=20)
search_results.grid(row=10, column=0, columnspan=3,)

# Run the GUI
root.mainloop()

# Close the database connection
conn.close()
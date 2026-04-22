import tkinter as tk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    course TEXT
)
""")
conn.commit()

def add_student():
    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()

    if name and age and course:
        cursor.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)",(name, age, course))
        conn.commit()
        messagebox.showinfo("Success", "Student Added")
        clear_fields()
        view_students()
    else:
        messagebox.showwarning("Error", "Fill all fields")

def view_students():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        listbox.insert(tk.END, row)

def delete_student():
    try:
        selected = listbox.get(listbox.curselection())
        cursor.execute("DELETE FROM students WHERE id=?", (selected[0],))
        conn.commit()
        view_students()
    except:
        messagebox.showwarning("Error", "Select a student")

def update_student():
    try:
        selected = listbox.get(listbox.curselection())
        cursor.execute("""UPDATE students SET name=?, age=?, course=? WHERE id=?""", (name_entry.get(), age_entry.get(), course_entry.get(), selected[0]))
        conn.commit()
        view_students()
    except:
        messagebox.showwarning("Error", "Select a student")

def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Student Management System")
root.geometry("500x500")
root.configure(bg="lightblue")

tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Age").pack()
age_entry = tk.Entry(root)
age_entry.pack()

tk.Label(root, text="Course").pack()
course_entry = tk.Entry(root)
course_entry.pack()

tk.Button(root, text="Add Student", command=add_student).pack(pady=5)
tk.Button(root, text="Update Student", command=update_student).pack(pady=5)
tk.Button(root, text="Delete Student", command=delete_student).pack(pady=5)
tk.Button(root, text="View Students", command=view_students).pack(pady=5)
tk.Button(root, text="Clear Fields", command=clear_fields).pack(pady=5)

listbox = tk.Listbox(root, width=50)
listbox.pack(pady=20)

root.mainloop()

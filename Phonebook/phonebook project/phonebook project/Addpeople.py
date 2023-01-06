from tkinter import *
from tkinter import messagebox
import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()


class addpeople(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        self.geometry("650x550+600+200")
        self.title("My People")
        self.resizable(False, False)
        # Frame

        self.top = Frame(self, height=150, background='white')
        self.top.pack(fill=X)

        self.bottom = Frame(self, height=500, background='#34baeb')
        self.bottom.pack(fill=X)

        # top Frame Desing
        self.top_image = PhotoImage(file='C:\\Users\\HP\\Downloads\\phonebook.png')
        self.top_image_label = Label(self.top, image=self.top_image, background='white')
        self.top_image_label.place(x=90, y=10)

        self.heading = Label(self.top, text='Add New Person', font='arial 15 bold', background='white',
                             foreground='blue')
        self.heading.place(x=230, y=60)

        # Name
        self.label_name = Label(self.bottom, text='NAME', font='arial 12 bold', fg='white', bg='#fcc324')
        self.label_name.place(x=40, y=40)

        self.entry_name = Entry(self.bottom, width=30, bd=4)
        self.entry_name.insert(0, "Enter Name")
        self.entry_name.place(x=150, y=40)

        # surname
        self.label_surname = Label(self.bottom, text='SURNAME', font='arial 12 bold', fg='white', bg='#fcc324')
        self.label_surname.place(x=40, y=80)

        self.entry_surname = Entry(self.bottom, width=30, bd=4)
        self.entry_surname.insert(0, "Enter surname")
        self.entry_surname.place(x=150, y=80)

        # email
        self.label_email = Label(self.bottom, text='EMAIL', font='arial 12 bold', fg='white', bg='#fcc324')
        self.label_email.place(x=40, y=120)

        self.entry_email = Entry(self.bottom, width=30, bd=4)
        self.entry_email.insert(0, "Enter Email")
        self.entry_email.place(x=150, y=120)

        # Mobile Number
        self.label_number = Label(self.bottom, text='NUMBER', font='arial 12 bold', fg='white', bg='#fcc324')
        self.label_number.place(x=40, y=160)

        self.entry_number = Entry(self.bottom, width=30, bd=4)
        self.entry_number.insert(0, "Enter mobile number")
        self.entry_number.place(x=150, y=160)

        # address
        self.label_address = Label(self.bottom, text='ADDRESS', font='arial 12 bold', fg='white', bg='#fcc324')
        self.label_address.place(x=40, y=200)

        self.entry_address = Text(self.bottom, width=30, height=7)
        self.entry_address.place(x=150, y=200)

        # button
        btn = Button(self.bottom, text="ADD PERSON", width=12, command=self.add_people)
        btn.place(x=250, y=350)

    def add_people(self):
        name = self.entry_name.get()
        surname = self.entry_surname.get()
        email = self.entry_email.get()
        number = self.entry_number.get()
        address = self.entry_address.get(1.0, 'end-1c')

        # COnnecting to Database

        if name and surname and email and number and address != "":
            try:
                # add to the database
                # insert into phonebook (person_name,person_surname, person_email, person_number, person_address)
                query = "insert into 'addressbook' (person_name,person_surname, person_email, person_number, person_address) values (?,?,?,?,?)"
                cur.execute(query, (name, surname, email, number, address))
                con.commit()
                messagebox.showinfo("Success", "contact added")
                self.destroy()

            except EXCEPTION as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Fill all fields", icon='warning')

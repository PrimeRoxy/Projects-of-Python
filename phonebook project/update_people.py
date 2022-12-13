from tkinter import *
from tkinter import messagebox
import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()

class Update_people(Toplevel):
    def __init__(self, person_id):
        Toplevel.__init__(self)

        self.geometry("650x650+600+200")
        self.title("Update Person")
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

        self.heading = Label(self.top, text='Update person profile', font='arial 15 bold', background='white',
                             foreground='blue')
        self.heading.place(x=230, y=60)

        # fetching data from database through persion id

        query = "select * from addressbook where person_id = '{}'".format(person_id)
        result = cur.execute(query).fetchone()
        print(result)
        self.person_id = person_id
        person_name = result[1]
        person_surname = result[2]
        person_email = result[3]
        person_number = result[4]
        person_address = result[5]

        # Name
        self.label_name = Label(self.bottom, text='NAME', font='arial 12 bold', fg='white', bg='#fcc324')
        self.label_name.place(x=40, y=40)

        self.entry_name = Entry(self.bottom, width=30, bd=4)
        self.entry_name.insert(0, person_name)
        self.entry_name.place(x=150, y=40)

        # surname
        self.label_surname = Label(self.bottom, text='SURNAME', font='arial 12 bold', fg='white', bg='#fcc324')
        self.label_surname.place(x=40, y=80)

        self.entry_surname = Entry(self.bottom, width=30, bd=4)
        self.entry_surname.insert(0, person_surname)
        self.entry_surname.place(x=150, y=80)

        # email
        self.label_email = Label(self.bottom, text='EMAIL', font='arial 12 bold', fg='white', bg='#fcc324')
        self.label_email.place(x=40, y=120)

        self.entry_email = Entry(self.bottom, width=30, bd=4)
        self.entry_email.insert(0, person_email)
        self.entry_email.place(x=150, y=120)

        # Mobile Number
        self.label_number = Label(self.bottom, text='NUMBER', font='arial 12 bold', fg='white', bg='#fcc324')
        self.label_number.place(x=40, y=160)

        self.entry_number = Entry(self.bottom, width=30, bd=4)
        self.entry_number.insert(0, person_number)
        self.entry_number.place(x=150, y=160)

        # address
        self.label_address = Label(self.bottom, text='ADDRESS', font='arial 12 bold', fg='white', bg='#fcc324')
        self.label_address.place(x=40, y=200)

        self.entry_address = Text(self.bottom, width=30, height=7)
        self.entry_address.insert(1.0, person_address)
        self.entry_address.place(x=150, y=200)

        # button
        btn = Button(self.bottom, text="UPDATE", width=12, command=self.update_profile)
        btn.place(x=250, y=350)

    def update_profile(self):
        Id = self.person_id
        name = self.entry_name.get()
        surname = self.entry_surname.get()
        email = self.entry_email.get()
        number = self.entry_number.get()
        address = self.entry_address.get(1.0, 'end-1c')
        query = "update addressbook set person_name = '{}', person_surname = '{}', person_email = '{}', person_number = {}, person_address = '{}' where person_id = {}".format(name, surname, email, number, address, Id)
        try:
            cur.execute(query)
            con.commit()
            messagebox.showinfo("success", "contact updated")

        except EXCEPTION as e:

            print(e)


from tkinter import *
from Addpeople import addpeople, cur
from update_people import Update_people
from display_people import Display
from tkinter import messagebox
import sqlite3

con = sqlite3.connect('Database.db')
quary = con.cursor()

class MyPeople(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        self.geometry("650x550+600+200")
        self.title("My People")
        self.resizable(False,False)
        #Frame

        self.top = Frame(self, height=150, background='white')
        self.top.pack(fill=X)

        self.bottom = Frame(self, height=450, background='orange')
        self.bottom.pack(fill=X)

        # top Frame Design
        self.top_image = PhotoImage(file='C:\\Users\\HP\\Downloads\\phonebook.png')
        self.top_image_label = Label(self.top, image=self.top_image, background='white')
        self.top_image_label.place(x=90, y=10)

        self.heading = Label(self.top, text='My People', font='arial 15 bold', background='white',
                             foreground='blue')
        self.heading.place(x=230, y=60)

        # LIST & SCROLLBAR
        self.scroll = Scrollbar(self.bottom, orient=VERTICAL)
        self.listbox = Listbox(self.bottom, width=40, height=25)
        self.listbox.grid(row=0, column=0, padx=(20,0))
        self.scroll.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scroll.set)

        persons = cur.execute("select * from 'addressbook'").fetchall()
        print(persons)
        count = 0
        for person in persons:
            self.listbox.insert(count, str(person[0]) + ". "+person[1] + " "+person[2])
            count += 1
        self.scroll.grid(row=0, column=1, sticky=N+S)

        #Buttons
        buttonadd =Button(self.bottom, text="Add", width=12, font='Sans 12 bold', command=self.add_people)
        buttonadd.grid(row=0, column=2, padx=20, pady=10, sticky=N)

        buttonupdate = Button(self.bottom, text="Update", width=12, font='Sans 12 bold', command=self.update_people)
        buttonupdate.grid(row=0, column=2, padx=20, pady=50, sticky=N)

        buttonDisplay = Button(self.bottom, text="Display", width=12, font='Sans 12 bold', command=self.display_detail)
        buttonDisplay.grid(row=0, column=2, padx=20, pady=90, sticky=N)

        buttonDelete = Button(self.bottom, text="Delete", width=12, font='Sans 12 bold', command=self.delete_person)
        buttonDelete.grid(row=0, column=2, padx=20, pady=130, sticky=N)

    def add_people(self):
        add_page = addpeople()
        self.destroy()
    def update_people(self):
        selected_items = self.listbox.curselection()
        person = self.listbox.get(selected_items)
        person_id = person.split(".")[0]

        updatepage = Update_people(person_id)

    def display_detail(self):
        selected_items = self.listbox.curselection()
        person = self.listbox.get(selected_items)
        person_id = person.split(".")[0]

        displaypage = Display(person_id)

    def delete_person(self):
        selected_items = self.listbox.curselection()
        person = self.listbox.get(selected_items)
        person_id = person.split(".")[0]

        query = "delete from addressbook where person_id = {}".format(person_id)
        warning = messagebox.askquestion("Warning", "Are you sure to delete ?")
        if warning == 'yes':
            try:
                cur.execute(query)
                con.commit()
                messagebox.showinfo("Success", "Deleted")
                self.destroy()
            except EXCEPTION as e:
                messagebox.showinfo("Info", str(e))

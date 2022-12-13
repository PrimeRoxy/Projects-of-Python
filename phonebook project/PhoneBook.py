from tkinter import *
import datetime
from mypeople import MyPeople
from Addpeople import addpeople
from about import About
date = datetime.datetime.now().date()
date = str(date)


class Application(object):
    def __init__(self, master):
        self.master = master

        # frames

        self.top = Frame(master, height=200, background='white')
        self.top.pack(fill=X)

        self.bottom = Frame(master, height=450, background='blue')
        self.bottom.pack(fill=X)

        # top Frame Desing
        self.top_image = PhotoImage(file='C:\\Users\\HP\\Downloads\\phonebook.png')
        self.top_image_label = Label(self.top, image=self.top_image, background='white')
        self.top_image_label.place(x=90, y=10)

        self.heading = Label(self.top, text='My Phonebook App', font='arial 15 bold', background='white',
                             foreground='red')
        self.heading.place(x=230, y=60)

        # date
        self.date_label = Label(self.top, text="Today's Date:" + date, font='arial 12 bold', fg='black', bg='white')
        self.date_label.place(x=450, y=170)

        # button 1 - View people
        self.veiw_button = Button(self.bottom, text="My People", font='arial 10 bold', width=12, command=self.my_people)
        self.veiw_button.place(x=250, y=70)

        # button 2 - Add people
        self.add_button = Button(self.bottom, text="Add People", font='arial 10 bold', width=12,
                                 command=self.addpeoplefunction)
        self.add_button.place(x=250, y=130)

        # button 3 - About us
        self.about = Button(self.bottom, text='About Us', font='arial 10 bold', width=13, command=self.aboutus)
        self.about.place(x=250, y=190)

    # importing mypeople code for working my people button
    def my_people(self):
        people = MyPeople()

    # importing add people code for working add people button
    def addpeoplefunction(self):
        addpeoplewindow = addpeople()

    def aboutus(self):
        aboutpage = About()

def main():
    root = Tk()
    app = Application(root)
    root.title("PhoneBook")
    root.geometry("650x650+500+200")
    root.resizable(False, False)
    root.mainloop()


if __name__ == '__main__':
    main()

from tkinter import *


class About(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)

        self.geometry("550x550+550+200")
        self.title("About Us")
        self.resizable(False, False)
        self.top = Frame(self, height=550, width=550, bg="orange")
        self.top.pack(fill=BOTH)

        self.text = Label(self.top, text='WELCOME' 
                                         '\n'
                          '\n This page is about us.'
                          '\n This application is just simple project'
                          '\n Phonebook appliction is coded in python language'
                          '\n This application is made for educational purpose'
                           '\n'              
                          '\n You can contact us on:'
                                         '\n'
                          '\n Email : vipuldashingboy@gmail.com'
                                         
                          '\n Instagram : https://www.instagram.com/ismartvipul/'
                          '\n'
                          '\n LinkdenIn : https://www.linkedin.com/in/ismart-vipulray'
                                         '\n'
                          '\n Thanks for using mine application', font= "arial 13 bold", bg= "orange", fg='white')
        self.text.place(x =60, y=60)
from tkinter import *
import smtplib
import re

class EmailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Application")

        self.server = None
        self.username = None
        self.password = None

        self.create_widgets()
        self.hide_login_label()

    def create_widgets(self):
        self.f1 = Frame(self.root, width=1000, height=800)
        self.f1.pack(side=TOP)

        Label(self.f1, width=25, text="Enter your Credentials", font=("calibri 18 bold")).grid(row=0, columnspan=3, pady=10, padx=10)
        Label(self.f1, text="Email").grid(row=1, sticky=E, pady=5, padx=10)
        Label(self.f1, text="Password").grid(row=2, sticky=E, pady=5, padx=10)

        self.entry1 = Entry(self.f1)
        self.entry2 = Entry(self.f1, show="*")

        self.entry1.grid(row=1, column=1, pady=5)
        self.entry2.grid(row=2, column=1)

        btn1 = Button(self.f1, text="Login", width=10, bg="black", fg="white", command=self.login)
        btn1.grid(row=3, columnspan=3, pady=10)

        self.f2 = Frame(self.root)
        self.f2.pack(side=TOP, expand=NO, fill=NONE)

        self.label4 = Message(self.f2, width=400, bg="cyan", fg="red", font=("Calibri 12 bold"), aspect=400)
        self.label4.grid(row=0, column=0, columnspan=2, pady=5)

        btn2 = Button(self.f2, text="Logout", bg="black", fg="white", command=self.logout)
        btn2.grid(row=0, column=4, sticky=E, pady=10, padx=(5, 0))

        self.f3 = Frame(master=self.root)
        self.f3.pack(side=TOP, expand=NO, fill=NONE)

        Label(self.f3, width=20, text="Compose Email", font=("Calibri 18 bold")).grid(row=0, columnspan=3, pady=10)
        Label(self.f3, text="To").grid(row=1, sticky=E, pady=5)
        Label(self.f3, text="Subject").grid(row=2, sticky=E, pady=5)
        Label(self.f3, text="Message").grid(row=3, sticky=E)

        self.entry3 = Entry(self.f3)
        self.entry4 = Entry(self.f3)
        self.entry5 = Entry(self.f3)

        self.entry3.grid(row=1, column=1, pady=5)
        self.entry4.grid(row=2, column=1, pady=5)
        self.entry5.grid(row=3, column=1, pady=5, rowspan=3, ipady=10)

        btn3 = Button(self.f3, text="Send Mail", width=10, bg="black", fg="white", command=self.send_mail)
        btn3.grid(row=6, columnspan=3, pady=10)

        self.label9 = Label(self.f3, width=20, fg="white", bg="black", font=("Calibri 18 bold"))
        self.label9.grid(row=7, columnspan=3, pady=5)

    def login(self):
        if self.validate_login():
            self.username = self.entry1.get()
            self.password = self.entry2.get()  # Ensure this is the app-specific password
            try:
                self.server = smtplib.SMTP("smtp.gmail.com:587")
                self.server.ehlo()
                self.server.starttls()
                self.server.login(self.username, self.password)
                self.f2.pack()
                self.label4["text"] = "Logged In!"
                self.f1.pack_forget()
                self.f3.pack()
                self.label9.grid_remove()
            except Exception as e:
                self.label4["text"] = f"Error: {e}"
                self.f2.pack()

    def hide_login_label(self):
        self.f2.pack_forget()
        self.f3.pack_forget()

    def send_mail(self):
        if self.validate_message():
            self.label9.grid_remove()
            receiver = self.entry3.get()
            subject = self.entry4.get()
            msgbody = self.entry5.get()
            msg = f"From: {self.username}\nTo: {receiver}\nSubject: {subject}\n\n{msgbody}"
            try:
                self.server.sendmail(self.username, receiver, msg)
                self.label9.grid()
                self.label9["text"] = "Mail Sent!"
                self.root.after(3000, self.reset_form)  # Hide message and reset form after 3 seconds
            except Exception as e:
                self.label9.grid()
                self.label9["text"] = f"Error: {e}"

    def reset_form(self):
        self.entry3.delete(0, END)
        self.entry4.delete(0, END)
        self.entry5.delete(0, END)
        self.label9.grid_remove()

    def logout(self):
        try:
            self.server.quit()
            self.f3.pack_forget()
            self.f2.pack()
            self.label4["text"] = "Logged Out Successfully"
            self.f1.pack()
            self.entry2.delete(0, END)
        except Exception as e:
            self.label4["text"] = f"Error: {e}"

    def validate_login(self):
        email_text = self.entry1.get()
        pass_text = self.entry2.get()
        if not email_text or not pass_text:
            self.label4["text"] = "Fill all the Fields"
            self.f2.pack()
            return False
        else:
            EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
            if not EMAIL_REGEX.match(email_text):
                self.label4["text"] = "Enter a valid Email Address"
                self.f2.pack()
                return False
            else:
                return True

    def validate_message(self):
        email_text = self.entry3.get()
        sub_text = self.entry4.get()
        msg_text = self.entry5.get()

        if not email_text or not sub_text or not msg_text:
            self.label9["text"] = "Fill in all the Fields"
            self.label9.grid()
            return False
        else:
            EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
            if not EMAIL_REGEX.match(email_text):
                self.label9["text"] = "Enter a Valid Email Address"
                self.label9.grid()
                return False
            elif len(sub_text) < 3 or len(msg_text) < 3:
                self.label9["text"] = "Enter at least 3 Characters"
                self.label9.grid()
                return False
            else:
                return True

root = Tk()
app = EmailApp(root)
root.mainloop()
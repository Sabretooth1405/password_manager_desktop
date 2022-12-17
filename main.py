import json
from tkinter import *
from tkinter import font
from tkinter import messagebox
from click import command
from pygments import highlight
from tkmacosx import Button as bt
from password_generator import PasswordGenerator
import pyperclip

window = Tk()
window.config(padx=20, bg='white')
window.minsize(height=400, width=400)
window.title('Password Manager')

canvas = Canvas(width=200, height=200, bg='white', highlightthickness=0)
logo_img = PhotoImage(
    file="./logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1, padx=20, pady=20)

website_label = Label(text='Website', font=('Arial', 18), bg='white', padx=10)
website_label.grid(row=1, column=0)

website_entry = Entry(bg='white', highlightthickness=0)
website_entry.grid(row=1, column=1, columnspan=1, sticky='ew')
website_entry.focus()

def search_website():
    try:
        a = pass_dict[website_entry.get()]
        messagebox.showinfo(title=website_entry.get(),
                            message=f'Username: {a[0]}\nPassword: {a[1]}')
    except KeyError:
        messagebox.showerror(title=website_entry.get(),message=f'Sorry but the website: {website_entry.get()} does not exist in our database')

search_btn = bt(text='Search', font=('Arial', 12),
                bg="#0E7AFE", highlightthickness=0, bd=0,command=search_website)
search_btn.grid(row=1, column=2, padx=10)
username_label = Label(text='Username/Email',
                       font=('Arial', 18), bg='white', padx=10)
username_label.grid(row=2, column=0)

username_entry = Entry(bg='white', highlightthickness=0)
username_entry.grid(row=2, column=1, columnspan=2, sticky='ew')
username_entry.insert(0,'sabretooth1405@gmail.com')


password_label = Label(text='Password', font=(
    'Arial', 18), bg='white', padx=10)
password_label.grid(row=3, column=0)

password_entry = Entry(bg='white', highlightthickness=0)
password_entry.grid(row=3, column=1, columnspan=1, sticky='ew')
with open('pass_dict.json', 'r') as pd:
    pass_dict = json.load(pd)


def update_json():
    pass_dict[website_entry.get()] = [username_entry.get(),
                                      password_entry.get()]
    with open('pass_dict.json', 'w')as pd:
        json.dump(pass_dict, pd,indent=4)


def generate_passwd():
    pwo = PasswordGenerator()
    pwo.minlen = 12
    pwo.maxlen = 16
    pwo.minuchars = 2
    pwo.minlchars = 3
    pwo.minnumbers = 1
    pwo.minschars = 1
    pass_str = pwo.generate()
    pyperclip.copy(pass_str)
    password_entry.delete(0, END)
    password_entry.insert(0, pass_str)


    # print(pass_str)
    #password_entry.insert(0, pass_str)
passwort_btn = Button(text='Generate Password', bg='White',
                      font=('Arial', 12), highlightthickness=0, bd=0, command=generate_passwd)
passwort_btn.grid(row=3, column=2, padx=10)


def popup_empty(fields):
    if fields['w'] == '':
        website_entry.config(highlightcolor='red',
                             highlightthickness=2, highlightbackground='red')
    if fields['u'] == '':
        username_entry.config(highlightcolor='red',
                              highlightthickness=2, highlightbackground='red')
    if fields['p'] == '':
        password_entry.config(highlightcolor='red',
                              highlightthickness=2, highlightbackground='red')
    messagebox.showerror(
        title='Empty Fields', message='Seems Like you left some fields empty.Please go back and check')


def save_passwd():
    pass_str = f'WEBSITE: {website_entry.get()} | Username/Email:{username_entry.get()} | Password: {password_entry.get()}'
    with open('my_pass.txt', 'a+') as mp:
        mp.write(pass_str+'\n')
    update_json()
    website_entry.delete(0,END)
    password_entry.delete(0,END)
    username_entry.delete(0,END)


def popup_ok():
    win = Toplevel()
    win.wm_title("Verify Command")

    l = Label(
        win, text=f"Do you want to save the Username and Password of the website {website_entry.get()} in file my_pass.txt")
    l.grid(row=0, column=0)

    b = bt(win, text="Okay", command=lambda: [
           win.destroy(), save_passwd()], highlightthickness=0, bd=0, bg='#0E7AFE', font=('Arial', 12))
    c = bt(win, text="Close", command=lambda: [
           win.destroy()], highlightthickness=0, bd=0, bg='#0E7AFE', font=('Arial', 12))

    b.grid(row=1, column=2, pady=10)
    c.grid(row=1, column=3, pady=10)


def add_check():

    if website_entry.get() == '' or username_entry.get() == '' or password_entry.get() == '':
        fields = {'w': website_entry.get(), 'u': username_entry.get(),
                  'p': password_entry.get()}
        popup_empty(fields)
    else:
        popup_ok()


add_btn = bt(text='Add', bg='#0E7AFE', font=(
    'Arial', 12), highlightthickness=0, bd=0, command=add_check)
add_btn.grid(row=4, column=1, columnspan=2, sticky='ew')


window.mainloop()

import random
from tkinter import *
from random import choice, randint
from tkinter import messagebox
import pyperclip
import json


numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z']
cap_letter = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
symbols = ['@', '#', '$', '%', '&', '?', '!']

for i in letters:
    cap_letter.append(i.upper())

def generate_pass():
    num_len = randint(2, 4)
    symbols_len = randint(1, 3)
    letters_len = randint(6, 8)
    cap_letter_len = randint(1, 2)
    final_password = ""

    password.delete(0, END)

    password_l = [choice(numbers) for i in range(0, num_len)]
    password_li = [choice(symbols) for i in range(0, symbols_len)]
    password_lis = [choice(letters) for i in range(0, letters_len)]
    password_list = [choice(cap_letter) for i in range(0, cap_letter_len)]

    final_list = password_l + password_li + password_lis + password_list
    print(final_list)
    random.shuffle(final_list)
    final_password = final_password.join(final_list)
    print(final_password)
    password.insert(0, final_password)
    pyperclip.copy(final_password)


def add_to_file():
    data = {
        website.get() : {
            "email" : email.get(),
            "password" : password.get()
        }
    }
    if website.get() != "" and email.get() != "" and password.get() != "":
        msg = messagebox.askyesno(title="Confirm",
                                  message="Click 'Yes' to add the below details :"f" \nWebsite : {website.get()} \n Email : {email.get()} \n Password : {password.get()}")
        print(msg)
        if msg is True:
            with open("password_data.text", "a") as pass_write:
                pass_write.write(f"\n{website.get()} | {email.get()} | {password.get()}")
            try:
                with open("password_data.json","r") as json_read:
                    json_data = json.load(json_read)
                    json_data.update(data)

            except FileNotFoundError as error:
                print(error)
                with open("password_data.json","w") as json_write:
                    json.dump(data,json_write,indent=4)

            else:
                with open("password_data.json","w") as json_write:
                    json.dump(json_data,json_write,indent=4)
            finally:
                website.delete(0, END)
                password.delete(0, END)
                print("Added")
    else:
        messagebox.showinfo(title="Error", message="Website or Email or Password is empty")


def search_json():
    try:
        with open("password_data.json","r") as read_json_data:
            json_dic_data = json.load(read_json_data)
    except FileNotFoundError as error:
        print(error)
        messagebox.showinfo(title="File Error", message="No file found")
    else:
        try:
            val = json_dic_data[website.get()]
        except KeyError as error:
            print(error)
            messagebox.showinfo(title="No websites", message="No websites found, Check for any other name")
        else:
            email.delete(0, END)
            password.delete(0, END)
            email.insert(0, val["email"])
            password.insert(0, val["password"])
            messagebox.showinfo(title=website.get(), message=f"Email: {val['email']} \nPassword: {val['password']}")


screen = Tk()
screen.minsize(600, 350)

pic = PhotoImage(file="logo.png")
canvas = Canvas(width=220, height=180, highlightthickness=0)
canvas.create_image(105, 95, image=pic, )
canvas.grid_configure(row=0, column=1, columnspan=2)

# label
websitel = Label(text="Website : ")
websitel.grid_configure(row=1, column=0)
emaill = Label(text="Email/Username : ", width=20)
emaill.grid_configure(row=2, column=0)
passl = Label(text="Password : ")
passl.grid_configure(row=3, column=0)

# input
website = Entry(width=36)
website.grid_configure(row=1, column=1)
website.focus()
search = Button(text="Search",width=15,command=search_json)
search.grid_configure(row=1, column=2, columnspan=2)
email = Entry(width=55)
email.insert(0, "aezhil005@gmail.com")
email.grid_configure(row=2, column=1, columnspan=2)
password = Entry(width=36)
password.grid_configure(row=3, column=1)

# button
generate_pass = Button(text="Generate Password", command=generate_pass)
generate_pass.grid_configure(row=3, column=2)
add = Button(text="Add", command=add_to_file, width=46)
add.grid_configure(row=4, column=1, columnspan=2)

screen.mainloop()

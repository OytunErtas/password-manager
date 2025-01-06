from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    password_entry.delete(0, END)

    letter_list = [choice(letters) for _ in range(randint(8, 10))]
    symbol_list = [choice(symbols) for _ in range(randint(2, 4))]
    number_list = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = letter_list + symbol_list + number_list
    shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, string=password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    # create data in json format
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title="Error", message="Please make sure that you haven't left any fields are empty.")
    else:
        answer = messagebox.askokcancel(title=website, message=f"These are the details entered:\n Email: {email} \n "
                                                               f"Password: {password} \n Is it ok to save?")
        if answer:
            with open("data.txt", "a") as file:
                file.write(f"{website} || {email} || {password} \n")
            website_entry.delete(0, END)
            password_entry.delete(0, END)

        try:
            with open("data.json", "r") as file:
                # Read old data
                data = json.load(file)

        except FileNotFoundError:
            with open("data.json", "w") as file:
                # Save updated data
                json.dump(new_data, file, indent=4)
        else:
            # Update old data
            data.update(new_data)
            with open("data.json", "w") as file:
                # Save updated data
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- SEARCH BUTTON FUNCTION ------------------------------- #


def find_password():
    key_website = website_entry.get()

    try:
        with open("data.json", "r") as file:
            data = json.load(file)
        email = data[key_website]["email"]
        password = data[key_website]["password"]
    except KeyError:
        messagebox.showerror(title="ERROR", message="No details for the website exists.")
    except FileNotFoundError:
        messagebox.showerror(title="ERROR", message="No Data File Found")
    else:
        messagebox.showinfo(title=key_website, message=f"Email: {email}\nPassword: {password}")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)


canvas = Canvas(width=190, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)


# Entries
website_entry = Entry(width=32)
website_entry.grid(column=1, row=1)
website_entry.focus()

email_entry = Entry(width=50)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "oytunertas.pl@gmail.com")

password_entry = Entry(width=32)
password_entry.grid(column=1, row=3)


# Buttons
add_button = Button(text="Add", width=42, command=save)
add_button.grid(column=1, row=4, columnspan=2)

gen_pass_button = Button(text="Generate Password", width=14, command=generate_password)
gen_pass_button.grid(column=2, row=3)

search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(column=2, row=1)


window.mainloop()

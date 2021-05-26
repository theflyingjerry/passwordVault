#!
#passWordSaver.py - GUI that securly saves passwords for future use

import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from pathlib import Path
import hashlib
import keyring
import pyperclip

#Function to check if entered code is correct

def CodeChecker():

    inputCode = codeEntry.get()
    accepted = False

    #TO-DO: 
        #Read hashed file from other program
        #Seperate key from salt
        #hash inputcode
        #check if it matches
    p = Path.cwd()
    hashFile = open(p/'hash.txt','rb')
    passHash = hashFile.read()
    salt = passHash[:32]
    hashedCode = passHash[32:]

    newHashCode = hashlib.pbkdf2_hmac('sha256', inputCode.encode('utf-8'), salt, 100000)

    

    if hashedCode == newHashCode:
        print('Code Accepted')
        accepted = True
    else:
        print('Code Denied')
        codeEntry.delete(0,tk.END)

    if accepted == True:
        titleLabel.configure(text = 'Password Vault')
        entryLabel.configure(text = 'Site Name:')
        codeEntry.grid_forget()
        codeGrid.rowconfigure([0,1,2], weight = 1)
        codeGrid.columnconfigure([0,1], weight = 1)
        submitButton.pack_forget()

        siteEnty.grid(row = 0, column = 1)
        userNameLabel.grid(row = 1, column = 0)
        userNameEnty.grid(row = 1, column = 1)
        passwordLabel.grid(row = 2, column = 0)
        passwordEnty.grid(row = 2, column = 1)
        saveButton.pack(anchor = "center", fill = "both")
        bigFrame.pack(anchor = "center", fill ="both", ipadx = 10)
        siteFrame.grid(row = 0, column = 0)
        usernameFrame.grid(row = 0, column = 1)
        passwordFrame.grid(row = 0, column = 2)
        
        siteTitLabel.pack(anchor = "center", fill ="both", ipadx = 5)
        usernameTitLabel.pack(anchor = "center", fill ="both", ipadx = 5)
        passwordTitLabel.pack(anchor = "center", fill ="both", ipadx = 5)
        readFunction()
        packLabelFunction()

        


def readFunction():
    global myPWLabels, myPWList
    #TO-DO:
        #read site username file
        #seperate by line
        #split by space
        #get password for each combo
        #add to dictionary

    siteUsernameFile = open(Path.cwd()/'suf.txt','r')
    siteUserNameText = siteUsernameFile.read()
    siteUserNameList = siteUserNameText.splitlines()

    for line in siteUserNameList:
        
        littleList = line.split('-')
       
        site = littleList[0]
        username = littleList[1]
        password = keyring.get_password(site, username)
        myPWList.append(password)

        myPWLabels.append([ttk.Label(master = siteFrame, text = site), ttk.Label(master = usernameFrame, text = username), ttk.Label(master = passwordFrame, text = password)])

def packLabelFunction():
    #TO-DO
        #Somehow set row for the grid to length dict + 1
        #make label for site, username, and password and grid in loop
    global myPWLabels

    for list in myPWLabels:
        for entry in list:
            entry.pack()
        
        list[2].bind('<Button-1>', lambda e: callback(e))

  

            

def saveFunction():

     #TO-DO
        #get entries
        #save password securly
        #add site and username to file
        #add new site username and password as labels in grid frame to gui
        #clear the entries

    global myPWLabels

    siteInput = siteEnty.get()
    usernameInput = userNameEnty.get()
    passwordInput = passwordEnty.get()

    keyring.set_password(siteInput, usernameInput, passwordInput)

    p = Path.cwd()
    siteUserNameFile = open(p/'suf.txt','a')
    siteUserNameFile.write(siteInput+'-'+usernameInput+'\n')
    siteUserNameFile.close()

    ttk.Label(master = siteFrame, text = siteInput).pack()
    ttk.Label(master = usernameFrame, text = usernameInput).pack()
    label3 = ttk.Label(master = passwordFrame, text = passwordInput)
    label3.pack()
    label3.bind('<Button-1>', lambda e: callback(e))
    
    

    siteEnty.delete(0,tk.END)
    userNameEnty.delete(0,tk.END)
    passwordEnty.delete(0,tk.END)

def callback(event):
    global myPWList
    
    pyperclip.copy(event.widget.cget("text"))
    

#First Page Window


myPWLabels = []
myPWList = []
 
window = ThemedTk(theme='yaru')
window.title('Password Vault')

titleLabel = ttk.Label(master = window, text = "Input Entry Code", style = "title.TLabel")

codeGrid = ttk.Frame(master = window)
codeGrid.rowconfigure(0, weight = 1)
codeGrid.columnconfigure([0,1], weight =1)

entryLabel = ttk.Label(master= codeGrid, text = "Code:", style = "text.TLabel")
codeEntry = ttk.Entry(master = codeGrid, show = "*")

submitButton = ttk.Button(master = window, text = 'Sumbit',command = CodeChecker)

styleTitleLabel = ttk.Style().configure("title.TLabel",anchor = tk.CENTER, font = 'monospace 18')
styleTextLabel = ttk.Style().configure("text.TLabel",anchor = tk.CENTER, font = 'helvitica 12 bold')


#Second Page window objects

siteEnty = ttk.Entry(master = codeGrid)
userNameLabel = ttk.Label(master = codeGrid, text = "Username:", style = "text.TLabel")
userNameEnty = ttk.Entry(master = codeGrid)
passwordLabel = ttk.Label(master = codeGrid, text = "Password:", style = "text.TLabel")
passwordEnty = ttk.Entry(master = codeGrid)
saveButton = ttk.Button(master = window, text = "Save", command = saveFunction)

bigFrame = ttk.Frame(master = window)
bigFrame.columnconfigure([0,1,2],weight = 1)
bigFrame.rowconfigure(0, weight = 1)

siteFrame = ttk.Frame(master = bigFrame)
usernameFrame = ttk.Frame(master = bigFrame)
passwordFrame = ttk.Frame(master = bigFrame)


usernameTitLabel = ttk.Label(master = siteFrame, text = "Site",style = "text.TLabel")
passwordTitLabel = ttk.Label(master = usernameFrame, text = "Username",style = "text.TLabel")
siteTitLabel = ttk.Label(master = passwordFrame, text = "Password",style = "text.TLabel")


titleLabel.pack(anchor = "center", fill = "both")
codeGrid.pack(anchor = "center", fill = "both")
entryLabel.grid(row = 0, column = 0)
codeEntry.grid(row = 0, column = 1, padx= 2)
submitButton.pack(anchor = "center", fill = "both")



window.mainloop()
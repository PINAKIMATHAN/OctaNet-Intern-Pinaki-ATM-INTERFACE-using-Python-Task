import os
import time
import random

from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

from BankAtm import *
from Admin import *
from Design import *

rnd = [i for i in range(1000,5000+1) if i%100 == 0]
master = Tk()

class Bank(Frame):        
    def __init__(self,master = None):
        self.main()
        self.chances = 4

    def main(self):
        mainDesign(master,self)
        mainMenu(master,self)
        
        Label(self,text = "WELCOME TO PSM ATM OUTLET",fg = "#ffa500",
              relief = RAISED,bg = "#141a5c",borderwidth = 10,height = 2,padx = 3,pady = 3,
              width = 46,font = ("arial", "15", "bold")).grid()
        
        Button(self,text = "Click To Enter As *Admin*",bg = "#048db3",fg = "#012630",width = 40,font = ("arial", "15", "bold"),
               height = 2,command = self.AdminStart,activeforeground = "red").grid(sticky = W+S,pady = 10,padx = 5)
        
        Button(self,text = "Click To Enter As *User*",bg = "#048db3",fg = "#012630",width = 40,font = ("arial", "15", "bold"),
               height = 2,command = self.UserStart,activeforeground = "red").grid(sticky = W+S,padx = 5)


    def UserStart(self):
        
        def toggle():
            self.e.configure(show = "") if self.cVar.get() == 1 else self.e.configure(show = "*")
                
        userDesign(master,self)
        mainMenu(master,self)
        
        if self.chances>0:
            if self.chances == 1:
                messagebox.showinfo("log-in trial","Last log-in trial....")
            if self.chances == 2:
                messagebox.showinfo("log-in trial","Only 2 more log-in trials allowed....")

            self.name = StringVar()
            self.pin = StringVar()
            
            Label(self,text = "ACCOUNT NAME :",fg = "#6f569c",bg = "#c0c5fc",width = 20, font = ("arial", "10", "bold"), 
                  justify = LEFT).grid(sticky = E+S+N+W,pady = 10,padx = 5)
            self.e1 = Entry(self,bg = "#048db3",fg = "white",width = 30,textvariable = self.name, font = ("arial", "10"),
                  exportselection = 0)
            self.e1.grid(row = 1,column = 1,sticky = W+N+S+E,pady = 10,padx = 5)
            
            Label(self,text = "ACCOUNT NUMBER :",fg = "#6f569c",bg = "#c0c5fc",width = 20, font = ("arial", "10", "bold"),
                  justify = LEFT).grid(sticky = E+S+N+W,padx = 5)
            self.e = Entry(self,bg = "#048db3",fg = "white",width = 30,textvariable = self.pin, font = ("arial", "10"),
                  exportselection = 0,show = "*")
            self.e.grid(row = 2,column = 1,sticky = W+N+S+E,padx = 5)

            self.cVar = IntVar()
            Checkbutton(self,text = "Show Password",variable = self.cVar,command = toggle,bg = "#c0c5fc",
                        activebackground = "blue").grid(sticky = N+W+S+E,column = 1)
            
            Button(self,text = "Log-In",bg = "#66c9fa",fg = "#023b57",width = 10,height = 2,font = ("arial", "10", "bold"),
               activeforeground = "red",command = self.NameCheck).grid()

        else:
            pin = random.choice(rnd) 
            acct = BankAcct.ResetPin(self.name.get(),pin)
            if acct:
                messagebox.showinfo("CHANGED","Your Pin Has Been Changed Automatically\
                                \nDue To Failure To Provide Correct Pin\nExiting Now ...")
                self.master.quit()
            else:
                messagebox.showinfo("EXIT","Exiting Now...")
                self.master.quit()
                 
    def NameCheck(self):
         name = self.name.get()
         name = name.lower()
         acct = BankAcct.CheckName(name)
         
         if acct:
             result = self.CheckPin() 
             if result:
                 if self.k == 1234:
                     self.ChangePin()
                 else:
                     self.UserOption()
             else:
                 self.chances -= 1
                 self.UserStart()
         else:
             messagebox.showerror("InValid Credentials","Invalid Log-in credential !!")

    def CheckPin(self):
        try:
            int(self.pin.get())
        except ValueError:
            messagebox.showerror("ERROR","password can only be in integer")
            return
        
        self.k = int(self.pin.get())
        if isinstance(self.k,int) or isinstance(self.k,float):
            acct = BankAcct(self.k)
            ac = acct.CheckPin(self.name.get())
            del acct
            if ac: return True
            else:
                messagebox.showerror("InValid Credentials","Invalid Account Pin !!")
                return False
            
    def User(self,str):
        userDesign(master,self,str)
        userMenu(master,self)
  
    def UserOption(self):
        
        userDesign(master,self)
        userMenu(master,self)
        
        Button(self,text = "Deposit Cash",bg = "#66c9fa",fg = "#023b57",width = 40,height = 2,font = ("arial", "13", "bold"),
               activeforeground = "red",command = self.Deposit).grid(columnspan = 100,pady = 3)
        Button(self,text = "Withdraw Cash",bg = "#66c9fa",fg = "#023b57",width = 40,height = 2,font = ("arial", "13", "bold"),
               activeforeground = "red",command = self.Withdraw).grid(columnspan = 100,pady = 3)
        
        Button(self,text = "Balance Inquiry",bg = "#66c9fa",fg = "#023b57",width = 40,height = 2,font = ("arial", "13", "bold"),
               activeforeground = "red",command = self.balance).grid(columnspan = 100,pady = 3)
        Button(self,text = "Transfer Cash",bg = "#66c9fa",fg = "#023b57",width = 40,height = 2,font = ("arial", "13", "bold"),
               activeforeground = "red",command = self.Transfer).grid(columnspan = 100,pady = 3)
        
        Button(self,text = "Change Pin",bg = "#66c9fa",fg = "#023b57",width = 40,height = 2,font = ("arial", "13", "bold"),
               activeforeground = "red",command = self.ChangePin).grid(columnspan = 100,pady = 3)
        Button(self,text = "Delete Account",bg = "#66c9fa",fg = "#023b57",width = 40,height = 2,font = ("arial", "13", "bold"),
               activeforeground = "red",command = self.DelAccount).grid(columnspan = 100,pady = 3)
        
        Button(self,text = "Return Card",bg = "#66c9fa",fg = "#023b57",width = 40,height = 2,font = ("arial", "13", "bold"),
               activeforeground = "red",command = self.Cancel).grid(columnspan = 100,pady = 3)

    def Deposit(self): 
        
        def dep():
            try:
                amnt = int(self.amnt.get())
                if not amnt%1000==0:
                    messagebox.showinfo("Error","Amount Should Be In Multiples Of Thousands!!.")
                    return
                if amnt<0:
                    messagebox.showinfo("Error","Amount should be greater than zero.!!")
                    return
            except ValueError:
                messagebox.showwarning("ERROR","Anount Can Only Be In Integers")
                return
            
            acct = BankAcct(self.k)
            result = acct.Deposit(amnt)
            del acct
            self.Result("Deposition",result)

        self.User("DEPOSIT FUNDS")
        self.amnt = StringVar()
        
        Label(self,text = "Amount Can Only be In Multiples Of Thousands...",fg = "#6f569c", font = ("arial", "13", "bold"),
              bg = "#c0c5fc",justify = LEFT).grid(columnspan = 50,sticky = E+S+N+W,pady = 10,padx = 5)
        
        Label(self,text = "Amount :",fg = "#6f569c",bg = "#c0c5fc",width = 10, font = ("arial", "13", "bold"),
              justify = LEFT).grid(row = 2,column = 0,sticky = E+S+N+W,pady = 10,padx = 5)
        Entry(self,bg = "#048db3",fg = "white",width = 15,textvariable = self.amnt, font = ("arial", "13", "bold"),
                  exportselection = 0).grid(row = 2,column = 1,sticky = W+N+S+E,pady = 10,padx = 5)
        
        Button(self,text = "Deposit",fg = "#023b57",width = 10,height = 2,font = ("arial", "10", "bold"),
               activeforeground = "red",command = dep).grid()

    def Withdraw(self):
        
        def WithDrawal(amnt):
            acct = BankAcct(self.k)
            result = acct.WithDraw(amnt)
            del acct
            self.Result("Withdrawal",result)

        def AmountCheck():
            try:
                amnt = int(self.amnt.get())
                if not amnt%1000==0:
                    messagebox.showinfo("Error","Amount Should Be In Multiples Of Thousands!!.")
                    return
                if amnt<0:
                    messagebox.showinfo("Error","Amount should be greater than zero.")
                    return
            except ValueError:
                messagebox.showwarning("ERROR","Anount Can Only Be In Integers")
                return
            WithDrawal(amnt)
            
        def Others():
            self.User("WITHDRAW CASH")
            self.amnt = StringVar()
        
            Label(self,text = "Amount Can Only be In Multiples Of Thousands...",fg = "#6f569c", font = ("arial", "13", "bold"),
              bg = "#c0c5fc",justify = LEFT).grid(columnspan = 50,sticky = E+S+N+W,pady = 10,padx = 5)
        
            Label(self,text = "Amount :",fg = "#6f569c",bg = "#c0c5fc",width = 10, font = ("arial", "13", "bold"),
                  justify = LEFT).grid(row = 2,column = 0,sticky = E+S+N+W,pady = 10,padx = 5)
            Entry(self,bg = "#048db3",fg = "white",width = 15,textvariable = self.amnt, font = ("arial", "13", "bold"),
                  exportselection = 0).grid(row = 2,column = 1,sticky = W+N+S+E,pady = 10,padx = 5)
        
            Button(self,text = "Withdraw",fg = "#023b57",width = 10,height = 2,font = ("arial", "10", "bold"),
               activeforeground = "red",command = AmountCheck).grid()
        
        self.User("WITHDRAW CASH")
        Label(self,text = "Select The Amount You Want To Withdraw:",fg = "#6f569c", font = ("arial", "13", "bold"),
              bg = "#c0c5fc").grid(columnspan = 50,sticky = E+S+N+W,pady = 10,padx = 5)
        
        Button(self,bg = "#66c9fa",fg = "#023b57", font = ("arial", "13", "bold"),text = "1,000",command = lambda:WithDrawal(1000),
               activeforeground = "red",width = 20).grid(row = 2,column = 0,sticky = E+S+N+W,padx = 10)
        Button(self,bg = "#66c9fa",fg = "#023b57", font = ("arial", "13", "bold"),text = "2,000",command = lambda:WithDrawal(2000),
               activeforeground = "red",width = 20).grid(row = 2,column = 1,sticky = E+S+N+W,padx = 5)

        Button(self,bg = "#66c9fa",fg = "#023b57", font = ("arial", "13", "bold"),text = "5,000",command = lambda:WithDrawal(5000),
               activeforeground = "red",width = 20).grid(row = 3,column = 0,sticky = E+S+N+W,padx = 10,pady = 10)
        Button(self,bg = "#66c9fa",fg = "#023b57", font = ("arial", "13", "bold"),text = "10,000",command = lambda:WithDrawal(10000),
               activeforeground = "red",width = 20).grid(row = 3,column = 1,sticky = E+S+N+W,padx = 5,pady = 10)

        Button(self,bg = "#66c9fa",fg = "#023b57", font = ("arial", "13", "bold"),text = "20,000",command = lambda:WithDrawal(20000),
               activeforeground = "red",width = 20).grid(row = 4,column = 0,sticky = E+S+N+W,padx = 10,pady = 10)
        Button(self,bg = "#66c9fa",fg = "#023b57", font = ("arial", "13", "bold"),text = "Select Others",command = Others,
               activeforeground = "red",width = 20).grid(row = 4,column = 1,sticky = E+S+N+W,padx = 5,pady = 10)
 

    def balance(self):
        self.User("BALANCE INQUIRY")
        acct = BankAcct(self.k)
        bal = acct.GetBalance()
        bal = self.strAmnt(bal)
        del acct
        var = "Your Account Balance Is  ₹ {}.00".format(bal)
        messagebox.showinfo("BALANCE",var)
        self.UserOption()

    def Transfer(self):
        
        def Trans():
            self.User("TRANSFER FUNDS")
            self.amnt = StringVar()
        
            Label(self,text = "Amount Can Only be In Multiples Of Thousands...",fg = "#6f569c", font = ("arial", "13", "bold"),
              bg = "#c0c5fc",justify = LEFT).grid(columnspan = 50,sticky = E+S+N+W,pady = 10,padx = 5)
        
            Label(self,text = "Amount To Transfer :",fg = "#6f569c",bg = "#c0c5fc",width = 20, font = ("arial", "13", "bold"),
                  justify = LEFT).grid(row = 2,column = 0,sticky = E+S+N+W,padx = 5)
            Entry(self,bg = "#048db3",fg = "white",width = 15,textvariable = self.amnt, font = ("arial", "13", "bold"),
                  exportselection = 0).grid(row = 2,column = 1,sticky = W+N+S+E,padx = 5)
        
            Button(self,text = "Transfer",fg = "#023b57",width = 10,height = 2,font = ("arial", "10", "bold"),
               activeforeground = "red",command = AmountCheck).grid()
            
        def AmountCheck():
            try:
                amnt = int(self.amnt.get())
                if not amnt%1000 == 0:
                    messagebox.showinfo("Error","Amount Should Be In Multiples Of Thousands!!.")
                    return
                if amnt<0:
                    messagebox.showinfo("Error","Amount should be greater than zero.!!")
                    return
            except ValueError:
                messagebox.showwarning("ERROR","Anount Can Only Be In Integers")
                return
            acct = BankAcct(self.k)
            result = acct.Transfer(int(self.acctNo.get()),amnt)
            del acct
            self.Result("Transfer",result)
        
        def CheckAcctNo():
            try:
                int(self.acctNo.get())
                if not len(self.acctNo.get()) == 6:
                    messagebox.showwarning("Invalid Acct. Number","Type In A Valid Account Number")
                    return
                else: Trans()
            except ValueError:
                messagebox.showwarning("Error","Please Type In A Valid Account Number!!")
                return
        self.User("TRANSFER FUNDS")
        self.acctNo = StringVar()
        
        Label(self,text = "Recipient's Acct No:",fg = "#6f569c",bg = "#c0c5fc",width = 20, font = ("arial", "13", "bold"),
              justify = LEFT).grid(sticky = E+S+N+W,pady = 10,padx = 5)
        Entry(self,bg = "#048db3",fg = "white",font = ("arial", "13", "bold"),width = 15,textvariable = self.acctNo,
              exportselection = 0).grid(row = 1,column = 1,sticky = W+N+S+E,pady = 10,padx = 5)
        
        Button(self,text = "continue",fg = "#023b57",width = 10,height = 2,font = ("arial", "10", "bold"),
               activeforeground = "red",command = CheckAcctNo).grid()

    def strAmnt(self,amnt):
        n = str(int(amnt))
        sAmnt = ""
        try:
            for i in range(-1,-(len(n)+1),-1):
                sAmnt += n[i]
                if i%-3==0 and n[i-1]:
                    sAmnt += ","
        except IndexError: pass
        return sAmnt[::-1]

    def Result(self,message,result):
        if result:
            amnt=self.strAmnt(result[1])
            messagebox.showinfo("SUCCESS","₹{}.00 Of Money Was Successful.\
                                \nYour New Acct. Balance Is  ₹{}.00".format(message,amnt))
        else: messagebox.showinfo("FAIL","₹{}.00 Of Money Was Not Successful.".format(message))
        self.UserOption()
        
    def ChangePin(self):
        
        def checkNewPin():
            try:
                int(self.new_pin.get())
                if not len(self.new_pin.get()) == 4:
                    messagebox.showwarning("ERROR","pin must be four digits...")
                    return
            except ValueError:
                messagebox.showwarning("ERROR","pin can only be in integers !!..")
                return

            if int(self.new_pin.get())<0:
                messagebox.showinfo("Error","Pin should not be a negative number.!!")
                return
            acct = BankAcct(self.k)
            result = acct.ChangePin(int(self.new_pin.get()),self.name.get())
            del acct
            if result:
                messagebox.showinfo("SUCCESS","Your Pin Has Been Changed Successfully.\
                                    \nExiting Now To Save Changes....")
                time.sleep(2)
                self.quit()
            else: messagebox.showerror("ERROR","Change Of Pin Was Not Successful")
        if self.k == 1234:
            userDesign(master,self)
            mainMenu(master,self)
        else:
            self.User("CHANGE PIN")
        self.new_pin = StringVar()
        Label(self,text = "Input New Pin :",fg = "#6f569c",bg = "#c0c5fc",width = 20, font = ("arial", "13", "bold"),
              justify = LEFT).grid(sticky = E+S+N+W,pady = 10,padx = 5)
        Entry(self,bg = "#048db3",fg = "white",font = ("arial", "13", "bold"),width = 15,textvariable = self.new_pin,
              exportselection = 0).grid(row = 1,column = 1,sticky = W+N+S+E,pady = 10,padx = 5)

        Button(self,text = "change pin",fg = "#023b57",width = 10,height = 2,font = ("arial", "10", "bold"),
               activeforeground = "red",command = checkNewPin).grid() 

    def DelAccount(self):
        self.User("DELETE ACCOUNT")
        if messagebox.askyesno("DELETE ACCOUNT","Are You Sure You Want To Delete Your Account ?"):
            acct = BankAcct(self.k)
            result = acct.DelAcct(self.name.get())
            del acct
            if result:
                messagebox.showinfo("SUCCESS","Account Was Deleted Successfully.\
                                    \nExiting Now...")
                self.quit()
            else:
                messagebox.showinfo("FAILURE","Account Was Not Deleted Successfully.\
                                    \nExiting Now...")
                self.quit()

    def Cancel(self):
        if messagebox.askyesno("QUIT","Do You Really Want To Exit ?"):
            messagebox.showinfo("EXITING","Thanks For Banking With Us.")
            master.quit()

    def Exit(self):
        if messagebox.askyesno("QUIT","Do You Really Want To Exit ?"):
            self.master.quit()

    def AdminStart(self):
        
        def toggle():
            self.e1.configure(show = "") if self.cVar.get() == 1 else self.e1.configure(show = "*")
            
        adminDesign(master,self)
        mainMenu(master,self)
        
        self.adminPin = StringVar()
        Label(self,text = "Admin Pin :",fg = "#6f569c",bg = "#c0c5fc",width = 20, font = ("arial", "10", "bold"),
              justify = LEFT).grid(sticky = E+S+N+W,pady = 5,padx = 5)
        self.e1 = Entry(self,bg = "#048db3",fg = "white",width = 30,textvariable = self.adminPin,font = ("arial", "10"),
                        exportselection = 0,show = "*")
        self.e1.grid(row = 1,column = 1,columnspan = 5,sticky = W+N+S+E,pady = 5,padx = 5)

        self.cVar = IntVar()
        Checkbutton(self,text = "show pin",variable = self.cVar,command = toggle,bg = "#c0c5fc",
                    activebackground = "blue").grid(sticky = N+W+S+E,column = 1)
        Button(self,text = "Log-In",bg = "#66c9fa",fg = "#023b57",width = 10,height = 2,font = ("arial", "10", "bold"),command = self.AdminPinCheck).grid()

    def AdminPinCheck(self):
        
        try:
            int(self.adminPin.get())
        except ValueError:
            messagebox.showerror("ERROR","Please Type A Valid Pin...")
            return
        pin=int(self.adminPin.get())
        if len(str(pin))==4:
            acct = Admin(pin)
            if acct.CheckPin():
                self.adminPin = pin
                self.AdminOption()
            else:
                messagebox.showerror("INCORRECT PIN","Invalid Admin Pin,Exiting Admin Mode !!")
                self.destroy()
                self.main()
        else:
            messagebox.showerror("INCORRECT PIN","Invalid Amin Pin,Exiting Admin Mode !!")
            self.destroy()
            self.main()

    def Admin(self):
        adminDesign(master,self)
        adminMenu(master,self)

    def AdminOption(self):
        
        self.Admin()
        Button(self,text = "Deposit Cash In ATM",bg = "#66c9fa",fg = "#023b57",width = 40,height = 2,font = ("arial", "13", "bold"),
               activeforeground = "red",command = self.AdminDeposit).grid(columnspan = 100,pady = 6)
        Button(self,text = "Check Balance In ATM",bg = "#66c9fa",fg = "#023b57",width = 40,height = 2,font = ("arial", "13", "bold"),
               activeforeground = "red",command = self.AdminBalance).grid(columnspan = 100,pady = 6)
        Button(self,text = "Register New User",bg = "#66c9fa",fg = "#023b57",width = 40,height = 2,font = ("arial", "13", "bold"),
               activeforeground = "red",command = self.register_new_user).grid(columnspan = 100,pady = 6)
        Button(self,text = "Users' Info",bg = "#66c9fa",fg = "#023b57",width = 40,height = 2,font = ("arial", "13", "bold"),
               activeforeground = "red",command = self.usersInfo).grid(columnspan = 100,pady = 6)
        Button(self,text = "View All Users' Cash",bg = "#66c9fa",fg = "#023b57",width = 40,height = 2,font = ("arial", "13", "bold"),
               activeforeground = "red",command = self.view_all_cash).grid(columnspan = 100,pady = 6)
        Button(self,text = "Delete User Account",bg = "#66c9fa",fg = "#023b57",width = 40,height = 2,font = ("arial", "13", "bold"),
               activeforeground = "red",command = self.delete_user_account).grid(columnspan = 100,pady = 6)

    def AdminBalance(self):
        
        self.Admin()
        acct = Admin(self.adminPin)
        balance = acct.GetBalance()
        del acct
        balance = self.strAmnt(balance)
        var = "Balance In ATM Is  ₹ {}.00".format(balance)
        messagebox.showinfo("BALANCE",var)
        messagebox.showinfo("EXIT","Exiting Admin Mode...")
        self.destroy()
        self.main()

    def AdminDeposit(self):
        
        def dep():
            try:
                amnt = int(self.amnt.get())
                if not amnt%1000==0:
                    messagebox.showinfo("Error","Please Type In A Valid Amount!!.")
                    return
                if amnt<0:
                    messagebox.showinfo("Error","Amount shouldn't be a negative number.!!")
                    return
            except ValueError:
                messagebox.showwarning("ERROR","Amount Should Be In Integers")
                return

            acct = Admin(self.adminPin)
            result = acct.Deposit(amnt)
            del acct
            balance = result[1]
            balance = self.strAmnt(balance)
            messagebox.showinfo("SUCCESS","Deposition Of Money In ATM Was Successful,\
                                \nTotal Cash In ATM is now  ₹ {}.00".format(balance))
            messagebox.showinfo("EXIT","Exiting Admin Mode...")
            self.destroy()
            self.main()

        self.Admin()
        self.amnt = StringVar()
        
        Label(self,text = "Amount Can Only be In Multiples Of Thousands...",fg = "#6f569c", font = ("arial", "13", "bold"),
              bg = "#c0c5fc",justify = LEFT).grid(columnspan = 50,sticky = E+S+N+W,pady = 10,padx = 5)
        
        Label(self,text = "Amount To Deposit In ATM :",fg = "#6f569c",bg = "#c0c5fc",width = 10, font = ("arial", "13", "bold"),
              justify = LEFT).grid(row = 2,column = 0,sticky = E+S+N+W,pady = 10,padx = 5)
        Entry(self,bg = "#048db3",fg = "white",width = 15,textvariable = self.amnt,font = ("arial", "13", "bold"),
                  exportselection = 0).grid(row = 2,column = 1,sticky = W+N+S+E,pady = 10,padx = 5)
        
        Button(self,text = "Deposit",fg = "#023b57",width = 10,height = 2,font = ("arial", "10", "bold"),
               activeforeground = "red",command = dep).grid()

    def register_new_user(self):
        """REGISTERS A NEW USER INTO THE BANK'S DATABASE WITH DEFAULT PASSWORD OF 1234"""
        
        def create():
            new_username = self.new_username.get()
            if new_username:
                result = Admin.register_user(new_username)
                if result:
                    messagebox.showinfo("SUCCESS","Creation Of New User-Account Was Successful..\
                                        \nExiting Admin Mode...")
                    self.destroy()
                    self.main()
                else:
                    messagebox.showinfo("SUCCESS","Creation Of New User-Account Was Successful..\
                                        \nExiting Admin Mode...")
                    self.destroy()
                    self.main()
            else: return

        self.Admin()
        if messagebox.askyesno("CREATE NEW USER-ACCOUNT","Are You Sure You Want To Create A new User Account ?"):
            self.new_username = StringVar()
            Label(self,text = "Log-In Name Is Case-Sensitive",fg = "#6f569c", font = ("arial", "13", "bold"),
              bg = "#c0c5fc",justify = LEFT).grid(columnspan = 50,sticky = E+S+N+W,padx = 5)
            
            Label(self,text = "New Account's Log-in Name :",fg = "#6f569c",bg = "#c0c5fc",width = 25, font = ("arial", "13", "bold"),
                  justify = LEFT).grid(row = 2,column = 0,sticky = E+S+N+W,pady = 10,padx = 5)
            Entry(self,bg = "#048db3",fg = "white",width = 15,textvariable = self.new_username,font = ("arial", "13", "bold"),
                  exportselection = 0).grid(row = 2,column = 1,sticky = W+N+S+E,pady = 10,padx = 5)
            Button(self,text = "Create",fg = "#023b57",width = 10,height = 2,font = ("arial", "10", "bold"),
               activeforeground = "red",command = create).grid()

    def usersInfo(self):
        def done():
            messagebox.showinfo("DONE","Exiting Admin Mode...")
            self.destroy()
            self.main()
        self.Admin()
        acct = Admin(self.adminPin)
        database = acct.UserInfo()
        del acct

        self.text = ScrolledText(self,width = 52,borderwidth = 10,relief = SUNKEN,height = 16,bg = "#f8fc6a",fg = "#041d5c",font = ("arial", "13", "bold")) 
        self.text.grid(pady = 5)
        Button(self,text = "OK",fg = "#023b57",font = ("arial", "10", "bold"),command = done,width=52,borderwidth = 5,relief = RAISED).grid()

        headings = "s/n | Acct. Name   | Acct. No.| Acct. Bal (₹)\n"
        dots = "-----|------------------|-------------|-------------\n"
        self.text.insert(1.0,headings)
        self.text.insert(2.0,dots)
        
        index = 1
        text_index = 3.0
        for key,value in database.items():
            if value[0] != "admin":
                balance = self.strAmnt(value[2])
                if index > 9:
                    n = " "+str(index)+" | "
                else: n = " "+str(index)+"  | "
                n += str(value[0]).ljust(13)+"| "
                n += str(key)+"   | "+balance.rjust(12)+"\n"
                self.text.insert(text_index,n)
                index += 1
                text_index += 1
        self.text.config(state = DISABLED)

    def view_all_cash(self):
        def done():
            messagebox.showinfo("DONE","Exiting Admin Mode...")
            self.destroy()
            self.main()
            
        self.Admin()
        acct = Admin(self.adminPin)
        database = acct.UserInfo()
        del acct
        
        self.text = ScrolledText(self,width = 52,borderwidth = 10,relief = SUNKEN,height = 16,bg = "#f8fc6a",fg = "#041d5c",font = ("arial", "13", "bold")) 
        self.text.grid(pady = 5)
        Button(self,text = "OK",fg = "#023b57",font = ("arial", "10", "bold"),command = done,width=52,borderwidth = 5,relief = RAISED).grid()

        total = 0
        for key,value in database.items():
            if value[0] != "admin":
                total += value[2]
        total = self.strAmnt(total)
        word = "Total Cash Of All users Is  ₹ {}.00".format(total)
        self.text.insert(1.0,word)
        self.text.config(state = DISABLED)

    def delete_user_account(self):
        def proceed2():
            try:
                self.account_number = int(self.account_number.get())
            except ValueError:
                messagebox.showerror("ERROR","Account Number Can Only Be In Digits!!")
                return
            acct = Admin(self.adminPin)
            result = acct.delete_user_account(self.account_number,self.account_name)
            del acct
            if result:
                messagebox.showinfo("SUCCESS","Account Was Deleted Successfully.\
                                    \nExiting Admin Mode...")
                self.destroy()
                self.main()
            else:
                messagebox.showinfo("FAILURE","Account Was Not Deleted Successfully.\
                                    \nExiting Admin Mode...")
                self.destroy()
                self.main()
        def proceed():
            self.Admin()
            self.account_number = StringVar()
            self.account_name = self.account_name.get()
            Label(self,text = "User's Account No. :",fg = "#6f569c",bg = "#c0c5fc",width = 25,font = ("arial", "10", "bold"),
                  justify = LEFT).grid(sticky = E+S+N+W,pady = 10,padx = 5)
            Entry(self,bg = "#048db3",fg = "white",width = 15,textvariable = self.account_number,font = ("arial", "10"),
                  exportselection = 0).grid(row = 1,column = 1,sticky = E+S+N+W,pady = 10,padx = 5)
            Button(self,text = "Proceed",bg = "#66c9fa",fg = "#023b57",width = 10,height = 2,font = ("arial", "10", "bold"),
               activeforeground = "red",command = proceed2).grid()
        self.Admin()
        self.account_name = StringVar()
        
        Label(self,text = "User's Account Name :",fg = "#6f569c",bg = "#c0c5fc",width = 25,font = ("arial", "10", "bold"),
              justify = LEFT).grid(column = 0,sticky = E+S+N+W,pady = 10,padx = 5)
        Entry(self,bg = "#048db3",fg = "white",width = 15,textvariable = self.account_name,font = ("arial", "10"),
              exportselection = 0).grid(row = 1,column = 1,sticky = E+S+N+W,pady = 10,padx = 5)
        Button(self,text = "Continue",bg = "#66c9fa",fg = "#023b57",width = 10,height = 2,font = ("arial", "10", "bold"),
               activeforeground = "red",command = proceed).grid()
   
if __name__ == "__main__":
    Bank().mainloop()

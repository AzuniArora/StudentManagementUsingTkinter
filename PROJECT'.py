from tkinter import *
from tkinter.ttk import Combobox,Treeview

from tkinter import messagebox
import sqlite3


def table():
    conn=sqlite3.connect("sqlite.db")
    curr=conn.cursor()
    curr.execute("""create table IF NOT EXISTS Student
    ( Roll text PRIMARY KEY,
    Name text,
    Class text,
    Section text,
    Contact text,
    Father_Name text,
    Address text,
    Gender text,
    D_O_B text ) """)

    curr.execute("""create table IF NOT EXISTS
        USER(User_name text PRIMARY KEY,password text ) """)

    conn.close()
def load_data(s="select * from Student "):
    conn=sqlite3.connect("sqlite.db")
    curr=conn.cursor()
    curr.execute(s)
    data=curr.fetchall()
    conn.close()
    Student_table.delete(* Student_table.get_children())
    for row in data:
        Student_table.insert('','end',values=row)

def clear_detail():
    data=" "
    r.set(data)
    n.set(data)
    c_l.set(data)
    s.set(data)
    c_t.set(data)
    f_n.set(data)
    a.set(data)
    g.set(data)
    dob.set(data)

def Add_detail(r,n,c_l,s,c_t,f_n,a,g,dob):
     conn=sqlite3.connect("sqlite.db")
     curr=conn.cursor()
     if not( r and n and c_l and s and c_t and f_n and a and g and dob):
        messagebox.showinfo("Alert","All fields are required")
        return
     r=r.strip()
     n=n.strip()
     c_l=c_l.strip()
     s=s.strip()
     c_t=c_t.strip()
     f_n=f_n.strip()
     a=a.strip()
     g=g.strip()
     dob=dob.strip()
     
     try:
         curr.execute("""insert into Student(Roll,
        Name ,
        Class ,
        Section,
        Contact,
        Father_Name,
        Address ,
        Gender ,
        D_O_B ) values (?,?,?,?,?,?,?,?,?)""",(r,n,c_l,s,c_t,f_n,a,g,dob))
         messagebox.showinfo("Success","Successfully Details Added")
         conn.commit()
         load_data()
         clear_detail()
         
     except sqlite3.IntegrityError:
         messagebox.showerror("Error","Roll number Already Exists")
     finally:
         conn.close()

def tree(event):
    selected=Student_table.selection()
    if selected:
        i=Student_table.item(selected[0])
        print(i)
        values=i["values"]
        r.set(values[0])
        n.set(values[1])
        c_l.set(values[2])
        s.set(values[3])
        c_t.set(values[4])
        f_n.set(values[5])
        a.set(values[6])
        g.set(values[7])
        dob.set(values[8])
        Roll_entry.config(state='readonly')



def show():
    load_data()
def new():
    clear_detail()
    Roll_entry.config(state='normal')
    
def update():
    conn=sqlite3.connect("sqlite.db")
    curr=conn.cursor()
    if not r.get().strip():
        messagebox.showinfo("Alert","Roll no must be required")
        return
        
    try:
         curr.execute("""update Student set 
        Name=? ,
        Class=? ,        Section=?,
        Contact=?,
        Father_Name=?,
        Address=? ,
        Gender=? ,
        D_O_B=? where Roll=? """,(n.get(),c_l.get(),s.get(),c_t.get(),f_n.get(),a.get(),g.get(),dob.get(),r.get()))
         conn.commit()
         if curr.rowcount==0:
             messagebox.showinfo("error"," information not found")
             return
             
         messagebox.showinfo("success","successfully updated")
         load_data()
         new()
    except Exception as e:
        messagebox.showerror("error",str(e))
    finally:
        conn.close()

def delete():
    conn=sqlite3.connect("sqlite.db")
    curr=conn.cursor()
    if not r.get().strip():
        messagebox.showinfo("Alert","Roll no must be required")
        return
    
    try:
        curr.execute("delete from Student where Roll= ? ",(r.get(),))
        conn.commit()
        messagebox.showinfo("Success","Data Deleted Successfully")
        load_data()
        new()
    except Exception as e:
        messagebox.showerror("error",str(e))
    finally:
        conn.close()
def search():
    conn=sqlite3.connect("sqlite.db")
    curr=conn.cursor()
    x=se.get()
    y=s1.get()
    if x and y:
        s=f"select *  from Student where {x} like '%{y}%'"
        load_data(s)
    else:
        messagebox.showerror("Error","Please fill both search field")


#login

def log_in(n,ps):
    conn=sqlite3.connect("sqlite.db")
    curr=conn.cursor()
   
    curr.execute("select * from USER where User_name=? and password=?",(n,ps))
    if curr.fetchone():
        root.destroy()
        student_management()
    else:
        messagebox.showerror("Error","Incorrect Username or Password")
    
    

def login_form():
    global root
    root= Tk()
    root.geometry("500x300")
    root.title("Form")

    l=Label(root,text="Login Form",font=("ALGERIAN",26,'bold','italic'),fg="#008080")
    l.grid(row=0,column=2,sticky="w",pady=5)
    l2=Label(root,text="Username :",font=("ALGERIAN",20,"bold","italic"),fg="#008080")
    l2.grid(row=1,column=1,sticky="w",pady=5,padx=5)
    user_name=StringVar()
    E1=Entry(root,textvariable=user_name,font=("ALGERIAN",18,"italic"),bd=5)
    E1.grid(row=1,column=2,sticky="w",pady=5,padx=5)
    l3=Label(root,text="Password :",font=("ALGERIAN",20,"bold","italic"),fg="#008080")
    l3.grid(row=2,column=1,sticky="w",pady=5,padx=5)

    password=StringVar()
    E2=Entry(root,textvariable=password,font=("ALGERIAN",18,"italic"),show="*",bd=5)
    E2.grid(row=2,column=2,sticky="w",pady=5,padx=5)

    l4=Button(root,text="Submit",font=("ALGERIAN",24,'bold','italic'),bd=10,fg="#008080",command=lambda:log_in(user_name.get(),password.get()))
    l4.grid(row=3,column=1,pady=10,padx=4)

    l5=Button(root,text="Register",font=("ALGERIAN",24,'bold','italic'),bd=10,fg="#008080",command=reg_form)
    l5.grid(row=3,column=2,pady=15)

    
def register(us,p,cp):
    if p!=cp:
        messagebox.showerror("Invalid password","password not match with exact password")
        return
    conn=sqlite3.connect("sqlite.db")
    curr=conn.cursor()
    try:
        curr.execute("insert into USER(User_name,password) values (?,?)",(us,p))
        messagebox.showinfo("Success","successfully registered")
        conn.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error","username Already Exists")
    finally:
        conn.close()

    conn.close()
    
#Registration form

def reg_form():
    r=Toplevel(root)
    r.geometry("700x300")
    r.title("Registration")
    l=Label(r,text="Registration Form",font=("ALGERIAN",26,'bold','italic'),fg="#008080")
    l.grid(row=0,column=0,columnspan=2,pady=5)
    l2=Label(r,text="Username :",font=("ALGERIAN",20,"bold","italic"),fg="#008080")
    l2.grid(row=1,column=0,sticky="w",pady=5,padx=5)

    user_name=StringVar()
    E1=Entry(r,textvariable=user_name,font=("ALGERIAN",18,"italic"),bd=5)
    E1.grid(row=1,column=1,sticky="w",pady=5,padx=5)
    l3=Label(r,text="Password :",font=("ALGERIAN",20,"bold","italic"),fg="#008080")
    l3.grid(row=2,column=0,sticky="w",pady=5,padx=5)

    password=StringVar()
    E2=Entry(r,textvariable=password,font=("ALGERIAN",18,"italic"),show="*",bd=5)
    E2.grid(row=2,column=1,sticky="w",pady=5,padx=5)
    l4=Label(r,text="Confirm Password :",font=("ALGERIAN",20,"bold","italic"),fg="#008080")
    l4.grid(row=3,column=0,sticky="w",pady=5,padx=5)

    confirm_pass=StringVar()
    E=Entry(r,textvariable=confirm_pass,font=("ALGERIAN",18,"italic"),show="*",bd=5)
    E.grid(row=3,column=1,sticky="w",pady=5,padx=5)

    l5=Button(r,font=("ALGERIAN",24,'bold','italic'),bd=10,fg="#008080",command=lambda:register(user_name.get(),password.get(),confirm_pass.get()),text="Register")
    l5.grid(row=4,column=0,columnspan=2,pady=10)



def student_management():
    global pro,r,n,c_l,s,c_t,f_n,a,g,dob,Student_table,Roll_entry,s1,se
    pro= Tk()
    pro.geometry("1400x800")
    pro.title("Project")
    pro.config(bg="#CCCCFF")
    #Label 1
    La=Label(text=" STUDENT MANAGEMENT SYSTEM ",font=("ALGERIAN",54,'bold','italic'),bg="#CCCCFF",fg="Black")
    La.pack(fill="x",padx=1,pady=1)
    frame1=LabelFrame(pro,relief=GROOVE,bd=10,text=" Enter Details ",font=("ALGERIAN",20,'bold','italic'),fg="Black",bg="#CCCCFF")
    frame1.place(x=30,y=90,width=540,height=610)

    Roll_label=Label(frame1,text="Roll No",font=("ALGERIAN",16,"bold"),bd=8,bg="#CCCCFF")
    Roll_label.grid(row=0,column=0,sticky="w",padx=5,pady=5)
    r=StringVar()
    Roll_entry=Entry(frame1,font=("ALGERIAN",16,"bold"),bd=8,textvariable=r)
    Roll_entry.grid(row=0,column=2,sticky="w",padx=5,pady=5)

    N_label=Label(frame1,text="Name",font=("ALGERIAN",16,"bold"),bg="#CCCCFF",bd=8)
    N_label.grid(row=1,column=0,sticky="w",padx=5,pady=5)
    n=StringVar()

    N_entry=Entry(frame1,font=("ALGERIAN",16,"bold"),bd=8,textvariable=n)
    N_entry.grid(row=1,column=2,sticky="w",padx=5,pady=5)

    Class_label=Label(frame1,text="Class",font=("ALGERIAN",16,"bold"),bd=8,bg="#CCCCFF")
    Class_label.grid(row=2,column=0,sticky="w",padx=5,pady=5)
    c_l=StringVar()

    Class_entry=Entry(frame1,font=("ALGERIAN",16,"bold"),bd=8,textvariable=c_l)
    Class_entry.grid(row=2,column=2,sticky="w",padx=5,pady=5)

    S_label=Label(frame1,text="Section",font=("ALGERIAN",16,"bold"),bd=8,bg="#CCCCFF")
    S_label.grid(row=3,column=0,sticky="w",padx=5,pady=5)
    s=StringVar()

    S_entry=Entry(frame1,font=("ALGERIAN",16,"bold"),bd=8,textvariable=s)
    S_entry.grid(row=3,column=2,sticky="w",padx=5,pady=5)

    C_label=Label(frame1,text="Contact",font=("ALGERIAN",16,"bold"),bd=8,bg="#CCCCFF")
    C_label.grid(row=4,column=0,sticky="w",padx=5,pady=5)
    c_t=StringVar()

    C_entry=Entry(frame1,font=("ALGERIAN",16,"bold"),bd=8,textvariable=c_t)
    C_entry.grid(row=4,column=2,sticky="w",padx=5,pady=5)

    F_label=Label(frame1,text="Father's Name",font=("ALGERIAN",16,"bold"),bd=8,bg="#CCCCFF")
    F_label.grid(row=5,column=0,sticky="w",padx=5,pady=5)
    f_n=StringVar()

    F_entry=Entry(frame1,font=("ALGERIAN",16,"bold"),bd=8,textvariable=f_n)
    F_entry.grid(row=5,column=2,sticky="w",padx=5,pady=5)

    A_label=Label(frame1,text="Address",font=("ALGERIAN",16,"bold"),bd=8,bg="#CCCCFF")
    A_label.grid(row=6,column=0,sticky="w",padx=5,pady=5)
    a=StringVar()

    A_entry=Entry(frame1,font=("ALGERIAN",16,"bold"),bd=8,textvariable=a)
    A_entry.grid(row=6,column=2,sticky="w",padx=5,pady=5)

    G_label=Label(frame1,text="Gender",font=("ALGERIAN",16,"bold"),bd=8,bg="#CCCCFF")
    G_label.grid(row=7,column=0,sticky="w",padx=5,pady=5)
    g=StringVar()

    G_entry=Combobox(frame1,font=("ALGERIAN",16,"bold"),state="readonly",textvariable=g)
    G_entry["values"]=("Male","Female","other")
    G_entry.grid(row=7,column=2,sticky="w",padx=5,pady=5)

    DOB_label=Label(frame1,text="D.O.B",font=("ALGERIAN",18,"bold"),bd=8,bg="#CCCCFF")
    DOB_label.grid(row=8,column=0,sticky="w",padx=5,pady=5)
    dob=StringVar()

    D_entry=Entry(frame1,font=("ALGERIAN",16,"bold"),bd=8,textvariable=dob)
    D_entry.grid(row=8,column=2,sticky="w",padx=5,pady=5)

    #in Frame
    in_frame=Frame(frame1,relief=GROOVE,bd=10,bg="#CCCCFF")
    in_frame.place(x=30,y=490,width=460,height=70)

    #Button
    Add_button=Button(in_frame,text=" Add ",font=("ALGERIAN",16,"bold"),bg="#CCCCFF",bd=5,pady=3,padx=3,command=lambda:Add_detail(r.get(),n.get(),c_l.get(),s.get(),c_t.get(),f_n.get(),a.get(),g.get(),dob.get()))
    Add_button.grid(row=1,column=0)

    Update_button=Button(in_frame,text=" Update ",font=("ALGERIAN",16,"bold"),bg="#CCCCFF",bd=5,pady=3,padx=3,command=update)
    Update_button.grid(row=1,column=1)

    Delete_button=Button(in_frame,text=" Delete ",font=("ALGERIAN",16,"bold"),bg="#CCCCFF",bd=5,pady=3,command=delete)
    Delete_button.grid(row=1,column=2)

    Clear_button=Button(in_frame,text=" Clear ",font=("ALGERIAN",16,"bold"),bg="#CCCCFF",bd=5,pady=3,command=new)
    Clear_button.grid(row=1,column=3)


    #Frame 2
    frame2=LabelFrame(pro,relief=GROOVE,bd=10,font=("ALGERIAN",24,'bold','italic'),bg="#CCCCFF",fg="Black")
    frame2.place(x=580,y=100,width=750,height=600)
    
    #In frame1
    In_frame1=LabelFrame(frame2,relief=GROOVE,bd=5,font=("ALGERIAN",20,'bold','italic'),bg="#CCCCFF",fg="Black")
    In_frame1.place(x=10,y=9,width=710,height=70)
    
    #label in frame1
    Se_label=Label(In_frame1,text="Search:",font=("Impact",18,"italic"),bg="#CCCCFF",bd=5)
    Se_label.grid(row=0,column=0,sticky="w",padx=5)

    se=StringVar()

    Se_entry=Combobox(In_frame1,font=("Impact",12,"italic"),textvariable=se)
    Se_entry["values"]=("Roll","Name" ,"Class","Section","Contact","Father_Name","Address","Gender", "D_O_B")
    Se_entry.grid(row=0,column=1,sticky="w",padx=5,pady=5)

    s1=StringVar()

    S1_entry=Entry(In_frame1,font=("Impact",11),textvariable=s1)
    S1_entry.grid(row=0,column=2,sticky="w",padx=5,pady=5)

    #Button in frame 1
    S_button=Button(In_frame1,text="Search",font=("Impact",16,"italic"),bg="#CCCCFF",bd=5,pady=3,padx=5,command=search)
    S_button.grid(row=0,column=7)

    Show_button=Button(In_frame1,text=" Show All ",font=("Impact",16,"italic"),command=show,bg="#CCCCFF",bd=5,pady=3,padx=5)
    Show_button.grid(row=0,column=8)

    #In frame 2
    In_frame2=LabelFrame(frame2,relief=GROOVE,bd=5,fg="Black",bg="#CCCCFF")
    In_frame2.place(x=10,y=95,width=710,height=480)

    y_scroll=Scrollbar(In_frame2,orient=VERTICAL)
    x_scroll=Scrollbar(In_frame2,orient=HORIZONTAL)
 
    Student_table=Treeview(In_frame2,columns=("Roll","Name" ,"Class","Section","Contact","Father Name","Address","Gender", "D O B"),yscrollcommand=y_scroll.set,xscrollcommand=x_scroll.set)
    y_scroll.config(command=Student_table.yview)
    x_scroll.config(command=Student_table.xview)

    y_scroll.pack(side=RIGHT,fill=Y)
    x_scroll.pack(side=BOTTOM,fill=X)
    
 
    

    Student_table.heading("Roll",text="Roll")
    Student_table.heading("Name",text="Name")
    Student_table.heading("Class",text="Class")
    Student_table.heading("Section",text="Section")
    Student_table.heading("Contact",text="Contact")
    Student_table.heading("Father Name",text="Father Name")
    Student_table.heading("Address",text="Address")
    Student_table.heading("Gender",text="Gender")
    Student_table.heading("D O B",text="D O B")
    Student_table["show"]="headings"
    
    Student_table.column("Roll",width=100,anchor="center")
    Student_table.column("Name",width=100,anchor="center")
    Student_table.column("Class",width=100,anchor="center")
    Student_table.column("Section",width=100,anchor="center")
    Student_table.column("Contact",width=100,anchor="center")
    Student_table.column("Father Name",width=100,anchor="center")
    Student_table.column("Address",width=300,anchor="center")
    Student_table.column("Gender",width=100,anchor="center")
    Student_table.column("D O B",width=100,anchor="center")

    Student_table.pack(expand=True,fill='both')
    
    Student_table.bind("<<TreeviewSelect>>",tree)

    load_data()

if __name__=="__main__":
    login_form()
    table()

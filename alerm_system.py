from tkinter import *
import customtkinter as ctk
import time,os,pygame
from tkinter import filedialog,messagebox
from plyer import notification
from pygame import mixer

pygame.init()
#defined colors
col1="#000066"
col2="aliceblue"
col3="gold"
col4="black"
col5="#FF0000"

#defined fonts
fonttitle=("times",16,"bold")
fontforclock=("times",14,"bold")
font1=("times",14)

win=ctk.CTk(fg_color=col1)
win_width=500
win_height=300
screen_w=win.winfo_screenwidth()
screen_h=win.winfo_screenheight()
x_cord=screen_w-win_width-30
y_cord=screen_h-win_height-100
win.geometry("%dx%d+%d+%d"%(win_width,win_height,x_cord,y_cord))
win.resizable(False,False)
win.title("Alerm System")
icon=PhotoImage(file="icons/time.png")
win.iconphoto(False,icon)

#defined variables
today=time.strftime("%A %d/%m/%Y")
day_of_months=time.strftime("%e")
txtwidth=win_width-win_width//3
btn_width=win_width//4-20
music_selected=""
con_msg=""
alerm_time=[]

current_workingdir=os.getcwd()
music_folder=f"{current_workingdir}\\resources\\music"
files_folder=f"{current_workingdir}\\resources\\files"
if not os.path.exists(music_folder):
    os.makedirs(music_folder)
elif not os.path.exists(files_folder):
    os.makedirs(files_folder)
else:
    pass

#def functions
def to_quit():
    msg=messagebox.askyesno("Quit message","Do you want to exit?")
    if msg==1:
        pygame.quit()
        exit()
def show_currenttime():
    if int(time.strftime("%H"))>=12:
        cur_time=str(int(time.strftime("%H"))-12)+str(time.strftime(":%M:%S %p"))
    else:
        cur_time=str(time.strftime("%H:%M:%S %p"))
    
    lbl_current_time.configure(text="Time: "+cur_time)
    win.after(200,show_currenttime)
def change_byclock():
    cur_hour,cur_minute=time.strftime("%H"),time.strftime("%M")
    if len(str(cur_hour))<2:
        al_Hour.set(f'0{cur_hour}')
    else:
        al_Hour.set(f'{cur_hour}')
    
    if len(str(cur_minute))<2:
        al_Minute.set(f'0{cur_minute}')
    else:
        al_Minute.set(f'{cur_minute}')
    
    win.after(100*60*60+5,change_byclock)
def select_music():
    global music_selected
    selected_file=filedialog.askopenfilename(initialdir="",title="Select Sound or music",filetypes=[
        ("Sound or Music","*.mp3;*.wav;*.ogg")
    ])
    if selected_file:
        music_selected=selected_file
        txt_music.configure(state="normal")
        txt_music.delete(0,END)
        txt_music.insert(0,str(selected_file))
        txt_music.configure(state='readonly')
        mixer.music.load(selected_file)
        mixer.music.play(-1)
    else:
        if txt_music.get()=="":
            messagebox.showwarning("warning","Music not selected")
        else:
            pass
def save():
    global con_msg,music_selected
    if music_selected=="" or al_Hour.get()!="" or al_Minute.get()!="" or al_Interval.get()!="" or txt_music.get()!="":
        music=os.path.basename(music_selected)
        m1=os.path.basename(music_selected)
        music=music_folder+"\\"+str(music).replace(" ", "_")
        values=[f'{al_Hour.get()}\n',f'{al_Minute.get()}\n',f'{al_Interval.get()}\n',f'{str(m1).replace(" ","_")}\n','ON\n']
        
        try:
            if not os.path.exists(f'{files_folder}\\{al_Hour.get()}{al_Minute.get()}.txt'):
                with open(f'{files_folder}\\{al_Hour.get()}{al_Minute.get()}.txt','w') as txt:
                    txt.writelines(values)
                    txt.close()
                con_msg="Alert saved successfully"
            else:
                with open(f'{files_folder}\\{al_Hour.get()}{al_Minute.get()}.txt','w') as txt:
                    txt.writelines(values)
                    txt.close()
                con_msg="Alerm updated successfully"
            file=open(music_selected,'rb')
            file1=open(music,'wb')
            file1.write(file.read())
            
            
        except IOError:
            pass
        finally:
            messagebox.showinfo("success",con_msg)
            txt_music.configure(state='normal')
            txt_music.delete(0,END)
            txt_music.insert(0,str(m1).replace(" ","_"))
            txt_music.configure(state='readonly')
            file.close()
            file1.close()
            check_set_alerms()
            alerming_taking()

    else:
        select_music()
def check_alermtime():
    pass

def check_set_alerms():
    global alerm_time
    alerm_time=[]
    for i in os.listdir(files_folder):
        if i.endswith("txt"):
            alerm_time.append(str(i).replace(".txt", ""))
    
timex=40
x1=200    
def alerming_taking():
    global alerm_time,x1
    
    aler_t_file=f'{files_folder}\\"".txt'
    cur_time=time.strftime("%H:%M")
    if len(str(time.strftime("%H")))<2:
        cur_h=f'0{time.strftime("%H")}'
    else:
        cur_h=f'{time.strftime("%H")}'
    if len(str(time.strftime("%M")))<2:
        cur_m=f'0{time.strftime("%M")}'
    else:
        cur_m=f'{time.strftime("%M")}'
    cur_time=cur_h+cur_m
    if cur_time in alerm_time:
        with open(f'{files_folder}\\{cur_time}.txt','r') as fp:
            line_num=[3]
            pl_music=""
            for i,line in enumerate(fp):
                if i in line_num:
                    pl_music=line.strip()
                else:
                    pass
            
            alerming(pl_music)
                 
    win.after(x1,alerming_taking)

def alerming(file):
    global x1
    mixer.music.load(f'{music_folder}\\{file}')
    if x1>=58000:
        mixer.music.stop()
        x1=200
    else:
        mixer.music.play()
        notification.notify(
            title="Timer Alerm",message="Alerm At "+str(time.strftime("%H:%M")),
            timeout=3,app_icon='ico.ico'
        )
        x1=58000
def reset_all():
    msg=messagebox.askyesno("Confirm","do you want to reset?")
    if msg==True:
        files=os.listdir(files_folder)
        for i in files:
            os.remove(f'{files_folder}\\{i}')
        
        ms_files=os.listdir(music_folder)
        for j in ms_files:
            os.remove(f'{music_folder}\\{j}') 
def view_alerms():
    files=os.listdir(files_folder)
    my_alerms=[]
    myt=[]
    for i in files:
        if i.endswith("txt"):
            my_alerms.append(str(i).replace(".txt", ""))
    for j in my_alerms:
        h=j[0:2]
        m=j[2:4]
        tme=h+":"+m+" Hours"
        myt.append(tme)
    messagebox.showinfo("My set alerms",str(myt))

hours_values=[]
for i in range(0,24):
    if len(str(i))<2:
        hours_values.append(f'0{i}')
    else:
        hours_values.append(f'{i}')

minutes_values=[]
for i in range(0,60):
    if len(str(i))<2:
        minutes_values.append(f'0{i}')
    else:
        minutes_values.append(f'{i}')

interval_values=['Once','Daily','Weekly']



lbl=ctk.CTkLabel(win,text="Alert Clock",font=fonttitle,text_color=col3)
lbl.pack(side=TOP,fill=X,pady=(4,10))

frame_current=ctk.CTkFrame(win,fg_color=col1,height=50)
frame_current.pack(side=TOP,fill=X,pady=(4,10))
lbl_current_date=ctk.CTkLabel(frame_current,text="Today: "+str(today),font=fontforclock,text_color=col2)
lbl_current_date.place(x=10,y=0)
lbl_current_time=ctk.CTkLabel(frame_current,text="Time: ",font=fontforclock,text_color=col2)
lbl_current_time.place(x=win_width//2+10,y=0)

frame_select=ctk.CTkFrame(win,fg_color=col1)
frame_select.pack(side=TOP,fill=X,pady=(8,8),padx=(10,10))
lbl_Hour=ctk.CTkLabel(frame_select,text="Hour",text_color=col2,font=font1)
lbl_Hour.grid(column=0,row=0,padx=10)
lbl_Hour=ctk.CTkLabel(frame_select,text="Minute",text_color=col2,font=font1)
lbl_Hour.grid(column=1,row=0,padx=10)
lbl_Hour=ctk.CTkLabel(frame_select,text="Interval",text_color=col2,font=font1)
lbl_Hour.grid(column=2,row=0,padx=10)

al_Hour=ctk.CTkOptionMenu(frame_select,button_color=col2,button_hover_color=col2,fg_color=col2,text_color=col4,values=hours_values)
al_Hour.grid(column=0,row=1,padx=10)
al_Minute=ctk.CTkOptionMenu(frame_select,button_color=col2,button_hover_color=col2,fg_color=col2,text_color=col4,values=minutes_values)
al_Minute.grid(column=1,row=1,padx=10)
al_Interval=ctk.CTkOptionMenu(frame_select,button_color=col2,button_hover_color=col2,fg_color=col2,text_color=col4,values=interval_values)
al_Interval.grid(column=2,row=1,padx=10)

frame_music=ctk.CTkFrame(win,fg_color=col1)
frame_music.pack(side=TOP,fill=X,padx=(10,10),pady=(8,8))
btn_browsemusic=ctk.CTkButton(frame_music,text="Select Sound",width=btn_width,fg_color=col3,hover_color=col3,text_color=col4,cursor="hand2",command=select_music)
btn_browsemusic.pack(side=LEFT,padx=(10,0))
txt_music=ctk.CTkEntry(frame_music,border_width=1,fg_color=col2,text_color=col4,width=txtwidth,state='readonly')
txt_music.pack(side=LEFT,fill=X,padx=(0,10))

frame_btns=ctk.CTkFrame(win,fg_color=col1)
frame_btns.pack(side=TOP,fill=X,padx=(10,10),pady=(30,8))
frame_btns1=ctk.CTkFrame(frame_btns,fg_color=col1)
frame_btns1.pack(side=TOP)
btn_resetall=ctk.CTkButton(frame_btns1,text="Reset All",width=btn_width,text_color=col4,fg_color=col2,hover_color=col5,cursor="hand2",command=reset_all)
btn_resetall.grid(column=1,row=0,padx=6)
btn_save=ctk.CTkButton(frame_btns1,text="Save",width=btn_width,text_color=col4,fg_color=col3,hover_color=col3,cursor="hand2",command=save)
btn_save.grid(column=2,row=0,padx=6)
btn_viewset=ctk.CTkButton(frame_btns1,text="View",width=btn_width,text_color=col4,fg_color=col2,hover_color=col3,cursor="hand2",command=view_alerms)
btn_viewset.grid(column=3,row=0,padx=6)

show_currenttime()
change_byclock()
check_set_alerms()
alerming_taking()
win.protocol('WM_DELETE_WINDOW',to_quit)
win.mainloop()
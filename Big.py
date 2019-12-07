import MapReduce as mr
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
import matplotlib.pyplot as plti
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
import datetime
from PIL import ImageTk

colors = iter(['violet','indigo','blue','green','yellow','orange','red'])
class graph:
    def __init__(self,root):
        
        path="C:/Users/Ashutosh/Bigdata/Uber.json"
        self.l2=mr.fun1(path)
        self.l1=mr.fun3()
        self.el=mr.event()
        self.deve=pd.DataFrame(self.el,columns=['Ename','Edate','Base','Trips'])
        for i in range(len(self.deve['Edate'])):
            day,month, year = (int(j) for j in self.deve['Edate'][i].split('/'))
            year=int('20'+str(year))
            born = datetime.date(year, month, day)
            self.deve['Edate'][i]=str(born)
        self.ds1=pd.DataFrame(self.l2,columns=['Dispatch_Base','Day','Trips'])
        self.ds2=pd.DataFrame(self.l1,columns=['Dispatch_Base','Day','Active_Vehicles'])
        self.ds3=pd.merge(self.ds1,self.ds2)
        self.ds4=self.ds3.set_index("Dispatch_Base")
        self.ds5=self.ds3.set_index("Day")
        self.root=root
        self.root.title("Taxi Management System")
        self.root.geometry("1350x700+0+0")
     
        #..............................................................
        self.canvas2 = Canvas(self.root, width=600, height=280,bd=0,bg="dimgray",highlightthickness=0,relief='ridge')
        self.canvas2.place(x=70, y=-20)
        self.gif2 = ImageTk.PhotoImage(file=r'highway.jpg')
        self.canvas2.create_image(0,250,image=self.gif2)
        self.gif1 = ImageTk.PhotoImage(file=r'taxi2.png')
        self.ball =self.canvas2.create_image(0,0,image=self.gif1)
        graph.animate(self,self.ball)
    #...........................................................................
        
        T=Text(self.root,height=1,width=32,font=("bold",24),bg="dimgray",bd=0,fg="mistyrose2")
        T.pack()
        T.insert(END,'Welcome to Taxi Management System')
        self.root.configure(background="dimgray")
        l=Label(self.root,text='Enter the database path:-',font=('bold',16),fg="white",bg="dimgray")
        l.place(x=10,y=310,width=300,height=25)
        self.varr=StringVar(self.root)
        self.e1=Entry(self.root,textvariable=self.varr)
        self.e1.place(x=290,y=310,width=400,height=25)
        self.varr.set("C:/Users/Ashutosh/Bigdata/Cab.json")
        l=Label(self.root,text='Location:-',font=('bold',16),fg="white",bg="dimgray")
        l.place(x=130,y=350,width=100,height=25)
        self.loca=list(set(self.ds1['Dispatch_Base']))
        self.loca.append('All')
        self.locavar=StringVar(root)
        self.locavar.set(self.loca[0])
        w=OptionMenu(self.root,self.locavar,*self.loca)
        w.place(x=250,y=350,width=110,height=25)
        l=Label(self.root,text='Week Day:-',font=('bold',16),fg="white",bg="dimgray")
        l.place(x=440,y=350,width=115,height=25)
        self.day=list(set(self.ds1['Day']))
        self.day.append('All')
        self.dayvar=StringVar(self.root)
        self.dayvar.set(self.day[0])
        w=OptionMenu(self.root,self.dayvar,*self.day)
        w.place(x=580,y=350,width=110,height=25)
        l=Label(self.root,text='Enter the type of Analysis:-',font=('bold',16),fg="white",bg="dimgray")
        l.place(x=10,y=390,width=300,height=25)
        self.toa=['Trips on all week days of a location','Active Vehicles on all week days of a location','Trips per Vehicle on all week days of a location','Trips per Vehicle on a week day of all locations','Trips per Vehicle on all week days of all locations']
        self.toavar=StringVar(self.root)
        self.toavar.set(self.toa[0])
        w=OptionMenu(self.root,self.toavar,*self.toa)
        w.place(x=320,y=390,width=370,height=25)
        btn3=Button(self.root,command=self.analyze,text="Analyze",compound=LEFT,font=("Industry Inc Detail Fill", 20, "bold"), bg="white", fg="dimgray")
        btn3.place(x=320,y=440,height=50,width=120)
        l=Label(self.root,text='Upcoming Event:-',font=('bold',16),fg="white",bg="dimgray")
        l.place(x=40,y=500,width=180,height=25)
        self.e_icon=ImageTk.PhotoImage(file=r"events.jpg")
        e_lb1 = Label(self.root, image=self.e_icon,bg="dimgray")
        e_lb1.place(x=60, y=540,width=600,height=150)
        self.eda=self.edate()
        dst='-'.join(list(reversed(self.eda.split('-'))))
        a,self.ba,self.c=self.event(self.eda)
        l=Label(self.root,text=f"{a} at {self.ba} on {dst}",font=('bold',16),fg="white",bg="dimgray")
        l.place(x=160,y=600,width=400,height=25)
        
        
    def analyze(self):
        if self.toavar.get()==self.toa[0]:
            self.dayvar.set('All')
            self.graph1(self.locavar.get(),self.dayvar.get())
        elif self.toavar.get()==self.toa[1]:
            self.dayvar.set('All')
            self.graph2(self.locavar.get(),self.dayvar.get())
        elif self.toavar.get()==self.toa[2]:
            self.dayvar.set('All')
            self.graph3(self.locavar.get(),self.dayvar.get())
        elif self.toavar.get()==self.toa[3]:
            self.locavar.set('All')
            self.graph4(self.locavar.get(),self.dayvar.get())
        else:
            self.dayvar.set('All')
            self.locavar.set('All')
            self.graph5(self.locavar.get(),self.dayvar.get())
    def graph1(self,lo,dday):
        if lo!='All' and dday=='All':
            d=self.ds4.loc[lo]
            s=list(d['Trips'])
            t=list(d['Day'])
            fig=Figure(figsize=(7,7))
            plt=fig.add_subplot(111)
            plt.scatter(d['Day'],d['Trips'],color='white')
            b=OffsetImage(plti.imread('taxi2.png'),zoom=0.06)
            for x0, y0 in zip(d['Day'],d['Trips']):
                ab = AnnotationBbox(b, (x0, y0), frameon=False)
                plt.add_artist(ab)
            plt.set_xlabel('Day')
            plt.set_ylabel('Trips')
            plt.set_title(f'Trips on week days of location {lo}')
            dc=(max(d['Trips'])+min(d['Trips']))/500
            for i in range(len(s)):
                plt.annotate(s[i],(t[i],s[i]+dc))
            canvas=FigureCanvasTkAgg(fig,master=self.root)
            canvas.get_tk_widget().place(x=780,y=100)
            canvas.draw()
            btn4=Button(self.root,command=self.suggestion,text="Suggestions?",compound=LEFT,font=("Industry Inc Detail Fill", 20, "bold"), bg="white", fg="dimgray")
            btn4.place(x=930,y=620,height=50,width=200)
    def graph2(self,lo,dday):
        if lo!='All' and dday=='All':
            d=self.ds4.loc[lo]
            s=list(d['Active_Vehicles'])
            t=list(d['Day'])
            fig=Figure(figsize=(7,7))
            plt=fig.add_subplot(111)
            plt.scatter(d['Day'],d['Active_Vehicles'],color='white')
            b=OffsetImage(plti.imread('taxi2.png'),zoom=0.05)
            for x0, y0 in zip(d['Day'],d['Active_Vehicles']):
                ab = AnnotationBbox(b, (x0, y0), frameon=False)
                plt.add_artist(ab)
            plt.set_xlabel('Day')
            plt.set_ylabel('Active Vehicles')
            plt.set_title(f'Active Vehicles on week days of location {lo}')
            dc=(max(d['Active_Vehicles'])+min(d['Active_Vehicles']))/320
            for i in range(len(s)):
                plt.annotate(s[i],(t[i],s[i]+dc))
            canvas=FigureCanvasTkAgg(fig,master=self.root)
            canvas.get_tk_widget().place(x=780,y=100)
            canvas.draw()
            btn4=Button(self.root,command=self.suggestion,text="Suggestions?",compound=LEFT,font=("Industry Inc Detail Fill", 20, "bold"), bg="white", fg="dimgray")
            btn4.place(x=930,y=620,height=50,width=200)
        else:
            messagebox.showerror("Error","Select the Correct Location and Week Day for this graph!")
    def graph3(self,lo,dday):
        if lo!='All' and dday=='All':
            d=self.ds4.loc[lo]
            fig=Figure(figsize=(7,7))
            plt=fig.add_subplot(111)
            s=list((d['Trips']/d['Active_Vehicles']))
            dc=(max(s)+min(s))/800
            s=list(map(lambda x:round(x,2),s))
            t=list(d['Day'])
            plt.scatter(d['Day'],(d['Trips']/d['Active_Vehicles']),color='white')
            b=OffsetImage(plti.imread('taxi2.png'),zoom=0.05)
            for x0, y0 in zip(d['Day'],(d['Trips']/d['Active_Vehicles'])):
                ab = AnnotationBbox(b, (x0, y0), frameon=False)
                plt.add_artist(ab)
            plt.set_xlabel('Day')
            plt.set_ylabel('Trips per Vehicle')
            plt.set_title(f'Trips per Vehicle on week days of location {lo}')
            for i in range(len(s)):
                plt.annotate(s[i],(t[i],s[i]+dc))
            canvas=FigureCanvasTkAgg(fig,master=self.root)
            canvas.get_tk_widget().place(x=780,y=100)
            canvas.draw()
            btn4=Button(self.root,command=self.suggestion,text="Suggestions?",compound=LEFT,font=("Industry Inc Detail Fill", 20, "bold"), bg="white", fg="dimgray")
            btn4.place(x=930,y=620,height=50,width=200)
        else:
            messagebox.showerror("Error","Select the Correct Location and Week Day for this graph!")
    def graph4(self,lo,dday):
        if lo=='All' and dday!='All':
            de=self.ds5.loc[dday]
            fig=Figure(figsize=(7,7))
            plt=fig.add_subplot(111)
            s=list((de['Trips']/de['Active_Vehicles']))
            dc=(max(s)+min(s))/800
            s=list(map(lambda x:round(x,2),s))
            t=list(de['Dispatch_Base'])
            b=OffsetImage(plti.imread('taxi2.png'),zoom=0.05)
            plt.scatter(de['Dispatch_Base'],(de['Trips']/de['Active_Vehicles']),color='white')
            for x0, y0 in zip(de['Dispatch_Base'],(de['Trips']/de['Active_Vehicles'])):
                ab = AnnotationBbox(b, (x0, y0), frameon=False)
                plt.add_artist(ab)
            plt.set_xlabel('Dispatch Bases')
            plt.set_ylabel('Trips per Vehicle')
            plt.set_title(f'Trips per Vehicle on week day {dday} of all locations')
            for i in range(len(s)):
                plt.annotate(s[i],(t[i],s[i]+dc))
            canvas=FigureCanvasTkAgg(fig,master=self.root)
            canvas.get_tk_widget().place(x=780,y=100)
            canvas.draw()
            btn4=Button(self.root,command=self.suggestion,text="Suggestions?",compound=LEFT,font=("Industry Inc Detail Fill", 20, "bold"), bg="white", fg="dimgray")
            btn4.place(x=930,y=620,height=50,width=200)
        else:
            messagebox.showerror("Error","Select the Correct Location and Week Day for this graph!")
    def graph5(self,lo,dday):
        if lo=='All' and dday=='All':
            self.day.remove('All')
            fig=Figure(figsize=(7,7))
            plt=fig.add_subplot(111)
            for i in self.day:
                de=self.ds5.loc[i]
                plt.scatter(de['Dispatch_Base'],(de['Trips']/de['Active_Vehicles']),color=next(colors),label=i)
            plt.legend()
            plt.set_xlabel('Dispatch Bases')
            plt.set_ylabel('Trips per Vehicle')
            plt.set_title(f'Trips per Vehicle on week day {dday} of all locations')
            canvas=FigureCanvasTkAgg(fig,master=self.root)
            canvas.get_tk_widget().place(x=780,y=100)
            canvas.draw()
            btn4=Button(self.root,command=self.suggestion,text="Suggestions?",compound=LEFT,font=("Industry Inc Detail Fill", 20, "bold"), bg="white", fg="dimgray")
            btn4.place(x=930,y=620,height=50,width=200)
        else:
            messagebox.showerror("Error","Select the Correct Location and Week Day for this graph!")
    def suggestion(self):
        tp=Toplevel()
        tp.title("Suggestions")
        tp.geometry("700x700+400+0")
        tp.configure(background="dimgray")
        bg_i=ImageTk.PhotoImage(file=r"suggestions.png")
        bg_l = Label(tp, image=bg_i,bg="dimgray")
        bg_l.place(x=230, y=10,width=240,height=230)
        l=Label(tp,text='Select the date for which you want suggestion:-',font=('bold',16),fg="white",bg="dimgray")
        l.place(x=10,y=250,width=460,height=25)
        self.cal = DateEntry(tp, width=12, background='darkblue',foreground='white', borderwidth=2)
        self.cal.place(x=500,y=250,width=110,height=25)
        btn4=Button(tp,command=self.suggest,text="Suggest",compound=LEFT,font=("Industry Inc Detail Fill", 20, "bold"), bg="white", fg="dimgray")
        btn4.place(x=280,y=290,height=50,width=120)
        self.T=Text(tp,height=6,width=42,font=("bold",14),bg="dimgray",bd=0,fg="mistyrose2")
        self.T.place(x=150,y=370)
        self.T1=Text(tp,height=6,width=42,font=("bold",14),bg="dimgray",bd=0,fg="mistyrose2")
        self.T1.place(x=150,y=475)
        tp.mainloop()
    def suggest(self):
        self.T.delete(1.0,END)
        self.T1.delete(1.0,END)
        month,day, year = (int(i) for i in self.cal.get().split('/'))
        year=int('20'+str(year))
        born = datetime.date(year, month, day)
        dat=str(born)
        b=born.strftime("%A")
        d1=self.ds5.loc[b].reset_index()
        cdi=mr.fun2()
        if dat==self.eda:
            tr=round(sum(d1['Trips'])/sum(d1['Active_Vehicles']),1)
            for i in range(len(d1)):
                if d1['Dispatch_Base'][i]==self.ba:
                    a=((d1['Trips'][i]/cdi[b])+self.c)//tr
                else:
                    a=(d1['Trips'][i]/cdi[b])//tr
                av=d1['Active_Vehicles'][i]//cdi[b]
                if a<av:
                    c=int(av-a)
                    self.T1.insert(END,f"{c} Vehicles can be transferred from {d1['Dispatch_Base'][i]}\n")
                else:
                    d=int(a-av)
                    self.T.insert(END,f"{d} Vehicles can be transferred to {d1['Dispatch_Base'][i]}\n")
        else:
            tr=round(sum(d1['Trips'])/sum(d1['Active_Vehicles']),1)
            for i in range(len(d1)):
                a=(d1['Trips'][i]/cdi[b])//tr
                av=d1['Active_Vehicles'][i]//cdi[b]
                if a<av:
                    c=int(av-a)
                    self.T1.insert(END,f"{c} Vehicles can be transferred from {d1['Dispatch_Base'][i]}\n")
                else:
                    d=int(a-av)
                    self.T.insert(END,f"{d} Vehicles can be transferred to {d1['Dispatch_Base'][i]}\n")
    def edate(self):
        di={}
        for i in self.deve['Edate']:
            td=datetime.datetime.today()
            di[i]=(datetime.datetime.strptime(i,'%Y-%m-%d')-td).days
        em=min(di.values())
        for j in di:
            if di[j]==em:
                ed=j
        return ed
    def event(self,ed):
        i=list(self.deve['Edate']).index(ed)
        return (self.deve['Ename'][i],self.deve['Base'][i],self.deve['Trips'][i])
    
    def animate(self,obj_id):
        self.canvas2.move(obj_id, 3, 0.5)
        x0,y0= self.canvas2.coords(obj_id)
        if x0 > self.canvas2.winfo_width():
            self.canvas2.coords(obj_id, 0,200)
        self.canvas2.after(50,self.animate, obj_id)
        self.canvas2.move(obj_id, 3, -0.5)
    
        
if __name__=="__main__":
    root = Tk()
    
   
    
    obj = graph(root)
    root.mainloop()

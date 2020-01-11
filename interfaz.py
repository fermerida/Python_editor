import tkinter as tk
import os     
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter import ttk


from pygments import highlight
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.lexers import CLexer
from pygments.token import Token
from scrollimage import ScrollableImage   
import sys

sys.setrecursionlimit(2000)

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None
        

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        try:
            result = self.tk.call(cmd)
        except Exception:
            return None

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or 
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result        

class Notepad: 
    ts_global = None
    ts3d_global = None
    c3d_global = None
    ms_global = None
 




    def __init__(self,**kwargs): 
  
        self.window = Tk()
        # default window width and height 
        self.__thisWidth = 300
        self.__thisHeight = 300
        self.ToAnalize = CustomText(self.window)
        self.ToParse = CustomText(self.window)
        self.ToConsole = Text(self.window,height = 200, background="#2A2C2E",foreground="#24EA3C") 

        #Frames
        self.Frame1 = Frame(self.window,height = 40) 
        self.Frame2 = Frame(self.window,height = 40) 
        self.F_space1 = Frame(self.window,height = 20) 
        self.Fleft = Text(self.window,width = 20) 
        self.Fcenter = Text(self.window,width = 20) 
        self.Fcenter2 = Text(self.window,width = 20) 
        self.Fright = Text(self.window, width=20) 

        self.playico = PhotoImage(file="./ico/play7.png")
        self.playpic = self.playico.subsample(25,25)


        self.debico = PhotoImage(file="./ico/debug.png")
        self.debpic = self.debico.subsample(14,14)

        self.desico = PhotoImage(file="./ico/play4.png")
        self.despic = self.desico.subsample(15,15)

        self.labtra = Label(self.window, text="Traducir")

        self.ToGo = Button(self.Frame2, text = 'Go!',bd=0)
        self.To3D = Button(self.Frame2, text = 'Translate',bd=0)
        self.To3DEB = Button(self.Frame2, text = 'Debugger',bd=0)
        self.Deb3ST = Button(self.Frame2, text = 'Stop',bd=0,state='disabled')
        self.Deb3NX = Button(self.Frame2, text = 'Next',bd=0,state ='disabled')
        self.ToOPT = Button(self.Frame2, text = 'Optimizado',bd=0)

        self.ToRun = Button(self.Frame1, text = 'Analizar',bd=0)
        self.ToDES = Button(self.Frame1, text = 'Descendente',bd=0)
        self.ToDEB = Button(self.Frame1, text = 'Debugger',bd=0)
        self.DebNX = Button(self.Frame1, text = 'Next',bd=0,state ='disabled')
        self.DebST = Button(self.Frame1, text = 'Stop',bd=0,state='disabled')
        self.MenuBar = Menu(self.window) 
        self.BarFile = Menu(self.MenuBar, tearoff=0) 
        self.BarEdit = Menu(self.MenuBar, tearoff=0) 
        self.BarOptions = Menu(self.MenuBar, tearoff=0) 
        self.BarHelp = Menu(self.MenuBar, tearoff=0) 
        self.BarReport = Menu(self.MenuBar, tearoff=0) 
        self.linenumbers = TextLineNumbers(self.Fcenter2, width=20)
        self.linenumbers3d = TextLineNumbers(self.Fleft, width=20)
        # To add scrollbar 
        self.ScrollA = Scrollbar(self.Fright)  
        self.ScrollB = Scrollbar(self.Fcenter)      
        self.ScrollC = Scrollbar(self.ToConsole)      
        self.archivo = None
        self.errores = None
        self.shouldcolor = False
        self.backcolor = 0
        self.shouldlines =True
        set
        # Set icon 
        try: 
                self.window.wm_iconbitmap("./ico/not2.png")  
        except: 
                pass
  
        # Set window size (the default is 300x300) 
  
        try: 
            self.__thisWidth = kwargs['width'] 
        except KeyError: 
            pass
  
        try: 
            self.__thisHeight = kwargs['height'] 
        except KeyError: 
            pass
  
        # Set the window text 
        self.window.title("Untitled - Notepad") 
  
        # Center the window 
        screenWidth = self.window.winfo_screenwidth() 
        screenHeight = self.window.winfo_screenheight() 
      
        # For left-alling 
        left = (screenWidth / 2) - (self.__thisWidth / 2)  
          
        # For right-allign 
        top = (screenHeight / 2) - (self.__thisHeight /2)  
          
        # For top and bottom 
        self.window.geometry('%dx%d+%d+%d' % (self.__thisWidth, 
                                              self.__thisHeight, 
                                              left, top))  
  
        # To make the textarea auto resizable 
        self.window.rowconfigure(1, weight=3) 
        self.window.rowconfigure(3, weight=1) 
        self.window.columnconfigure(1, weight=2) 
        self.window.columnconfigure(4, weight=2) 
  
        # Add controls (widget) 
        self.ToRun.config(image = self.playpic)
        self.ToDEB.config(image = self.debpic)
        self.ToDES.config(image = self.despic)
        self.ToRun.grid(row = 0,column=3,padx = 30)
        self.ToDES.grid(row = 0,column=4,padx = 30)
        self.ToDEB.grid(row = 0,column=1)
        self.DebST.grid(row = 0,column=0)
        self.DebNX.grid(row = 0,column=2)

        self.ToGo.config(image = self.playpic)
        self.To3D.config(image = self.despic)
        self.ToOPT.config(image = self.despic)
        self.To3DEB.config(image = self.debpic)
        self.ToGo.grid(row = 0,column=4,padx = 18)
        self.To3D.grid(row = 0,column=3,padx = 16)
        self.To3DEB.grid(row = 0,column=1)
        self.Deb3ST.grid(row = 0,column=0)
        self.Deb3NX.grid(row = 0,column=2)
        self.ToOPT.grid(row = 0,column=5,padx = 16)


        self.ToAnalize.grid(row=1,column=4,sticky = N + E + S + W) 
        self.ToParse.grid(row=1,column=1,sticky = N + E + S + W) 
        self.Frame1.grid(row=0,column=4,sticky = N + E + S + W)
        self.Frame2.grid(row=0,column=1,sticky = N + E + S + W)
        self.F_space1.grid(row=2,column=1,sticky = N + E + S + W)
        self.ToConsole.grid(columnspan=4,row=3,column=1,sticky = N + E + S + W)
        self.Fleft.grid(row=1,column=0,sticky = N + E + S + W)
        self.Fcenter.grid(row=1,column=2,sticky = N + E + S + W)
        self.Fcenter2.grid(row=1,column=3,sticky = N + E + S + W)
        self.Fright.grid(row=1,column=5,sticky = N + E + S + W)

        self.ToConsole.tag_config('minor',  foreground="yellow")

          
        # To open new file 
        self.BarFile.add_command(label="New", 
                                        command=self.__newFile)     
          
        # To open a already existing file 
        self.BarFile.add_command(label="Open", 
                                        command=self.__openFile) 
          
        # To save current file 
        self.BarFile.add_command(label="Save", 
                                        command=self.__saveFile)  

        self.BarFile.add_command(label="Save As", 
                                        command=self.__saveFileAs)   

  
        # To create a line in the dialog         
        self.BarFile.add_separator()    
        self.BarFile.add_command(label="Close", 
                                        command=self.__newFile)                                          
        self.BarFile.add_command(label="Exit", 
                                        command=self.__quitApplication) 
        self.MenuBar.add_cascade(label="File", 
                                       menu=self.BarFile)      
          
        # To give a feature of cut  
        self.BarEdit.add_command(label="Cut", 
                                        command=self.__cut)              
      
        # to give a feature of copy     
        self.BarEdit.add_command(label="Copy", 
                                        command=self.__copy)          
          
        # To give a feature of paste 
        self.BarEdit.add_command(label="Paste", 
                                        command=self.__paste)          
          
        # To give a feature of editing 
        self.MenuBar.add_cascade(label="Edit", 
                                       menu=self.BarEdit)      

        # To give a feature of cut  
        self.BarOptions.add_command(label="Toogle Colors", 
                                        command=self.__toggleColors)  
        self.BarOptions.add_command(label="Toogle Lines", 
                                        command=self.__toggleLines)              
        self.BarOptions.add_command(label="Change Background color", 
                                        command=self.__backgroundchange)  
          
        # To give a feature of editing 
        self.MenuBar.add_cascade(label="Options", 
                                       menu=self.BarOptions)     
          
        # To create a feature of description of the notepad 
        self.BarHelp.add_command(label="Help", 
                                        command=self.__showAbout) 
        self.BarHelp.add_command(label="About", 
                                        command=self.__showAbout) 
        self.MenuBar.add_cascade(label="Help", 
                                       menu=self.BarHelp) 

       
  
        self.window.config(menu=self.MenuBar) 
  
        self.ScrollA.pack(side=RIGHT,fill=Y)                     
          
        # Scrollbar will adjust automatically according to the content         
        #self.ScrollA.config(command=self.Fright.yview)      
        #self.Fright.config(yscrollcommand=self.ScrollA.set) 

        self.ScrollB.pack(side=RIGHT,fill=Y)     
                        
        self.ScrollC.pack(side=RIGHT,fill=Y)                     
          
        # Scrollbar will adjust automatically according to the content         

        self.linenumbers.attach(self.ToAnalize)
        self.linenumbers.pack(side=LEFT, fill=Y)
        self.linenumbers3d.attach(self.ToParse)
        self.linenumbers3d.pack(side=LEFT, fill=Y)

        self.ToAnalize.bind("<<Change>>", self._on_change)
        self.ToAnalize.bind("<Configure>", self._on_change)
        self.ToParse.bind("<<Change>>", self._on_change3d)
        self.ToParse.bind("<Configure>", self._on_change3d)
        self.window.bind("<space>", self.syn)


    def syn(self,event=None):

        def colorize(word, color):
            index = []
            index1 = self.ToParse.search(word, "1.0", "end")
            while index1:
                index2 = ".".join([index1.split(".")[0], str(int(index1.split(".")[1]) + len(word))])
                index.append((index1, index2))
                index1 = self.ToParse.search(word, index2, "end")
            for i, j in index:
                self.ToParse.tag_add(word, i, j)
                self.ToParse.tag_configure(word, foreground=color)
        if self.shouldcolor:
            text = self.ToParse.get("1.0", "end")
            for token, content in lex(text, PythonLexer()):
                if token == Token.Literal.Number.Integer:
                    colorize(content, color="purple")
                elif token == Token.Operator:
                    colorize(content, color="#d69340")
                elif token == Token.Name.Builtin:
                    colorize(content, color="blue")
                elif token == Token.Comment.Hashbang or token == Token.Comment.Single:
                    colorize(content, color="grey")
                elif token == Token.Keyword:
                    colorize(content, color="#5f9490")
                elif token == Token.Namespace:
                    colorize(content, color="green")
                elif token == Token.Punctuation:
                    colorize(content, color="brown")
                elif token == Token.Literal.String.Double:
                    colorize(content, color="orange")
                
                elif token == Token.Name:
                    if (content == "printf"):
                        colorize(content, color="#5f9490")
                    else:
                        colorize(content, color="green")
                elif (content == "%"):
                        colorize(content, color="orange")
            

    

    def _on_change(self, event):
        
        self.linenumbers.redraw()
        if self.shouldlines:
            self.linenumbers.pack(side=LEFT, fill=Y)
        else:
            self.linenumbers.pack_forget()
        
    def _on_change3d(self, event):
        
        self.linenumbers3d.redraw()
        if self.shouldlines:
            self.linenumbers3d.pack(side=LEFT, fill=Y)
        else:
            self.linenumbers3d.pack_forget()


    def __quitApplication(self): 
        self.window.destroy() 
        # exit() 
  
    def __showAbout(self): 
        showinfo("About","Fernando Andrés Mérida Antón \n 201314713") 
  
    def __openFile(self): 
          
        self.archivo = askopenfilename(defaultextension=".txt", 
                                      filetypes=[("All Files","*.*"), 
                                        ("Text Documents","*.txt")]) 
  
        if self.archivo == "": 
              
            # no file to open 
            self.archivo = None
        else: 
              
            # Try to open the file 
            # set the window title 
            self.window.title(os.path.basename(self.archivo) + " - Notepad") 
            self.ToParse.delete(1.0,END) 
  
            file = open(self.archivo,"r") 
  
            self.ToParse.insert(1.0,file.read()) 
  
            file.close() 
  
          
    def __newFile(self): 
        self.window.title("Untitled - Notepad") 
        self.archivo = None
        self.ToParse.delete(1.0,END) 
  
    def __saveFile(self): 
  
        if self.archivo == None: 
            # Save as new file 
            self.archivo = asksaveasfilename(initialfile='Untitled.txt', 
                                            defaultextension=".txt", 
                                            filetypes=[("All Files","*.*"), 
                                                ("Text Documents","*.txt")]) 
  
            if self.archivo == "": 
                self.archivo = None
            else: 
                  
                # Try to save the file 
                file = open(self.archivo,"w") 
                file.write(self.ToParse.get(1.0,END)) 
                file.close() 
                  
                # Change the window title 
                self.window.title(os.path.basename(self.archivo) + " - Notepad") 
                  
              
        else: 
            file = open(self.archivo,"w") 
            file.write(self.ToParse.get(1.0,END)) 
            file.close() 

    def __saveFileAs(self): 
  
            # Save as new file 
            self.archivo = asksaveasfilename(initialfile='Untitled.txt', 
                                            defaultextension=".txt", 
                                            filetypes=[("All Files","*.*"), 
                                                ("Text Documents","*.txt")]) 
  
            if self.archivo == "": 
                self.archivo = None
            else: 
                  
                # Try to save the file 
                file = open(self.archivo,"w") 
                file.write(self.ToParse.get(1.0,END)) 
                file.close() 
                  
                # Change the window title 
                self.window.title(os.path.basename(self.archivo) + " - Notepad") 
                  
              
        
  
    def __cut(self): 
        self.ToAnalize.event_generate("<<Cut>>") 
  
    def __copy(self): 
        self.ToAnalize.event_generate("<<Copy>>") 
  
    def __paste(self): 
        self.ToAnalize.event_generate("<<Paste>>") 
    
    def __toggleColors(self): 
        if self.shouldcolor:
            self.shouldcolor = False
        else:
            self.shouldcolor = True

    def __toggleLines(self): 
        if self.shouldlines:
            self.shouldlines = False
        else:
            self.shouldlines = True
    
    def __backgroundchange(self): 
        self.backcolor +=1
        if self.backcolor == 0:
            self.ToAnalize.configure(background="white")
        elif self.backcolor == 1:
            self.ToAnalize.configure(background="#e1f1fa")
        elif self.backcolor == 2:
            self.ToAnalize.configure(background="#faded9")
        elif self.backcolor == 3:
            self.ToAnalize.configure(background="#ecffe6")
        elif self.backcolor == 4:
            self.ToAnalize.configure(background="#f6d5f7")
        elif self.backcolor == 5:
            self.ToAnalize.configure(background="#c1f6f7")
            self.backcolor = -1
        else:
            self.ToAnalize.configure(background="white")
  
    def run(self): 
  
        # Run main application 
        self.window.mainloop() 


  
  # Run main application 
notepad = Notepad(width=1400,height=800) 
notepad.run() 
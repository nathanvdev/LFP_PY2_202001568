
from os import startfile
from tkinter import *
import webbrowser
import sys

from jinja2 import Environment, FileSystemLoader, select_autoescape
import CSV, Analizador, Objects
from Analizador import LexicalError, SyntacticalError, TokenList

PartidosList = []
ChatWindow = Tk()
PartidosList = CSV.FileUpload()

def chatGUI():
    ChatWindow.geometry("570x850")
    ChatWindow.resizable(width=False, height=False)
    ChatWindow.config(bg="#202C33")
    ChatWindow.iconbitmap("Assets/580b57fcd9996e24bc43c543.ico")

    PorfileFrame = Frame()
    PorfileFrame.config(bg="#00a884", pady=10)
    PorfileFrame.place(relwidth=1,relheight=0.09)

    img = PhotoImage(file="Assets/LaLiga_logo_(stacked).svg.png")
    img = img.subsample(4)
    labl = Button(PorfileFrame, image=img, bg="#00a884", borderwidth=0, pady=0)
    labl.place(x=30, y=0)
    
    menubutton = Menubutton(PorfileFrame, text = "• • •", background="#00a884", foreground="#ffffff")
    menubutton.menu = Menu(menubutton)   
    menubutton["menu"]= menubutton.menu 
    menubutton.menu.add_command(label = "Reporte de Errores", background="#00a884", foreground="#ffffff", command=lambda: ReporteErrores())   
    menubutton.menu.add_command(label = "Limpiar Log de Errores", background="#00a884", foreground="#ffffff", command=lambda:Analizador.LexicalError.clear()) 
    menubutton.menu.add_command(label = "Reporte de Tokens", background="#00a884", foreground="#ffffff", command=lambda: ReporteTokens())
    menubutton.menu.add_command(label = "Limpiar Log de Tokens", background="#00a884", foreground="#ffffff", command=lambda:Analizador.TokenList.clear()) 
    menubutton.menu.add_command(label = "Manual de Usuario", background="#00a884", foreground="#ffffff", command=lambda: manual_usuario()) 
    menubutton.menu.add_command(label = "Manual Tecnico", background="#00a884", foreground="#ffffff", command=lambda: manual_tecnico()) 
    menubutton.config(bg="#00a884", activebackground="#00a884", foreground="#ffffff", activeforeground="#ffffff", font=('Berlin Sans FB',13))
    menubutton.place(x=500, y=10)

    Porfile_label = Label(master=PorfileFrame, bg="#00a884", text='La Liga BOT', font=('Berlin Sans FB',20), padx=10, foreground="#ffffff")
    Porfile_label.place(x=90, y=10)

    global BoxTXT
    BoxTXT = Text(ChatWindow, width=100,height=2,bg="#111b21", fg="#ffffff", padx=5, pady=5, font=('Berlin Sans FB',13), state='disabled', cursor="arrow")
    BoxTXT.place(relheight=0.78, relwidth=0.9,x=30,y=100)

    scrollB = Scrollbar(BoxTXT)
    scrollB.place(relheight=1, relx=0.98)
    scrollB.configure(command= BoxTXT.yview)

    global BoxMSG
    BoxMSG = Entry(ChatWindow, bg="#111b21", fg="#ffffff", font=('Berlin Sans FB',13))
    
    BoxMSG.focus()
    BoxMSG.place(x=30, y=780, relheight=0.06, relwidth=0.75)


    img2 = PhotoImage(file="Assets/download-icon-send+icon-1320185654900887696_512.png")
    img2 = img2.subsample(9)
    SendBtn = Button(ChatWindow, image=img2, bg="#202C33", borderwidth=0, command=lambda:UserMessage(), activebackground="#202C33")
    SendBtn.place(x=480, y=775)


    ChatWindow.config()
    ChatWindow.mainloop()

def UserMessage():
    global TokenList
    msg = ''
    msg = BoxMSG.get()
    SendMessage('YOU',msg)
    Comando = ()
    Comando = Analizador.LexiconAnalyzer(msg)
    CorrectSyntax,CorrectLexicon = Analizador.SyntacticAnalizer(Comando)
    BoxMSG.delete(0,END)

    if CorrectSyntax and CorrectLexicon:
        if Comando[0].Lexeme == 'RESULTADO':
            Encontrado = False
            for Partido in PartidosList:
                if Partido.Local == Comando[1].Lexeme and Partido.Visit == Comando[3].Lexeme and Partido.Temp == Comando[5].Lexeme:
                    Encontrado = True
                    mensaje = Partido.getPartido()
                    SendMessage('BOT', mensaje)
                    break 
            if Encontrado == False:
                SendMessage('BOT','Partido no encontrado')

        if Comando[0].Lexeme == 'JORNADA':
            SendMessage('BOT','Generando archivo de resultados jornada {} temporada {}'.format(Comando[1].Lexeme, Comando[3].Lexeme))
            JornadaList = []
            for Partido in PartidosList:
                if Partido.Temp == Comando[3].Lexeme and Partido.Journey == Comando[1].Lexeme:
                    JornadaList.append(Partido)

            FileName = 'Jornada.html'
            if len(Comando)>5:
                FileName = Comando[5].Lexeme
                FileName +='.html'
            nombre = 'Partidos Jornada #{}'.format(Comando[1].Lexeme)
            arvg = Environment(loader=FileSystemLoader('Assets/'), autoescape = select_autoescape(['html']))
            template = arvg.get_template('Plantilla Jornadas.html')
            html_file = open(FileName, 'w+', encoding='utf-8')
            html_file.write(template.render(nombre= nombre, JornadaList = JornadaList))
            html_file.close()
            startfile(FileName)
        
        if Comando[0].Lexeme == 'GOLES':
            Goles = 0
            temp = ''
            Partido: Objects.Partidos
            for Partido in PartidosList:
                if Partido.Local == Comando[2].Lexeme and Partido.Temp == Comando[4].Lexeme:
                    Goles += int(Partido.GoalsL)
                    temp = str(Partido.Temp)
                    temp = temp.replace('-',' ')

            mensaje = 'Los goles anotados por el {} en total en la temporada {} fueron {}'
            SendMessage('BOT', mensaje)


        if Comando[0].Lexeme == 'TABLA':
            SendMessage('BOT','Generando archivo de clasificación de temporada {}'.format(Comando[2].Lexeme))
            TablaList = []
            for Partido in PartidosList:
                PointsL = 0 
                PointsV = 0
                Nuevo = True
                Nuevo2 = True
                if Partido.Temp == Comando[2].Lexeme:
                    if Partido.GoalsL > Partido.GoalsV:
                        PointsL += 3
                    elif Partido.GoalsL < Partido.GoalsV:
                        PointsV += 3
                    elif Partido.GoalsV == Partido.GoalsL:
                        PointsL += 1
                        PointsV += 1

                    for x in TablaList:
                        
                        if x.Equipo == Partido.Local:
                            x.Puntos += PointsL
                            Nuevo = False
                        if x.Equipo == Partido.Visit:
                            x.Puntos += PointsV
                            Nuevo2 = False
                    if Nuevo == True:
                        NewTeam = Objects.Tabla(Partido.Local, PointsL)
                        TablaList.append(NewTeam)
                    if Nuevo2 == True:
                        NewTeam = Objects.Tabla(Partido.Visit, PointsV)
                        TablaList.append(NewTeam)

            TablaList = bubble_sort_UP(TablaList)
            
            FileName = 'temporada.html'
            if len(Comando) > 3 :
                FileName = Comando[4].Lexeme
                FileName +='.html'
            nombre = 'Tabla de clasificacion temporada {}'.format(Comando[2].Lexeme)
            arvg = Environment(loader=FileSystemLoader('Assets/'), autoescape = select_autoescape(['html']))
            template = arvg.get_template('Plantilla Tablas.html')
            html_file = open(FileName, 'w+', encoding='utf-8')
            html_file.write(template.render(nombre= nombre, TablaList = TablaList))
            html_file.close()
            startfile(FileName)
        if Comando[0].Lexeme == 'ADIOS':
            SendMessage('BOT','Gracias por utilizar este programa')
        
    else:
        SendMessage('BOT','Se ha producido un error en el comando, revisar el log de errores')

def bubble_sort_UP(data):
    for i in range(len(data) - 1):
        for j in range(0, len(data) - i - 1):
            if data[j].Puntos < data[j + 1].Puntos:
                    data[j], data[j + 1] = data[j + 1], data[j]
    return data

def SendMessage(sender, msg):
    global BoxMSG
    global BoxTXT

    if msg != '':
        msg1 = f"{sender}: {msg}\n\n"
        BoxTXT.config(state=NORMAL)
        BoxTXT.insert(END, msg1)
        BoxTXT.config(state=DISABLED)
        
def ReporteTokens():
    global TokenList
    FileName = 'Reporte de Tokens.html'
    nombre = 'Reporte de Tokens'
    arvg = Environment(loader=FileSystemLoader('Assets/'), autoescape = select_autoescape(['html']))
    template = arvg.get_template('Plantilla Reportes.html')
    html_file = open(FileName, 'w+', encoding='utf-8')
    html_file.write(template.render(nombre= nombre, TokenList = TokenList))
    html_file.close()
    startfile(FileName)

def ReporteErrores():
    global LexicalError, SyntacticalError
    FileName = 'Reporte de Errores.html'
    nombre = 'Reporte de Errores'
    arvg = Environment(loader=FileSystemLoader('Assets/'), autoescape = select_autoescape(['html']))
    template = arvg.get_template('Plantilla Errores.html')
    html_file = open(FileName, 'w+', encoding='utf-8')
    html_file.write(template.render(nombre= nombre, LexicalError = LexicalError, SyntacticalError = SyntacticalError))
    html_file.close()
    startfile(FileName)

def manual_usuario():
        webbrowser.open_new('Manuales\Manual de Usuario.pdf')

def manual_tecnico():
        webbrowser.open_new('Manuales\Manual Tecnico.pdf')


if __name__ == '__main__':
    chatGUI()
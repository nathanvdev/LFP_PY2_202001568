class Partidos:
    def __init__(self, Date, Temp, Journey, Local, Visit, GoalsL, GoalsV):
        self.Date = Date
        self.Temp = Temp
        self.Journey = Journey
        self.Local = Local
        self.Visit = Visit
        self.GoalsL = GoalsL
        self.GoalsV = GoalsV

    def ShowMatch(self):
        print(self.Date, self.Temp, self.Journey, self.Local, self.Visit, self.GoalsL, self.GoalsV)

    def getPartido(self):
        str = 'El Resultado de este partido fue: {} {} - {} {}'.format(self.Local, self.GoalsL, self.Visit, self.GoalsV)
        return str



class TokenObject:
    def __init__(self, Type, Lexeme):
        self.Type = Type
        self.Lexeme = Lexeme
    
    def ShowToken(self):
        print('tipo:', self.Type, '==\t', self.Lexeme)


class Tabla:
    def __init__(self, Name):
        self.POS = 0
        self.Name = Name
        self.PJ = 0
        self.G = 0
        self.E = 0
        self.P = 0
        self.DF = 0
        self.PTS = 0
        self.logo = ''
        self.Blogo = False

    def getPoints(self):
        print(self.Equipo, self.Puntos)
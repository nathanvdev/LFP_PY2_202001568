
import unicodedata


class Partidos:
    def __init__(self, Date, Temp, Journey, Local, Visit, GoalsL, GoalsV):
        self.Date = Date
        self.Temp = Temp
        self.Journey = Journey
        self.Local = Local
        self.Icon1 = ''
        self.Icon2 = ''
        self.Visit = Visit
        self.GoalsL = GoalsL
        self.GoalsV = GoalsV

        logos = open("Assets/logos.txt", "r")
        LocalFind = str(self.Local)
        VisitFind = str(self.Visit)
        LocalFind = LocalFind.lower().replace(' ','-')
        LocalFind = LocalFind.replace("ñ", "#").replace("Ñ", "%")
        LocalFind = unicodedata.normalize("NFKD", LocalFind)\
                .encode("ascii","ignore").decode("ascii")\
                .replace("#", "ñ").replace("%", "Ñ")

        VisitFind = VisitFind.lower().replace(' ','-')
        VisitFind = VisitFind.replace("ñ", "#").replace("Ñ", "%")
        VisitFind = unicodedata.normalize("NFKD", VisitFind)\
                .encode("ascii","ignore").decode("ascii")\
                .replace("#", "ñ").replace("%", "Ñ")
        
        for line in logos:
            LogoCode = line.split('.')
            LogoCode[3] = LogoCode[3].split(' ')

            if LocalFind in LogoCode[3][0]:
                self.Icon1 = LogoCode[3][0]
                self.Icon1 = 'shield-sprite xl {}'.format(self.Icon1)
                break
            elif VisitFind in LogoCode[3][0]:
                self.Icon2 = LogoCode[3][0]
                self.Icon2 = 'shield-sprite xl {}'.format(self.Icon2)
                break



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
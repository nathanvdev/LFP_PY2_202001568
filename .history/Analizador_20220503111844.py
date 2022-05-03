from ast import Pass
from Objects import TokenObject

Reserved =['RESULTADO','VS','TEMPORADA','JORNADA','GOLES','PARTIDOS','TOP','ADIOS','TABLA']
Cond1 = ['LOCAL','VISITANTE','TOTAL']
Cond2 = ['SUPERIOR','INFERIOR']
Flags = ['-','f','j','i','f','n']
TokenList = []
LexicalError = []
SyntacticalError = []
InsertedCommand = []
LexiconApproved = True
SyntacticalApproved = False


def DefineState(character):
    if character.isupper():
        return 1
    elif character == '"' or character == "'":
        return 2
    elif character == '<':
        return 3
    elif character == '-':
        return 4
    elif character.isdigit():
        return 5
    elif character.isalpha():
        return 6
    else:
        return 0

def LexiconAnalyzer(string):
    global LexiconApproved, InsertedCommand
    LexiconApproved = True
    InsertedCommand = []
    string += ' '
    State = 0
    Buffer = ''
    Column = 0
    for character in string:
        Column += 1
        if State == 0:
            State = DefineState(character)

        if State == 1:
            State = DefineState(character)
            if State != 1:
                if Buffer in Reserved:
                    NewToken = TokenObject('RESERVED', Buffer, Column)
                    TokenList.append(NewToken)
                    InsertedCommand.append(NewToken)
                    NewToken.ShowToken()
                    Buffer = ''
                    State = 0
                elif Buffer in Cond1:
                    NewToken = TokenObject('COND1', Buffer, Column)
                    TokenList.append(NewToken)
                    InsertedCommand.append(NewToken)
                    NewToken.ShowToken()
                    Buffer = ''
                    State = 0
                elif Buffer in Cond2:
                    NewToken = TokenObject('COND2', Buffer, Column)
                    TokenList.append(NewToken)
                    InsertedCommand.append(NewToken)
                    NewToken.ShowToken()
                    Buffer = ''
                    State = 0
                else:
                    NewToken = TokenObject('ERROR', Buffer, Column)
                    LexicalError.append(NewToken)
                    NewToken.ShowToken()
                    Buffer = ''
                    State = 0
                    LexiconApproved = False
            else:
                Buffer += character

        elif State == 2:
            if Buffer.count('"') == 2 or Buffer.count("'") == 2:
                Buffer = Buffer.replace('"','')
                Buffer = Buffer.replace("'","")
                token = TokenObject('STR', Buffer, Column)
                TokenList.append(token)
                InsertedCommand.append(token)
                token.ShowToken()
                State = 0
                Buffer = ''
            else:
                Buffer += character
        
        elif State == 3:
            if character == '<':
                Buffer = character
            elif character.isdigit() or character == '-':
                Buffer += character
            elif character == '>':
                Buffer += character
                if len(Buffer) == 11:
                    Buffer = Buffer.replace('<','')
                    Buffer = Buffer.replace(">","")
                    token = TokenObject('TEMP', Buffer, Column)
                    TokenList.append(token)
                    InsertedCommand.append(token)
                    token.ShowToken()
                    State = 0
                    Buffer = ''
                else:
                    NewToken = TokenObject('ERROR', Buffer, Column)
                    LexicalError.append(NewToken)
                    NewToken.ShowToken()
                    Buffer = ''
                    State = 0
                    LexiconApproved = False

        elif State == 4:
            if character in Flags:
                Buffer += character
            else:
                token = TokenObject('FLAG', Buffer, Column)
                TokenList.append(token)
                InsertedCommand.append(token)
                token.ShowToken()
                if token.Lexeme == '-f':
                    State = 6
                else:
                    State = 0
                if character == ' ' or character == '[' or character == ']':
                    Buffer = ''
                else: 
                    Buffer = character

        elif State == 5:
            if character.isdigit():
                Buffer += character
            else:
                if len(Buffer) > 0 and len(Buffer) < 3:
                    token = TokenObject('NUM', Buffer, Column)
                    TokenList.append(token)
                    InsertedCommand.append(token)
                    token.ShowToken()
                    State = 0
                    if character == ' ':
                        Buffer = ''
                    else: 
                        Buffer = character
                else:
                    NewToken = TokenObject('ERROR', Buffer, Column)
                    LexicalError.append(NewToken)
                    NewToken.ShowToken()
                    Buffer = ''
                    State = 0
                    LexiconApproved = False
        
        elif State == 6:
            if character == ' ':
                Error = True
                for x in range(len(InsertedCommand)):
                    if InsertedCommand[x].Lexeme == '-f':
                        token = TokenObject('NAME', Buffer, Column)
                        TokenList.append(token)
                        InsertedCommand.append(token)
                        token.ShowToken()
                        Buffer = ''
                        State = 0
                        Error = False
                        break

                if Error:
                    NewToken = TokenObject('ERROR', Buffer, Column)
                    LexicalError.append(NewToken)
                    NewToken.ShowToken()
                    Buffer = ''
                    State = 0
                    LexiconApproved = False
            else:
                Buffer += character
    
    if Buffer != '' and Buffer != ' ':
        Buffer = Buffer[:-1]
        

    return InsertedCommand

def SyntacticAnalizer(command: list):
    global LexiconApproved, SyntacticalApproved
    SyntacticalApproved = True
    while SyntacticalApproved:

        if command[0].Lexeme == 'RESULTADO':
            if len(command) > 1: 
                if command[1].Type != 'STR':
                    SyntacticalError.append(command[1])
                    SyntacticalApproved = False
                    break
                    
            if len(command) > 2:
                if command[2].Lexeme != 'VS':
                    SyntacticalError.append(command[2])
                    SyntacticalApproved = False
            
            if len(command) > 3:
                if command[3].Type != 'STR':
                    SyntacticalError.append(command[3])
                    SyntacticalApproved = False
            
            if len(command) > 3: 
                if command[4].Lexeme != 'TEMPORADA':
                    SyntacticalError.append(command[4])
                    SyntacticalApproved = False
            
            if len(command) > 4:
                if command[5].Type != 'TEMP':
                    SyntacticalError.append(command[5])
                    SyntacticalApproved = False
            break
        
        elif command[0].Lexeme == 'JORNADA':
            if len(command) > 1:
                if command[1].Type != 'NUM':
                    SyntacticalError.append(command[1])
                    SyntacticalApproved = False

            if len(command) > 2:
                if command[2].Lexeme != 'TEMPORADA':
                    SyntacticalError.append(command[2])
                    SyntacticalApproved = False

            if len(command) > 3: 
                if command[3].Type != 'TEMP':
                    SyntacticalError.append(command[3])
                    SyntacticalApproved = False

            if len(command) > 4:
                if command[4].Lexeme == '-f':
                    if command[5].Type != 'NAME':
                        SyntacticalError.append(command[5])
                        SyntacticalApproved = False
                elif len(command) > 4:
                    SyntacticalError.append(command[1])
                    SyntacticalApproved = False
            break

        elif command[0].Lexeme == 'GOLES':
            if len(command) > 1:
                if command[1].Type != 'COND1':
                    SyntacticalError.append(command[1])
                    SyntacticalApproved = False

            if len(command) > 1:
                if command[2].Type != 'STR':
                    SyntacticalError.append(command[2])
                    SyntacticalApproved = False
            
            if len(command) > 3:
                if command[3].Lexeme != 'TEMPORADA':
                    SyntacticalError.append(command[3])
                    SyntacticalApproved = False
            
            if len(command) > 4:
                if command[4].Type != 'TEMP':
                    SyntacticalError.append(command[4])
                    SyntacticalApproved = False
            break

        elif command[0].Lexeme == 'TABLA':
            if len(command) > 1:
                if command[1].Lexeme != 'TEMPORADA':
                    SyntacticalError.append(command[1])
                    SyntacticalApproved = False
            
            if len(command) > 2:
                if command[2].Type != 'TEMP':
                    SyntacticalError.append(command[2])
                    SyntacticalApproved = False

            if len(command) > 3:
                if command[3].Lexeme == '-f':
                    if command[4].Type != 'NAME':
                        SyntacticalError.append(command[4])
                        SyntacticalApproved = False
                elif len(command) > 3:
                    SyntacticalError.append(command[3])
                    SyntacticalApproved = False
            break

        elif command[0].Lexeme == 'PARTIDOS':
            if len(command) > 1:
                if command[1].Type != 'STR':
                    SyntacticalError.append(command[1])
                    SyntacticalApproved = False

            if len(command) > 2:
                if command[2].Lexeme != 'TEMPORADA':
                    SyntacticalError.append(command[2])
                    SyntacticalApproved = False
            
            if len(command) > 3:
                if command[3].Type != 'TEMP':
                    SyntacticalError.append(command[3])
                    SyntacticalApproved = False

            if len(command) > 4: 
                if command[4].Lexeme == '-f':
                    if command[5].Type != 'NAME':
                        SyntacticalError.append(command[5])
                        SyntacticalApproved = False
                elif len(command) > 4:
                    if command[4].Lexeme == '-ji' or command[4].Lexeme == '-jf':
                        if command[5].Type != 'NUM':
                            SyntacticalError.append(command[5])
                            SyntacticalApproved = False
                    else:
                        SyntacticalApproved = False
                        SyntacticalError.append(command[4])

            if len(command) > 6:
                if command[6].Lexeme == '-f':
                    if command[7].Type != 'NAME':
                        SyntacticalError.append(command[7])
                        SyntacticalApproved = False
                elif len(command) > 6:
                    if command[6].Lexeme == '-ji' or command[6].Lexeme == '-jf':
                        if command[7].Type != 'NUM':
                            SyntacticalError.append(command[7])
                            SyntacticalApproved = False
                    else:
                        SyntacticalApproved = False
                        SyntacticalError.append(command[6])
            
            elif len(command) > 8:
                if command[8].Lexeme == '-ji' or command[8].Lexeme == '-jf':
                    if command[9].Type != 'NUM':
                        SyntacticalError.append(command[9])
                        SyntacticalApproved = False
                else:
                    SyntacticalApproved = False
                    SyntacticalError.append(command[8])
            break

        elif command[0].Lexeme == 'TOP':
            if len(command) > 1:
                if command[1].Type != 'COND2':
                    SyntacticalApproved = False
                    SyntacticalError.append(command[1])
            
            if len(command) > 2:
                if command[2].Lexeme != 'TEMPORADA':
                    SyntacticalApproved = False
                    SyntacticalError.append(command[2])
            
            if len(command) > 3:
                if command[3].Type != 'TEMP':
                    SyntacticalApproved = False
                    SyntacticalError.append(command[3])

            if len(command) > 4:
                if command[4].Lexeme == '-n':
                    if command[5].Type != 'NUM':
                        SyntacticalApproved = False
                        SyntacticalError.append(command[5])
            break
        
        elif command[0].Lexeme == 'ADIOS':
            break

        else:
            SyntacticalError.append(command[0])
            SyntacticalApproved = False

    
    return SyntacticalApproved, LexiconApproved


        
        
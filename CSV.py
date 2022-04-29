import csv
from Objects import Partidos

def FileUpload():
    PartidosList = []
    with open('Assets\LaLigaBot-LFP.csv', newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            if row[2].isdigit(): 
                partido = Partidos(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
                PartidosList.append(partido)
        return PartidosList



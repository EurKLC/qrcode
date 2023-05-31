# -*- coding: utf-8 -*-
"""
@author: EurKLC
"""

import pyqrcode
import numpy as np
codinLatex = 'iso-8859-1' # l'encodage utilisé par latex pour les problèmes d'accents



# Côté du carré de réponses (donc n^2 questions)
n = 5



# On crée le QRcode
qr = pyqrcode.create("https://bit.ly/3HFV4du",error='L')





# On crée la matrice de QRcode dans laquelle on enlève des cases du coin inférieur droit de jusqu'à la limite de ce que le QR code puisse encaisser 
l = qr.text().split("\n")[4:-5]
for i in range(len(l)):
    l[i] = l[i][4:-4]


width = len(l[0])
height = width


QR = np.zeros((height, width))
for i in range(height):
    for j in range(width):
        QR[i,j] = int(l[i][j])


#On modifie 42 cases pour ne plus tolérer aucune réponse fausse

for i in range(18,width):
    for j in range(19,height):
        QR[i,j] = 1 - QR[i,j]




Grilles = []
Grilles.append(QR[ 10 : 15 , 10 : 15  ])




# On crée la liste des question et le liste des réponses (1 pour vrai, 0 pour faux)

fichier = open("questions.tex","r")
text = fichier.read()
fichier.close()
liste = text.split("\question")[1:]
questions = []
reponses = []


for m in liste:
    l = m.split("\\reponse")
    questions.append(l[0].encode(codinLatex).decode('utf8'))
    if ("Vrai" in l[1]) or ("vrai" in l[1]):
        reponses.append(1)
    else:
        reponses.append(0)






# Prend une grille et renvoie le tikzpicture correspondant
def grilleToText(grille):
    a,b = np.shape(grille)
    text = "\\begin{tikzpicture}[scale = \echelle ]\n"

    for i in range(a):
        for j in range(b):
            J = a-i-1
            I = j
            if grille[i,j] == 0:
                text += "\draw [line width=0,black] (" + str(I) + "," + str(J) + ") rectangle (" +  str((I+1))  + "," + str((J+1)) +");\n"
            else:
                text += "\draw [black, fill = black] (" + str(I) + "," + str(J) + ") rectangle (" +  str((I+1))  + "," + str((J+1)) +");\n"

    text += "\end{tikzpicture}"

    return text.encode('utf8').decode(codinLatex)

# Prend en entré un entier m en renvoie le text tikzpicture d'une grille vierge de dimension  m x m avec lignes et colonnes numérotés 
def grilleViergeToText(m):
    text = "\\begin{tikzpicture}[scale = \echelle ]\n"
    l = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

    for i in range(m):
        for j in range(m):
            J = m-i-1
            I = j
            text += "\draw [line width=0,black] (" + str(I) + "," + str(J) + ") rectangle (" +  str((I+1))  + "," + str((J+1)) +");\n"
    
    for i in range(m):
        text += "\draw  (" + str(-0.5) + "," + str( m-i-0.5) + ") node {" + l[i] + "  };\n"
    for j in range(m):
        text += "\draw  (" + str(j+0.5) + "," + str( m + 0.5) + ") node {" + str(j+1) + "  };\n"

    text += "\end{tikzpicture}"

    return text.encode('utf8').decode(codinLatex)

"""
Devenu inutile
# Prend une grille et renvoie le tikzpicture numéroté correspondant
def grilleToTextNumerote(grille):
    a,b = np.shape(grille)
    text = "\\vspace*{7mm}\n\\begin{center}\n\\begin{tikzpicture}[scale = \echelle ]\n"

    for i in range(a):
        for j in range(b):
            J = a-i-1
            I = j
            text += "\draw [line width=0,black] (" + str(I) + "," + str(J) + ") rectangle (" +  str((I+1))  + "," + str((J+1)) +");\n\draw [gray] (" + str(I+0.5) + "," + str(J+0.5) +") node {" + str(i*n+j+1) +"};\n"
            

    text += "\end{tikzpicture}\n\end{center}\n\n"

    return text.encode('utf8').decode(codinLatex)
"""


# Texte avec une grille donnée

def qcm(grille):
    a,b = np.shape(grille)
    text=""

    m1 = "\\begin{center}\n $\square$ Vrai \quad\quad\quad\quad\quad\quad $\\blacksquare$ Faux\n \end{center}"
    m2 = "\\begin{center}\n $\\blacksquare$ Vrai \quad\quad\quad\quad\quad\quad $\square$ Faux\n \end{center}"

    for i in range(a):
        for j in range(b):
            text += "\question " + questions[i*b+j] +"\n\\nopagebreak" + "\n"

            if grille[i,j]==1 and reponses[i*b+j] ==1:
                text += m2
            elif grille[i,j]==1 and reponses[i*b+j] ==0:
                text += m1
            elif grille[i,j]==0 and reponses[i*b+j] ==1:
                text += m1
            elif grille[i,j]==0 and reponses[i*b+j] ==0:
                text += m2
            
            text += "\n"

    return text


# Texte pour la section Enoncés


def enonces():
    text = "\cleardoublepage\n\section{\\'Enoncés}\n\setcounter{NumQLigne}{1}\n\setcounter{NumQColonne}{1}\n"

    i=1
    for grille in Grilles:
        text += qcm(grille)
        text += "\n\cleardoublepage\n"
        i+=1
    
    return text.encode('utf8').decode(codinLatex)



# Texte d'introduction.
def entete():
    fichier = open("entete.tex","r")
    text = fichier.read()
    fichier.close()
    return text

# Texte Sommaire
def sommaire():
    text = "\cleardoublepage\n\\tableofcontents\n\n"
    return text.encode('utf8').decode(codinLatex)


# Texte de la section grilles solutions
def grillesSolutions():
    text = "\cleardoublepage\n\section{Grilles solutions}\n"
    
    text += "\\begin{multicols}{3}\n\setlength{\columnseprule}{0pt}\n\\begin{enumerate}"

    for grille in Grilles:
        text += "\item ~ \n\\begin{center}\n" + grilleToText(grille) + "\n\end{center}\n"

    text += "\end{enumerate}\n\end{multicols}"
    return text.encode('utf8').decode(codinLatex)


# Texte de la section grilles supplémentaires vierges (m grilles supplémentaire)
def grillesViergesSupplementaires(m):
    text = "\cleardoublepage\n\section{Grilles vierges}\n"
    
    text += "\\begin{multicols}{3}\n\setlength{\columnseprule}{0pt}\n\\begin{enumerate}"

    for grille in range(m):
        text += "\item ~ \n\\begin{center}\n" + grilleViergeToText(n) + "\n\end{center}\n"

    text += "\end{enumerate}\n\end{multicols}"
    return text.encode('utf8').decode(codinLatex)

# Texte de la section Grille réponse
def grilleReponse():
    text = "\cleardoublepage\n\section{Grille réponse}\n\\begin{center}\n\\begin{tikzpicture}[scale = \echelle ]\n"
    a,b = np.shape(QR)
    for i in range(0,a):
        for j in range(0,b):
            if (i<10 or 14<i) or (j<10 or 14<j):
                J = a-i-1
                I = j
                if QR[i,j] == 0:
                    text += "\draw [line width=0,black] (" + str(I) + "," + str(J) + ") rectangle (" +  str((I+1))  + "," + str((J+1)) +");\n"
                else:
                    text += "\draw [black, fill = black] (" + str(I) + "," + str(J) + ") rectangle (" +  str((I+1))  + "," + str((J+1)) +");\n"
    
    

    text += "\end{tikzpicture}\n\end{center}\n"
    return text.encode('utf8').decode(codinLatex)


# Texte de la section Solution
def grilleSolution():
    text = "\cleardoublepage\n\section{Solution}\n\\begin{center}\n" + grilleToText(QR) + "\n\end{center}"
    return text.encode('utf8').decode(codinLatex)










with open('qrcode.tex', 'w') as f:
    f.write(entete() +  enonces() + grilleReponse() + grillesViergesSupplementaires(48)  + grilleSolution() + "\n\end{document}")
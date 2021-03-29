'''
Created on Oct 26, 2020

@author: bogdan
'''
import re
import string
from BST import *

''' Incarcare din file codurile simbolurilor intr-un dict'''
atom_cod={}
def atmcod(numefis):
    f=open(numefis,"r")
    for line in f:
        atom_cod[line.split()[0]]=line.split()[1]
atmcod("coduri.txt")
atom_cod[' ']=22
atom_cod[" "]=55
atom_cod['']=123

keywords=[]
'''Creare KEYWORDS'''




#daca nu e cuvant rezervat e identificator

'''TOKEN MAKER'''
''' Parcurge o linie litera cu litera, cand da de un separator creaza cuvantul
si il adauga intr-un vector, dupa care adauga si separatorul
'''

        

def TT_Maker(line):
    vect=[]
    stri=''
    for i in range(0,len(line)):
        if line[i] not in atom_cod:
            stri=stri+line[i]
        elif(line[i] in atom_cod):
            vect.append(stri)
            vect.append(line[i])
            stri=''
        elif(i==len(line)-1 and stri != ''):
            vect.append(stri)
    return vect

#print(TT_Maker("numb[1] = 3;"))

''' Verifica daca atm este scris gresit, daca e string si nu are gilimeaua inchisa / char si nu are apostroful 
input atm
output return false daca are eroare si true daca nu are 
'''
cifre=[1234567890]
def errConst(atm):
    if(atm[0]=="\"" and atm[len(atm)-1]!="\""): #daca nu se termina cu " return false
        return False
    if(atm[0]=="\"" and atm[len(atm)-1]=="\""): #daca se termina cu " si nu contine litere sau cifre return false
        for i in range(1,len(atm)-1):
            if(atm[i] not in string.ascii_letters or atm[i] not in cifre):
                return False
    if(atm[0]=="\'" and atm[len(atm)-1]!="\'" ): #analog string
        return False
    if(atm[0]=="\'" and atm[len(atm)-1]=="\'" ):
        if(len(atm)>3):
            return False
        if(len(atm)==3 and atm[1] not in string.ascii_letters or atm[1] not in cifre ):
            return False
    if(atm.isdigit()==False):
            return False
    return True
#print(errConst("a"))
'''Verificam daca atm este constant, adica daca string, char si int sunt scrise corect
string verificam daca contine cifre si litere
char daca este intre '' si daca are val 3(adica daca continec ele 2 ghilimele si un char)
int daca isdigit or not
daca sunt scrise bine returneaza true
'''
def isConst(atm):
    ok=True
    if(atm[0]=="\"" and atm[len(atm)-1]=="\"" ):
        for i in range(1,len(atm)-1):
            if(atm[i] in string.ascii_letters or atm[i]  in cifre):
                ok=True
            else:
                return False
    elif(atm[0]=="\'" and atm[len(atm)-1]=="\'"):
        if(atm[1] in string.ascii_letters or atm[1] in cifre ):
            ok=True
        else:
            return False
    elif(atm[0]=="\'" and atm[len(atm)-1]=="\'" and len(atm)>3 ):
        return False
    elif(atm.isdigit()==False):
        return False
    return ok
    
#print(isConst("1"))

#print (isConst(TT_Maker("{")))

def isIdent(atm):
    if(atm[0] not in string.ascii_letters):
        return False
    elif(atm[0] in string.ascii_letters):
        ok=True
        for i in range(1,len(atm)):
            if(atm[i] in string.ascii_letters or atm[i]  in cifre):
                ok=True
            else:
                return False
    return ok
        
    
#print(isIdent("1"))
'''Analizatorul lexical'''
FIP=[] #FIP care o sa fie un vector de tupluri (cod_atom,pozitie_arbore)

BST_ID=BinarySearchTree()   #Arborele binar pentru identificatori
BST_CT=BinarySearchTree()   #Arborele binar pentru constante

def Analizator(numefile):
    f=open(numefile,"r")
    j=1# numarul liniei
    i_ct=0
    i_id=0
    for line in f:
        tok=TT_Maker(line)
        for atm in tok:
            if atm in atom_cod:
                if(atom_cod[atm]!=123):
                    FIP.append((atom_cod[atm],))
            else:
                if(isConst(atm)==True): #daca este constanta 
                    if(findVal(atm,BST_CT)==False): #verificam daca se afla in tabela de dispersie    
                        BST_CT.put(i_ct, atm)#daca nu se afla il adaugam
                        i_ct=i_ct+1
                    FIP.append((atom_cod["ct"],i_ct))
                elif isIdent(atm) == True :
                    if(len(atm)>8):
                        print("Error: Identifier is too long",atm,"line: ",j) #daca are lungime mai mare de 8 eroare:
                        return
                    if(findVal(atm,BST_ID)==False): #verificam daca se afla in tabela de dispersie    
                        BST_ID.put(i_id, atm)#daca nu se afla il adaugam
                        i_id=i_id+1
                    FIP.append((atom_cod["id"],i_id))
                elif(isConst(atm)==False):
                    print("Error: Constant: ",atm,"is wrong","line:",j)
                    return
                elif(isIdent(atm)==False):
                    print("Error: Identifier: ",atm,"is wrong","line:",j)
                    return
                
        j=j+1
    print(FIP)
    
    print("BST CONSTANTE:")
    for i in range(len(BST_CT)):
        print(i, BST_CT[i])
    print("BST INDEX:")
    for i in range(len(BST_ID)):
        print(i, BST_ID[i])
        
    
Analizator("codulet.txt")                         
                            
#print(BST_CT[3])
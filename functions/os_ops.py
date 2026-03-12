import os
import subprocess as sp

paths = {
    'calculator': 'C:\\Windows\\System32\\calc.exe',
    'cursor': 'C:\\Users\\Jeff\\AppData\\Local\\Programs\\cursor\\Cursor.exe'
}

def openCalculator():
    pathCalc = paths['calculator']
    if os.path.exists(pathCalc):
        sp.Popen(pathCalc)
    else:
        print("No se encontró la calculadora en la ruta especificada.")

def openCursor():
    pathCursor = paths['cursor']
    if os.path.exists(pathCursor):
        sp.Popen(pathCursor)
    else:
        print("No se encontró Cursor en la ruta especificada.")
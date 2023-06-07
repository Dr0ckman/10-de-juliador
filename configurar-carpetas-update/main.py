import sqlite3
import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Tomar carpetas de 10 de Julio y cambiar archivos dependiendo de ID e IP que se encuentra en db.
# Logica basica:
# Si ADN es Maestro:
#   ConsWS/param.js -> Cambiar [IP] por IP del equipo.
#   GateGayWS/V26GateWay.exe.config -> Cambiar [IP] por IP del equipo.
#   Monitoreo/TP.config -> Cambiar [ID] por ID del equipo en forma 1xxx.
#   PantallaWS/param.js -> Cambiar [IP] por IP del equipo.

db = sqlite3.connect('db.db')
cur = db.cursor()

# Funciones

def isMaestro():
    if selected.get() == "Maestro":
        return True
    else:
        return False

def limpiarDatoQuery(datoQuery):
    word = ""

    for character in str(datoQuery):
        if character == "(" or character == ")" or character == "," or character == "'":
            character = ""
        word += character

    datoQuery = word
    return datoQuery

def generateNombreSucursal():
    nombreSucursal = cur.execute("select sucursal from Hoja1 where id = " + inputUsuario.get()).fetchone()
    nombreSucursal = limpiarDatoQuery(nombreSucursal)

    return nombreSucursal

def generateNombreEquipo():
    n = ""
    if 4 - len(inputUsuario.get()) >= 1:
        if isMaestro():
            n = "1"
        else:
            n = "2"
        nombreEquipo = "ADN-TUR" + n + "0" * (3 - len(inputUsuario.get())) + inputUsuario.get()

    else:
        nombreEquipo = "ADN-TUR" + n + inputUsuario.get()

    return nombreEquipo

def generateIp():
    ip = 0
    if isMaestro():
        ip = cur.execute("select maestro from Hoja1 where id = " + inputUsuario.get()).fetchone()
    else:
        ip = cur.execute("select esclavo from Hoja1 where id = " + inputUsuario.get()).fetchone()
    ip = limpiarDatoQuery(ip)

    return ip

def verificar(event):
    nombreSucursal = generateNombreSucursal()
    textoEntryNombreSucursal.set(nombreSucursal)
    nombreEquipo = generateNombreEquipo()
    textoEntryNombreEquipo.set(nombreEquipo)

def generateCarpetas():
    pathArchivos = os.path.join("Archivos generados", generateNombreEquipo() + " " + generateNombreSucursal())
    if not os.path.exists(os.path.join(pathArchivos, "ConsWS")):
        os.makedirs(os.path.join(pathArchivos, "ConsWS"))
    if not os.path.exists(os.path.join(pathArchivos, "GateWayWS")):
        os.makedirs(os.path.join(pathArchivos, "GateWayWS"))
    if not os.path.exists(os.path.join(pathArchivos, "Monitoreo")):
        os.makedirs(os.path.join(pathArchivos, "Monitoreo"))
    if not os.path.exists(os.path.join(pathArchivos, "PantallaWS")):
        os.makedirs(os.path.join(pathArchivos, "PantallaWS"))

def configurar():
    ip = generateIp()
    generateCarpetas()

    listaArchivosIp = [os.path.join("ConsWS", "param.js"),
                    os.path.join("GateWayWS", "V26GateWay.exe.config"),
                    os.path.join("Monitoreo", "TP.config"),
                    os.path.join("PantallaWS", "param.js")]

    for carpeta in listaArchivosIp:
        f = open(os.path.join("files", carpeta), "r")
        fileContents = f.read().replace("[IP]", ip).replace("[ID]", generateNombreEquipo())

        f.close()

        f = open(os.path.join("Archivos generados", generateNombreEquipo() + " " + generateNombreSucursal(), carpeta), "w+")
        f.write(fileContents)
        f.close()

    messagebox.showinfo(message="Archivos configurados con datos:\n\nIP: " + str(generateIp()) + "\nID: " + str(generateNombreEquipo()), title="Archivos generados correctamente")


root = Tk()
root.geometry("550x200")
root.title("Configurar archivos actualizacion")
root.resizable(0, 0)

frmIzq = ttk.Frame(root, padding=20, borderwidth=0)
frmIzq.grid(column=0, row=0, sticky='nw')
frmDer = ttk.Frame(root, padding=20, borderwidth=0)
frmDer.grid(column=2, row=0, sticky='ne')

ttk.Label(frmIzq, text="ID Sucursal").grid(column=0, row=0, sticky='w', pady=(4, 3))
inputUsuario = StringVar()

opcionesCBox = []
for id in cur.execute("select id from Hoja1"):
    opcionesCBox.append(id)

entryIDSucursal = ttk.Combobox(frmDer, state="readonly",textvariable=inputUsuario, values=opcionesCBox)
entryIDSucursal.grid(column=0, row=0)
entryIDSucursal.bind("<<ComboboxSelected>>", verificar)

ttk.Label(frmIzq, text="Nombre Sucursal").grid(column=0, row=1, pady=(4, 3), sticky='w')
textoEntryNombreSucursal = StringVar()
entryNombreSucursal = ttk.Entry(frmDer, state="disabled", textvariable=textoEntryNombreSucursal).grid(column=0, row=1) # Configurar esto cuando se ingrese el ID para que muestre el nombre de sucursal

ttk.Label(frmIzq, text="Nombre Equipo").grid(column=0, row=2, sticky='w')

textoEntryNombreEquipo = StringVar()
entryNombreEquipo = ttk.Entry(frmDer, state="disabled", textvariable=textoEntryNombreEquipo).grid(column=0, row=3)

buttonConfigurar = ttk.Button(frmDer, text="Configurar archivos", command=configurar).grid(column=0, row=4, sticky='ew')

selected = StringVar()
selected.set("Maestro")
ttk.Radiobutton(frmDer, text="Esclavo", value="Esclavo",variable=selected, command=lambda: verificar(None)).grid(column=3, row=0, sticky='e')
ttk.Radiobutton(frmDer, text="Maestro", value="Maestro",variable=selected, command=lambda: verificar(None)).grid(column=2, row=0, sticky='e', padx=(10,0))

root.mainloop()
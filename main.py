import subprocess
from tkinter import *
import os
import sys
#Entorno virtual: .\regalitosfinal\Scripts\activate
#Ventana Raiz
class Ventana(Frame):
    def __init__(self, ventanaMain=None):
        super().__init__(ventanaMain, bg='#D9D9D9')
        self.ventanaMain = ventanaMain
        self.pack(fill=BOTH, expand=True)
        self.decoraciones()


#Función para abrir el modulo Inventario
    def fInventario(self):
        try:
            self.ventanaMain.destroy()
            #os.system(f"{sys.executable} inventario.py")
            subprocess.run(['python', 'inventario.py'])
        except Exception as e:
            print('Oh, ha ocurrido un error: ', type(e))

#Función para abrir el modulo Ventas
    def fVentas(self):
        try:
            self.ventanaMain.destroy()
            #os.system(f"{sys.executable} ventas.py")
            subprocess.run(['python', 'ventas.py'])
        except Exception as e:
            print('Oh, ha ocurrido un error: ', type(e))


#Función para abir el modulo Reportes
    def fReportes(self):
        try:
            self.ventanaMain.destroy()
            #os.system(f"{sys.executable} reportes.py")
            subprocess.run(['python', 'reportes.py'])
        except Exception as e:
            print('Oh, ha ocurrido un error: ', type(e))


#Interfáz gráfica
    def decoraciones(self):
############################ CONTENEDORES ############################
        # Frame encabezado de pagina
        frame2 = Frame(self, bg='#7D7D7D')
        frame2.pack(side=TOP, fill=X)

        # Frame para colocar los botones
        frameButtons = Frame(self, bg='#D9D9D9')
        frameButtons.pack(pady=20)

        # Frame pie de pagina
        frame1 = Frame(self, bg='#6F6B6B')
        frame1.pack(side=BOTTOM, fill=X)

############################ BOTONES ############################
        self.bInventario = Button(frameButtons, text='Revisar el inventario', command=self.fInventario, bg='gray', fg='white', font=('Arial black', 12), justify='center', wraplength=120)
        self.bInventario.pack(side=LEFT, padx=10)

        self.bVentas = Button(frameButtons, text='Vender', command=self.fVentas, bg='gray', fg='white', font=('Arial black', 12))
        self.bVentas.pack(side=LEFT, padx=10)

        self.bReportes = Button(frameButtons, text='Ver reporte', command=self.fReportes, bg='gray', fg='white', font=('Arial black', 12))
        self.bReportes.pack(side=LEFT, padx=10)

############################ TEXTO ############################
        lb1 = Label(frame2, text="Regalitos.py", bg='#7D7D7D', font=("Arial Black", 50))
        lb1.pack(pady=10)

        lb2 = Label(frame2, text="Bienvenido, ¿qué deseas hacer hoy?", bg='#7D7D7D', font=("Arial Black", 15), justify='center', fg='white')
        lb2.pack(pady=10)


def main():
    ventanaMain = Tk()
    ventanaMain.title('Regalitos.py - Bienvenido')
    ventanaMain.resizable(True, True)
    ventanaMain.geometry('800x500')

    app = Ventana(ventanaMain=ventanaMain)
    app.mainloop()
    

if __name__ == "__main__":
    main()

import datetime
import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
import sqlite3
import uuid
from datetime import datetime

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Ventas")
        self.geometry("800x600")
        self.resizable(True, True)
        self.decoracionesVentas()
        self.articulos_venta = {} 
        self.iconbitmap('img\icono16.ico')
       
        
        self.monto.bind('<KeyRelease>', self.onMontoChanged)

    def decoracionesVentas(self):
        ################################## Contenedores ##########################################
        # Encabezado de página
        self.frame1 = Frame(self, bg='#B5B5B5')
        self.frame1.pack(side=TOP, fill=X)

        # Ventas
        self.lb1 = Label(self.frame1, text="Ventas", bg='#B5B5B5', font=("Arial Black", 50))
        self.lb1.pack(anchor='center', fill=BOTH)

        # Contenedor Añadir a la compra
        self.frame2 = Frame(self, bg='#D9D9D9')
        self.frame2.pack(side=TOP, fill=X, padx=0, pady=0)

        # Contenedor Resumen de venta
        self.frame4 = Frame(self, bg='#B5B5B5')
        self.frame4.pack(side=RIGHT,fill=Y, padx=10, pady=10)#fill=BOTH side=RIGHT

        #SubContenedores Resumen de venta
        self.subF5 = Frame(self.frame4, bg='#B5B5B5')
        self.subF5.pack(side=TOP, fill=X, padx=5,pady=2)
        self.subF1 = Frame(self.frame4, bg='#B5B5B5')
        self.subF1.pack(anchor='n', fill=X, padx=5, pady=5)
        self.subF6 = Frame(self.frame4, bg='#B5B5B5')
        self.subF6.pack(side=BOTTOM, fill=X, padx=5, pady=5)
        self.subF4 = Frame(self.frame4,bg='#B5B5B5')
        self.subF4.pack(side=BOTTOM, fill=X, padx=5,pady=2)
        self.subF3 = Frame(self.frame4, bg='#B5B5B5')
        self.subF3.pack(side=BOTTOM, fill=X, padx=5,pady=2)
        self.subF2 = Frame(self.frame4, bg='#B5B5B5')
        self.subF2.pack(side=BOTTOM, fill=X, padx=5, pady=5)

        # Contenedor botones inferiores
        self.frame3 = Frame(self, bg='#D9D9D9')
        self.frame3.pack(side=BOTTOM, fill=X, padx=10, pady=10)

        # Contenedor Tabla de productos
        self.frame5 = Frame(self, bg='#B5B5B5')
        self.frame5.pack(anchor='w', fill=BOTH, expand=TRUE, padx=15, pady=10)



        ################################## Botones ##############################################
        # Cancelar Venta
        self.bCancelar = Button(self.frame1, text='Cancelar venta', command=self.fCancelar, bg='#BB0E0E', fg='white',
                                font=("Arial Black",9), highlightbackground='#D9D9D9', 
                                width=15, height=2)
        self.bCancelar.pack(side=LEFT, padx=15, pady=10)
        # Regresar
        self.bRegresar = Button(self.frame1, text='Regresar', command=self.fRegresar, bg='#D9D9D9',
                                font=("Arial Black",9), highlightbackground='#D9D9D9', 
                                width=10, height=2)
        self.bRegresar.pack(side=RIGHT, padx=15, pady=10)
        
        # Añadir a la compra
        self.bAnadir = Button(self.frame2, text='Añadir a la compra', command=self.fAnadirCompra, bg='#088484', fg='white',
                                font=("Arial Black",9), highlightbackground='#D9D9D9', 
                                width=20)
        self.bAnadir.pack(side=LEFT, padx=15, pady=10)
        # Barra Añadir a la compra
        self.barra_b = Entry(self.frame2, bg='#B5B5B5')
        self.barra_b.pack(side=LEFT, expand=True, padx=15, pady=10, fill=X) 
        self.barra_b.focus()

        # Quitar articulo
        self.bQuitar = Button(self.frame3, text='Quitar articulo', command=self.fQuitar, bg='#F0E158',fg='white', 
                                font=("Arial Black",9), highlightbackground='#D9D9D9', 
                                width=20)
        self.bQuitar.pack(side=LEFT, padx=5, pady=10)
        # Articulo especial
        self.bEspecial = Button(self.frame3, text='Artículo especial', command=self.fEspecial, bg='#3BDFDF',fg='white',
                                font=("Arial Black",9), highlightbackground='#D9D9D9', 
                                width=20)
        self.bEspecial.pack(side=LEFT, padx=15, pady=10)
        # Buscar existencia
        self.bBuscar = Button(self.frame3, text='Buscar existencia', command=self.fBuscar, bg='#D017B3',fg='white',
                                font=("Arial Black",9), highlightbackground='#D9D9D9', 
                                width=20)
        self.bBuscar.pack(side=LEFT, padx=15, pady=10)
        #Escaner 
        self.bEscaner = tk.Button(self.frame3, text='Escanear',command=self.escanerBarras, bg='#234AD7',
                              font=("Arial Black",9),fg='white',width= 20)
        self.bEscaner.pack(side=LEFT, padx=15, pady=10)
        # Confirmar venta
        self.bVenta = Button(self.subF6, text='Confirmar venta', command=self.fConfirmar, bg='#088423',fg='white',
                                font=("Arial Black",9), highlightbackground='#D9D9D9', 
                                width=20)
        self.bVenta.pack(side=BOTTOM, padx=15, pady=10)



        ##################################### Texto #####################################
        #Resumen de venta
        self.resumen = Label(self.subF5, text='Resumen venta', fg='white', bg='#B5B5B5', font=("Arial Black", 12))
        self.resumen.pack(side=TOP, padx=10)

        #Monto recibido
        self.txtMonto = Label(self.subF1, text='Se recibe:', fg='black',bg='#B5B5B5',font=("Arial Black", 12))
        self.txtMonto.pack(side=LEFT, padx=5, pady=5)
        self.monto = Entry(self.subF1)
        self.monto.pack(side=LEFT, padx=5, pady=5)

        #Cambio
        self.cambio = Label(self.subF4, text='Cambio:', fg='#A20C0C',bg='#B5B5B5',font=("Arial Black", 12))
        self.cambio.pack(side=LEFT, padx=5, pady=5)
        self.cambioE = Entry(self.subF4)
        self.cambioE.pack(side=LEFT, padx=5, pady=5)


        #Total
        self.total = Label(self.subF3, text='Total:', fg='green',bg='#B5B5B5',font=("Arial Black", 12))
        self.total.pack(side=LEFT, padx=5, pady=5)
        self.totalE = Entry(self.subF3)
        self.totalE.pack(side=LEFT, padx=5, pady=5)

        #Articulos
        self.articulos = Label(self.subF2, text='Artículos:',fg='black',bg='#B5B5B5',font=("Arial Black", 12))
        self.articulos.pack(side=LEFT, padx=5, pady=5)
        self.articulosE = Entry(self.subF2)
        self.articulosE.pack(side=LEFT, padx=5, pady=5)


        ##################################### Tabla ##################################################
        scrollbar = ttk.Scrollbar(self.frame5)
        scrollbar.pack(side= RIGHT, fill=Y)

        self.tabla = ttk.Treeview(self.frame5,yscrollcommand=scrollbar.set)
        self.tabla.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.tabla.yview)
        
        self.tabla['columns'] = ('Cantidad', 'Nombre','Código', 'Precio unitario')
        self.tabla.column('#0', width=0, stretch=tk.NO)
        self.tabla.column('Cantidad', anchor=tk.CENTER, width=50)
        self.tabla.column('Nombre', anchor=tk.W, width=100)
        self.tabla.column('Código', anchor=tk.CENTER, width=100)
        self.tabla.column('Precio unitario', anchor=tk.CENTER, width=100)

        self.tabla.heading('#0', text='', anchor=tk.CENTER)
        self.tabla.heading('Cantidad', text='Cantidad', anchor=tk.CENTER)
        self.tabla.heading('Nombre', text='Nombre', anchor=tk.CENTER)
        self.tabla.heading('Código', text='Código', anchor=tk.CENTER)
        self.tabla.heading('Precio unitario', text='Precio unitario', anchor=tk.CENTER)


    def fRegresar(self):
        self.withdraw()
        os.system(f"{sys.executable} main.py")

    def escanerBarras(self):
        pass
#################################################################
    def fAnadirCompra(self):
        # 1. Verificar que se ha ingresado un dato en el Entry barra_b
        producto = self.barra_b.get()#.strip()
        if not producto:
            return

        # 2. Realizar la búsqueda en la base de datos
        conexion = sqlite3.connect('regalitosdb.db')
        cursor = conexion.cursor()

        # Buscar en los campos id_producto, nombre o codigo
        query = "SELECT nombre, codigo, precio FROM productos WHERE id_producto=? OR nombre=? OR codigo=?"
        cursor.execute(query, (producto, producto, producto))
        resultado = cursor.fetchone()

        if resultado:
            nombre, codigo, precio = resultado
            producto = codigo  # Usamos el código como identificador

            # 3. Actualizar o agregar la información del producto al diccionario 'articulos_venta'
            if producto in self.articulos_venta:
                self.articulos_venta[producto] += 1
                cantidad = self.articulos_venta[producto]
                self.tabla.set(producto, "Cantidad", cantidad)  # Actualizar la columna de cantidad
            else:
                self.articulos_venta[producto] = 1
                cantidad = self.articulos_venta[producto]
                self.tabla.insert("", END, iid=producto, text=cantidad, values=(cantidad, nombre, codigo, precio))

        # 4. Limpiar el Entry
        self.barra_b.delete(0, END)

        conexion.close()

        self.actualizarResumenVenta()




################################################################        
    def fQuitar(self):
        # Obtener el artículo seleccionado en la tabla
        seleccion = self.tabla.selection()
        if not seleccion:
            return

        # Obtener el código del artículo seleccionado
        codigo = self.tabla.item(seleccion)['values'][0]

        # Verificar si el código existe en el diccionario de artículos de venta
        if codigo in self.articulos_venta:
            # Reducir la cantidad en 1
            self.articulos_venta[codigo] -= 1

            # Verificar si la cantidad llega a 0 o menos y eliminar el artículo del diccionario
            if self.articulos_venta[codigo] <= 0:
                del self.articulos_venta[codigo]

        # Eliminar el artículo de la tabla
        self.tabla.delete(seleccion)

        self.actualizarResumenVenta()


    def actualizarTabla(self):
        self.tabla.delete(*self.tabla.get_children())  # Limpiar la tabla

        for producto, cantidad in self.articulos_venta.items():
            conexion = sqlite3.connect('regalitosdb.db')
            cursor = conexion.cursor()

            # Obtener los datos del producto desde la base de datos
            query = "SELECT nombre, codigo, precio FROM productos WHERE codigo=?"
            cursor.execute(query, (producto,))
            resultado = cursor.fetchone()

            if resultado:
                nombre, codigo, precio = resultado
                self.tabla.insert("", END, iid=producto, text=cantidad, values=(cantidad, nombre, codigo, precio))

            conexion.close()
##############################################################
    def actualizarResumenVenta(self):
        # Obtener todos los elementos de la tabla
        items = self.tabla.get_children()

        # Calcular el total de artículos
        total_articulos = 0
        for item in items:
            cantidad = int(self.tabla.item(item, 'values')[0])
            total_articulos += cantidad

        # Mostrar el total de artículos en el Entry correspondiente
        self.articulosE.delete(0, tk.END)
        self.articulosE.insert(0, str(total_articulos))

        # Calcular el total de la venta
        total_venta = 0
        for item in items:
            cantidad = int(self.tabla.item(item, 'values')[0])
            precio_unitario = self.tabla.item(item, 'values')[3]
            if precio_unitario:
                precio_unitario = float(precio_unitario)
                total_venta += cantidad * precio_unitario

        # Mostrar el total de la venta en el Entry correspondiente
        self.totalE.delete(0, tk.END)
        self.totalE.insert(0, str(total_venta))

        # Calcular el cambio
        monto_recibido = self.monto.get()
        if monto_recibido:
            try:
                monto_recibido = float(monto_recibido)
                cambio = monto_recibido - total_venta
                self.cambioE.delete(0, tk.END)
                self.cambioE.insert(0, str(cambio))
            except ValueError:
                # Si el monto recibido no es un número válido, dejar el campo de cambio vacío
                self.cambioE.delete(0, tk.END)
        else:
            # Si no se ha ingresado un monto recibido, dejar el campo de cambio vacío
            self.cambioE.delete(0, tk.END)

    def onMontoChanged(self, event):
        self.actualizarResumenVenta()
##########################################################    
    def fEspecial(self):
        try:
            self.ventana1 = ventanaEspecial(self)
            #self.wait_window(ventana1)

        except Exception as e:
            print('Oh, ha ocurrido un error:', type(e))

    def fBuscar(self):
        try:
            self.ventana2 = busqueda(self)
            #self.ventana2.wait_window()  # Esperar hasta que la ventana se cierre

        except Exception as e:
            print('Oh, ha ocurrido un error:', type(e))
###############################################################
    def decrementarExistencias(self):
            # Conectarse a la base de datos
        conexion = sqlite3.connect('regalitosdb.db')
        cursor = conexion.cursor()

        # Actualizar las existencias de los productos vendidos
        for codigo, cantidad in self.articulos_venta.items():
            # Verificar si el producto existe en la base de datos
            query_existencia = "SELECT existencias FROM productos WHERE codigo = ?"
            cursor.execute(query_existencia, (codigo,))
            resultado = cursor.fetchone()

            if resultado:
                existencia_actual = resultado[0]

                # Calcular la nueva existencia luego de la venta
                nueva_existencia = existencia_actual - cantidad

                # Actualizar la existencia en la base de datos
                query_actualizar = "UPDATE productos SET existencias = ? WHERE codigo = ?"
                cursor.execute(query_actualizar, (nueva_existencia, codigo))

        # Guardar los cambios en la base de datos
        conexion.commit()

        # Cerrar la conexión con la base de datos
        conexion.close()


    def fConfirmar(self):
        self.decrementarExistencias()

        # 1. Tomar el 'id_producto' de cada artículo de la tabla y almacenarlo en el campo 'art_vendido'
        articulos_vendidos = []
        for item in self.tabla.get_children():
            codigo = self.tabla.item(item, 'values')[2]
            articulos_vendidos.append(codigo)

        # 2. Tomar el valor de 'total_articulos' y almacenarlo en el campo 'cant_art'
        total_articulos = self.articulosE.get()

        # 3. Insertar la hora actual de la venta en el campo 'hora_venta' y la fecha actual en el campo 'fecha'
        hora_venta = datetime.now().strftime("%H:%M:%S")
        fecha_venta = datetime.now().strftime("%Y-%m-%d")

        # 4. Tomar el valor de 'total_venta' y almacenarlo en el campo 'total_v'
        total_venta = self.totalE.get()

        # 5. Llamar al método fCancelar para limpiar los Entry y la tabla
        self.fCancelar()

        # Conectarse a la base de datos
        conexion = sqlite3.connect('regalitosdb.db')
        cursor = conexion.cursor()

        # Insertar los datos en la tabla Concepto_venta
        query = "INSERT INTO concepto_venta (art_vendido, cant_art, t_productos, hora_venta, fecha, total_v) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(query, (",".join(articulos_vendidos), total_articulos, len(articulos_vendidos), hora_venta, fecha_venta, total_venta))

        
        # Guardar los cambios en la base de datos
        conexion.commit()

        # Cerrar la conexión con la base de datos
        conexion.close()



        

    def fCancelar(self):
        # 1. Eliminar cualquier dato ingresado en los Entry
        self.monto.delete(0, END)
        self.barra_b.delete(0, END)
        self.cambioE.delete(0, END)
        self.totalE.delete(0, END)
        self.articulosE.delete(0, END)

        # 2. Limpiar la tabla de la venta
        self.tabla.delete(*self.tabla.get_children())

        # 3. Limpiar el diccionario de artículos de venta
        self.articulos_venta = {}

        # 4. Actualizar el resumen de venta
        self.actualizarResumenVenta()

#Inserta aquí las modificaciones para añadir el producto encontrado por la clase 'busqueda'
    def agregarProductoTabla(self, producto):
        codigo = producto[1]  # Usamos el código como identificador del producto

        # Verificar si el producto ya está en la tabla
        items = self.tabla.get_children()
        for item in items:
            if self.tabla.item(item, 'values')[2] == codigo:
                # Si el producto ya está en la tabla, incrementar la cantidad en 1
                cantidad_actual = int(self.tabla.item(item, 'values')[0])
                nueva_cantidad = cantidad_actual + 1
                self.tabla.set(item, 'Cantidad', nueva_cantidad)
                self.articulos_venta[codigo] = nueva_cantidad
                self.actualizarResumenVenta()
                return

        # Si el producto no está en la tabla, agregarlo como un nuevo ítem
        nombre = producto[0]
        precio = producto[2]
        cantidad = 1
        self.tabla.insert("", END, iid=codigo, text=cantidad, values=(cantidad, nombre, codigo, precio))  # Precio unitario inicialmente vacío

        # Actualizar el resumen de venta después de insertar el artículo especial en la tabla
        self.articulos_venta[codigo] = cantidad
        self.actualizarResumenVenta()

#####
    def agregarProductoDesdeBusqueda(self, nombre, codigo, precio):
        # Verificar si el producto ya está en la tabla
        items = self.tabla.get_children()
        for item in items:
            if self.tabla.item(item, 'values')[2] == codigo:
                # Si el producto ya está en la tabla, incrementar la cantidad en 1
                cantidad_actual = int(self.tabla.item(item, 'values')[0])
                nueva_cantidad = cantidad_actual + 1
                self.tabla.set(item, 'Cantidad', nueva_cantidad)
                self.articulos_venta[codigo] = nueva_cantidad
                self.actualizarResumenVenta()
                return

        # Si el producto no está en la tabla, agregarlo como un nuevo ítem
        cantidad = 1
        self.tabla.insert("", END, iid=codigo, text=cantidad, values=(cantidad, nombre, codigo, precio))

        # Actualizar el resumen de venta después de insertar el artículo especial en la tabla
        self.articulos_venta[codigo] = cantidad
        self.actualizarResumenVenta()


class ventanaEspecial(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Añadir un artículo especial a la venta")
        self.geometry("400x250")
        self.resizable(False, False)
        self.decoraciones()

        # Generar un código único para el artículo especial
        self.codigo = str(uuid.uuid4())

        # Asociar la función 'operacion' a los eventos 'KeyRelease' de los Entry correspondientes
        self.precioE.bind('<KeyRelease>', self.operacion)
        self.cantidadE.bind('<KeyRelease>', self.operacion)
        self.venderE.bind('<KeyRelease>', self.operacion)

    def decoraciones(self):
        ##################### CONTENEDORES #####################    
        #Encabezado de página
        frame1 = tk.Frame(self, bg='#B5B5B5')
        frame1.place(x=0, y=0, width=400, height=42)
        #Contenedor del formulario
        frame2 = tk.Frame(self, bg="#ADADAD")
        frame2.place(x=15, y=50, width=371, height=154)
        
        #Contenedor botones
        frame3 = tk.Frame(self, bg = '#6F6B6B')
        frame3.place(x=0, y=220, width=400, height=40)


        ##################### BOTONES #####################
        bAnadir = Button(frame3,text='Añadir a la venta', bg='#088423', command=self.fAnadir,
                         font=("Arial Black",9),fg='white',width= 15)
        bAnadir.place(x=265, y=0, width=140, height=30)
    

        bCancelar = Button(frame3, text='Cancelar', bg='#BB0E0E', command=self.fCancelar,
                           font=("Arial Black",9),fg='white',width= 15)
        bCancelar.place(x=0, y=0, width=110, height=30)
    


        ################################ Texto #################################################
        #Artículo especial
        lb1 = tk.Label(frame1, text="Artículo especial", bg='#B5B5B5', font=("Arial Black", 25))
        lb1.place(x=40, y=0)


        #Cantidad por costo
        self.cantidadE = tk.Entry(frame2)
        self.cantidadE.place(x=200, y=20, width=150, height=15)#(x=200, y=35, width=150, height=15)
        self.cantidadE.focus()
        self.cantidadS = tk.Label(frame2, text='Cantidad de piezas (pz):', bg='#ADADAD')
        self.cantidadS.place(x=0, y=20, width=180, height=15) #(x=0, y=35, width=190, height=15)
        #Precio del producto
        self.precioE = tk.Entry(frame2)
        self.precioE.place(x=200, y=35, width=150, height=15)#(x=200, y=20, width=150, height=15)
        self.precioS = tk.Label(frame2, text='Precio del producto ($):',  bg='#ADADAD')
        self.precioS.place(x=0, y=35, width=190, height=15)
        #Cantidad a vender
        self.venderE = tk.Entry(frame2)
        self.venderE.place(x=200, y=50, width=150, height=15)
        self.venderS = tk.Label(frame2, text='Cantidad solicitada por el cliente ($):', bg='#ADADAD')
        self.venderS.place(x=0, y=50, width=185, height=15)
        #Precio total a añadir
        self.totalE = tk.Entry(frame2)
        self.totalE.place(x=200, y=100, width=150, height=15)
        self.totalS = Label(frame2, text='Total piezas para el cliente (pz):', bg='#ADADAD')
        self.totalS.place(x=0, y=100, width=180, height=15)


    def operacion(self, event):
        try:
            # Obtener los valores de los Entry
            precio = float(self.precioE.get())
            cantidad = float(self.cantidadE.get())
            vender = float(self.venderE.get())

            # Realizar la regla de 3
            total = (vender * cantidad) / precio


            # Mostrar el resultado en el Entry correspondiente
            self.totalE.delete(0, tk.END)
            self.totalE.insert(0, str(total))

        except ValueError:
            # Si ocurre un error al convertir los valores a números, dejar el Entry vacío
            self.totalE.delete(0, tk.END)

    def fCancelar(self):
        self.destroy()

    def fAnadir(self):
        # Obtener el valor del Entry 'venderE'
        precioAnadir = float(self.venderE.get())

        # Verificar si se ingresó un valor válido
        if precioAnadir:
            # Añadir el artículo especial a la tabla de la clase 'VentanaPrincipal'
            self.master.agregarProductoTabla(('Artículo Especial', self.codigo, '', precioAnadir))

            # Insertar el precio en la columna 'Precio unitario' de la tabla de la clase 'VentanaPrincipal'
            self.master.tabla.set(self.codigo, 'Precio unitario', precioAnadir)

        # Destruir la ventana
        self.destroy()




class busqueda(tk.Toplevel):
    def __init__(self, ventana_principal):
        super().__init__()
        self.title("Buscar existencias de productos")
        self.geometry("400x250")
        self.resizable(False, False)
        self.decoraciones()

        self.ventana_principal = ventana_principal


    def decoraciones(self):
        ######################### CONTENEDORES #########################
        #Encabezado de página
        frame1 = Frame(self, bg='#B5B5B5')
        frame1.place(x=0, y=0, width=400, height=42)

        #Contenedor del formulario
        frame2 = Frame(self, bg="#ADADAD")#self.vExistencia
        frame2.place(x=15, y=50, width=371, height=154)
        subF1 = Frame(frame2, bg="#ADADAD")
        subF1.pack(side=TOP)
        #Contenedor botones
        frame3 = Frame(self, bg = '#6F6B6B')
        frame3.place(x=0, y=220, width=400, height=40)




        ######################### BOTONES #########################
        #Cancelar
        bCancelar = Button(frame3, text='Cancelar',justify='center', command=self.fCancelar, bg='#BB0E0E',
                          font=("Arial Black",9),fg='white',width= 15)
        bCancelar.place(x=0, y=0, width=80, height=30)
        #Buscar producto
        bBuscar = Button(frame3, text='Buscar producto',justify='center',command=self.fBuscar,bg='#6723D7',
                          font=("Arial Black",9),fg='white',width= 15)
        bBuscar.place(x=80, y=0, width=120, height=30)
        #Escaner 
        bEscaner = tk.Button(frame3, text='Escanear',command=self.escanerBarras, bg='#234AD7',
                              font=("Arial Black",9),fg='white',width= 10)
        bEscaner.place(x=190, y=0, width=80, height=30)

        #Añadir a la compra
        bAnadir = Button(frame3,text='Añadir a la compra',justify='center', command=self.anadirProducto, bg='#088423',
                          font=("Arial Black",9),fg='white',width= 20)
        bAnadir.place(x=270, y=0, width=130, height=30)



        ######################### TEXTO #########################
        titulo = Label(frame1,text="Buscar existencia", bg='#B5B5B5', font=("Arial Black", 25))
        titulo.pack(anchor='center', fill=BOTH)
        
        self.IDarticulo = Label(subF1, text='ID o nombre del artículo:', bg="#ADADAD", font=('Arial Black', 10), anchor=CENTER)
        self.IDarticulo.pack(side=LEFT, padx=10, pady=5)
        self.IDarticuloE = Entry(subF1)
        self.IDarticuloE.pack(side=LEFT, padx=10, pady=5)
        self.IDarticuloE.focus()
        ######################### TABLA #########################
        self.tabla = ttk.Treeview(frame2)
        self.tabla.pack(side=LEFT, fill=BOTH, expand=True)

        self.tabla['columns'] = ('Cantidad','Producto','Codigo de barras', 'Precio')
        self.tabla.column('#0', width=0, stretch=tk.NO)
        self.tabla.column('Cantidad', anchor=tk.CENTER, width=50)
        self.tabla.column('Producto', anchor=tk.W, width=50)
        self.tabla.column('Codigo de barras', anchor=tk.W, width=50)
        self.tabla.column('Precio', anchor=tk.CENTER, width=50)

        self.tabla.heading('#0', text='', anchor=tk.CENTER)
        self.tabla.heading('Cantidad', text='Cantidad', anchor=tk.CENTER)
        self.tabla.heading('Producto', text='Producto', anchor=tk.CENTER)
        self.tabla.heading('Codigo de barras', text='Codigo de barras', anchor=tk.CENTER)
        self.tabla.heading('Precio', text='Precio', anchor=tk.CENTER)        

    def fCancelar(self):
        self.destroy()
    
    def escanerBarras(self):
        pass

    def fBuscar(self):
        # Obtener el valor ingresado en el Entry IDarticulo
        valor_busqueda = self.IDarticuloE.get().strip()

        # Verificar que no se haya ingresado un dato vacío
        if not valor_busqueda:
            messagebox.showwarning("Dato faltante", "Por favor, ingrese un valor para buscar.")
            return

        # Conectar a la base de datos
        conexion = sqlite3.connect('regalitosdb.db')
        cursor = conexion.cursor()

        # Realizar la búsqueda en la base de datos
        query = "SELECT existencias, nombre,codigo, precio FROM productos WHERE id_producto=? OR nombre=? OR codigo=?"
        cursor.execute(query, ( valor_busqueda, valor_busqueda, valor_busqueda))
        resultado = cursor.fetchone()

        # Verificar si se encontró el producto
        if resultado:
            existencias, nombre, codigo, precio = resultado

            # Limpiar la tabla antes de agregar los nuevos datos
            self.tabla.delete(*self.tabla.get_children())

            # Agregar los datos del producto a la tabla
            self.tabla.insert("", END, values=(existencias, nombre, codigo, precio))
            
        else:
            messagebox.showinfo("Producto no encontrado", "El producto no ha sido encontrado en la base de datos.")

        # Cerrar la conexión a la base de datos
        conexion.close()
###################################################################################

    def anadirProducto(self):

        #self.ventana_principal.agregarProductoTabla(nombre, precio)
        producto = self.tabla.item(self.tabla.selection())['values']
        print(producto)
        nombre = producto[1]
        codigo = producto[2]
        precio = producto[3]
        productoE = nombre, codigo, precio
        self.master.agregarProductoTabla(productoE)

        self.destroy()  # Cerrar la ventana de búsqueda después de agregar el producto


if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()

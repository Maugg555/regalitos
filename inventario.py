import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
from datetime import datetime
import os
import sys
from tkinter import messagebox

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Inventario")
        self.geometry("800x600")
        self.iconbitmap('img\icono16.ico')
        self.resizable(True, True)
        self.decoracionesInv()
        
    def decoracionesInv(self):
        ####################### CONTENEDORES #######################
        # Encabezado de página
        frame1 = tk.Frame(self, bg='#B5B5B5')
        frame1.pack(side=tk.TOP, fill=tk.X)
        lb1 = tk.Label(frame1, text="Inventario", bg='#B5B5B5', font=("Arial Black", 40))
        lb1.pack(anchor='center', fill=tk.BOTH)
        
        fButtons = tk.Frame(self, bg='#D9D9D9') 
        fButtons.pack(side=tk.LEFT, fill=tk.BOTH)
        
        fBusqueda = tk.Frame(self, bg='#D9D9D9')
        fBusqueda.pack(side=tk.TOP, pady=0, padx=0, fill=tk.X)
        
        fTabla = tk.Frame(self, bg='black', width=655, height=350)
        fTabla.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)


        ####################### BOTONTES #######################
        #Boton regresar menu principal
        self.bRegresar = tk.Button(frame1, text='Regresar', command=self.fRegresar, bg='#D9D9D9', fg='Black', font=("Arial Black", 9), highlightbackground='#D9D9D9', width=10, height=2)
        self.bRegresar.pack(side=tk.RIGHT, padx=10, pady=5)
        #Busqueda de artículos
        self.bBuscar = tk.Button(fBusqueda, text='Buscar', bg='#6723D7', font=("Arial Black", 9), fg='white', width=10, command=self.busqueda)
        self.bBuscar.pack(side=tk.LEFT, padx=10, pady=10)
        self.barra_b = tk.Entry(fBusqueda, text='Categoria, nombre, ID o código de barras', bg='#B5B5B5')
        self.barra_b.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        self.barra_b.focus()
        #Añadir al inventario
        self.bAnadir = tk.Button(fButtons, text='Añadir', bg='#088423', font=("Arial Black", 9), fg='white', width=10, command=self.open_add_item_window)
        self.bAnadir.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
        #Editar artículo del inventario
        self.bEditar = tk.Button(fButtons, text='Editar', bg='#088484', font=("Arial Black", 9), fg='white', width=10, command=self.open_edit_item_window)
        self.bEditar.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
        #Borrar artículo de inventario
        self.bBorrar = tk.Button(fButtons, text='Borrar', bg='#BB0E0E', font=("Arial Black", 9), fg='white', width=10, command=self.open_delete_items_window)
        self.bBorrar.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
        #Escaner 
        bEscaner = tk.Button(fButtons, text='Escanear',command=self.escanerBarras, bg='#234AD7',
                              font=("Arial Black",9),fg='white',width= 10)
        bEscaner.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.X)
        #Ver artículos del inventario en tabla
        self.bVer = tk.Button(fButtons, text='Ver todo', command=self.mostrarEnTabla, bg='#B30A98', font=("Arial Black", 9), fg='white', width=10)
        self.bVer.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.X)
        #Limpiar la tabla
        self.bLimpiar = tk.Button(fButtons, text='Limpiar', bg='#4BC0F2', font=("Arial Black", 9), fg='white', width=10, command=self.limpiar)
        self.bLimpiar.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.X)



        ####################### TABLA #######################
        scrollbar = ttk.Scrollbar(fTabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tabla = ttk.Treeview(fTabla, yscrollcommand=scrollbar.set)
        self.tabla.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tabla.yview)
        
        self.tabla['columns'] = ('ID', 'Nombre', 'Descripcion','Código de barras', 'Costo','Marca', 'Precio', 'Categoria', 'Existencias')
        self.tabla.column('#0', width=0, stretch=tk.NO)
        self.tabla.column('ID', anchor=tk.CENTER, width=50)
        self.tabla.column('Nombre', anchor=tk.W, width=100)
        self.tabla.column('Descripcion', anchor=tk.CENTER, width=100)
        self.tabla.column('Código de barras', anchor=tk.CENTER, width=100)
        self.tabla.column('Costo', anchor=tk.CENTER, width=50)
        self.tabla.column('Marca', anchor=tk.CENTER, width=50)
        self.tabla.column('Precio', anchor=tk.CENTER, width=50)
        self.tabla.column('Categoria', anchor=tk.CENTER, width=100)
        self.tabla.column('Existencias', anchor=tk.CENTER, width=100)

        self.tabla.heading('#0', text='', anchor=tk.CENTER)
        self.tabla.heading('ID', text='ID', anchor=tk.CENTER)
        self.tabla.heading('Nombre', text='Nombre', anchor=tk.CENTER)
        self.tabla.heading('Descripcion', text='Descripción', anchor=tk.CENTER)
        self.tabla.heading('Código de barras', text='Código de barras', anchor=tk.CENTER)
        self.tabla.heading('Costo', text='Costo', anchor=tk.CENTER)
        self.tabla.heading('Marca', text='Marca', anchor=tk.CENTER)
        self.tabla.heading('Precio', text='Precio', anchor=tk.CENTER)
        self.tabla.heading('Categoria', text='Categoria', anchor=tk.CENTER)
        self.tabla.heading('Existencias', text='Existencias', anchor=tk.CENTER)

    #Función que muestra en la tabla el contenido de la base de datos
    def mostrarEnTabla(self):
        #Conectar a la BD
        conn = sqlite3.connect('regalitosdb.db')
        cursor = conn.cursor()
        #Obtener todos los registros de la tabla
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        #limpiar la tabla antes de mostrar datps
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        #Mostrar los productos en la tabla
        for registro in productos:
            # Asegúrate de que los campos se muestren en el orden correcto
            id_producto, nombre, descripcion, codigo, fecha, precio, costo, marca, categoria, existencias = registro
            self.tabla.insert('', 'end', values=(id_producto, nombre, descripcion, codigo,costo, marca, precio, categoria, existencias))

        #cerrar conexión BD
        conn.close()

    def busqueda(self):
        #Obtener el texto de busqueda
        txtBusqueda = self.barra_b.get().upper()
        if not txtBusqueda:
            return
        
        #Conexión BD
        conn = sqlite3.connect('regalitosdb.db')
        cursor = conn.cursor()
        #Ejecutar la busqueda
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE ? OR codigo LIKE ? OR categoria LIKE ?", 
                     (f"%{txtBusqueda}%", f"%{txtBusqueda}%", f"{txtBusqueda}"))
        #Obtener resultados de la consulta
        resultados = cursor.fetchall()
        #Borrar registros existentes de la tabal
        self.tabla.delete(*self.tabla.get_children())
        #Agregar los resultados a la tabla
        for resultado in resultados:
        # Asegúrate de que los campos se muestren en el orden correcto
            id_producto, nombre, descripcion, codigo, fecha, precio, costo, marca, categoria, existencias = resultado
            self.tabla.insert('', 'end', values=(id_producto, nombre, descripcion,codigo, costo, marca,precio, categoria, existencias))

        #Cerrar conexión BD
        cursor.close()
        conn.close()

    def fRegresar(self):
        self.withdraw()
        os.system(f"{sys.executable} main.py")

    def limpiar(self):
        # Eliminar todos los registros existentes en la tabla
        self.tabla.delete(*self.tabla.get_children())

    def escanerBarras(self):
        pass

    def open_add_item_window(self):
        self.add_item_window = AddItemWindow(self)
        
    def open_edit_item_window(self):
        self.edit_item_window = EditItemWindow(self)
        
    def open_delete_items_window(self):
        self.delete_items_window = DeleteItemsWindow(self)





class AddItemWindow(tk.Toplevel):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.title("Agregar Artículo")
        self.geometry("400x250")
        self.resizable(False, False)
        self.decoraciones()    

    def decoraciones(self):
    ############################### Contenedores #####################################
        #Encabezado de página
        frame1 = tk.Frame(self,bg='#B5B5B5')
        frame1.place(x=0, y=0, width=400, height=42)
        
        #Contenedor del formulario
        frame2 = tk.Frame(self, bg="#ADADAD")
        frame2.place(x=15, y=50, width=371, height=154)
        
        #Contenedor botones
        frame3 = tk.Frame(self, bg = '#6F6B6B')
        frame3.place(x=0, y=220, width=400, height=40)
    ################################# Botones #########################################
        #Guardar
        bGuardar = tk.Button(frame3,text='Guardar', command=self.fGuardar, bg='#088423',
                          font=("Arial Black",9),fg='white',width= 10)
        bGuardar.place(x=310, y=0, width=90, height=30)
        #Añadir otro
        bAnadirO = tk.Button(frame3, text='Añadir otro',command=self.fAnadir, bg='#6723D7',
                              font=("Arial Black",9),fg='white',width= 10)
        bAnadirO.place(x=100, y=0, width=90, height=30)
        #Escaner 
        bEscaner = tk.Button(frame3, text='Escanear',command=self.escanerBarras, bg='#234AD7',
                              font=("Arial Black",9),fg='white',width= 10)
        bEscaner.place(x=200, y=0, width=90, height=30)
        #Cancelar
        bCancelar = tk.Button(frame3, text='Cancelar', command=self.return_to_main, bg='#BB0E0E',
                           font=("Arial Black",9),fg='white',width= 10)
        bCancelar.place(x=0, y=0, width=90, height=30)


    ################################# Texto #############################################
        #Añadir
        lb1 = tk.Label(frame1, text="Añadir", bg='#B5B5B5', font=("Arial Black", 25))
        lb1.place(x=150, y=0)
        #Nombre
        self.nombreE = tk.Entry(frame2)
        self.nombreE.place(x=180, y=5, width=180, height=12)
        self.nombreE.focus()
        self.nombreS = tk.Label(frame2, text='Nombre del producto:', bg='#ADADAD')
        self.nombreS.place(x=0, y=5, width=150, height=12)

        #Descripcion
        self.descripcionE = tk.Entry(frame2)
        self.descripcionE.place(x=180, y=20, width=180, height=12)
        self.descripcionS = tk.Label(frame2, text='Descripción:', bg='#ADADAD')
        self.descripcionS.place(x=0, y=20, width=150, height=12)

        #Codigo de barras
        self.codigoE = tk.Entry(frame2)
        self.codigoE.place(x=180, y=35, width=180, height=12)
        self.codigoS = tk.Label(frame2, text='Código de barras o ID:', bg='#ADADAD')
        self.codigoS.place(x=0, y=34, width=150, height=12)

        #Costo
        self.costoE = tk.Entry(frame2)
        self.costoE.place(x=180, y=50, width=180, height=12)
        self.costoS = tk.Label(frame2, text='Costo del producto:', bg='#ADADAD')
        self.costoS.place(x=0, y=50, width=150, height=12)

        #Precio de venta
        self.precioE = tk.Entry(frame2)
        self.precioE.place(x=180, y=65, width=180, height=12)
        self.precioS = tk.Label(frame2, text='Precio al cliente:', bg='#ADADAD')
        self.precioS.place(x=0, y=65, width=150, height=12)

        #Marca
        self.marcaE = tk.Entry(frame2)
        self.marcaE.place(x=180, y=80, width=180, height=12)
        self.marcaS = tk.Label(frame2, text='Marca:', bg='#ADADAD')
        self.marcaS.place(x=0, y=80, width=150, height=12)

        #Categorias
        self.categoriaE = tk.Entry(frame2)
        self.categoriaE.place(x=180, y=95, width=180, height=12)
        self.categoriaS = tk.Label(frame2, text='Categoria:', bg='#ADADAD')
        self.categoriaS.place(x=5, y=95, width=150, height=12)

        #Cantidad
        self.cantidadE = tk.Entry(frame2)
        self.cantidadE.place(x=180, y=110, width=180, height=12)
        self.cantidadS = tk.Label(frame2, text='Cantidad de artículos:', bg='#ADADAD')
        self.cantidadS.place(x=5, y=110, width=150, height=12)
   


    def return_to_main(self):
        self.destroy()

    def validar_datos(self):
     # Obtener los datos ingresados en los Entry
        nombre = self.nombreE.get()
        descrip = self.descripcionE.get()
        codBarras = self.codigoE.get()
        costo = self.costoE.get()
        precio = self.precioE.get()
        marca = self.marcaE.get()
        categoria = self.categoriaE.get()
        cantidad = self.cantidadE.get()

        # Verificar si alguno de los campos está vacío
        if not nombre or not descrip or not codBarras or not costo or not precio or not marca or not categoria or not cantidad:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos")
            return False

        return True

    #Función para guardar artículos en la base de datos
    def fGuardar(self):
        # Validar los datos ingresados
        if not self.validar_datos():
            return
        #Conexion con la base de datos
        conn = sqlite3.connect('regalitosdb.db')
        cursor = conn.cursor()

        #Obtener los datos ingresados en los Entry

        # Obtener los datos ingresados en los Entry
        nombre = self.nombreE.get().upper()  # Convertir a mayúsculas
        descrip = self.descripcionE.get().lower()  # Convertir a minúsculas
        codBarras = self.codigoE.get().upper()  # Convertir a mayúsculas
        fecha_actual = datetime.now()  # Obtener la fecha y hora actual
        costo = self.costoE.get()
        precio = self.precioE.get()
        marca = self.marcaE.get().upper()  # Convertir a mayúsculas
        categoria = self.categoriaE.get().upper()  # Convertir a mayúsculas
        cantidad = self.cantidadE.get()

        #Insertar los datos en la tabla Productos
        cursor.execute("INSERT INTO productos (nombre, descripcion, codigo, fecha, precio, costo, marca, categoria, existencias) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (nombre,descrip, codBarras, fecha_actual, precio, costo, marca, categoria, cantidad))

        #Guardar los cambios y cerrar conexión
        conn.commit()
        conn.close()

        #Limpiar Entry después de añadir registros
        self.nombreE.delete(0,END)
        self.descripcionE.delete(0, END)
        self.codigoE.delete(0, END)
        self.costoE.delete(0, END)
        self.precioE.delete(0, END)
        self.marcaE.delete(0, END)
        self.categoriaE.delete(0,END)
        self.cantidadE.delete(0, END)

        self.destroy()

    def escanerBarras(self):
        pass

    def fAnadir(self):
        # Validar los datos ingresados
        if not self.validar_datos():
            return
        #Conexion con la base de datos
        conn = sqlite3.connect('regalitosdb.db')
        cursor = conn.cursor()

        #Obtener los datos ingresados en los Entry

        # Obtener los datos ingresados en los Entry
        nombre = self.nombreE.get().upper()  # Convertir a mayúsculas
        descrip = self.descripcionE.get().lower()  # Convertir a minúsculas
        codBarras = self.codigoE.get().upper()  # Convertir a mayúsculas
        fecha_actual = datetime.now()  # Obtener la fecha y hora actual
        costo = self.costoE.get()
        precio = self.precioE.get()
        marca = self.marcaE.get().upper()  # Convertir a mayúsculas
        categoria = self.categoriaE.get().upper()  # Convertir a mayúsculas
        cantidad = self.cantidadE.get()

        #Insertar los datos en la tabla Productos
        cursor.execute("INSERT INTO productos (nombre, descripcion, codigo, fecha, precio, costo, marca, categoria, existencias) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (nombre,descrip, codBarras, fecha_actual, precio, costo, marca, categoria, cantidad))

        #Guardar los cambios y cerrar conexión
        conn.commit()
        conn.close()

        self.nombreE.delete(0,END)
        self.descripcionE.delete(0, END)
        self.codigoE.delete(0, END)
        self.costoE.delete(0, END)
        self.precioE.delete(0, END)
        self.marcaE.delete(0, END)
        self.categoriaE.delete(0,END)
        self.cantidadE.delete(0, END)





class EditItemWindow(tk.Toplevel):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.title("Editar Artículo")
        self.geometry("400x250")
        self.resizable(False, False)
        self.decoraciones()
        self.id_producto = None
        
    def decoraciones(self):
################################ CONTENEDORES ###########################################
        #Encabezado de página
        frame1 = tk.Frame(self, bg='#B5B5B5')
        frame1.place(x=0, y=0, width=400, height=42)
        
        #Contenedor del formulario
        frame2 = tk.Frame(self, bg="#ADADAD")
        frame2.place(x=15, y=50, width=371, height=154)
        
        #Contenedor botones
        frame3 = tk.Frame(self, bg = '#6F6B6B')
        frame3.place(x=0, y=220, width=400, height=40)

        
    ################################ BOTONES ####################################################
        #Buscar producto
        self.bBuscar = tk.Button(frame2, text='Buscar producto:',command=self.fBuscar,bg='#6723D7',
                          font=("Arial Black",9),fg='white',width= 10)
        self.bBuscar.place(x=15, y=3, width=150, height=15)
        #Guardar
        self.bGuardar = tk.Button(frame3,text='Guardar', command=self.fGuardar, bg='#088423',
                          font=("Arial Black",9),fg='white',width= 10)
        self.bGuardar.place(x=310, y=0, width=90, height=30)
        #Escaner 
        bEscaner = tk.Button(frame3, text='Escanear',command=self.escanerBarras, bg='#234AD7',
                              font=("Arial Black",9),fg='white',width= 10)
        bEscaner.place(x=150, y=0, width=100, height=30)
        #Cancelar
        self.bCancelar = tk.Button(frame3, text='Cancelar', command=self.salir, bg='#BB0E0E',
                          font=("Arial Black",9),fg='white',width= 10)
        self.bCancelar.place(x=0, y=0, width=90, height=30)

    ################################# Texto #############################################
        #Editar
        lb1 = tk.Label(frame1, text="Editar", bg='#B5B5B5', font=("Arial Black", 25))
        lb1.place(x=150, y=0)
        #Buscar producto
        self.buscarE = tk.Entry(frame2)
        self.buscarE.place(x=180, y=5, width=180, height=12)
        self.buscarE.focus()

        #Nombre
        self.nombreE = tk.Entry(frame2)
        self.nombreE.place(x=180, y=20, width=180, height=12)
        self.nombreS = tk.Label(frame2, text='Nombre del producto:', bg='#ADADAD')
        self.nombreS.place(x=0, y=20, width=150, height=12)

        #Descripcion
        self.descripcionE = tk.Entry(frame2)
        self.descripcionE.place(x=180, y=35, width=180, height=12)
        self.descripcionS = tk.Label(frame2, text='Descripción:', bg='#ADADAD')
        self.descripcionS.place(x=0, y=35, width=150, height=12)

        #Codigo de barras
        self.codigoE = tk.Entry(frame2)
        self.codigoE.place(x=180, y=50, width=180, height=12)
        self.codigoS = tk.Label(frame2, text='Código de barras o ID:', bg='#ADADAD')
        self.codigoS.place(x=0, y=50, width=150, height=12)

        #Costo
        self.costoE = tk.Entry(frame2)
        self.costoE.place(x=180, y=65, width=180, height=12)
        self.costoS = tk.Label(frame2, text='Costo del producto:', bg='#ADADAD')
        self.costoS.place(x=0, y=65, width=150, height=12)

        #Precio de venta
        self.precioE = tk.Entry(frame2)
        self.precioE.place(x=180, y=80, width=180, height=12)
        self.precioS = tk.Label(frame2, text='Precio al cliente:', bg='#ADADAD')
        self.precioS.place(x=0, y=80, width=150, height=12)

        #Marca
        self.marcaE = tk.Entry(frame2)
        self.marcaE.place(x=180, y=95, width=180, height=12)
        self.marcaS = tk.Label(frame2, text='Marca:', bg='#ADADAD')
        self.marcaS.place(x=0, y=95, width=150, height=12)

        #Categorias
        self.categoriaE = tk.Entry(frame2)
        self.categoriaE.place(x=180, y=110, width=180, height=12)
        self.categoriaS = tk.Label(frame2, text='Categoria:', bg='#ADADAD')
        self.categoriaS.place(x=5, y=110, width=150, height=12)

        #Cantidad
        self.cantidadE = tk.Entry(frame2)
        self.cantidadE.place(x=180, y=125, width=180, height=12)
        self.cantidadS = tk.Label(frame2, text='Cantidad de artículos:', bg='#ADADAD')
        self.cantidadS.place(x=5, y=125, width=150, height=12)

    def fBuscar(self):
        #Obtener elemento a buscar
        txtBusqueda = self.buscarE.get().upper()

        # Validar que se haya ingresado algún dato
        if not txtBusqueda:
            self.mostrar_advertencia("Por favor, ingrese un valor de búsqueda")
            return
        #Conectar BD
        conn = sqlite3.connect('regalitosdb.db')
        cursor = conn.cursor()
        #Consulta SQL
        cursor.execute("SELECT id_producto, nombre, descripcion, codigo, costo, precio, marca, categoria, existencias "
                        "FROM productos WHERE id_producto=? OR nombre LIKE ? OR codigo LIKE ?",
                       (txtBusqueda,f"%{txtBusqueda}%", f"%{txtBusqueda}%"))
        #Resultado de busqueda
        resultado = cursor.fetchone()

        if resultado:
            #ID del producto encontrado
            self.id_producto = resultado[0]
            #Mostrar los datos en los Entry correspondientes
            self.nombreE.delete(0, tk.END)
            self.nombreE.insert(tk.END, resultado[1])

            self.descripcionE.delete(0, tk.END)
            self.descripcionE.insert(tk.END, resultado[2])  # Descripción

            self.codigoE.delete(0, tk.END)
            self.codigoE.insert(tk.END, resultado[3])  # Código de barras

            self.costoE.delete(0, tk.END)
            self.costoE.insert(tk.END, resultado[4])  # Costo

            self.precioE.delete(0, tk.END)
            self.precioE.insert(tk.END, resultado[5])  # Precio

            self.marcaE.delete(0, tk.END)
            self.marcaE.insert(tk.END, resultado[6])  # Marca

            self.categoriaE.delete(0, tk.END)
            self.categoriaE.insert(tk.END, resultado[7])  # Categoría

            self.cantidadE.delete(0, tk.END)
            self.cantidadE.insert(tk.END, resultado[8])  # Cantidad

        else:
            # Limpiar los datos en los Entry
            self.nombreE.delete(0, tk.END)
            self.descripcionE.delete(0, tk.END)
            self.codigoE.delete(0, tk.END)
            self.costoE.delete(0, tk.END)
            self.precioE.delete(0, tk.END)
            self.marcaE.delete(0, tk.END)
            self.categoriaE.delete(0, tk.END)
            self.cantidadE.delete(0, tk.END)
            # Reiniciar el ID del producto
            self.id_producto = None
        #Cerrar conexión BD
        cursor.close()
        conn.close()
    
    def mostrar_advertencia(self, mensaje):
        advertencia = tk.Toplevel(self)
        advertencia.title("Advertencia")
        advertencia.geometry("300x100")
        advertencia.resizable(False, False)

        lbl_mensaje = tk.Label(advertencia, text=mensaje, font=("Arial", 12))
        lbl_mensaje.pack(pady=20)

        # Programar el cierre de la advertencia después de 3 segundos
        advertencia.after(900, advertencia.destroy)

    def validar(self):
        #Obtener valores de los Entry
        nombre = self.nombreE.get()
        descripcion = self.descripcionE.get()
        codBarras = self.codigoE.get()
        costo = self.costoE.get()
        precio = self.precioE.get()
        marca = self.marcaE.get()
        categoria = self.categoriaE.get()
        cantidad = self.cantidadE.get()

        #Verificar que no haya campos vacios
        if not nombre or not descripcion or not codBarras or not costo or not precio or not marca or not categoria or not cantidad:
            messagebox.showerror("Error","Todos los campos son obligatorios.")
            return False
        
        self.validacion_exitosa = True
        return True
    

    def escanerBarras(self):
        pass

    def fGuardar(self):
        #Validar los campos
        if not self.validar():
            return

        if self.id_producto is None:
            messagebox.showwarning("Advertencia", "No se ha seleccionado ningún producto")
            return
        

        #Obtener valores de los Entry
        nombre = self.nombreE.get()
        descripcion = self.descripcionE.get()
        codBarras = self.codigoE.get()
        fecha = datetime.now()# Obtener la fecha y hora actual
        costo = self.costoE.get()
        precio = self.precioE.get()
        marca = self.marcaE.get()
        categoria = self.categoriaE.get()
        cantidad = self.cantidadE.get()

        #Conectar a la BD
        conn = sqlite3.connect('regalitosdb.db')
        cursor = conn.cursor()

        #Ejecutar consulta SQL para actualizar campos
        cursor.execute("UPDATE productos SET nombre=?, descripcion=?, codigo=?, fecha=?, costo=?, precio=?, marca=?, "
                       "categoria=?, existencias=? WHERE id_producto=?",
                       (nombre, descripcion, codBarras, fecha, costo, precio, marca, categoria, cantidad, self.id_producto))
        
        #Guardar los cambios en la BD
        conn.commit()
        #Cerrar la conexión con la BD
        cursor.close()
        conn.close()

        #Operación exitosa
        messagebox.showinfo("Éxito", "Artículo actualizado correctamente")

        self.destroy()
        
    def return_to_main(self):
        if self.validacion_exitosa:
            self.destroy()
        else:
            #Mensaje de advertencia
            messagebox.showwarning("Advertencia","Por favor, rellena todos los campos")

    def salir(self):
        self.destroy()





class DeleteItemsWindow(tk.Toplevel):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.title("Eliminar artículos")
        self.geometry("400x250")
        self.resizable(False, False)
        self.decoraciones()
        self.id_producto = None
        self.productos_similares = []

    def decoraciones(self):
        ################################# CONTENEDORES ################################################
        # Encabezado de página
        frame1 = tk.Frame(self, bg='#B5B5B5')
        frame1.place(x=0, y=0, width=400, height=42)
        lb1 = tk.Label(frame1, text="Eliminar", bg='#B5B5B5', font=("Arial Black", 25))
        lb1.place(x=150, y=0)

        # Contenedor del formulario
        frame2 = tk.Frame(self, bg="#ADADAD")
        frame2.place(x=15, y=50, width=371, height=75)

        # Contenedor de advertencia
        fAdvertencia = tk.LabelFrame(self, text='--Advertencia--', bg="#ADADAD")
        fAdvertencia.place(x=15, y=130, width=371, height=75)

        # Contenedor botones
        frame3 = tk.Frame(self, bg='#6F6B6B')
        frame3.place(x=0, y=220, width=400, height=40)

        ############################### Botones #######################################################
        # Buscar producto
        bBuscar = tk.Button(frame2, text='Buscar producto:', command=self.fBuscar, bg='#6723D7',
                          font=("Arial Black",9),fg='white',width= 10)
        bBuscar.place(x=15, y=3, width=150, height=15)
    
        # Eliminar producto
        bEliminar = tk.Button(frame3, text='Eliminar', command=self.fEliminar, bg='#088423',
                          font=("Arial Black",9),fg='white',width= 10)
        bEliminar.place(x=290, y=0, width=100, height=30)
        #Escaner 
        bEscaner = tk.Button(frame3, text='Escanear',command=self.escanerBarras, bg='#234AD7',
                              font=("Arial Black",9),fg='white',width= 10)
        bEscaner.place(x=150, y=0, width=100, height=30)
        # Ver todo el inventario
        bCancelar = tk.Button(frame3, text='Cancelar', command=self.return_to_main, bg='#BB0E0E',
                          font=("Arial Black",9),fg='white',width= 10)
        bCancelar.place(x=0, y=0, width=100, height=30)

        ##################################### TEXTO #################################
        # Buscar producto
        self.buscarE = tk.Entry(frame2)
        self.buscarE.place(x=180, y=5, width=180, height=12)
        self.buscarE.focus()

        # Nombre
        self.nombreE = tk.Entry(frame2)
        self.nombreE.place(x=180, y=20, width=180, height=12)
        self.nombreS = tk.Label(frame2, text='Nombre del producto:', bg='#ADADAD')
        self.nombreS.place(x=0, y=20, width=150, height=12)

        # Descripcion
        self.descripcionE = tk.Entry(frame2)
        self.descripcionE.place(x=180, y=35, width=180, height=12)
        self.descripcionS = tk.Label(frame2, text='Descripción:', bg='#ADADAD')
        self.descripcionS.place(x=0, y=35, width=150, height=12)

        # Advertencia
        advertencia = tk.Label(fAdvertencia, text='Revisar que el producto sea el correcto.\nUna vez eliminado, no podrán deshacerse los cambios.\n\t¿Desea continuar?',
                            bg='#ADADAD')
        advertencia.place(x=25, y=0, width=300, height=55)

    def escanerBarras(self):
        pass

    def fEliminar(self):
        # Obtener el id_producto actual
        id_producto_actual = self.id_producto

        # Verificar si se ha seleccionado un producto
        if id_producto_actual is None:
            messagebox.showwarning("Advertencia", "No se ha seleccionado un producto para eliminar")
            return

        # Conectarse a la base de datos
        connection = sqlite3.connect('regalitosdb.db')
        cursor = connection.cursor()

        try:
            # Eliminar el producto de la tabla productos utilizando el id_producto
            cursor.execute("DELETE FROM productos WHERE id_producto=?", (id_producto_actual,))
            connection.commit()

            # Mostrar mensaje de eliminación exitosa
            messagebox.showinfo("Eliminación exitosa", "El producto ha sido eliminado correctamente")
        except Exception as e:
            # Mostrar mensaje de error en caso de fallar la eliminación
            messagebox.showerror("Error", f"No se pudo eliminar el producto: {str(e)}")
        finally:
            # Cerrar la conexión a la base de datos
            cursor.close()
            connection.close()

        # Limpiar la lista de productos similares
        self.productos_similares = []

        # Cerrar la ventana
        self.destroy()


    def fBuscar(self):
        # Obtener el nombre ingresado en el Entry
        nombre = self.buscarE.get()

        # Verificar si se ingresó un nombre
        if not nombre:
            # Mostrar mensaje de advertencia si no se ingresó un nombre
            messagebox.showwarning("Advertencia", "Ingrese un nombre de producto")
            return

        # Conectarse a la base de datos
        connection = sqlite3.connect('regalitosdb.db')
        cursor = connection.cursor()

        # Buscar el producto por nombre
        cursor.execute("SELECT id_producto, nombre, descripcion FROM productos WHERE id_producto=? OR nombre LIKE ? OR codigo LIKE ?", 
                       (nombre,f"%{nombre}%",f"%{nombre}%"))
        producto = cursor.fetchone()

        if producto:
            # Si se encontró el producto, obtener los valores de nombre, descripción y id_producto
            self.id_producto = producto[0]

            # Mostrar los valores obtenidos en los Entries correspondientes
            self.nombreE.delete(0, tk.END)
            self.nombreE.insert(0, producto[1])
            self.descripcionE.delete(0, tk.END)
            self.descripcionE.insert(0, producto[2])

             # Almacenar productos similares en la variable de instancia
            cursor.execute("SELECT id_producto, nombre, descripcion FROM productos WHERE nombre LIKE ?",
                       (f"%{producto[1]}%",))
            self.productos_similares = cursor.fetchall()
        else:
            self.nombreE.delete(0, tk.END)
            self.descripcionE.delete(0, tk.END)
            # Mostrar mensaje de advertencia si no se encontró el producto
            messagebox.showwarning("Advertencia", "Producto no encontrado, intente de nuevo")
            self.id_producto = None

        # Cerrar la conexión a la base de datos
        cursor.close()
        connection.close()

    def siguienteProductoSimilar(self):
        if self.productos_similares:
            self.indice_producto = (self.indice_producto + 1) % len(self.productos_similares)
            producto_actual = self.productos_similares[self.indice_producto]

            self.id_producto = producto_actual[0]
            self.nombreE.delete(0, tk.END)
            self.nombreE.insert(0, producto_actual[1])
            self.descripcionE.delete(0, tk.END)
            self.descripcionE.insert(0, producto_actual[2])



    def return_to_main(self):
        self.destroy()


if __name__ == "__main__":
    root = MainWindow()
    root.mainloop()

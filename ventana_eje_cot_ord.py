#from customtkinter import *
from func_ctk import *
import pandas as pd
import os
print(f"Working directory actual: {os.getcwd()}")
# Cargar y limpiar el CSV al iniciar
dataset_ = pd.read_csv('data/productos_temp.csv')
dataset_.reset_index(drop=True, inplace=True)  # Corregido: Agregar inplace=True
dataset_.to_csv("data/productos_temp.csv", index=False)
dataset = pd.read_csv('data/productos_temp.csv')

# VARIABLES GLOBALES
fuente_botton = ("Verdana", 16)
fuente_labels = ("Arial", 18)

# VENTANA PRINCIPAL
ventana_creator = CTk()
ventana_creator.geometry("1000x670")
ventana_creator.title("Creación del Documento")
ventana_creator.resizable(False, False)
ventana_creator.iconbitmap("imgs/favicon.ico")
# FRAMES
datos_cliente = CTkFrame(master=ventana_creator, width=960, height=215)
datos_producto = CTkFrame(master=ventana_creator, width=345, height=357)
sec_productos = CTkFrame(master=ventana_creator, width=595, height=357)

def cerrar():
    ventana_creator.destroy()
# BOTONES PRINCIPALES


boton_crear = CTkButton(master=ventana_creator, text="Crear", width=160, font=fuente_botton, command=lambda:boton_crear_pdf(tipo_doc,ruc,cliente,placa,moneda, ventana_creator,error_label, scroll_tabla_productos,dataset,lmonto,boton_volver,lsigno) )
boton_volver = CTkButton(master=ventana_creator, text="Cerrar", width=160, font=fuente_botton, command=cerrar,state="normal")
lcopy = CTkLabel(ventana_creator, text="© Copyright. 2025 El Miguelin Projects - Repuestos Huanca | Derechos Reservados", font=("Verdana", 8))

lcopy.pack(side="bottom", pady=2)
boton_volver.place(x=20, y=622)
boton_crear.place(x=820, y=622)
datos_cliente.place(x=20, y=20)
datos_producto.place(x=20, y=245)
sec_productos.place(x=385, y=245)

# DATOS DE CLIENTE
ltipo_doc = CTkLabel(datos_cliente, text="Tipo de documento :", font=fuente_labels)
ltipo_doc.place(x=20, y=20)
lruc = CTkLabel(datos_cliente, text="RUC :", font=fuente_labels)
lruc.place(x=20, y=53)
lcliente = CTkLabel(datos_cliente, text="Razon Social :", font=fuente_labels)
lcliente.place(x=20, y=86)
lmoneda = CTkLabel(datos_cliente, text="Moneda:", font=fuente_labels)
lmoneda.place(x=20, y=119)
lplaca = CTkLabel(datos_cliente, text="Placa :", font=fuente_labels)
lplaca.place(x=20, y=152)

# Etiqueta para errores
error_label = CTkLabel(datos_cliente, text="", text_color="red", font=fuente_labels)
error_label.place(x=20, y=185)

# DATOS DEL PRODUCTO
ltitulo_prod = CTkLabel(datos_producto, text="Datos del Producto", font=fuente_labels)
ltitulo_prod.place(x=96, y=13)
lcant = CTkLabel(datos_producto, text="Cant :", font=fuente_labels)
lcod = CTkLabel(datos_producto, text="Cod :", font=fuente_labels)
lmarca = CTkLabel(datos_producto, text="Marca :", font=fuente_labels)
ldescrip = CTkLabel(datos_producto, text="Descrip. :", font=fuente_labels)
lprec_uni = CTkLabel(datos_producto, text="Prec. Unit. :", font=fuente_labels)

lcant.place(x=20, y=73-21)
lcod.place(x=20, y=126-21)
lmarca.place(x=20, y=179-21)
ldescrip.place(x=20, y=232-21)
lprec_uni.place(x=20, y=285-21)

# VARIABLES PARA LOS INPUTS
moneda = IntVar(value=0)
tipo_doc = StringVar(value="")

# TABLA DE PRODUCTOS
sec_productos.pack_propagate(False)
ltitulo_tabla = CTkLabel(sec_productos, text="Tabla de Productos", font=fuente_labels)
ltitulo_tabla.place(x=219.5, y=13)

tabla_productos = CTkFrame(sec_productos, width=595, height=279)
tabla_productos.pack(side="bottom", pady=45)
scroll_tabla_productos = CTkScrollableFrame(tabla_productos, width=595, height=279)
scroll_tabla_productos.pack(fill="both", expand=True)
mostrar_productos(scroll_tabla_productos)

ltotal = CTkLabel(sec_productos, text="TOTAL : ", font=fuente_labels)
ltotal.place(x=400, y=320)
lsigno = CTkLabel(sec_productos, font=fuente_labels)
lsigno.place(x=473, y=320)
lmonto = CTkLabel(sec_productos, text="", font=fuente_labels)
lmonto.place(x=500, y=320)


# INPUTS DATOS DEL CLIENTE
doc_cot = CTkRadioButton(datos_cliente, font=fuente_botton, text="Cotización", variable=tipo_doc, value="COTIZACIÓN")
doc_ord = CTkRadioButton(datos_cliente, font=fuente_botton, text="Orden de Compra", variable=tipo_doc, value="ORDEN DE COMPRA")
ruc = CTkEntry(datos_cliente, font=fuente_labels)
cliente = CTkEntry(datos_cliente, font=fuente_labels, width=300)
soles = CTkRadioButton(datos_cliente, font=fuente_labels, text="Soles - S/.", variable=moneda, value=1, command=lambda: cambio_signo(moneda, lsigno))
dolares = CTkRadioButton(datos_cliente, font=fuente_labels, text="Dolares - $", variable=moneda, value=2, command=lambda: cambio_signo(moneda, lsigno))
placa = CTkEntry(datos_cliente, font=fuente_labels)
# Vincular eventos a las entradas para verificar datos
ruc.bind("<KeyRelease>", lambda event: verificar_datos_cliente(tipo_doc,moneda,ruc,cliente,placa,boton_volver))
cliente.bind("<KeyRelease>", lambda event: verificar_datos_cliente(tipo_doc,moneda,ruc,cliente,placa,boton_volver))
placa.bind("<KeyRelease>", lambda event: verificar_datos_cliente(tipo_doc,moneda,ruc,cliente,placa,boton_volver))

# Llamada inicial para verificar el estado
verificar_datos_cliente(tipo_doc,moneda,ruc,cliente,placa,boton_volver)
# Botones de búsqueda
buscar_nombre_btn = CTkButton(datos_cliente, text="Buscar Nombre", command=lambda: buscar_nombre_por_ruc(ruc.get(), cliente, error_label))
buscar_nombre_btn.place(x=225, y=53)  # Junto al campo RUC
buscar_ruc_btn = CTkButton(datos_cliente, text="Buscar RUC", command=lambda: buscar_ruc_por_nombre(cliente.get(), ruc, cliente, error_label))
buscar_ruc_btn.place(x=452, y=86)  # Junto al campo cliente

doc_cot.place(x=205, y=20)
doc_ord.place(x=355, y=20)
ruc.place(x=75, y=53)
soles.place(x=105, y=119)
dolares.place(x=255, y=119)
cliente.place(x=142, y=86)
placa.place(x=80, y=152)

# INPUTS DATOS DEL PRODUCTO
cant = CTkEntry(datos_producto, font=fuente_labels)
cod = CTkEntry(datos_producto, font=fuente_labels)
marca = CTkEntry(datos_producto, font=fuente_labels)
descrip = CTkEntry(datos_producto, font=fuente_labels)
prec_uni = CTkEntry(datos_producto, font=fuente_labels)

x_inputs = 70
cant.place(x=x_inputs+5, y=73-21)
cod.place(x=x_inputs, y=126-21)
marca.place(x=x_inputs+18, y=179-21)
descrip.place(x=x_inputs+33, y=232-21)
prec_uni.place(x=x_inputs+50, y=285-21)

# BOTONES PRODUCTOS
boton_mas = CTkButton(datos_producto, width=35, height=35, text="+", font=fuente_botton)
boton_mmenos = CTkButton(datos_producto, width=35, height=35, text="-", font=fuente_botton, command=lambda: ven_eliminar_fila(ventana_creator, dataset, scroll_tabla_productos, lmonto))
boton_mod = CTkButton(datos_producto, width=195, height=35, text="Modificar", font=fuente_botton, command=lambda: modificar_datos(ventana_creator, dataset, scroll_tabla_productos, lmonto))

boton_mas.place(x=20, y=302)
boton_mmenos.place(x=75, y=302)
boton_mod.place(x=130, y=302)
boton_mas.configure(command=lambda: agregar_producto(cant, cod, marca, descrip, prec_uni, scroll_tabla_productos, lmonto))

ventana_creator.mainloop()
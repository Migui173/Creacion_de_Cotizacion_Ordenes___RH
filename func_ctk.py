from customtkinter import *
import pandas as pd
from datetime import datetime
import json
import os
from PIL import Image
from gen_pdf import generar_pdf
import platform

def limpiar_entradas(*entradas):
    for entrada in entradas:
        entrada.delete(0, 'end')

def cargar_productos():
    try:
        df = pd.read_csv("data/productos_temp.csv")
        print(f"CSV cargado: {df.to_string()}")  # Depuración
    except FileNotFoundError:
        df = pd.DataFrame(columns=["cant", "cod", "marca", "descrip", "prec_uni", "precio_total"])
        print("CSV no encontrado, creado DataFrame vacío")
    return df

def mostrar_productos(scroll_frame):
    for widget in scroll_frame.winfo_children():
        widget.destroy()

    try:
        df = cargar_productos()
        encabezado = CTkFrame(scroll_frame)
        encabezado.pack(fill="x", pady=(0, 5))
        mis_coloumnas = ["CANT.", "COD.", "MARCA", "DESCRIP.", "PREC. UNIT.", "PREC. TOTAL"]
        for col in mis_coloumnas:
            CTkLabel(encabezado, text=col, width=100, anchor="w", font=("Arial", 11)).pack(side="left")

        for _, row in df.iterrows():
            fila = CTkFrame(scroll_frame)
            fila.pack(fill="x", pady=2)
            for valor in row:
                if isinstance(valor, float) and valor.is_integer():
                    valor = int(valor)
                texto = str(valor)
                if len(texto) > 10:
                    texto = texto[:5] + "..."
                CTkLabel(fila, text=texto, width=100, anchor="w", font=("Arial", 11)).pack(side="left")
    except Exception as e:
        CTkLabel(scroll_frame, text=f"Error al cargar productos: {str(e)}", text_color="red").pack()

def agregar_producto(cant, cod, marca, descrip, prec_uni, scroll, lmonto):
    dataset = pd.read_csv("data/productos_temp.csv")
    cantidad = cant.get().strip()
    codigo = cod.get().strip()
    marca_ = marca.get().strip()
    descripcion = descrip.get().strip()
    precio_uni = prec_uni.get().strip()

    if not all([cantidad, codigo, marca_, descripcion, precio_uni]):
        CTkLabel(scroll, text="Todos los campos son obligatorios", text_color="red").pack()
        return

    try:
        cantidad = int(cantidad)
        precio_uni = float(precio_uni)
    except ValueError:
        CTkLabel(scroll, text="Cantidad y Precio deben ser numéricos", text_color="red").pack()
        return

    producto = {
        "cant": cantidad,
        "cod": codigo,
        "marca": marca_,
        "descrip": descripcion,
        "prec_uni": precio_uni,
        "precio_total": round(precio_uni * cantidad, 2)
    }

    dt = pd.DataFrame([producto])
    dataset = pd.concat([dataset, dt], ignore_index=True)
    try:
        dataset.to_csv("data/productos_temp.csv", index=False)
        print("CSV guardado correctamente")  # Depuración
    except Exception as e:
        CTkLabel(scroll, text=f"Error al guardar CSV: {str(e)}", text_color="red").pack()
        return

    mostrar_productos(scroll)
    limpiar_entradas(cant, cod, marca, descrip, prec_uni)
    actualizar_monto(dataset, lmonto)
    cant.focus_set()

def cambio_signo(moneda, lsigno):
    moneda_valor = int(moneda.get())
    if moneda_valor == 1:
        lsigno.configure(text="S/.")
    elif moneda_valor == 2:
        lsigno.configure(text="$")
    elif moneda_valor == 0:
        lsigno.configure(text="")

def actualizar_monto(dataset, lmonto):
    monto_total = dataset["precio_total"]
    suma = 0
    for i in monto_total:
        suma += i
    lmonto.configure(text=str(round(suma, 2)))

def bloquear_ventana(vent, vent_pri):
    vent.resizable(width=False, height=False)
    vent.update()
    vent.transient(vent_pri)
    vent.grab_set()
    vent.focus_force()


def ven_eliminar_fila(ven_cre, dataset, scroll, lmonto):
    # Recargar el CSV para asegurar que dataset esté actualizado
    dataset = pd.read_csv("data/productos_temp.csv")
    dataset.reset_index(drop=True, inplace=True)
    dataset.to_csv("data/productos_temp.csv", index=False)

    ventana_eliminar = CTkToplevel(ven_cre)
    ventana_eliminar.title("Eliminar fila")
    ventana_eliminar.geometry("350x300")
    ventana_eliminar.iconbitmap("imgs/favicon.ico")
    bloquear_ventana(ventana_eliminar, ven_cre)
    CTkLabel(ventana_eliminar, text="¿Cuál fila desea eliminar?", font=("Arial", 18), width=130).place(x=71, y=20)
    entrada = CTkEntry(ventana_eliminar, placeholder_text="Ingrese el ID que quiere eliminar", width=200)
    entrada.place(x=75, y=65)
    CTkButton(ventana_eliminar, text="Cerrar", command=ventana_eliminar.destroy, font=("Arial", 14), width=130).place(
        x=110, y=255)
    CTkLabel(
        ventana_eliminar,
        text="Recordatorio:\nLa ID de las filas empieza en 1 para la primera fila,\n2 para la segunda, y así sucesivamente.\nAsegúrate de ingresar un número válido.",
        font=("Arial", 12.5),
        text_color="gray",
        wraplength=280,
        justify="left"
    ).place(x=38.5, y=170)

    def funcion_eliminar_fila():
        try:
            id_borrar = int(entrada.get()) - 1
            lista_indice = list(dataset.index)
            print(f"Intentando eliminar ID: {id_borrar}, Índices disponibles: {lista_indice}")  # Depuración
            if id_borrar not in lista_indice or id_borrar < 0:
                CTkLabel(ventana_eliminar, text="ID NO VÁLIDA", text_color="red").place(x=133.5, y=100)
            else:
                dataset.drop(id_borrar, inplace=True)
                dataset.reset_index(drop=True, inplace=True)
                dataset.to_csv("data/productos_temp.csv", index=False)
                CTkLabel(ventana_eliminar, text="FILA ELIMINADA", text_color="green").place(x=130.5, y=100)
                mostrar_productos(scroll)
                actualizar_monto(dataset, lmonto)
        except ValueError:
            CTkLabel(ventana_eliminar, text="⚠ Debes ingresar un número", text_color="orange").place(x=100, y=100)

    CTkButton(ventana_eliminar, text="Eliminar", font=("Arial", 14), command=funcion_eliminar_fila, width=130).place(
        x=110, y=130)


def modificar_datos(ven_cre, dataset, scroll, lmonto):
    # Recargar el CSV para asegurar que dataset esté actualizado
    dataset = pd.read_csv("data/productos_temp.csv")
    dataset.reset_index(drop=True, inplace=True)
    dataset.to_csv("data/productos_temp.csv", index=False)

    vent_mod = CTkToplevel(ven_cre)
    vent_mod.title("Modificar Producto")
    vent_mod.iconbitmap("imgs/favicon.ico")
    vent_mod.geometry("350x250")
    bloquear_ventana(vent_mod, ven_cre)
    CTkLabel(vent_mod, text="¿Cuál fila desea modificar?", font=("Arial", 18), width=130).place(x=66, y=20)
    entrada = CTkEntry(vent_mod, placeholder_text="Ingrese el ID del producto", width=200)
    entrada.place(x=75, y=65)
    CTkLabel(
        vent_mod,
        text="Recordatorio:\nLa ID de las filas empieza en 1 para la primera fila,\n2 para la segunda, y así sucesivamente.\nAsegúrate de ingresar un número válido.",
        font=("Arial", 12.5),
        text_color="gray",
        wraplength=280,
        justify="left"
    ).place(x=38.5, y=170)

    def cargar_datos():
        try:
            id_mod = int(entrada.get()) - 1  # Ajustar al índice base 0
            lista_indice = list(dataset.index)
            print(f"Intentando modificar ID: {id_mod}, Índices disponibles: {lista_indice}")  # Depuración
            if id_mod < 0 or id_mod not in lista_indice:
                CTkLabel(vent_mod, text="ID NO VÁLIDA", text_color="red").place(x=133.5, y=100)
            else:
                CTkLabel(vent_mod, text="ID válida, cargando datos...", text_color="green").place(x=83, y=100)
                vent_mod.destroy()
                vent_datos = CTkToplevel(ven_cre)
                vent_datos.title(f"Datos del producto {id_mod + 1}")
                vent_datos.geometry("400x400")
                vent_datos.iconbitmap("imgs/favicon.ico")
                bloquear_ventana(vent_datos, ven_cre)

                fila = dataset.loc[id_mod]
                # Excluir precio_total de los campos editables
                campos_editables = [campo for campo in dataset.columns if campo != "precio_total"]
                entradas = {}
                for i, campo in enumerate(campos_editables):
                    CTkLabel(vent_datos, text=campo, font=("Arial", 13)).place(x=50, y=30 + i * 40)
                    entrada_ = CTkEntry(vent_datos, width=250)
                    entrada_.insert(0, str(fila[campo]))
                    entrada_.place(x=100, y=30 + i * 40)
                    entradas[campo] = entrada_

                def guardar_cambios():
                    try:
                        for campo_ in campos_editables:
                            nuevo_valor = entradas[campo_].get().strip()
                            if not nuevo_valor:  # Verificar si el campo está vacío
                                CTkLabel(vent_datos, text="Todos los campos son obligatorios", text_color="red").place(
                                    x=100, y=30 + len(campos_editables) * 40 + 20)
                                return
                            if campo_ == "cant":
                                dataset.at[id_mod, campo_] = int(nuevo_valor)
                            elif campo_ == "prec_uni":
                                dataset.at[id_mod, campo_] = float(nuevo_valor)
                            else:
                                dataset.at[id_mod, campo_] = nuevo_valor
                        # Recalcular precio_total
                        dataset.at[id_mod, "precio_total"] = round(
                            dataset.at[id_mod, "cant"] * dataset.at[id_mod, "prec_uni"], 2)
                        dataset.to_csv("data/productos_temp.csv", index=False)
                        mostrar_productos(scroll)
                        actualizar_monto(dataset, lmonto)
                        vent_datos.destroy()
                    except ValueError:
                        CTkLabel(vent_datos, text="Valores numéricos inválidos", text_color="red").place(x=100,
                                                                                                         y=30 + len(
                                                                                                             campos_editables) * 40 + 20)
                    except Exception as e:
                        CTkLabel(vent_datos, text=f"Error: {str(e)}", text_color="red").place(x=100, y=30 + len(
                            campos_editables) * 40 + 20)

                CTkButton(vent_datos, text="Guardar cambios", command=guardar_cambios).place(x=130, y=30 + len(
                    campos_editables) * 40)

        except ValueError:
            CTkLabel(vent_mod, text="⚠ Debes ingresar un número", text_color="orange").place(x=100, y=100)

    CTkButton(vent_mod, text="Cargar Datos", font=("Arial", 14), command=cargar_datos, width=130).place(x=110, y=130)


def cargar_clientes():
    """
    Carga el archivo ruc_clientes.csv en un DataFrame.
    Si no existe, crea un DataFrame vacío con las columnas adecuadas.
    """
    try:
        df = pd.read_csv("data/ruc_clientes.csv", dtype={'ruc': str, 'nombre_cliente': str})
    except FileNotFoundError:
        df = pd.DataFrame(columns=["ruc", "nombre_cliente"])
    return df


def buscar_nombre_por_ruc(ruc_val, cliente_entry, error_label):
    """
    Busca la razón social correspondiente a un RUC y actualiza el campo cliente.
    Muestra un mensaje de error si no se encuentra.
    """
    ruc_val = ruc_val.strip()
    clientes = cargar_clientes()
    resultado = clientes[clientes['ruc'] == ruc_val]
    if not resultado.empty:
        nombre = resultado['nombre_cliente'].iloc[0]
        cliente_entry.delete(0, 'end')
        cliente_entry.insert(0, nombre)
        error_label.configure(text="")
    else:
        error_label.configure(text="RUC no encontrado")


def buscar_ruc_por_nombre(nombre_val, ruc_entry, cliente_entry, error_label):
    """
    Busca el RUC correspondiente a una palabra clave en la razón social.
    Si hay varias coincidencias, muestra una ventana para seleccionar.
    """
    nombre_val = nombre_val.strip().lower()
    if not nombre_val:
        error_label.configure(text="Ingresa una palabra clave")
        return
    clientes = cargar_clientes()
    resultado = clientes[clientes['nombre_cliente'].str.lower().str.contains(nombre_val, na=False)]
    if resultado.empty:
        error_label.configure(text="No se encontraron coincidencias")
    elif len(resultado) == 1:
        ruc = resultado['ruc'].iloc[0]
        nombre = resultado['nombre_cliente'].iloc[0]
        ruc_entry.delete(0, 'end')
        ruc_entry.insert(0, ruc)
        cliente_entry.delete(0, 'end')
        cliente_entry.insert(0, nombre)
        error_label.configure(text="")
    else:
        mostrar_opciones_ruc(resultado, ruc_entry, cliente_entry, error_label)


def mostrar_opciones_ruc(resultados, ruc_entry, cliente_entry, error_label):
    """
    Muestra una ventana con una lista de opciones para seleccionar un RUC, usando un scrollbar.
    """
    ventana_opciones = CTkToplevel()
    ventana_opciones.title("Seleccionar RUC")
    ventana_opciones.geometry("960x650")
    ventana_opciones.iconbitmap("imgs/favicon.ico")
    bloquear_ventana(ventana_opciones, ventana_opciones.master)

    CTkLabel(ventana_opciones, text="Selecciona un RUC:", font=("Arial", 12)).pack(pady=10)

    # Usar CTkScrollableFrame para las opciones
    scroll_frame = CTkScrollableFrame(ventana_opciones, width=280, height=120)
    scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

    opciones = []
    for index, row in resultados.iterrows():
        texto = f"{row['ruc']} - {row['nombre_cliente']}"
        btn = CTkButton(scroll_frame, text=texto,
                        command=lambda r=row['ruc'], n=row['nombre_cliente']: seleccionar_ruc(r, n, ruc_entry,
                                                                                              cliente_entry,
                                                                                              error_label,
                                                                                              ventana_opciones),
                        width=280, height=30)
        btn.pack(pady=5, fill="x")
        opciones.append(btn)

    def cerrar_ventana():
        error_label.configure(text="Selección cancelada")
        ventana_opciones.destroy()

    CTkButton(ventana_opciones, text="Cancelar", command=cerrar_ventana, width=280, height=30).pack(pady=10, fill="x")


def seleccionar_ruc(ruc, nombre, ruc_entry, cliente_entry, error_label, ventana):
    """
    Actualiza los campos RUC y razón social con los valores seleccionados y cierra la ventana.
    """
    ruc_entry.delete(0, 'end')
    ruc_entry.insert(0, ruc)
    cliente_entry.delete(0, 'end')
    cliente_entry.insert(0, nombre)
    error_label.configure(text="")
    ventana.destroy()
def num_pc():
    with open("pc.txt", "r", encoding="utf-8") as archivo:
        primera_linea = archivo.readline().strip()  # .strip() elimina el salto de línea
        return str(primera_linea)

def fecha_hora():
    ahora = datetime.now()
    fecha = ahora.strftime("%d-%m-%Y")
    hora= ahora.strftime("%H:%M")
    return fecha, hora

def subtotal_igv_total(dataset):
    monto_total = dataset["precio_total"]
    total = 0
    for i in monto_total:
        total += i
    igv = round((total*18/100),2)
    subtotal = round(total - igv,2)
    total_ = round(subtotal + igv,2)
    return subtotal, igv, total_
def open_json_cot_data():
    if os.path.exists("data/cot_data.json"):
        with open("data/cot_data.json","r") as cot_data:
            return json.load(cot_data)
    else:
        return {}

def save_json_cot_data(data_cot):
    with open("data/cot_data.json","w") as cot_data:
        json.dump(data_cot,cot_data,indent=4)

def open_json_ord_data():
    if os.path.exists("data/ord_data.json"):
        with open("data/ord_data.json","r") as ord_data:
            return json.load(ord_data)
    else:
        return {}

def save_json_ord_data(data_ord):
    with open("data/ord_data.json","w") as ord_data:
        json.dump(data_ord,ord_data,indent=4)

def conversion_pd_a_list_dict(dat_pd):
    lista_diccionarios = dat_pd.to_dict(orient="records")
    return lista_diccionarios

def conversion_pd_a_list_list(dat_pd):
    lista_listas = dat_pd.values.tolist(orient="records")
    return lista_listas
def abrir_documento(ruta_archivo):
    ruta_completa = os.path.abspath(ruta_archivo)
    print(f"Abrir archivo (absoluto): {ruta_completa}")  # Depuración
    if os.path.exists(ruta_completa):
        if platform.system() == "Windows":
            os.startfile(ruta_completa)
        elif platform.system() == "Darwin":  # macOS
            os.system(f"open '{ruta_completa}'")
        else:  # Linux
            os.system(f"xdg-open '{ruta_completa}'")
    else:
        print(f"❌ Archivo no encontrado: {ruta_completa}")

def dect_abrir_documento(id_unico):
    if "COT" in str(id_unico):
        abrir_documento(f"cotizacion/{id_unico}.pdf")
    else:
        abrir_documento(f"ordenes/{id_unico}.pdf")

def registar_contenido(dict_prin, dataset):
    if dict_prin["cot_o_ord"]== "COTIZACIÓN":
        contenido = open_json_cot_data()
        id_unico = f"COT-{dict_prin["pc"]}-{len(contenido)+1:06}"
    else:
        contenido = open_json_ord_data()
        id_unico = f"ORD-{dict_prin["pc"]}-{len(contenido)+1:06}"
    contenido[id_unico] = {
        "ruc" : dict_prin["ruc"],
        "cliente" : dict_prin["cliente"],
        "placa" : dict_prin["placa"],
        "fecha" : dict_prin["fecha"],
        "hora" : dict_prin["hora"],
        "moneda" : dict_prin["moneda"],
        "denominacion" : dict_prin["denominacion"],
        "productos": conversion_pd_a_list_dict(dataset),
        "subtotal" : dict_prin["subtotal"],
        "igv" : dict_prin["igv"],
        "total" : dict_prin["total"]
    }
    print(f"¡Nuevo registrado con ID: {id_unico}!")
    if dict_prin["cot_o_ord"] == "COTIZACIÓN":
        save_json_cot_data(contenido)
    else:
        save_json_ord_data(contenido)
    return id_unico

def boton_crear_pdf(doc,ruc,cliente,placa,moneda, ven_cre, error_label,scrool,dataset,lmonto,boton_vol,lsigno):
    tabla = pd.read_csv("data/productos_temp.csv")
    if not doc.get() or moneda.get() == 0 and not ruc.get() =="":
        CTkLabel(ven_cre, text="Seleccione tipo de documento y moneda", text_color="red").place(x=350, y=600)
        return

    doc_ = doc.get()
    num_ruc = ruc.get()
    val_cliente = str(cliente.get())
    num_placa = str(placa.get())
    val_signo = moneda.get()

    estado_guia = {}
    estado_guia["pc"] = num_pc()
    estado_guia["cot_o_ord"] = doc_
    estado_guia["ruc"] = num_ruc
    estado_guia["cliente"] = val_cliente
    estado_guia["placa"] = num_placa
    estado_guia["fecha"], estado_guia["hora"] = fecha_hora()

    if val_signo == 1:
        estado_guia["moneda"] = "SOLES"
        estado_guia["denominacion"] = "S/. "
    elif val_signo == 2:
        estado_guia["moneda"] = "DOLARES"
        estado_guia["denominacion"] = "$ "

    estado_guia["subtotal"], estado_guia["igv"], estado_guia["total"] = subtotal_igv_total(tabla)

    id_usar = registar_contenido(estado_guia, tabla)
    ventana_exito(ven_cre, id_usar, scrool, dataset, lmonto)
    restablecer_datos_cliente(doc,ruc,cliente,moneda,placa,error_label)
    ruc.bind("<KeyRelease>", lambda event: verificar_datos_cliente(doc, moneda, ruc, cliente, placa, boton_vol))
    cliente.bind("<KeyRelease>",
                 lambda event: verificar_datos_cliente(doc, moneda, ruc, cliente, placa, boton_vol))
    placa.bind("<KeyRelease>",
               lambda event: verificar_datos_cliente(doc, moneda, ruc, cliente, placa, boton_vol))
    verificar_datos_cliente(doc,moneda,ruc,cliente,placa,boton_vol)
    generar_pdf(id_usar, tabla, estado_guia)
    ven_cre.after(1000, lambda: dect_abrir_documento(id_usar))
    lsigno.configure(text="N")
def restablecer_datos_cliente(tipo_doc_var, ruc_entry, cliente_entry, moneda_var, placa_entry, error_label):
    """
    Restablece los valores de los campos de datos del cliente a su estado inicial.
    """
    tipo_doc_var.set("TEMPORARY")
    tipo_doc_var.set("")  # Restablece el tipo de documento
    ruc_entry.delete(0, 'end')  # Limpia el campo RUC
    cliente_entry.delete(0, 'end')  # Limpia el campo de razón social
    moneda_var.set(0)  # Restablece la moneda a ninguna seleccionada
    placa_entry.delete(0, 'end')  # Limpia el campo de placa
    error_label.configure(text="")  # Limpia la etiqueta de error

def restableecer_datos_de_la_tabla(lmonto):
    dtframe = pd.read_csv("data/productos_temp.csv")
    dtframe.drop(dtframe.index, inplace=True)
    dtframe.reset_index(drop=True, inplace=True)
    dtframe.to_csv("data/productos_temp.csv", index=False)
    dtframe = pd.read_csv("data/productos_temp.csv")
    actualizar_monto(dtframe, lmonto)
def prevenir_cierre():
    print("No")
def ventana_exito(ven_cre,id_unico,scrool,dataset,lmonto):
    ven_exito = CTkToplevel(ven_cre)
    ven_exito.geometry("400x300")
    ven_exito.protocol("WM_DELETE_WINDOW", prevenir_cierre)
    ven_exito.title("Documento Creado")
    ven_exito.iconbitmap("imgs/favicon.ico")
    bloquear_ventana(ven_exito,ven_cre)
    CTkLabel(
        ven_exito,
        text=f"¡ El documento {id_unico}\nse generó exitosamente !",
        font=("Arial", 20, "bold"),
        text_color="springgreen3",
        justify="center"
    ).pack(pady=40)
    def juntar_funciones():
        restableecer_datos_de_la_tabla(lmonto)
        mostrar_productos(scrool)
        ven_exito.destroy()
    CTkButton(
        ven_exito,
        text="Cerrar",
        font=("Arial", 16),
        command=juntar_funciones,
        width=150
    ).place(x=125,y=235)

    CTkButton(
        ven_exito,
        text="Abrir documento",
        font=("Arial", 16),
        command=lambda: dect_abrir_documento(id_unico),
        width=150
    ).place(x=125,y=200)
    actualizar_monto(dataset, lmonto)
    imagen_pil = Image.open("imgs/check.png")
    check = CTkImage(light_image=imagen_pil, size=(70, 70))
    eti_check = CTkLabel(ven_exito, image=check, text="")
    eti_check.place(x=165, y=110)


def verificar_datos_cliente(tipo_doc,moneda,ruc,cliente,placa,boton_vol):
    tiene_datos = (tipo_doc.get() != "" or moneda.get() != 0 or
                   ruc.get().strip() != "" or cliente.get().strip() != "" or
                   placa.get().strip() != "")
    boton_vol.configure(state="disabled" if tiene_datos else "normal")

# Cargar marcas desde CSV
marcas_df = pd.read_csv('data/marcas.csv')
lista_marcas = marcas_df["MARCA"].dropna().unique().tolist()

from customtkinter import *

def seleccionar_marca(marca, entrada, frame_sugerencias):
    entrada.delete(0, "end")
    entrada.insert(0, marca)
    frame_sugerencias.place_forget()  # Ocultar sugerencias

def crear_frame_sugerencias(parent):
    frame = CTkScrollableFrame(parent, width=200, height=0)  # altura se ajustará después
    frame.place_forget()
    return frame

def filtrar_marcas(entrada, frame_sugerencias):
    texto = entrada.get().lower()

    # Limpiar sugerencias anteriores
    for widget in frame_sugerencias.winfo_children():
        widget.destroy()

    if texto == "":
        frame_sugerencias.place_forget()
        return

    # Filtrar solo las marcas que comienzan con el texto escrito
    coincidencias = [m for m in lista_marcas if m.lower().startswith(texto)]

    if coincidencias:
        # Posición del Entry en pantalla
        x = entrada.winfo_x() - 13
        y = entrada.winfo_y() + entrada.winfo_height() -20

        # Altura dinámica → cada botón ~27px, máx. 6 visibles
        altura = min(len(coincidencias), 6) * 27
        frame_sugerencias.configure(height=altura)

        frame_sugerencias.place(x=x, y=y)

        for m in coincidencias:
            btn = CTkButton(
                frame_sugerencias,
                text=m,
                width=180,
                height=25,
                fg_color="transparent",
                text_color=None,  # Auto según tema
                hover_color=("lightgray", "#2a2a2a"),
                anchor="w",
                command=lambda marca_texto=m: seleccionar_marca(marca_texto, entrada, frame_sugerencias)
            )
            btn.pack(fill="x", padx=5, pady=1)
    else:
        frame_sugerencias.place_forget()







# ----------------------------------------
# LIBRERIAS
#-----------------------------------------
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

#------------------------------------------

# ------------------------------------------
# DATASET
#--------------------------------------------


def conversion_pd_a_list_list(dat_pd):
    lista_listas = dat_pd.values.tolist()
    return lista_listas
#-----------------------------------------------


# -----------------------
# COLORES
# -----------------------
# COLOR ROJO PRIN: 192,0,0
# COLOR ROJO SEC: 255,171,171
# COLOR AZUL PRIN: 48,84,150
# COLOR AZUL SEC: 142,169,219
def generar_pdf(id_usar,dataset,dict_pri ):
    if dict_pri["cot_o_ord"] == "COTIZACIÓN":
        color_prin = colors.Color(192/255,0/255,0/255)
        color_sec = colors.Color(255/255,171/255,171/255)
    else:
        color_prin = colors.Color(48/255,84/255,150/255)
        color_sec = colors.Color(142/255,169/255,219/255)
    # -----------------------

    # ***********************
    # ESTILOS
    # ***********************
    estilo = TableStyle([
        # ---- ENCABEZADO ----
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),  # Fondo blanco
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Texto negro
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Negrita
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Centrado

        # Líneas solo inferiores y verticales en encabezado
        ('LINEBELOW', (0, 0), (-1, 0), 1.2, color_prin),  # Línea inferior color principal
        ('LINEBEFORE', (1, 0), (-1, 0), 0.8, color_prin),  # Líneas verticales internas (excepto la primera)

        # ---- CUERPO DE PRODUCTOS ----
        ('GRID', (0, 1), (-1, -1), 0.5, color_sec),  # Rejilla para celdas de productos
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),

        # Quitar borde exterior izquierdo y derecho (visual limpio)
        ('LINEBEFORE', (0, 1), (0, -1), 0.3, colors.white),  # Oculta línea izquierda
        ('LINEAFTER', (-1, 1), (-1, -1), 0.3, colors.white),  # Oculta línea derecha
    ])
    tabla_estilo_info = TableStyle([
        # ENCABEZADO (fila 0)
        ('BACKGROUND', (0,0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), color_prin),
        ('FONTNAME', (0, 0), (-1, 0), 'Roboto-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10.5),

        # RESTO DE FILAS (de la 1 a la última)
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), color_prin),
        ('FONTNAME', (0, 1), (-1, -1), 'Roboto-MediumItalic'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),

        # ALINEACIÓN Y ESPACIADO
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ])

    estilo_firma = TableStyle([
        ('LINEABOVE', (0, 0), (0, 0), 1, colors.black),  # Solo línea superior
        ('LINEBELOW', (0, 0), (0, 0), 0, colors.white),  # Quita línea inferior
        ('LINEBEFORE', (0, 0), (0, 0), 0, colors.white), # Quita línea izquierda
        ('LINEAFTER', (0, 0), (0, 0), 0, colors.white),  # Quita línea derecha

        ('ALIGN', (0, 0), (0, 0), 'CENTER'),             # Alineación horizontal
        ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),            # Alineación vertical

        ('FONTNAME', (0, 0), (0, 0), 'Helvetica'),
        ('FONTSIZE', (0, 0), (0, 0), 10),
        ('TEXTCOLOR', (0, 0), (0, 0), colors.black),
        ('TOPPADDING', (0, 0), (0, 0), 2),
        ('BOTTOMPADDING', (0, 0), (0, 0), 2),
    ])


    # -----------------------
    # 1. Crear el PDF
    # -----------------------
    if dict_pri["cot_o_ord"] == "COTIZACIÓN":
        pdf = canvas.Canvas(f"cotizacion/{id_usar}.pdf", pagesize=A4)
    else:
        pdf = canvas.Canvas(f"ordenes/{id_usar}.pdf", pagesize=A4)
    width, height = A4
    # -----------------------
    # 1.1 Fuentes
    # -----------------------
    pdfmetrics.registerFont(TTFont("Menbere-Thin", "Fonts/Menbere-Thin.ttf"))
    pdfmetrics.registerFont(TTFont("Oswald-SemiBold", "Fonts/Oswald-SemiBold.ttf"))
    pdfmetrics.registerFont(TTFont("Roboto-MediumItalic", "Fonts/RobotoCondensed-MediumItalic.ttf"))
    pdfmetrics.registerFont(TTFont("Roboto-SemiBold", "Fonts/RobotoCondensed-SemiBold.ttf"))
    pdfmetrics.registerFont(TTFont("Roboto-Bold", "Fonts/RobotoCondensed-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("Intel-Italic", "Fonts/IntelOneMono-Italic.ttf"))
    # ----------------------

    # -----------------------
    # 2. LOGO
    # -----------------------
    pdf.drawImage("imgs/logo_imagen.png", x=2 * cm, y=height - 3.8 * cm, width=5 * cm, height=2 * cm)

    # -----------------------
    # 3. Título
    # -----------------------
    pdf.setFont("Helvetica-Bold", 11)
    # 3.1 Encabezado
    pdf.drawString(7.2 * cm, height - 2.35 * cm, "REPUESTOS HUANCA E.I.R.L.")
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(7.2 * cm, height - 2.65 * cm, "AV. COLECTORA MZA A7 LOTE 13 URB.")
    pdf.drawString(7.2 * cm, height - 2.95 * cm, "LOS PORTALES, SANTA ANITA, LIMA - LIMA")
    pdf.drawString(7.2 * cm, height - 3.25 * cm, "repuestoshuanca@hotmail.com")
    pdf.drawString(7.2 * cm, height - 3.55 * cm, "999493285 / 989596852 / 989596848")
    # -----------------------
    # 3.2 Rectangulo
    # -----------------------
    pdf.setStrokeColor(color_prin)  # Color de borde (negro)
    pdf.setLineWidth(1.2)           # Grosor de línea
    #14.5*cm , height - 3.75 * cm
    pdf.roundRect(14.5*cm, height - 3.75 * cm, 4.85 * cm , 1.8 * cm , radius=6.5, stroke=1, fill=0)
    pdf.setFont("Helvetica-Bold", 9.1)
    pdf.drawCentredString(16.9*cm, height-2.56 *cm, f"{dict_pri["cot_o_ord"]}")
    pdf.drawCentredString(16.9*cm, height-2.96 *cm, "RUC : 20515974513")
    pdf.drawCentredString(16.9*cm, height-3.36 *cm, f"{id_usar}")
    # ------------------------

    # -----------------------
    # 4. Datos del Cliente
    # -----------------------
    pdf.setFont("Helvetica", 9.1)
    pdf.drawString(2 * cm, height - 5 * cm, f"FECHA DE EMISIÓN  :   {dict_pri['fecha']}")
    #pdf.drawString(2 * cm, height - 5.5*cm, "FECHA VALIDA : 25-07-2025") # SI ES COTIZACION
    pdf.drawString(2 * cm, height - 5.5 * cm, f"HORA DE EMISION    :   {dict_pri['hora']}")
    pdf.drawString(2 * cm, height - 6 * cm, f"RUC                             :   {dict_pri["ruc"]}")
    pdf.drawString(2 * cm, height - 6.5 * cm, f"RAZON SOCIAL          :   {dict_pri['cliente']}")
    pdf.drawString(2 * cm, height - 7*cm, f"MONEDA                     :   {dict_pri['moneda']}")
    pdf.drawString(2 * cm, height - 7.5*cm, f"PLACA                         :   {dict_pri['placa']}")


    # -----------------------
    # 6. Tabla de productos
    # -----------------------
    produ = conversion_pd_a_list_list(dataset)
    produ.insert(0, ["CANT", "COD","MARCA","DESCRIPCIÓN","PREC. UNIT.","PREC.TOTAL"])

    # Crear tabla
    y_inicio_tabla = height - 8.2 * cm

    tabla = Table(produ, colWidths=[1.3*cm, 2*cm,3.5*cm, 6*cm, 2.3*cm, 2.3*cm])
    tabla.setStyle(estilo)

    # Posicionar tabla
    tabla.wrapOn(pdf, width, height)
    ancho_tabla, alto_tabla = tabla.wrap(0, 0)
    tabla.drawOn(pdf, 2*cm, y_inicio_tabla - alto_tabla)

    datos_totales_v2 = [
        ['', '', '', '', 'Subtotal', f'{dict_pri["denominacion"]}{dict_pri["subtotal"]}'],
        ['', '', '', '', 'IGV', f'{dict_pri["denominacion"]}{dict_pri["igv"]}'],
        ['', '', '', '', 'Total', f'{dict_pri["denominacion"]}{dict_pri["total"]}']
    ]

    tabla_totales = Table(datos_totales_v2, colWidths=[1.3*cm, 2*cm,3.5*cm, 6*cm, 2.3*cm, 2.3*cm])
    tabla_totales.setStyle(TableStyle([
        ('SPAN', (0, 0), (3, 0)),  # Unimos las 4 celdas vacías
        ('SPAN', (0, 1), (3, 1)),
        ('SPAN', (0, 2), (3, 2)),

        ('ALIGN', (5, 0), (5, -1), 'RIGHT'),
        ('FONTNAME', (4, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (4, 0), (-1, -1), 10),
        ('LINEABOVE', (4, 2), (-1, 2), 1, color_prin),
    ]))
    y_totales = y_inicio_tabla - alto_tabla - 2.2*cm
    tabla_totales.wrapOn(pdf, width, height)

    tabla_totales.drawOn(pdf, 2*cm, y_totales)

    tb_cuentas = [
        ["CUENTAS BANCARIAS :"],
        ["  BCP SOLES        :   191-1608322-0-76"],
        ["  BCP DOLARES  :   191-2098562-1-04"]
    ]

    tb_terminos_coti = [
        ["TERMINOS Y CONDICIONES :"],
        ["   Cotización valida por las 72 horas desde su emisión,"],
        ["   sujeta a cambios."]
    ]

    tb_terminos_ord = [
        ["TERMINOS Y CONDICIONES :"],
        ["Orden de Compra sujeta a facturación al momento de su"],
        ["cancelación, en caso de deuda con letra de cambio."]
    ]

    tb_firma = [
        ["RECIBIDO POR"]
    ]


    tabla_cuentas = Table(tb_cuentas, colWidths=[6*cm])
    tabla_cuentas.setStyle(tabla_estilo_info)
    tabla_cuentas.wrapOn(pdf, width, height)
    tabla_cuentas.drawOn(pdf, 2*cm, y_totales- 2*cm)

    if dict_pri["cot_o_ord"] == "Cotización":
        tabla_reco = Table(tb_terminos_coti, colWidths=[6*cm])
        tabla_reco.setStyle(tabla_estilo_info)
        tabla_reco.wrapOn(pdf, width, height)
        tabla_reco.drawOn(pdf, 2*cm, y_totales- 4.5*cm)
    else:
        tabla_reco = Table(tb_terminos_ord, colWidths=[6*cm])
        tabla_reco.setStyle(tabla_estilo_info)
        tabla_reco.wrapOn(pdf, width, height)
        tabla_reco.drawOn(pdf, 2 * cm, y_totales - 4.5 * cm)

    tabla_firma = Table(tb_firma, colWidths=[4.6*cm])
    tabla_firma.setStyle(estilo_firma)
    tabla_firma.wrapOn(pdf, width, height)
    tabla_firma.drawOn(pdf, 14.8*cm, y_totales- 4.2*cm)


    # -----------------------
    # 7. Pie de página
    # -----------------------
    pdf.setFont("Intel-Italic", 8)
    pdf.drawString(2 * cm, 2 * cm, "Gracias por confiar en nosotros.")


    # Guardar
    pdf.save()
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
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

def conversion_pd_a_list_list(dat_pd):
    lista_listas = dat_pd.values.tolist()
    return lista_listas

def generar_pdf(id_usar, dataset, dict_pri):
    inicio_pdf = 1.3
    if dict_pri["cot_o_ord"] == "COTIZACIÓN":
        color_prin = colors.Color(192/255,0/255,0/255)
        color_sec = colors.Color(255/255,171/255,171/255)
    else:
        color_prin = colors.Color(48/255,84/255,150/255)
        color_sec = colors.Color(142/255,169/255,219/255)

    # --- estilos de tablas ---
    estilo = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('LINEBELOW', (0, 0), (-1, 0), 1.2, color_prin),
        ('LINEBEFORE', (1, 0), (-1, 0), 0.8, color_prin),
        ('LINEABOVE', (0, 1), (-1, -1), 0.5, color_sec),  # Líneas horizontales
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('LINEBEFORE', (0, 1), (0, -1), 0.3, colors.white),
        ('LINEAFTER', (-1, 1), (-1, -1), 0.3, colors.white),
        ('VALIGN', (0, 1), (-1, -1), 'TOP'),
        ('ROWHEIGHT', (0, 1), (-1, -1), 15),
        ('LINEBELOW', (0, -1), (-1, -1), 0.5, color_sec),  # Línea horizontal final
    ])

    tabla_estilo_info = TableStyle([
        ('BACKGROUND', (0,0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), color_prin),
        ('FONTNAME', (0, 0), (-1, 0), 'Roboto-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10.5),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), color_prin),
        ('FONTNAME', (0, 1), (-1, -1), 'Roboto-MediumItalic'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ])

    estilo_firma = TableStyle([
        ('LINEABOVE', (0, 0), (0, 0), 1, colors.black),
        ('LINEBELOW', (0, 0), (0, 0), 0, colors.white),
        ('LINEBEFORE', (0, 0), (0, 0), 0, colors.white),
        ('LINEAFTER', (0, 0), (0, 0), 0, colors.white),
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
        ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica'),
        ('FONTSIZE', (0, 0), (0, 0), 10),
        ('TEXTCOLOR', (0, 0), (0, 0), colors.black),
        ('TOPPADDING', (0, 0), (0, 0), 2),
        ('BOTTOMPADDING', (0, 0), (0, 0), 2),
    ])

    # --- crear PDF ---
    if dict_pri["cot_o_ord"] == "COTIZACIÓN":
        pdf = canvas.Canvas(f"cotizacion/{id_usar}.pdf", pagesize=A4)
    else:
        pdf = canvas.Canvas(f"ordenes/{id_usar}.pdf", pagesize=A4)
    width, height = A4
    pdf.setTitle(id_usar)

    # --- fuentes ---
    pdfmetrics.registerFont(TTFont("Menbere-Thin", "Fonts/Menbere-Thin.ttf"))
    pdfmetrics.registerFont(TTFont("Oswald-SemiBold", "Fonts/Oswald-SemiBold.ttf"))
    pdfmetrics.registerFont(TTFont("Roboto-MediumItalic", "Fonts/RobotoCondensed-MediumItalic.ttf"))
    pdfmetrics.registerFont(TTFont("Roboto-SemiBold", "Fonts/RobotoCondensed-SemiBold.ttf"))
    pdfmetrics.registerFont(TTFont("Roboto-Bold", "Fonts/RobotoCondensed-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("Intel-Italic", "Fonts/IntelOneMono-Italic.ttf"))

    # --- logo ---
    pdf.drawImage("imgs/logo_imagen.png", x=inicio_pdf * cm, y=height - 3.8 * cm, width=5 * cm, height=2 * cm)

    # --- título ---
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(6.5 * cm, height - 2.35 * cm, "REPUESTOS HUANCA E.I.R.L.")
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(6.5 * cm, height - 2.65 * cm, "AV. COLECTORA MZA A7 LOTE 13 URB.")
    pdf.drawString(6.5 * cm, height - 2.95 * cm, "LOS PORTALES, SANTA ANITA, LIMA - LIMA")
    pdf.drawString(6.5 * cm, height - 3.25 * cm, "repuestoshuanca@hotmail.com")
    pdf.drawString(6.5 * cm, height - 3.55 * cm, "999493285 / 989596852 / 989596848")

    pdf.setStrokeColor(color_prin)
    pdf.setLineWidth(1.2)
    pdf.roundRect(14.7*cm, height - 3.75 * cm, 4.85 * cm , 1.8 * cm , radius=6.5, stroke=1, fill=0) #F
    pdf.setFont("Helvetica-Bold", 9.1)#F
    pdf.drawCentredString(17.1*cm, height-2.56 *cm, f"{dict_pri['cot_o_ord']}")#F
    pdf.drawCentredString(17.1*cm, height-2.96 *cm, "RUC : 20515974513")#F
    pdf.drawCentredString(17.1*cm, height-3.36 *cm, f"{id_usar}")#F

    # --- datos cliente ---
    pdf.setFont("Helvetica", 9.1)
    pdf.drawString(inicio_pdf * cm, height - 5 * cm, f"FECHA DE EMISIÓN  :   {dict_pri['fecha']}")
    pdf.drawString(inicio_pdf * cm, height - 5.5 * cm, f"HORA DE EMISION    :   {dict_pri['hora']}")
    pdf.drawString(inicio_pdf * cm, height - 6 * cm, f"RUC                             :   {dict_pri['ruc']}")
    pdf.drawString(inicio_pdf * cm, height - 6.5 * cm, f"RAZON SOCIAL          :   {dict_pri['cliente']}")
    pdf.drawString(inicio_pdf * cm, height - 7*cm, f"MONEDA                     :   {dict_pri['moneda']}")
    pdf.drawString(inicio_pdf * cm, height - 7.5*cm, f"PLACA                         :   {dict_pri['placa']}")

    # --- tabla productos ---
    produ = conversion_pd_a_list_list(dataset)
    produ.insert(0, ["ITEM","CANT","COD","MARCA","DESCRIPCIÓN","PRE.UNIT.","PRE.TOT."])
    # estilo para COD
    estilo_cod = ParagraphStyle(
        name="codigo",
        fontName="Helvetica",
        fontSize=9,
        alignment=1,  # centrado
        leading=11,
        wordWrap='CJK',
        maxWidth=2 * cm,
        maxLines=1
    )
    for i in range(1, len(produ)):
        produ[i][2] = Paragraph(str(produ[i][2]), estilo_cod)
    # estilo para descripción
    estilo_desc = ParagraphStyle(
        name="descripcion",
        fontName="Helvetica",
        fontSize=9,
        alignment=0,
        leading=11,
        wordWrap='CJK',
        maxWidth=4.5*cm,
        maxLines=1  # Limita a una sola línea
    )
    for i in range(1, len(produ)):
        produ[i][4] = Paragraph(str(produ[i][4]), estilo_desc)

    for i in range(1, len(produ)):
        produ[i][5] = f"{produ[i][5]:.2f}"
        produ[i][6] = f"{produ[i][6]:.2f}"
    y_inicio_tabla = height - 8.2 * cm
    tabla = Table(produ, colWidths=[1.3*cm,1.3*cm, 2*cm,3.5*cm, 6*cm, 2.1*cm, 2.1*cm])
    tabla.setStyle(estilo)
    tabla.wrapOn(pdf, width, height)
    ancho_tabla, alto_tabla = tabla.wrap(0, 0)
    tabla.drawOn(pdf, inicio_pdf*cm, y_inicio_tabla - alto_tabla)

    # --- totales ---
    datos_totales_v2 = [
        ['', '', '', "", '', 'Subtotal', f'{dict_pri["denominacion"]}{dict_pri["subtotal"]:.2f}'],
        ['', '', '', '', "", 'IGV', f'{dict_pri["denominacion"]}{dict_pri["igv"]:.2f}'],
        ['', '', '', '', "",'Total', f'{dict_pri["denominacion"]}{dict_pri["total"]:.2f}']
    ]
    tabla_totales = Table(datos_totales_v2, colWidths=[1.3*cm,1.3 * cm, 2 * cm, 3.5 * cm, 6 * cm, 2.1 * cm, 2.1 * cm])
    #tabla_totales = Table(datos_totales_v2, colWidths=[1.3*cm, 2*cm, 3.5*cm, 4.5*cm, 2.3*cm, 2.3*cm])
    tabla_totales.setStyle(TableStyle([
        ('SPAN', (0, 0), (4, 0)),
        ('SPAN', (0, 1), (4, 1)),
        ('SPAN', (0, 2), (4, 2)),
        ('ALIGN', (6, 0), (6, -1), 'RIGHT'),
        ('FONTNAME', (5, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (5, 0), (-1, -1), 10),
        ('LINEABOVE', (5, 2), (-1, 2), 1, color_prin),
    ]))
    y_totales = y_inicio_tabla - alto_tabla - 2.2*cm
    tabla_totales.wrapOn(pdf, width, height)
    tabla_totales.drawOn(pdf, inicio_pdf*cm, y_totales)

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
        ["   Orden de Compra sujeta a facturación al momento de su"],
        ["   cancelación, en caso de deuda con letra de cambio."]
    ]
    tb_firma = [["RECIBIDO POR"]]

    tabla_cuentas = Table(tb_cuentas, colWidths=[6*cm])
    tabla_cuentas.setStyle(tabla_estilo_info)
    tabla_cuentas.wrapOn(pdf, width, height)
    tabla_cuentas.drawOn(pdf, inicio_pdf*cm, y_totales- 2*cm)

    if dict_pri["cot_o_ord"] == "Cotización":
        tabla_reco = Table(tb_terminos_coti, colWidths=[6*cm])
    else:
        tabla_reco = Table(tb_terminos_ord, colWidths=[6*cm])
    tabla_reco.setStyle(tabla_estilo_info)
    tabla_reco.wrapOn(pdf, width, height)
    tabla_reco.drawOn(pdf, inicio_pdf*cm, y_totales- 4.5*cm)

    tabla_firma = Table(tb_firma, colWidths=[4.6*cm])
    tabla_firma.setStyle(estilo_firma)
    tabla_firma.wrapOn(pdf, width, height)
    tabla_firma.drawOn(pdf, 15*cm, y_totales- 4.2*cm)

    pdf.save()

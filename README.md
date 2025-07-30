# Sistema de Órdenes y Cotizaciones

Este proyecto es una aplicación de escritorio desarrollada en Python con CustomTkinter, diseñada para registrar productos, generar cotizaciones y órdenes de compra, exportar datos a CSV y trabajar con una interfaz moderna.

## 🧩 Características
- Interfaz gráfica intuitiva con CustomTkinter
- Registro de productos y servicios
- Generación de cotizaciones profesionales en PDF
- Creación de órdenes de compra
- Creación de cotizaciones
- Soporte para múltiples productos en una sola operación
- Compatible con sistemas Windows

## 🚀 Tecnologías utilizadas
- Python 3.13
- CustomTkinter
- Pandas
- ReportLab (para generación de PDF)
- PIL (para manejo de imágenes)
- os, json, csv

## 📦 Instalación y uso

1. Descarga el archivo ZIP desde la pestaña [Releases](https://github.com/Migui173/Creacion_de_Cotizacion_Ordenes___RH/releases)
2. Extrae el contenido
3. Ejecuta `ventana_eje_cot_ord.exe` (si está compilado) o `ventana_eje_cot_ord.py` si tienes Python instalado.
4. Asegúrate de tener las dependencias instaladas si lo corres desde código fuente:

```bash
pip install -r requirements.txt
```
5. (Opcional) Para un mejor ajuste tener los accesos directos en el escritorio del `ventana_eje_cot_ord.exe` y de las carpetas `cotizaciones` y `ordenes`

## 📁 Estructura del Proyecto

```
Creacion_de_Cotizacion_Ordenes___RH/
├── ventana_eje_cot_ord.py      # Interfaz principal de usuario
├── func_ctk.py                 # Funciones auxiliares y lógicas de producto
├── gen_pdf.py                  # Función para la generación de pdfs
├── data/                       # Carpeta donde se almacenan los datos JSON y CSV
├── imgs/                       # Imágenes e íconos
├── dist/                       # Carpeta para el ejecutable o ZIP compilado
├── requirements.txt            # Lista de dependencias
├── pc.txt                      # Número de pc donde va ser instaldo el programa
└── README.md                   # Este archivo
```

## 👥 Público objetivo
- Pequeñas empresas
- Emprendedores
- Usuarios sin conocimientos técnicos que necesitan automatizar procesos de compra y cotización

## 📃 Licencia
Este proyecto está bajo la Licencia MIT.

### 🧑 Creador del programa
The Miguelin Projects

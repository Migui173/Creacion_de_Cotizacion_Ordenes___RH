# Sistema de Órdenes y Cotizaciones

Este proyecto es una aplicación de escritorio desarrollada en Python con CustomTkinter, diseñada para registrar productos, generar cotizaciones y órdenes de compra, exportar datos a CSV y trabajar con una interfaz moderna.

## 🧩 Características
- Interfaz gráfica intuitiva con CustomTkinter
- Registro de productos y servicios
- Generación de cotizaciones profesionales en PDF
- Creación de órdenes de compra
- Exportación de datos a archivos CSV
- Soporte para múltiples productos en una sola operación
- Compatible con sistemas Windows

## 🚀 Tecnologías utilizadas
- Python 3
- CustomTkinter
- Pandas
- fpdf / ReportLab (para generación de PDF)
- PIL (para manejo de imágenes)
- os, json, csv

## 📦 Instalación y uso

1. Descarga el archivo ZIP desde la pestaña [Releases](https://github.com/TU_USUARIO/ordenes_cotizaciones/releases)
2. Extrae el contenido
3. Ejecuta `ventana_eje_cot_ord.exe` (si está compilado) o `ventana_eje_cot_ord.py` si tienes Python instalado.
4. Asegúrate de tener las dependencias instaladas si lo corres desde código fuente:

```bash
pip install -r requirements.txt
```

## 📁 Estructura del Proyecto

```
Creacion_de_Cotizacion_Ordenes___RH/
├── ventana_eje_cot_ord.py      # Interfaz principal de usuario
├── func_ctk.py                 # Funciones auxiliares y lógicas de producto
├── data/                       # Carpeta donde se almacenan los datos JSON
├── assets/                     # Imágenes e íconos
├── dist/                       # Carpeta para el ejecutable o ZIP compilado
├── requirements.txt            # Lista de dependencias
└── README.md                   # Este archivo
```

## 👥 Público objetivo
- Pequeñas empresas
- Emprendedores
- Usuarios sin conocimientos técnicos que necesitan automatizar procesos de compra y cotización

## 📃 Licencia
Este proyecto está bajo la Licencia MIT.

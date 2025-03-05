import streamlit as st
import re
import os
import subprocess
import time
import webbrowser


def login():
    st.title("🔒 Ingreso a Buscador de Kits")
    usuario = st.text_input("Usuario")
    contraseña = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if (usuario == "admin" and contraseña == "Serfriair25") or (usuario == "Partner" and contraseña == "Serfriair25"): 
            st.session_state["autenticado"] = True
            st.session_state["recargar"] = True
        else:
            st.error("Usuario o contraseña incorrectos")

if "autenticado" not in st.session_state or not st.session_state["autenticado"]:
    login()
    st.stop()

def extraer_valores_serie(serie):
    """Extrae los valores de la serie en formato SS-AA-VALOR o PXXXXXX."""
    match = re.match(r"(\d+)-(\d+)-([A-Z\d]+)", serie)
    if match:
        semana, anio, valor = match.groups()
        return int(anio), int(semana), valor  # Devuelve el año, la semana y el número
    return None, None, serie  # Si no es SS-AA-VALOR, devuelve la serie original

# Diccionario de equivalencias entre nombres de modelos
equivalencias_modelo = {
    "MKE23": "SDN10", "SDN10": "SDN10",
    "MKE38": "SDN20", "SDN20": "SDN20",
    "MKE53": "SDN30", "SDN30": "SDN30",
    "MKE70": "SDN35", "SDN35": "SDN35",
    "MKE100": "SDN40", "SDN40": "SDN40",
    "MKE155": "SDN50", "SDN50": "SDN50",
    "MKE190": "SDN60", "SDN60": "SDN60",
    "MKE210": "SDN70", "SDN70": "SDN70",
    "MKE305": "SDN80", "SDN80": "SDN80",
    "MKE375": "SDN90", "SDN90": "SDN90",
    "MKE495": "SDN100", "SDN100": "SDN100",
    "MKE623": "SDN110", "SDN110": "SDN110",
    "MKE930": "SDN120", "SDN120": "SDN120",
    "MKE1200": "SDN130", "SDN130": "SDN130",
    "MKE1388": "SDN140", "SDN140": "SDN140",
    "MKE1800": "SDN150", "SDN150": "SDN150",
    "MKE2500": "SDN160", "SDN160": "SDN160",
    "MKE2775": "SDN170", "SDN170": "SDN170",
    "MKE3330": "SDN180", "SDN180": "SDN180",
    "MKE3915": "SDN190", "SDN190": "SDN190",
    "MKE5085": "SDN200", "SDN200": "SDN200",
    "MKE5850": "SDN210", "SDN210": "SDN210"
}

# Base de datos integrada en el código
data = [
    ["SDN10", "MKO50KIT", "hasta: 14-18-MA09504"],
    ["SDN10", "MKO45KIT", "desde: 14-18-MA09505 hasta: P100070791"],
    ["SDN10", "MKON55KIT", "desde: P100070792 hasta: P104774156"],
    ["SDN10", "MKON65KIT", "desde: P104774157"],
    ["SDN20", "MKO50KIT", "hasta: 14-18-MA09504"],
    ["SDN20", "MKO45KIT", "desde: 14-18-MA09505 hasta: P100070791"],
    ["SDN20", "MKON55KIT", "desde: P100070792 hasta: P104774156"],
    ["SDN20", "MKON65KIT", "desde: P104774157"],
    ["SDN30", "MKO50KIT", "hasta: 14-18-MA09504"],
    ["SDN30", "MKO45KIT", "desde: 14-18-MA09505 hasta: P100070791"],
    ["SDN30", "MKON55KIT", "desde: P100070792 hasta: P104774156"],
    ["SDN30", "MKON65KIT", "desde: P104774157"],
]

def obtener_kit(modelo, numero_serie):
    modelo_normalizado = equivalencias_modelo.get(modelo, modelo)
    anio_serie, semana_serie, valor_serie = extraer_valores_serie(numero_serie)

    # 📌 Regla General para números de serie en formato SS-AA-VALOR
    if modelo_normalizado in ["SDN10", "MKE23"] and anio_serie is not None:
    if (anio_serie > 18 or 
        (anio_serie == 18 and semana_serie > 14) or 
        (anio_serie == 18 and semana_serie == 14 and valor_serie >= "MA09505")):
        return "El kit correspondiente es: MKO45KIT"
    else:
        return "El kit correspondiente es: MKO50KIT"

    # 📌 Regla para modelos con formato PXXXXX
    if valor_serie.startswith("P"):
        if modelo_normalizado in ["SDN30", "MKE53"] and valor_serie >= "P104774157":
            return "El kit correspondiente es: MKON65KIT"
        if modelo_normalizado in ["SDN10", "MKE23"] and "P100070792" <= valor_serie <= "P104774156":
            return "El kit correspondiente es: MKON55KIT"
        if modelo_normalizado in ["SDN10", "MKE23"] and valor_serie >= "P104774157":
            return "El kit correspondiente es: MKON65KIT"

    # 📌 Recorre la base de datos integrada para buscar coincidencias
    for row in data:
        if modelo_normalizado == row[0]:
            kit, rango_serie = row[1], row[2]
            if not rango_serie:
                return f"El kit correspondiente es: {kit}"
            match_hasta = re.search(r"hasta:\s*([P\d-]+)", rango_serie)
            match_desde = re.search(r"desde:\s*([P\d-]+)", rango_serie)
            if match_hasta and numero_serie <= match_hasta.group(1):
                return f"El kit correspondiente es: {kit}"
            if match_desde and numero_serie >= match_desde.group(1):
                return f"El kit correspondiente es: {kit}"

    return "No se encontró un kit asociado. Por favor, revise el modelo y el número de serie."

st.title("\U0001F50D Buscador de Kits por Número de Serie")
modelo = st.text_input("Ingrese el modelo del secador:")
numero_serie = st.text_input("Ingrese el número de serie:")

if st.button("Buscar Kit"):
    if modelo and numero_serie:
        resultado = obtener_kit(modelo, numero_serie)
        st.success(resultado)
    else:
        st.warning("Por favor, ingrese un modelo y un número de serie.")

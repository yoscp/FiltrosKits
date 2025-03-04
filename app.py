import streamlit as st
import pandas as pd
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

# Base de datos interna en el código
data = [
    ["SDN10", "MKO50KIT", "hasta: 14-18-MA09504"],
    ["SDN10", "MKO45KIT", "desde: 14-18-MA09505"],
    ["SDN20", "MKO50KIT", ""],
    ["SDN20", "MKO45KIT", "desde: 14-18-MA09505 hasta: P100070791"],
    ["SDN20", "MKON55KIT", "desde: P100070792 hasta: P104774156"],
    ["SDN20", "MKON65KIT", "desde: P104774157"],
    ["SDN30", "MKO50KIT", "desde: P10000000 hasta: P1134515181"],
    ["SDN50", "MKO155KIT", "desde: 01-22-MA05400 hasta: 01-22-MA05450"],
    ["SDN40", "MKON155KIT", "desde: 04-20-MA06260"],
    ["SDN50", "MKON155KIT", "desde: 04-20-MA06260"],
    ["SDN60", "MKON155KIT", "desde: 04-20-MA06260"],
    ["SDN40", "MKON155KIT", "desde: P00000000"],
    ["SDN50", "MKON155KIT", "desde: P00000000"],
    ["SDN60", "MKON155KIT", "desde: P00000000"],
    ["SDN10", "MKON65KIT", "desde: P104774157"],
    ["SDN20", "MKON65KIT", "desde: P104774157"],
    ["SDN30", "MKON65KIT", "desde: P104774157"],
    ["SDN180", "MKOHC5850KIT", "desde: P00000000"],
    ["SDN190", "MKOHC5850KIT", "desde: P00000000"],
    ["SDN200", "MKOHC5850KIT", "desde: P00000000"],
    ["SDN210", "MKOHC5850KIT", "desde: P00000000"],
    ["SDN180", "2 x MKO2700KIT", "hasta: 02-20-MA05588"],
    ["SDN180", "MKOHC5850KIT", "desde: 02-20-MA05589"],
    ["SDN40", "MKON155KIT", "desde: 04-20-MA06260"],
    ["SDN50", "MKON155KIT", "desde: 04-20-MA06260"],
    ["SDN60", "MKON155KIT", "desde: 04-20-MA06260"],
]

def obtener_kit(modelo, numero_serie):
    modelo_normalizado = equivalencias_modelo.get(modelo, modelo)
    for _, row in df_filtered.iterrows():
        if modelo_normalizado == row["Modelo"]:
            kit = row["Kit"]
            rango_serie = row["N_Serie"]
            if not rango_serie:
                return f"El kit correspondiente es: {kit}"
            match_hasta = re.search(r"hasta:\s*([P\d]+)", rango_serie)
            match_desde = re.search(r"desde:\s*([P\d]+)", rango_serie)
            if match_hasta and numero_serie <= match_hasta.group(1):
                return f"El kit correspondiente es: {kit}"
            if match_desde and numero_serie >= match_desde.group(1):
                return f"El kit correspondiente es: {kit}"
    return "No se encontró un kit asociado. Por favor, revise el modelo y el número de serie."

df_filtered = pd.DataFrame(data, columns=["Modelo", "Kit", "N_Serie"])

st.title("🔍 Buscador de Kits por Número de Serie")
modelo = st.text_input("Ingrese el modelo del secador:")
numero_serie = st.text_input("Ingrese el número de serie:")

if st.button("Buscar Kit"):
    if modelo and numero_serie:
        resultado = obtener_kit(modelo, numero_serie)
        st.success(resultado)
    else:
        st.warning("Por favor, ingrese un modelo y un número de serie.")

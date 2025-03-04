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
    "MKE-23": "SDN10", "SDN10": "SDN10",
    "MKE-38": "SDN20", "SDN20": "SDN20",
    "MKE-53": "SDN30", "SDN30": "SDN30",
    "MKE-70": "SDN35", "SDN35": "SDN35",
    "MKE-100": "SDN40", "SDN40": "SDN40",
    "MKE-155": "SDN50", "SDN50": "SDN50",
    "MKE-190": "SDN60", "SDN60": "SDN60",
    "MKE-210": "SDN70", "SDN70": "SDN70",
    "MKE-305": "SDN80", "SDN80": "SDN80",
    "MKE-375": "SDN90", "SDN90": "SDN90",
    "MKE-495": "SDN100", "SDN100": "SDN100",
    "MKE-623": "SDN110", "SDN110": "SDN110",
    "MKE-930": "SDN120", "SDN120": "SDN120",
    "MKE-1200": "SDN130", "SDN130": "SDN130",
    "MKE-1388": "SDN140", "SDN140": "SDN140",
    "MKE-1800": "SDN150", "SDN150": "SDN150",
    "MKE-2500": "SDN160", "SDN160": "SDN160",
    "MKE-2775": "SDN170", "SDN170": "SDN170",
    "MKE-3330": "SDN180", "SDN180": "SDN180",
    "MKE-3915": "SDN190", "SDN190": "SDN190",
    "MKE-5085": "SDN200", "SDN200": "SDN200",
    "MKE-5850": "SDN210", "SDN210": "SDN210"
}

# Base de datos interna en el código
data = [
    ["SDN10", "MKO50KIT", "hasta: 14-18-MA09504"],
    ["SDN10", "MKO45KIT", ""],
    ["SDN10", "MKON55KIT", ""],
    ["SDN10", "MKON65KIT", ""],
    ["SDN20", "MKO50KIT", ""],
    ["SDN20", "MKO45KIT", "desde: 14-18-MA09505 hasta: P100070791"],
    ["SDN20", "MKON55KIT", "desde: P100070792 hasta: P104774156"],
    ["SDN20", "MKON65KIT", "desde: P104774157"],
    ["SDN30", "MKO50KIT", ""],
    ["SDN30", "MKO45KIT", ""],
    ["SDN30", "MKON55KIT", ""],
    ["SDN30", "MKON65KIT", ""],
    ["SDN35", "MKON65KIT", "desde: P104774157"],
    ["SDN35", "MKON75KIT", "desde: P100070792 hasta: P104774156"],
    ["SDN35", "MKO70KIT", "hasta: P100070791"],
    ["SDN40", "MKON155KIT", "desde: 04-20-MA06260"],
    ["SDN40", "MKO150KIT", ""],
]

df_filtered = pd.DataFrame(data, columns=["Modelo", "Kit", "N_Serie"])

def obtener_kit(modelo, numero_serie):
    modelo_normalizado = equivalencias_modelo.get(modelo, modelo)
    numero_serie_num = int(re.sub(r"\D", "", numero_serie))

    for _, row in df_filtered.iterrows():
        modelo_guardado = str(row["Modelo"]).strip()

        if modelo_normalizado == modelo_guardado:
            kit_asociado = str(row["Kit"]).strip()
            rango_serie = str(row["N_Serie"]).strip()

            match_hasta = re.search(r"hasta:\s*([\w-]+)", rango_serie)
            match_desde = re.search(r"desde:\s*([\w-]+)", rango_serie)

            dentro_rango = False

            if match_hasta:
                serie_max = match_hasta.group(1)
                serie_max_num = int(re.sub(r"\D", "", serie_max))
                if numero_serie_num <= serie_max_num:
                    dentro_rango = True

            if match_desde:
                serie_min = match_desde.group(1)
                serie_min_num = int(re.sub(r"\D", "", serie_min))
                if numero_serie_num >= serie_min_num:
                    dentro_rango = True

            if dentro_rango:
                return f"El kit correspondiente es: {kit_asociado}"

    return "No se encontró un kit asociado. Por favor, revise el modelo y el número de serie."

st.title("🔍 Buscador de Kits por Número de Serie")
modelo = st.text_input("Ingrese el modelo del secador:")
numero_serie = st.text_input("Ingrese el número de serie:")

if st.button("Buscar Kit"):
    if modelo and numero_serie:
        resultado = obtener_kit(modelo, numero_serie)
        st.success(resultado)
    else:
        st.warning("Por favor, ingrese un modelo y un número de serie.")

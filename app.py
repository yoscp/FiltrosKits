import streamlit as st 
import re
import os
import subprocess
import time
import webbrowser

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
    ["SDN10", "MKO45KIT ", "desde: 14-18-MA09505"],
    ["SDN20", "MKO45KIT PVP 156EUR", "desde: 14-18-MA09505 hasta: P100070791"],
    ["SDN20", "MKON55KIT", "desde: P100070792 hasta: P104774156"],
    ["SDN20", "MKON65KIT", "desde: P104774157"],
    ["SDN30", "MKO50KIT", "desde: P10000000 hasta: P1134515181"],
    ["SDN30", "MKO45KIT PVP 156EUR", "desde: 14-18-MA09505 hasta: P100070791"],
    ["SDN35", "MKON65KIT", "desde: P104774157"],
    ["SDN35", "MKON75KIT", "desde: P100070792 hasta: P104774156"],
    ["SDN35", "MKO70KIT", "hasta: P100070791"],
    ["SDN40", "MKON155KIT", "desde: 04-20-MA06260 y desde P000000000"],
    ["SDN40", "MKO150KIT", "hasta: 04-20-MA06259"],
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
    ["SDN180", "MKOHC5850KIT", "desde: 02-20-MA05589"],
    ["SDN180", "2 x MKO2700KIT", "hasta: 02-20-MA05588"],
    ["SDN190", "MKOHC5850KIT", "desde: P00000000"],
    ["SDN190", "MKOHC5850KIT", "desde: 02-20-MA05589"],
    ["SDN190", "2 x MKO2700KIT", "hasta: 02-20-MA05588"],
    ["SDN200", "MKOHC5850KIT", "desde: P00000000"],
    ["SDN200", "2 x MKO2700KIT", "hasta: 02-20-MA05588"],
    ["SDN200", "MKOHC5850KIT", "desde: 02-20-MA05589"],
    ["SDN210", "MKOHC5850KIT", "desde: P00000000"],
    ["SDN210", "2 x MKO2700KIT", "hasta: 02-20-MA05588"],
    ["SDN210", "MKOHC5850KIT", "desde: 02-20-MA05589"],
    ["SDN40", "MKON155KIT", "desde: 04-20-MA06260"],
    ["SDN50", "MKON155KIT", "desde: 04-20-MA06260"],
    ["SDN60", "MKON155KIT", "desde: 04-20-MA06260"],
    ["SDN70", "MKON405KIT", "desde: P100078377"],
    ["SDN70", "MKO500KIT", "hasta: P100078376"],
    ["SDN80", "MKON405KIT", "desde: P100078377"],
    ["SDN80", "MKO500KIT", "hasta: P100078376"],
    ["SDN90", "MKON405KIT", "desde: P100078377"],
    ["SDN90", "MKO500KIT", "hasta: P100078376"],
    ["SDN100", "MKO851KIT", "hasta: P100077609"],
    ["SDN100", "MKO805KIT", "desde: P100077610"],
    ["SDN110", "MKON805KIT", "desde: P100077610"],
    ["SDN110", "MKO1210KIT", "hasta: P100077609"],
    ["SDN120", "MKON1205KIT", "desde: P100077610"],
    ["SDN120", "MKO1210KIT", "hasta: P100077609"],
    ["SDN130", "MKON1205KIT", "desde: P100077610"],
    ["SDN130", "MKO1210KIT", "hasta: P100077609"],
    ["SDN140", "MKONHC1805 KIT", "desde: P100079932"],
    ["SDN140", "MKO1820KIT", "hasta: P100079931"],
    ["SDN150", "MKONHC1805 KIT", "desde: P100079932"],
    ["SDN150", "MKO1820KIT", "hasta: P100079931"],
    ["SDN160", "MKONHC2775 KIT", "desde: P101076064"],
    ["SDN160", "MKO2700KIT", "hasta: P101076063"],
    ["SDN170", "MKONHC2775 KIT", "desde: P101076064"],
    ["SDN170", "MKO2700KIT", "hasta: P101076063"]
]

def validar_datos(modelo, numero_serie):
    """Verifica si el modelo y el número de serie son correctos."""
    
    # 📌 Verificar si el modelo existe en la base de equivalencias
    if modelo not in equivalencias_modelo:
        return "Número de modelo incorrecto"
        
    # 📌 Expresión regular mejorada para validar formatos
    formato_ssaa = re.fullmatch(r"\d{2}-\d{2}-MA\d{5}$", numero_serie)  # Exactamente SS-AA-MA##### (5 dígitos después de MA)
    formato_pnnnnnnnnn = re.fullmatch(r"P\d{9}$", numero_serie)  # Exactamente P seguido de 9 dígitos
    
    if not formato_ssaa and not formato_pnnnnnnnnn:
        return "Número de serie incorrecto"
    return None
    
def obtener_kit(modelo, numero_serie):

    # 📌 Validación del modelo y número de serie
    error_validacion = validar_datos(modelo, numero_serie)
    if error_validacion:
        return error_validacion
        
    modelo_normalizado = equivalencias_modelo.get(modelo, modelo)
    anio_serie, semana_serie, valor_serie = extraer_valores_serie(numero_serie)

      
    # 📌 Regla General para números de serie en formato SS-AA-VALOR

    if modelo_normalizado in ["SDN10","MKE23","SDN20","MKE38","SDN30","MKE53"] \
       and valor_serie.startswith("P") and valor_serie <= "P100070791":
        return "El kit correspondiente es: MKO45KIT, PVP 156 EUR"
           
    if modelo_normalizado in ["SDN10", "MKE23", "SDN20", "MKE38", "SDN30", "MKE53"] and anio_serie is not None:
        if (anio_serie > 18) or (anio_serie == 18 and semana_serie > 14) or \
           (anio_serie == 18 and semana_serie == 14 and valor_serie >= "MA09505"):
            return "El kit correspondiente es: MKO45KIT, PVP 156EUR."
        else:
            return "El kit correspondiente es: MKO50KIT, PVP 156EUR."

    # 📌 Regla para modelos con formato PXXXXX
    if valor_serie.startswith("P"):
        if modelo_normalizado in ["SDN70", "MKE210", "SDN80", "MKE305", "SDN90", "MKE375"] and valor_serie >= "P100078377":
            return "El kit correspondiente es: MKON405KIT , PVP 447EUR."
            
        if modelo_normalizado in ["SDN35", "MKE70"] and valor_serie >= "P100070791":
            return "El kit correspondiente es: MKO70KIT , PVP 187EUR."
        if modelo_normalizado in ["SDN35", "MKE70"] and "P100070792" <= valor_serie <= "P104774156":
            return "El kit correspondiente es: MKO75KIT , PVP 210EUR."
        
        if modelo_normalizado in ["SDN10", "MKE23", "SDN20", "MKE38", "SDN30", "MKE53"] and valor_serie >= "P104774157":
            return "El kit correspondiente es: MKON65KIT, PVP 168 EUR."
        if modelo_normalizado in ["SDN10", "MKE23", "SDN20", "MKE38", "SDN30", "MKE53"] and "P100070792" <= valor_serie <= "P104774156":
            return "El kit correspondiente es: MKON55KIT, PVP 168 EUR"
        if modelo_normalizado in ["SDN10", "MKE23", "SDN20", "MKE38", "SDN30", "MKE53"] and  valor_serie <= "14-18-MA09505":
            return "El kit correspondiente es: MKON45KIT, PVP 156 EUR"
        if modelo_normalizado in ["SDN10", "MKE23", "SDN20", "MKE38", "SDN30", "MKE53"] and " P000000000" <= valor_serie <= " P100070791":
            return "El kit correspondiente es: MKON45KIT, PVP 156 EUR"    
        if modelo_normalizado in ["SDN10", "MKE23", "SDN20", "MKE38", "SDN30", "MKE53", "MKE70"] and valor_serie >= "P104774157":
            return "El kit correspondiente es: MKON65KIT, PVP 168EUR."
        if modelo_normalizado in ["SDN70", "MKE210", "SDN80", "MKE305", "SDN90", "MKE375"] and valor_serie <= "P100078376":
            return "El kit correspondiente es: MKO500KIT, PVP 382EUR."

       


        if modelo_normalizado in ["SDN100", "MKE495", "SDN110", "MKE623" ] and valor_serie <= "P100077609":
            return "El kit correspondiente es: MKO851KIT , PVP 468EUR." 
       
        if modelo_normalizado in ["SDN100", "MKE495", "SDN110", "MKE623" ] and valor_serie >= "P100077610":
            return "El kit correspondiente es: MKON805KIT, PVP 533EUR" 
       
        if modelo_normalizado in [ "SDN120", "MKE930", "SDN130", "MKE1200"] and valor_serie >= "P100077610":
            return "El kit correspondiente es: MKON1205KIT, PVP 613EUR"
        if modelo_normalizado in ["SDN120", "MKE930", "SDN130", "MKE1200"] and valor_serie <= "P100077609":
            return "El kit correspondiente es: MK1O210KIT, PVP 529EUR"
            
        if modelo_normalizado in ["SDN100", "MKE495", "SDN110", "MKE623", "SDN120", "MKE930", "SDN130", "MKE1200"] and valor_serie <= "P100077609":
            return "El kit correspondiente es: MKO851KIT ,PVP 468EUR."

        if modelo_normalizado in ["SDN140", "MKE1388", "SDN150", "MKE1800"] and valor_serie >= "P100079932":
            return "El kit correspondiente es: MKONHC1805 KIT , PVP 870EUR." 
        if modelo_normalizado in ["SDN140", "MKE1388", "SDN150", "MKE1800"] and valor_serie <= "P100079931":
            return "El kit correspondiente es: MKO1820KIT , PVP 628EUR."

        if modelo_normalizado in [ "SDN160", "MKE2500", "SDN170", "MKE2775"] and valor_serie >= "P101076064":
            return "El kit correspondiente es: MKONHC2775 KIT, PVP 1086,00EUR." 
        if modelo_normalizado in ["SDN160", "MKE2500", "SDN170", "MKE2775"] and valor_serie <= "P101076063":
            return "El kit correspondiente es: MKO2700KIT , PVP 874EUR."

    
# 📌Lógica específica para MKE-100 (SDN40)
    if modelo_normalizado in ["SDN40", "MKE100", "SDN50", "MKE150", "SDN60", "MKE190"]:
        if valor_serie >= "P000000000":
            return "El kit correspondiente es: MKON155KIT , PVP 262EUR."
     
    if modelo_normalizado in ["SDN40", "MKE100", "SDN50", "MKE150", "SDN60", "MKE190"] and anio_serie is not None:
        if (anio_serie > 20) or (anio_serie == 20 and semana_serie > 4) or \
           (anio_serie == 20 and semana_serie == 4 and valor_serie >= "MA06260"):
            return "El kit correspondiente es: MKON155KIT, PVP 262EUR."
        else:
            return "El kit correspondiente es: MKO150KIT , PVP 212EUR."
            
    # 📌Lógica específica para MKE-100 (SDN180)
    if modelo_normalizado in ["SDN180", "MKE3300", "SDN190", "MKE3915", "SDN200", "MKE5085" ,"SDN210", "MKE5850"]:
        if valor_serie >= "P000000000":
            return "El kit correspondiente es: MKOHC5850KIT , PVP 1511,00EUR."
     
    if modelo_normalizado in ["SDN180", "MKE3300", "SDN190", "MKE3915", "SDN200", "MKE5085" ,"SDN210", "MKE5850"] and anio_serie is not None:
        if (anio_serie > 20) or (anio_serie == 20 and semana_serie > 2) or \
           (anio_serie == 20 and semana_serie == 2 and valor_serie >= "MA05589"):
            return "El kit correspondiente es: MKOHC5850KIT , PVP 1511,00EUR."
        else:
            return "El kit correspondiente es: 2 x MKO2700KIT , PVP 874,00EUR."
    
    
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
    
# Asegúrate de tener el archivo serfriair_logo.png en la misma carpeta que app.py

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image("serfriair_logo1.png", width=200)
         
st.title("\U0001F50D Buscador de Kits por Número de Serie ")
modelo = st.text_input("Ingrese el modelo del secador:")
numero_serie = st.text_input("Ingrese el número de serie:")

st.markdown(
    """
    <div style="text-align: center; font-size: 18px; color: #4c4c4c;">
        <strong>Soluciones técnicas con precisión</strong>
    </div>
    """,
    unsafe_allow_html=True
)

import streamlit as st


if st.button("Buscar Kit"):
    if modelo and numero_serie:
        resultado = obtener_kit(modelo, numero_serie)
        st.success(resultado)
    else:
        st.warning("Por favor, ingrese un modelo y un número de serie.    Si usted es Albert puede medir con una regla")

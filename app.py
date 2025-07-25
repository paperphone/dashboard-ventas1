import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import os
os.system("cls")

st.set_page_config(page_title="Dashboard de ventas", layout="centered", page_icon="📈")
st.title("Ventas trimestre I 2024")
df=pd.read_excel("ventas_supermercado.xlsx", skiprows=1, header=1)
#st.write(df.head())

def formato(numero):
    """Convierte número a formato: 1.234.567,89"""
    return f"{numero:,.2f}".replace(",", "X").replace(".",",").replace("X", ".")

#Calcular KPIs
total_ventas = df["Total"].sum()
ingreso_bruto = df["Ingreso bruto"].sum()
promedio_calificacion = df["Calificación"].mean()

#Mostrar KPIs en columnas con formato personalizado
#st.metric("💰 Total Ventas", f"${formato(total_ventas)}")
#st.metric("📈 Ingreso Bruto", f"${formato(ingreso_bruto)}")
#st.metric("⭐ Calificación Promedio", f"{formato(promedio_calificacion)}")

#organizar los KPIs en columnas
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.metric("💰 Total Ventas", f"${formato(total_ventas,)}")
with col2:
    st.metric("📈 Ingreso Bruto", f"${formato(ingreso_bruto,)}")
with col3:
    st.metric("⭐ Calificación Promedio", f"${formato(promedio_calificacion,)}")

with st.sidebar:
    st.header("Filtros")
    #Selección de ciudades y lineas de producto
    ciudades = st.multiselect("Selecciona ciudades:", df["Ciudad"].unique(), default=df["Ciudad"].unique())
    lineas=st.multiselect("Selecciona lienas de producto",df["Línea de producto"].unique(), default=df["Línea de producto"].unique())
    
#filtrar datos
df_filtrado=df[(df["Ciudad"].isin(ciudades))&(df["Línea de producto"].isin(lineas))]
df_filtrado["Mes"]=df_filtrado["Fecha"].dt.to_period("M").astype(str)
df_filtrado["Mes"]=df_filtrado["Fecha"].dt.strftime("%m-%Y")



#Organizar los datos en pestañas

tab1, tab2, tab3 = st.tabs(["📅 Ventas por mes", "📦 Por Línea", "📁 Dotos"], width = "stretch")

with tab1:
    st.subheader("📅 Ventas por mes")
    df_filtrado["Mes"]=df_filtrado["Fecha"].dt.to_period("M").astype(str)
    df_filtrado["Mes"]=df_filtrado["Fecha"].dt.strftime("%m-%Y")
    ventas_mes=df_filtrado.groupby("Mes")["Total"].sum().sort_index()
    fig1, ax1=plt.subplots()
    ventas_mes.plot(kind="line", marker="o" , ax=ax1, color="teal", title="Tendencia de Ventas Mensuales")

    ax1.set_xlabel("Mes")
    ax1.set_ylabel("Total Ventas")
    ax1.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig1)
with tab2:
    st.subheader("📦 Ventas Por Línea de Producto")
    ventas_linea=df_filtrado.groupby("Línea de producto")["Total"].sum().sort_values()
    fig2, ax2=plt.subplots()
    ventas_linea.plot(kind="barh",   ax=ax2, color="green", title="Ventas por línea de producto")

    ax2.set_xlabel("")
    ax2.set_ylabel(" Ventas")    
    st.pyplot(fig2)
    df_filtrado.reset_index(drop=True, inplace=True)
    df_filtrado.index=range(1, len(df_filtrado)+1)
with tab3:
    st.subheader("📁 Dotos")
    st.dataframe(df_filtrado)
#exportar a excel en memoria 
output=BytesIO()
with pd.ExcelWriter(output, engine="xlsxwriter") as writer:df_filtrado.to_excel(writer, index=False, sheet_name="Ventas")
#Boton de descarga
st.download_button(label="Descargar datos en excel", data=output.getvalue(), file_name="ventas_filtradas.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
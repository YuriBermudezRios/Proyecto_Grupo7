# Importación de las Librerías

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime
import plotly.express as px
import folium
from streamlit_folium import st_folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim

# Importar archivo de BD en formato .CSV
df = pd.read_csv('BD_energiasrenovables1.csv')

# Reemplazar espacios en los nombres de las columnas para evitar problemas al acceder
df.columns = df.columns.str.replace(' ', '_')

# Título de la aplicación
st.title("Análisis de Proyectos de Energías Renovables")

# Selección de Tipo de Proyecto
tipo_proyecto = st.selectbox("Selecciona el tipo de proyecto:", df["Tipo"].unique())

# Filtrar el DataFrame según el tipo de proyecto seleccionado
df_filtrado = df[df["Tipo"] == tipo_proyecto]

# Mostrar datos filtrados
st.subheader("Datos Filtrados")
st.dataframe(df_filtrado)

# Suma total de inversión para el tipo de proyecto seleccionado
suma_inversion = df_filtrado["Inversión_estimada_[COP]"].sum()
st.write(f"La suma total de inversión para proyectos de tipo '{tipo_proyecto}' es: {suma_inversion}")

# Obtenemos las 5 primeras líneas para dar una visión inicial al DataFrame
st.subheader("Primeras líneas del DataFrame")
st.write(df.head())

# Obtenemos las 5 últimas líneas para dar una visión final al DataFrame
st.subheader("Últimas líneas del DataFrame")
st.write(df.tail())


# Estadísticas Descriptivas
st.subheader("Estadísticas Descriptivas")
st.write(df.describe())

# Slider para seleccionar rango de usuarios
usuarios_min, usuarios_max = int(df["Usuarios"].min()), int(df["Usuarios"].max())
usuario_seleccion = st.slider("Selecciona el rango de usuarios:", min_value=usuarios_min, max_value=usuarios_max, value=(usuarios_min, usuarios_max))

# Filtrar DataFrame según el rango de usuarios seleccionado
df_usuarios_filtrados = df[(df["Usuarios"] >= usuario_seleccion[0]) & (df["Usuarios"] <= usuario_seleccion[1])]

# Mostrar el gráfico de dispersión para los usuarios filtrados
st.subheader("Relación Inversión vs Empleos para Usuarios Filtrados")
fig, ax = plt.subplots()
df_usuarios_filtrados.plot(kind='scatter', x='Empleos_estimados', y='Inversión_estimada_[COP]', ax=ax)
ax.set_title("Relación entre Inversión y Empleos Estimados para Usuarios Filtrados")
ax.set_xlabel("Empleos Estimados")
ax.set_ylabel("Inversión Estimada [COP]")
st.pyplot(fig)

# Gráfico de Barras = Eje X = Tipo de Proyecto VS Eje Y = Cantidad
# Agrupar por 'Tipo' y contar la columna 'Capacidad'
df_tipo = df.groupby(["Tipo"]).count()["Capacidad"]
print(df_tipo)

# Crear el gráfico de barras
ax = df_tipo.plot(title="Proyectos de Energías Renovables", xlabel="Tipo", ylabel="Cantidad", kind="bar")

# Agregar etiquetas a cada barra
for i, value in enumerate(df_tipo):
    ax.text(i, value, str(value), ha='center', va='bottom', fontsize=10)

# Mostrar el gráfico
plt.tight_layout()
st.pyplot(fig)

#Gráfico de Torta = % por Tipo de Proyecto: Solar 91,8% VS Eólica 8,2%
st.subheader("Porcentaje por Tipo de Proyecto")
df_tipo = df.groupby(["Tipo"]).count()["Código_Departamento"]
fig, ax = plt.subplots()
ax.pie(df_tipo, labels=df_tipo.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)

# Checkbox para mostrar información adicional
if st.checkbox("Mostrar Estadísticas Descriptivas"):
    st.subheader("Estadísticas Descriptivas")
    st.write(df.describe())

# Gráfico de Barras = Eje X = Departamentos VS Eje Y = Empleos generados
# Agrupación por departamento y conteo de empleos estimados
df_tipo = df.groupby(['Departamento']).count()['Empleos_estimados']
print(df_tipo)

# Crear una nueva figura para el gráfico de barras
fig, ax = plt.subplots()

# Creación del gráfico de barras
df_tipo.plot(ax=ax, title="Empleos estimados por cada Departamento", xlabel='Departamento', ylabel='Empleos estimados', kind='bar')

# Asignación de etiquetas para cada barra
for i in range(len(df_tipo)):
    ax.text(i, df_tipo[i], str(int(df_tipo[i])), ha='center', va='bottom', color='black', fontsize=10)

# Ajuste de diseño y muestra de la figura
plt.tight_layout()
st.pyplot(fig)


# Gráficas con streamlit
# Título de la aplicación
st.title("Análisis de Proyectos de Energías Renovables")

# Mostrar datos en un DataFrame
st.subheader("Datos de Proyectos")
st.dataframe(df)

# Suma total de inversión
suma_inversion = df["Inversión_estimada_[COP]"].sum()
st.write(f"La suma total de inversión en Proyectos es: {suma_inversion}")

# Gráfico de barras de Inversión estimada por Tipo de Proyecto
st.subheader("Inversión estimada por Tipo de Proyecto")
inversion_por_tipo = df.groupby("Tipo")["Inversión_estimada_[COP]"].sum()
fig, ax = plt.subplots()
inversion_por_tipo.plot(kind='bar', ax=ax)
st.pyplot(fig)

# Gráfico de barras de Código Departamento vs Capacidad Instalada en MW
st.subheader("Código Departamento vs Capacidad Instalada en MW")
capacidad_por_departamento = df.groupby("Código_Departamento")["Capacidad"].sum()
st.bar_chart(capacidad_por_departamento)


# Título de la aplicación
st.title("Distribución de Municipios por Departamento en Colombia")

# Datos de municipios y departamentos
data = {
    "Departamento": [
        "LA GUAJIRA", "VALLE DEL CAUCA", "BOLÍVAR", "CESAR", "META", "VALLE DEL CAUCA", 
        "ARCHIPIÉLAGO DE SAN ANDRÉS", "ATLÁNTICO", "TOLIMA", "TOLIMA", "ANTIOQUIA", 
        "ANTIOQUIA", "CHOCÓ", "META", "BOLÍVAR", "VALLE DEL CAUCA", "RISARALDA", 
        "RISARALDA", "RISARALDA", "RISARALDA", "RISARALDA", "RISARALDA", "RISARALDA", 
        "CÓRDOBA", "VALLE DEL CAUCA", "META", "META", "ANTIOQUIA", "ANTIOQUIA", 
        "GUAINÍA", "CHOCÓ", "ANTIOQUIA", "BOLÍVAR", "VALLE DEL CAUCA", "SANTANDER", 
        "CALDAS", "RISARALDA", "HUILA", "ARAUCA", "CÓRDOBA", "BOYACÁ", "ANTIOQUIA", 
        "VALLE DEL CAUCA", "BOGOTÁ D.C.", "NORTE DE SANTANDER", "CASANARE", "ATLÁNTICO", 
        "VALLE DEL CAUCA", "SUCRE", "META", "ATLÁNTICO", "ATLÁNTICO", "BOGOTÁ D.C.", 
        "CAUCA", "QUINDÍO", "HUILA", "BOLÍVAR", "LA GUAJIRA", "CESAR", "META", 
        "CALDAS", "META", "META", "CASANARE", "TOLIMA", "TOLIMA", "TOLIMA", "CÓRDOBA", 
        "CÓRDOBA", "TOLIMA", "ARAUCA", "SUCRE", "CÓRDOBA", "VALLE DEL CAUCA", 
        "NORTE DE SANTANDER", "NORTE DE SANTANDER", "NORTE DE SANTANDER", "MAGDALENA", 
        "ATLÁNTICO", "ATLÁNTICO", "META", "CÓRDOBA", "LA GUAJIRA", "BOLÍVAR", 
        "MAGDALENA", "HUILA", "BOLÍVAR", "META", "LA GUAJIRA", "LA GUAJIRA", "TOLIMA", 
        "VALLE DEL CAUCA", "CÓRDOBA", "ATLÁNTICO", "ATLÁNTICO", "BOLÍVAR", 
        "ATLÁNTICO", "SUCRE", "TOLIMA", "TOLIMA", "TOLIMA", "VALLE DEL CAUCA", 
        "TOLIMA", "TOLIMA", "VALLE DEL CAUCA", "VALLE DEL CAUCA", "CAUCA", 
        "META", "SANTANDER", "CUNDINAMARCA", "ATLÁNTICO", "ANTIOQUIA", "CUNDINAMARCA", 
        "CUNDINAMARCA", "CUNDINAMARCA", "CUNDINAMARCA", "BOGOTÁ D.C.", "BOGOTÁ D.C.", 
        "CUNDINAMARCA", "VALLE DEL CAUCA", "VALLE DEL CAUCA", "CAUCA", "ATLÁNTICO", 
        "SANTANDER", "LA GUAJIRA", "CESAR", "LA GUAJIRA", "LA GUAJIRA", "CESAR", 
        "CÓRDOBA", "NORTE DE SANTANDER", "CESAR", "SANTANDER", "ATLÁNTICO", 
        "CÓRDOBA", "ATLÁNTICO", "BOLÍVAR", "ATLÁNTICO", "ANTIOQUIA", "CALDAS", 
        "TOLIMA", "LA GUAJIRA", "CUNDINAMARCA", "LA GUAJIRA", "LA GUAJIRA", 
        "LA GUAJIRA", "TOLIMA", "NORTE DE SANTANDER", "BOGOTÁ D.C.", "ATLÁNTICO", 
        "MAGDALENA", "VALLE DEL CAUCA", "CÓRDOBA", "VALLE DEL CAUCA", "VALLE DEL CAUCA", 
        "SANTANDER", "META", "ARAUCA"
    ],
    "Municipio": [
        "URIBIA", "YUMBO", "SANTA ROSA", "EL PASO", "CASTILLA LA NUEVA", "CALI", 
        "SAN ANDRÉS", "SOLEDAD", "ESPINAL", "IBAGUÉ", "MEDELLÍN", "MEDELLÍN", 
        "UNGUÍA", "PUERTO GAITÁN", "CARTAGENA DE INDIAS", "YUMBO", "PEREIRA", 
        "PEREIRA", "PEREIRA", "PEREIRA", "PEREIRA", "PEREIRA", "PEREIRA", 
        "PLANETA RICA", "CANDELARIA", "PUERTO GAITÁN", "PUERTO GAITÁN", "RIONEGRO", 
        "RIONEGRO", "INÍRIDA", "UNGUÍA", "MEDELLÍN", "CARTAGENA DE INDIAS", 
        "YUMBO", "BARRANCABERMEJA", "MANIZALES", "PEREIRA", "HUILA", "ARAUCA", 
        "MONTERÍA", "TUNJA", "MEDELLÍN", "CALI", "BOGOTÁ D.C.", "SAN JOSÉ DE CÚCUTA", 
        "YOPAL", "BARRANQUILLA", "ZARZAL", "SAN BENITO ABAD", "CASTILLA LA NUEVA", 
        "GALAPA", "BARRANQUILLA", "BOGOTÁ D.C.", "POPAYÁN", "ARMENIA", "NEIVA", 
        "CARTAGENA DE INDIAS", "URIBIA", "EL PASO", "VILLAVICENCIO", "LA DORADA", 
        "PUERTO GAITÁN", "PUERTO GAITÁN", "VILLANUEVA", "ARMERO", "ARMERO", 
        "SAN SEBASTIÁN DE MARIQUITA", "CHINÚ", "CHINÚ", "ARMERO", "ARAUCA", 
        "SAN LUIS DE SINCÉ", "PLANETA RICA", "CARTAGO", "SAN JOSÉ DE CÚCUTA", 
        "SAN JOSÉ DE CÚCUTA", "SAN JOSÉ DE CÚCUTA", "ZONA BANANERA", "BARANOA", 
        "POLONUEVO", "VILLAVICENCIO", "CHINÚ", "URIBIA", "ARJONA", "CIÉNAGA", 
        "YAGUARÁ", "CANTAGALLO", "PUERTO GAITÁN", "MAICAO", "MAICAO", "MELGAR", 
        "ANDALUCÍA", "CHINÚ", "MALAMBO", "GALAPA", "ARJONA", "MANATÍ", 
        "SAN JOSÉ DE TOLUVIEJO", "FLANDES", "FLANDES", "FLANDES", "VALLE DEL CAUCA", 
        "FLANDES", "FLANDES", "VALLE DEL CAUCA", "VALLE DEL CAUCA", "PUERTO TEJADA", 
        "PUERTO GAITÁN", "LOS SANTOS", "GUADUAS", "SABANALARGA", "GIRARDOTA", 
        "SUESCA", "SOPÓ", "MADRID", "SOACHA", "BOGOTÁ D.C.", "BOGOTÁ D.C.", 
        "SESQUILÉ", "GINEBRA", "CALI", "POPAYÁN", "MALAMBO", "PIEDECUESTA", 
        "MAICAO", "AGUACHICA", "URIBIA", "URIBIA", "LA GLORIA", "MONTERÍA", 
        "LA ESPERANZA", "CHIRIGUANÁ", "CIMITARRA", "SABANALARGA", "MONTELÍBANO", 
        "MALAMBO", "SANTA CATALINA", "SABANALARGA", "PUERTO NARE", "LA DORADA", 
        "IBAGUÉ", "URIBIA", "GUADUAS", "MAICAO", "URIBIA", "URIBIA", "ALVARADO", 
        "OCAÑA", "BOGOTÁ D.C.", "SABANALARGA", "FUNDACIÓN", "TULUÁ", "MONTELÍBANO", 
        "BUGA", "BUGA", "BARRANCABERMEJA", "VILLAVICENCIO", "ARAUCA"
    ]
}

# Crear un dataframe a partir de los datos
df = pd.DataFrame(data)

# Crear un gráfico de barras para mostrar la cantidad de municipios por departamento
municipios_por_departamento = df.groupby("Departamento").size().reset_index(name='Cantidad de Municipios')

# Crear el gráfico usando Plotly
fig = px.bar(municipios_por_departamento, x='Departamento', y='Cantidad de Municipios',
             title="Cantidad de Municipios por Departamento",
             labels={'Cantidad de Municipios': 'Número de Municipios', 'Departamento': 'Departamento'},
             color='Cantidad de Municipios', height=600)

# Mostrar el gráfico en la aplicación de Streamlit
st.plotly_chart(fig)


# Datos de proyectos (nombre, departamento, municipio, latitud, longitud)
proyectos = [
    ("JEPIRACHI", "LA GUAJIRA", "URIBIA", 12.2819, -71.2752),
    ("AUTOG CELSIA SOLAR YUMBO", "VALLE DEL CAUCA", "YUMBO", 3.6081, -76.5704),
    ("CELSIA SOLAR BOLIVAR", "BOLÍVAR", "SANTA ROSA", 10.3010, -75.4292),
    ("EL PASO SOLAR (ENEL GREEN POWER)", "CESAR", "EL PASO", 10.3054, -74.2470),
    ("SOLAR CASTILLA ECP", "META", "CASTILLA LA NUEVA", 4.1622, -73.7350),
    ("AGPE TECNOEMPAQUES DE OCCIDENTE", "VALLE DEL CAUCA", "CALI", 3.4513, -76.5309),
    ("RADAR FAC SAN ANDRÉS", "ARCHIPIÉLAGO DE SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA", "SAN ANDRÉS", 12.5830, -81.7114),
    ("AGPE SFV MCDONALDS SOLEDAD", "ATLÁNTICO", "SOLEDAD", 10.9081, -74.7665),
    ("CELSIA SOLAR ESPINAL", "TOLIMA", "ESPINAL", 4.0070, -74.4650),
    ("FEDERACIÓN NACIONAL DE CAFETEROS", "TOLIMA", "IBAGUÉ", 4.4380, -75.2023),
    ("PANELES SOLARES ISA", "ANTIOQUIA", "MEDELLÍN", 6.2442, -75.5812),
    ("SENA PEDREGAL", "ANTIOQUIA", "MEDELLÍN", 6.2504, -75.5771),
    ("UNGUÍA 181 HOGARES + 5 ESCUELAS", "CHOCÓ", "UNGUÍA", 6.6525, -77.1245),
    ("BOSQUES SOLARES DE LOS LLANOS 1", "META", "PUERTO GAITÁN", 4.2563, -73.4830),
    ("BAYUNCA 1", "BOLÍVAR", "CARTAGENA DE INDIAS", 10.3910, -75.5142),
    ("PLASTICEL (AUTOCONSUMO)", "VALLE DEL CAUCA", "YUMBO", 3.6093, -76.5230),
    ("UTP", "RISARALDA", "PEREIRA", 4.8138, -75.6909),
    ("AEROPUERTO", "RISARALDA", "PEREIRA", 4.8135, -75.6894),
    ("UKUMARI", "RISARALDA", "PEREIRA", 4.8028, -75.6195),
    ("VIVA CERRITOS", "RISARALDA", "PEREIRA", 4.8486, -75.6948),
    ("CENTRO COMERCIAL VICTORIA", "RISARALDA", "PEREIRA", 4.8228, -75.6723),
    ("CENTRO COMERCIAL ALCIDES ARÉVALO", "RISARALDA", "PEREIRA", 4.8390, -75.6788),
    ("LICEO PINO VERDE", "RISARALDA", "PEREIRA", 4.8166, -75.6753),
    ("PÉTALO DE CÓRDOBA", "CÓRDOBA", "PLANETA RICA", 8.7921, -75.6192),
    ("CARMELO", "VALLE DEL CAUCA", "CANDELARIA", 3.6396, -76.5756),
    ("BOSQUES SOLARES DE LOS LLANOS 2", "META", "PUERTO GAITÁN", 4.2559, -73.4870),
    ("BOSQUES SOLARES DE LOS LLANOS 3", "META", "PUERTO GAITÁN", 4.2563, -73.4840),
    ("GRUPO SEB", "ANTIOQUIA", "RIONEGRO", 6.1434, -75.4028),
    ("AUTOGENERACIÓN PINTUCO", "ANTIOQUIA", "RIONEGRO", 6.1283, -75.4350),
    ("SOL DE INIRÍDA", "GUAINÍA", "INÍRIDA", 3.8663, -67.0491),
    ("EL SOL BRILLA PARA UNGUÍA", "CHOCÓ", "UNGUÍA", 6.6452, -77.1221),
    ("COMPLEJO CENTRAL", "HUILA", "0.06", 2.0947, -75.3863),
    ("PUERTO DE CARTAGENA", "BOLÍVAR", "CARTAGENA DE INDIAS", 10.3910, -75.5142),
    ("JOHNSON & JOHNSON", "VALLE DEL CAUCA", "YUMBO", 3.6081, -76.5704),
    ("ESSA GD Y AG (385 Proyectos)", "SANTANDER", "BARRANCABERMEJA", 8.1382, -74.2504),
    ("CHEC GD Y AG (184 Proyectos)", "CALDAS", "MANIZALES", 5.0692, -75.5176),
    ("GRANJA SOLAR BELMONTE", "RISARALDA", "PEREIRA", 4.8046, -75.6289),
    ("CENTRO DE LA INDUSTRIA", "HUILA", "0.06", 2.0947, -75.3863),
    ("CENTRO DE GESTIÓN Y DESARROLLO AGROINDUSTRIAL DE ARAUCA", "ARAUCA", "ARAUCA", 7.0823, -70.7490),
    ("AFINIA GD Y AG (167 Proyectos)", "CÓRDOBA", "MONTERÍA", 8.7494, -75.8836),
    ("EBSA GD Y AG (53 Proyectos)", "BOYACÁ", "TUNJA", 5.5424, -73.3672),
    ("EPM GD Y AG (1469 Proyectos)", "ANTIOQUIA", "MEDELLÍN", 6.2442, -75.5812),
    ("CELSIA GD Y AG (286 Proyectos)", "VALLE DEL CAUCA", "CALI", 3.4513, -76.5309),
    ("ENEL GD Y AG (331 PROYECTOS)", "BOGOTÁ D.C.", "BOGOTÁ D.C.", 4.6110, -74.0824),
    ("CENS GD Y AG (165 Proyectos)", "NORTE DE SANTANDER", "SAN JOSÉ DE CÚCUTA", 7.8935, -72.5078),
    ("ENERCA GD Y AG", "CASANARE", "YOPAL", 5.9917, -72.4007),
    ("AIRE GD Y AG", "ATLÁNTICO", "BARRANQUILLA", 10.9634, -74.7950),
    ("LA PAILA", "VALLE DEL CAUCA", "ZARZAL", 4.2642, -75.8124),
    ("LA SIERPE SOLAR", "SUCRE", "SAN BENITO ABAD", 9.0924, -75.0798),
    ("SAN FERNANDO", "META", "CASTILLA LA NUEVA", 4.1622, -73.7350),
    ("COMPLEJO SOLAR RELIANZ CAT", "ATLÁNTICO", "GALAPA", 10.9490, -74.7795),
    ("ZONA FRANCA LA CAYENA", "ATLÁNTICO", "BARRANQUILLA", 10.9634, -74.7950),
    ("COMPLEJO SUR BOGOTÁ", "BOGOTÁ D.C.", "BOGOTÁ D.C.", 4.6110, -74.0824),
    ("CEO GD Y AG (34 Proyectos)", "CAUCA", "POPAYÁN", 2.4364, -76.6032),
    ("EDEQ GD Y AG (64 Proyectos)", "QUINDÍO", "ARMENIA", 4.5304, -75.6781),
    ("ELECTROHUILA GD Y AG (125 Proyectos)", "HUILA", "NEIVA", 2.9742, -75.2203),
    ("EBSA GD Y AG (53 Proyectos)", "BOYACÁ", "TUNJA", 5.5424, -73.3672),
    ("GRANJA SOLAR ZUMBA", "NARIÑO", "PASTO", 1.0730, -77.2854),
    ("GRANJA SOLAR EL PALMAR", "VALLE DEL CAUCA", "YUMBO", 3.5563, -76.5971),
]

# Crear un mapa centrado en Colombia
m = folium.Map(location=[4.5709, -74.2973], zoom_start=5)

# Añadir marcadores al mapa
for proyecto in proyectos:
    nombre, departamento, municipio, latitud, longitud = proyecto
    folium.Marker(
        location=[latitud, longitud],
        popup=f"<strong>{nombre}</strong><br>{departamento}, {municipio}",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Mostrar el mapa en Streamlit
st.title("Proyectos Renovables en Colombia")
st_folium(m, width=700, height=500)

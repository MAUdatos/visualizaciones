import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import re

# Dashboard structure
st.set_page_config(page_title="MAU ", page_icon="🍃", layout="wide")

# Hide index when showing a table. CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

# data
df_bbdd =         pd.read_csv('mau_bbdd01012023.csv',sep=';').dropna(how = 'all')             # Base de datos consolidada (1er y 2do encuentro)
df_foda =         pd.read_csv('FODA2doencuentro.csv',sep=';').dropna(how = 'all')             # FODA realizado el segundo encuentro
df_expectativas = pd.read_csv('expectativas2doencuentro2022.csv',sep=';').dropna(how = 'all') # Expectativas sobre el MAU en formulario del 2do encuentro

# General Information for the main page
# st.caption('Sistematización y Mapeo. Prototipo Web App  1.0')
st.caption('<div style="text-align: right">Sistematización y Mapeo. Prototipo Web App  1.0</div>', unsafe_allow_html=True)          
col1, col2, col3, col4 = st.columns((2,0.5,3,4))
col1.image("logo_mau.png", width=225)
col3.text("  ")
col3.text("  ")
col3.subheader("Red de cooperación mutua que fomenta, reivindica y defiende el oficio de la agroecología en pro de la soberanía alimentaria")
st.markdown("  ")

### Objetivos
# Tabs to organize information
st.header('🍃 Información General MAU') 
st.subheader('Objetivos')
tab1, tab2 = st.tabs(["Objetivo General", "Objetivos Específicos"])
with tab1:
    st.markdown("""- Desarrollar una red de cooperación mutua que fomente, reivindique y defienda el oficio de la agroecología en pro de la soberanía alimentaria""") #(MAU 3/12/2022)
with tab2:
    st.markdown("- Generar redes de apoyo para potenciar el intercambio de saberes, experiencias y recursos entre organizaciones y territorios urbanos, \
    periurbanos y rurales\n- Recuperar y regenerar los espacios para el aumento de la biodiversidad y el cultivo de alimentos \
    saludables\n- Generar estrategias metodológicas para compartir saberes y experiencias en torno a la agroecología urbana, periurbana y rural")
st.markdown("""----""")

### Mau en números

# Key Variables
st.subheader('MAU en números')

total_members     = df_bbdd['Organización_Huerta_Colectivo'].nunique()
total_individuals = df_bbdd['Nombre_representante'].nunique()
total_localidad   = df_bbdd['Localidad'].nunique()
total_inst        = df_bbdd['Link redes sociales'].nunique()

col1, col2, col3, col4, col5 = st.columns((1.5,1,1,1,2))   #https://blog.streamlit.io/introducing-new-layout-options-for-streamlit/

col1.metric("Nº Organizaciones, Huertas y/o Comunidades",total_members)
col2.metric("Nº Personas representantes",total_individuals)
col3.metric("Nº Territorios identificados",total_localidad)
col4.metric("Nº Redes sociales",total_inst)

#https://stackoverflow.com/questions/33997361 
#https://stackoverflow.com/questions/50193159/converting-pandas-data-frame-with-degree-minute-second-dms-coordinates-to-deci

def dms2dd(s):
    # example: s = """0°51'56.29"S"""
    degrees, minutes, seconds, direction = re.split('[°\'"]+', s)
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    if direction in ('S','W'):
        dd*= -1
    return dd

#mapping coordinates to a Chilean map - work in progress

df_geo = df_bbdd[['Latitude','Longitude']]
st.table(df_geo)
"""
df_geo = df_geo.replace(['No info'], '')
df_geo = df_geo.replace(['No Info'], '')
df_geo['Latitude']  = df_geo['Latitude'].apply(dms2dd)
df_geo['Longitude'] = df_geo['Longitude'].apply(dms2dd)
st.write(df_geo)
df = pd.DataFrame(df_geo,columns=['Latitude','Longitude'])
st.map(df)
"""

st.caption("Fuente: Formularios de participación en 1er y 2do Encuentro MAU 2022")
st.markdown("""---""")

### Expectativas
st.header('🌻 Análisis Encuentros MAU (11/2022, 12/2022)') 
st.subheader('Análisis de expectativas')
#st.markdown("Análisis de respuestas a preguntas:") 

col0, col1, col2, col3 = st.columns((0.1,1,6,1))

col1.markdown("1er Encuentro:")
col1.markdown("2do Encuentro:")
col2.markdown("*¿Cuáles serían los objetivos de esta articulación* [Movimiento]?")
col2.markdown("*¿Qué esperas de una articulación entre huertas urbanas?*")

fuente_expectativa = st.multiselect("Selecciona fuente de información", 
                                    options=df_expectativas["Fuente"].unique(),)  #Multiselector for source of information regarding expectations (1r and 2d Meeting)
                                    #default=df_expectativas["Fuente"].unique())
all_options = st.checkbox("Ambos encuentros")

if all_options:
    fuente_expectativa = df_expectativas["Fuente"].unique().tolist()
            
df_expectativas_fuente = df_expectativas.query('Fuente == @fuente_expectativa')  #Filter by source of information

expectativas_s = st.multiselect("Selecciona tematica", options=df_expectativas_fuente["Dimensión"].unique(),)

df_expectativas_s = df_expectativas_fuente.query('Dimensión == @expectativas_s')

fig1 = px.sunburst(data_frame = df_expectativas_s, path = ['Dimensión','Indicador','Expectativa'],values = None)  

if  len(expectativas_s) == 0:
    st.markdown('Resultados:')
    st.caption(' 🥕 No hay información seleccionada')
else:   
    st.caption('Explora las respuestas interactuando con el gráfico solar. Puedes partir por seleccionar tu dimensión de interés.')    
    st.plotly_chart(fig1)                 #wrapping can be improved on -> https://github.com/plotly/plotly.py/issues/2527 plus avoid hover
    with st.expander("Ver detalle"):
            st.table(df_expectativas_s)
            st.caption('Fuente: Formulario de participación en 2do Encuentro MAU (3/12/2022)')

### Análisis FODA (12/2022)
st.subheader('Análisis FODA (12/2022)')
st.markdown('El análisis FODA es una herramienta de investigación participativa que permitió identificar características comunes entre los diferentes \
espacios que forman el MAU. Para ello se consideraron 4 marcos de análisis: Debilidades, Amenazas, Fortalezas y Oportunidades.')

foda_s = st.multiselect("Selecciona marco de análisis", options=df_foda["Tipo"].unique(),)

df_foda_s = df_foda.query('Tipo == @foda_s')

df_foda_summary = df_foda_s[['Tipo','Transcripción','Clasificación Específica','Clasificación Agrupada']]
df_foda_summary.rename(columns = {'Tipo':'Dimensión',}, inplace = True)

fig2 = px.sunburst(data_frame = df_foda_s,path = ['Tipo', 'Clasificación Agrupada', 'Clasificación Específica', 'Transcripción'],values = None)  

if  len(foda_s) == 0:
    st.markdown('Resultados:')
    st.caption('🥕 No hay información seleccionada')
else:
    st.caption('Explora las respuestas interactuando con el gráfico solar. Puedes partir por seleccionar tu dimensión de interés.')
    st.plotly_chart(fig2)
    with st.expander("Ver detalle"):
            st.table(df_foda_summary)
            st.caption('Fuente: Metodología Participativa, 2do Encuentro MAU (3/12/2022)')
st.markdown("""---""")

st.subheader("🌽 Análisis de sistematización y mapeo (12/2022)")

Territorio = st.multiselect("Territorio", options=df_bbdd["Localidad"].unique(),) 
all_options = st.checkbox("Todos los territorios")

if all_options:
    Territorio = df_bbdd["Localidad"].unique().tolist()

df_bbdd_by_ter = df_bbdd.query('Localidad == @Territorio')

miembros = st.multiselect("Organización, Huerta o Colectivo",options=df_bbdd_by_ter["Organización_Huerta_Colectivo"].unique(),default=df_bbdd_by_ter["Organización_Huerta_Colectivo"].unique())
all_options = st.checkbox("Todas")

if all_options:
    miembros = df_bbdd_by_ter["Organización_Huerta_Colectivo"].unique().tolist()

df_bbdd_filtered = df_bbdd_by_ter.query('Organización_Huerta_Colectivo == @miembros')

# Key Variables filtered
total_members_f     = df_bbdd_filtered['Organización_Huerta_Colectivo'].nunique()
total_individuals_f = df_bbdd_filtered['Nombre_representante'].nunique()
total_localidad_f   = df_bbdd_filtered['Localidad'].nunique()
total_inst_f        = df_bbdd_filtered['Link redes sociales'].nunique()

df_bbdd_summary = df_bbdd_filtered[['Organización_Huerta_Colectivo','Nombre_representante', \
                                    'Localidad','Relación con la agroecología','Link redes sociales']]

df_bbdd_summary.rename(columns = {'Organización_Huerta_Colectivo'                :'Nombre Organización, Huerta y/o Colectivo',
                                  'Nombre_representante'                         :'Nombre persona representante',
                                  'Link redes sociales'                          :'Instagram',},  inplace = True)
# treemap
# df_bbdd_summary_tree = df_bbdd_summary.by('Nombre Organización, Huerta y/o Colectivo')['Localidad'].nuinque()
# st.table(df_bbdd_summary_tree.groupby(["Nombre Organización, Huerta y/o Colectivo", "Localidad"])["Nombre persona representante"].count()
# fig3 = px.treemap()

if  len(Territorio) == 0:
    st.markdown('Resultados')
    st.caption('🥕 No hay información seleccionada')
else:
    col1, col2, col3, col4, col5 = st.columns((1.5,1,1,1,2))

    col1.metric("Nº Organizaciones, Huertas y/o Comunidades",total_members_f)
    col2.metric("Nº Personas representantes",total_individuals_f)
    col3.metric("Nº Territorios identificados",total_localidad_f)
    col4.metric("Nº Redes sociales",total_inst_f)            
            
    st.table(df_bbdd_summary)
    st.caption('Fuente: Formularios de participación en 1er y 2do Encuentro MAU 2022')

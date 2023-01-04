import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

#Dashboard structure
st.set_page_config(page_title="MAU ", page_icon="🍃", layout="centered")

#Hide index when showing a table
# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

#data
df_bbdd =         pd.read_csv('mau_bbdd01012023.csv',sep=';') #Base de datos consolidada (1er y 2do encuentro)
df_foda =         pd.read_csv('FODA2doencuentro.csv',sep=';') #FODA realizado el segundo encuentro
df_expectativas = pd.read_csv('expectativas2doencuentro2022.csv',sep=';') #Expectativas sobre el MAU en formulario del 2do encuentro

df_bbdd  = df_bbdd.dropna(how = 'all')
df_foda  = df_foda.dropna(how = 'all')
df_expectativas = df_expectativas.dropna(how = 'all')

#General Information for the main page

col_x, col_y = st.columns(2)
col_x.image("logo_mau.png", width= 200)
col_y.subheader("Red de cooperación mutua que fomenta, reivindica y defiende el oficio de la agroecología en pro de la soberanía alimentaria")
st.caption('Sistematización y Mapeo. Prototipo Web App  1.0')

tab1, tab2 = st.tabs(["Objetivo General", "Objetivos Específicos"])

with tab1:
   st.markdown("""- Desarrollar una red de cooperación mutua que fomente, reivindique y defienda el oficio de la agroecología en pro de la soberanía alimentaria (MAU 3/12/2022)       """)
   st.markdown(""" """)
   st.markdown(""" """)
   st.markdown(""" """)    #varias lineas vacias para evitar un salto de pagina al cambiar entre Objetivo General y Objetivos Especificos
   st.markdown(""" """)
   st.markdown(""" """)
with tab2:
   st.markdown("- Generar redes de apoyo para potenciar el intercambio de saberes, experiencias y recursos entre organizaciones y territorios urbanos, \
                periurbanos y rurales")
   st.markdown("- Recuperar y regenerar los espacios para el aumento de la biodiversidad y el cultivo de alimentos saludables")
   st.markdown("- Generar estrategias metodológicas para compartir saberes y experiencias en torno a la agroecología urbana, periurbana y rural")

st.markdown("""---""")

#Tabs to organice information
st.subheader('🍃 Información General MAU') #

# Key Variables
total_members     = df_bbdd['Organización_Huerta_Colectivo'].nunique()
total_individuals = df_bbdd['Nombre_representante'].nunique()
total_localidad   = df_bbdd['Localidad'].nunique()

left_column, middle_column, right_column, empty_column = st.columns(4)
with left_column:
    st.metric("Nº Organizaciones, Huertas y/o Comunidades",total_members)
with middle_column:
    st.metric("Nº Personas representantes",total_individuals)
with right_column:
    st.metric("Nº Territorios identificados",total_localidad)

st.caption('Fuente: Formularios de participación en 1er y 2do Encuentro MAU 2022')

st.markdown("""---""")

###Expectativas

st.header('🌻 Análisis 2do Encuentro MAU (3/12/2022)') #
st.subheader('Expectativas')

st.markdown('Análisis de respuestas a preguntas: *"¿Cuáles serían los objetivos de esta articulación [Movimiento]?"* (1er Encuentro) y *"¿Qué esperas de una articulación entre huertas urbanas? Tus ideas nos pueden ayudar delinear el programa de futuros encuentros (2do encuentro).*"')

fuente_expectativa = st.multiselect("Selecciona fuente de información", 
                                    options=df_expectativas["Fuente"].unique(),)  #Multiselector for source of information regarding expectations (1r and 2d Meeting)
                                    #default=df_expectativas["Fuente"].unique())

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

### Análisis FODA

st.subheader('Análisis FODA')
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

st.subheader("🌽 Análisis de sistematización y mapeo")

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

df_bbdd_summary = df_bbdd_filtered[['Organización_Huerta_Colectivo','Nombre_representante','Mail Colectivo / Organización o mail personal', \
                                    'Localidad','Relación con la agroecología','Link redes sociales']]

df_bbdd_summary.rename(columns = {'Organización_Huerta_Colectivo'                :'Nombre Organización, Huerta y/o Colectivo',
                                  'Nombre_representante'                         :'Nombre persona representante',
                                  'Mail Colectivo / Organización o mail personal':'Email',
                                  'Link redes sociales'                          :'Instagram',},  inplace = True)
#treemap
#df_bbdd_summary_tree = df_bbdd_summary.by('Nombre Organización, Huerta y/o Colectivo')['Localidad'].nuinque()
#st.table(df_bbdd_summary_tree.groupby(["Nombre Organización, Huerta y/o Colectivo", "Localidad"])["Nombre persona representante"].count()
                                              
                                                          
#fig3 = px.treemap()


if  len(Territorio) == 0:
    st.markdown('Resultados')
    st.caption('🥕 No hay información seleccionada')
else:
    left_column, middle_column, right_column, empty_column = st.columns(4)
    with left_column:
        st.metric("Nº Organizaciones, Huertas y/o Comunidades",total_members_f)
    with middle_column:
        st.metric("Nº Personas representantes",total_individuals_f)
    with right_column:
        st.metric("Nº Territorios identificados",total_localidad_f)
    

    st.table(df_bbdd_summary)
    st.caption('Fuente: Formularios de participación en 1er y 2do Encuentro MAU 2022')

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import re
import word_analysis as wa
import base64

#__________________________________________________________________________________________________________________________________________________________________
# Dashboard structure
#__________________________________________________________________________________________________________________________________________________________________
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

df_bbdd = df_bbdd.sort_values(by=['Organización_Huerta_Colectivo', 'Nombre_representante'])
df_bbdd.rename(columns = {'Latitud': 'lat', 'Longitud':'lon',},  inplace = True)  #obligatory names for the map

#__________________________________________________________________________________________________________________________________________________________________
# General Information for the main page
#__________________________________________________________________________________________________________________________________________________________________
#st.caption('Prototipo Web App 1.0 MAU 2023. Grupo de trabajo: "Sistematización y Mapeo".')
#st.caption('<div style="text-align: left">Sistematización y Mapeo. Prototipo Web App  1.0</div>', unsafe_allow_html=True)          

#col1, col2, col3, col4 = st.columns((2,0.5,3,4))
#col1.image("logo_mau.png", width=200)
#col3.text("  ")
#col3.text("  ")
#col3.subheader("Red de cooperación mutua que fomenta, reivindica y defiende el oficio de la agroecología en pro de la soberanía alimentaria")
#st.markdown("  ")

st.image("headermau2023.png")

#__________________________________________________________________________________________________________________________________________________________________
st.header('🌽 Mensaje de bienvenida ✨') 
#__________________________________________________________________________________________________________________________________________________________________
#______

video_file = open('video_intro_compress.mp4', 'rb')
video_bytes = video_file.read()

st.markdown('Te invitamos a ver el video explicativo y a descargar el informe con la presentación detallada del trabajo realizado.')
col1, col2, col3, col4 = st.columns((1,0.2,1,3))
col1.video(video_bytes)
col3.markdown("[![Foo](https://raw.githubusercontent.com/MAUdatos/visualizaciones/d06b2da83b6a80f2cf26a682d3dd15c7b4b4bf54/descargaaqui_pequen%CC%83o.png)](https://github.com/MAUdatos/visualizaciones/raw/e260dd4ac3c5513efcd8c02e52d12cccc4007872/Disen%CC%83o_prototipo_Web_App_MAU_2023.pdf)")

#with open("Diseño_prototipo_Web_App_MAU_2023.pdf", "rb") as pdf_file:
#    PDFbyte = pdf_file.read()

#st.download_button(label="Descarga la presentación de detallada aquí", 
#      data=PDFbyte,
#      file_name="Avances Sistematización y Mapeo MAU 2023.pdf",
#      mime='application/octet-stream')

st.markdown('<div style="text-align: justify;"></div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: justify;">El Prototipo Web App 1.0 - MAU 2023 es el primer resultado del grupo de trabajo “Sistematización y Mapeo”. Con él se busca avanzar hacia un modelo confiable de sistematización y mapeo de las organizaciones, huertas y/o comunidades que son parte del MAU, con el fin de unir y potenciar una red de cooperación mutua que fomente, reivindique y defienda el oficio de la agroecología en pro de la soberanía alimentaria.</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: justify;"></div>', unsafe_allow_html=True) ##Espacio Texto
st.markdown('<div style="text-align: justify;">Le invitamos a explorar este prototipo y a interactuar con las opciones de búsqueda, filtros, análisis, mapas y visualizaciones. Al final le agradecemos que pueda responder un breve formulario de retroalimentación que será de mucha ayuda para el futuro de esta iniciativa.</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: justify;"></div>', unsafe_allow_html=True) ##Espacio Texto
#st.markdown("- Explorar la experiencia de usuario con el Prototipo Web App 1.0 - MAU 2023\n- Caracterizar las diferentes visiones sobre el potencial de uso para una herramienta como el Prototipo Web App 1.0 - MAU 2023\n- Identificar potenciales contenidos a considerar en futuras etapas de sistematización y mapeo.\n- Identificar contenidos que deben considerarse dentro de la esfera pública del MAU y aquellos que sólo deban estar disponibles para la gestión interna del MAU")
st.markdown('<div style="text-align: justify;"></div>', unsafe_allow_html=True) ##Espacio Texto

with st.expander("Conocer más"):
    st.markdown("**¿Qué es el Prototipo Web App 1.0 - MAU 2023?**")     
    st.markdown("Es un prototipo de aplicación web que permite analizar, mapear y visualizar información sistematizada del MAU.")
    
    st.markdown("**¿Qué información es utilizada?**")
    st.markdown("Toda la información sistematizada de los dos primeros encuentros del MAU realizados en noviembre y diciembre 2022.")
   
    st.markdown("**¿Cómo trabajamos la información?**")
    st.markdown("La información aquí presentada no se divulga públicamente y solo es utilizada para el diseño de este prototipo dentro de red interna del MAU. La información se presenta a nivel de nombre de organización y no a nivel de personas individuales. Todo esto con el fin de asegurar un uso respetuoso de los datos. ")

    st.markdown("**¿Cómo lo hicimos?**")
    st.markdown("Co-diseño entre personas del grupo de trabajo “Sistematización y mapeo”. Para construcción se utilizó lenguaje de programación Python y otras herramientas de código abierto. Todo desde un repositorio en Github asociado al MAU.")

    st.markdown("**¿Para dónde vamos?**")
    st.markdown("En sintonía con los objetivos del MAU, con este prototipo se busca desarrollar un modelo confiable de sistematización y mapeo de las organizaciones, huertas y/o comunidades que son parte del MAU, con el fin de favorecer una red de cooperación mutua que fomente, reivindique y defienda el oficio de la agroecología en pro de la soberanía alimentaria.\n- Favorecer la sistematización y mapeo de redes de apoyo que potencien el intercambio de saberes, experiencias y recursos entre organizaciones y territorios urbanos, periurbanos y rurales.\n- Sistematizar y visibilizar avances en el objetivo de recuperar y regenerar los espacios para el aumento de la biodiversidad y el cultivo de alimentos saludables\n- Favorecer la visualización de avances y resultados de estrategias metodológicas empleadas para compartir saberes y experiencias en torno a la agroecología urbana, periurbana y rural")

#__________________________________________________________________________________________________________________________________________________________________
st.header('🍃 Información General ✨') 
#__________________________________________________________________________________________________________________________________________________________________
#______________________________
st.subheader('Objetivos del MAU')
#______________________________
tab1, tab2 = st.tabs(["Objetivo General", "Objetivos Específicos"])
with tab1:
    st.markdown("""- Desarrollar una red de cooperación mutua que fomente, reivindique y defienda el oficio de la agroecología en pro de la soberanía alimentaria""") #(MAU 3/12/2022)
with tab2:
    st.markdown("- Generar redes de apoyo para potenciar el intercambio de saberes, experiencias y recursos entre organizaciones y territorios urbanos, \
    periurbanos y rurales\n- Recuperar y regenerar los espacios para el aumento de la biodiversidad y el cultivo de alimentos \
    saludables\n- Generar estrategias metodológicas para compartir saberes y experiencias en torno a la agroecología urbana, periurbana y rural")
st.markdown("""----""")

#______________________________
st.subheader('Datos Globales')
#______________________________
total_members     = df_bbdd['Organización_Huerta_Colectivo'].nunique()
total_individuals = df_bbdd['Nombre_representante'].nunique()
total_localidad   = df_bbdd['Localidad'].nunique()
total_inst        = df_bbdd['Link redes sociales'].nunique()
       
st.caption('<div style="text-align: left">Fuente: Formularios de participación en 1er y 2do Encuentro MAU 2022</h1></div>', unsafe_allow_html=True) 
st.text("")

#st.caption("Fuente: Formularios de participación en 1er y 2do Encuentro MAU 2022")

col1, col2, col3, col4, col5 = st.columns((1.4,1,1,1,3))   #https://blog.streamlit.io/introducing-new-layout-options-for-streamlit/

col1.metric("Nº Organizaciones/Huertas/Comunidades",total_members)
col2.metric("Nº Personas representantes",total_individuals)
col3.metric("Nº Territorios identificados",total_localidad)
col4.metric("Nº Redes sociales",total_inst)

st.text("")

#https://stackoverflow.com/questions/33997361 
#https://stackoverflow.com/questions/50193159/converting-pandas-data-frame-with-degree-minute-second-dms-coordinates-to-deci

col5, col6, col7 = st.columns((6,1,6))

#___________________________________________________________________________________________________________________________________________________________
# TREEAMAP
#___________________________________________________________________________________________________________________________________________________________
df_tree = pd.DataFrame(df_bbdd,columns=['Region','Localidad','Organización_Huerta_Colectivo','Nombre_representante'])
df_tree = df_tree.groupby(['Region','Localidad','Organización_Huerta_Colectivo'])['Nombre_representante'].count()              # aggregating by number of persons
df_tree = df_tree.groupby(['Region','Localidad','Organización_Huerta_Colectivo']).size().reset_index(name='Personas')   # adding count agg as column

fig = px.treemap(df_tree, path=[px.Constant("Chile"),'Region','Localidad'], values = 'Personas')
fig.update_traces(root_color="lightgray")
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
#fig.show()   
col7.markdown('Distribución de Organizaciones/Huertas/Comunidades por Regiones y Localidades')
col7.caption('Explore el siguiente gráfico interactivo seleccionando algun territorio.')
col7.plotly_chart(fig)
col7.caption('Con esta herramienta analítica podremos visualizar, entre otras cosas, dónde estamos, qué territorios son aquellos donde tenemos mayor presencia u otro tema de interés para el MAU')

#___________________________________
# Changing geo coordinates to decimals
#___________________________________
@st.cache
def dms2dd(s):
    # example: s = """0°51'56.29"S"""
    degrees, minutes, seconds, direction = re.split('[°\'"]+', s)
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    if direction in ('S','O'):  #O oeste
        dd*= -1
    return dd
#________________________________________________________________________________________________________________________________________________________________
# GEO MAPPING - ALL ENTITIES
#________________________________________________________________________________________________________________________________________________________________
df = df_bbdd[['lat','lon']].drop_duplicates()
df = df[df['lat'] != 'No info']
df = df[df['lon'] != 'No Info']
df = df[~(df['lon']==df['lat'])] # to exclude error values -> .csv to be corrected
df['lat'] = df['lat'].apply(dms2dd)
df['lon'] = df['lon'].apply(dms2dd)
df_geo = pd.DataFrame(df,columns=['lat','lon'])
df_geo.style.set_caption("Hello World")
#df_geo.update_geos(fitbounds="locations") #for some reason it wont work now
col5.markdown("Distribución geográfica de las Organizaciones, Huertas y/o Comunidades")
col5.caption('Explore el siguiente mapa de huertas y organizaciones del MAU. Puede acercar y alejar la imagen del mapa segun su interés. Podría incluso buscar aquellas organizaciones del MAU que están mas cercana a su comunidad y desde ahi activar la red.')
col5.map(df_geo)
st.markdown("""---""")

#________________________________________________________________________________________________________________________________________________________________

st.header('🌻 Análisis Encuentros MAU (11/2022, 12/2022) ✨') 
#________________________________________________________________________________________________________________________________________________________________

df_bbdd_p = pd.DataFrame(df_bbdd,columns=['Region','Localidad','Organización_Huerta_Colectivo','Nombre_representante','Asistencia 1er Encuentro','Asistencia 2do Encuentro'])
asist_1er   = len(df_bbdd_p[df_bbdd_p['Asistencia 1er Encuentro']=='Sí'])
asist_2do   = len(df_bbdd_p[df_bbdd_p['Asistencia 2do Encuentro']=='Sí'])
asist_ambos = len(df_bbdd_p[(df_bbdd_p['Asistencia 1er Encuentro']=='Sí') & (df_bbdd_p['Asistencia 2do Encuentro']=='Sí')])

col1, col2, col3 = st.columns((6,1,6))
#_____________________________________
col1.subheader('Participación')
#_____________________________________
col1.markdown('**Asistencia personas a encuentros del MAU**')
col1.metric("1er Encuentro",asist_1er)
col1.metric("2do Encuentro",asist_2do)
col1.metric("Ambos Encuentros",asist_ambos) 
st.markdown("""---""")
#col4.caption('Análisis todas las respuestas a la pregunta *Relación con la agroecología*: 10 Palabras más frecuentes.')
#col4.table(wa.f.iloc[:10])

col3.subheader('Análisis de la relación con la agroecología (12/2022)')
col3.caption('Este gráfico se construye partir de las respuestas del formulario de inscripción destacando con tamaños más grandes las palabras que más se repitieron.')
#col3.caption('Aquí, por ejemplo, se puede reconocer algunas claves de lo que nos relaciona con la agroecología.')
col3.image('wordcloud_2doencuentro.png', width=700)


col1, col2, col3 = st.columns((6,1,6))

with col1:
    #____________________________________________________
    st.subheader('Análisis de Expectativas')
    #____________________________________________________
   
    st.markdown('En los primeros dos encuentros del MAU 2022 se abrieron preguntas acerca de las expectativas sobre el MAU.\nAquí se presenta una herramienta analítica que nos permite explorar estas respuestas.')
    st.caption("1er Encuentro: *¿Cuáles serían los objetivos de esta articulación* [Movimiento]?")
    st.caption("2do Encuentro: *¿Qué esperas de una articulación entre huertas urbanas?*")

    #Multiselector for source of information regarding expectations (1r and 2d Meeting)
    st.text(" ")
    fuente_expectativa = col1.multiselect("Selecciona fuente de información", options=df_expectativas["Fuente"].unique(),)  
    all_options = st.checkbox("Ambos encuentros")

    if all_options:
        fuente_expectativa = df_expectativas["Fuente"].unique().tolist()
            
    df_expectativas_fuente = df_expectativas.query('Fuente == @fuente_expectativa')  #Filter by source of information
    expectativas_s = col1.multiselect("Selecciona tematica", options=df_expectativas_fuente["Dimensión"].unique(),)
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

with col3:
    #________________________________________
    st.subheader('Análisis FODA (12/2022)')
    #________________________________________
    st.markdown(
    'El análisis FODA es una herramienta de investigación participativa que permitió identificar características comunes entre los diferentes \
    espacios que forman el MAU.\nPara ello se consideraron 4 marcos de análisis: Debilidades, Amenazas, Fortalezas y Oportunidades.')
    foda_s = st.multiselect("Selecciona marco de análisis", options=df_foda["Tipo"].unique(),)
    df_foda_s = df_foda.query('Tipo == @foda_s')
    df_foda_summary = df_foda_s[['Tipo','Transcripción','Clasificación Específica','Clasificación Agrupada']]
    df_foda_summary.rename(columns = {'Tipo':'Dimensión',}, inplace = True)

    fig2 = px.sunburst(data_frame = df_foda_s,path = ['Tipo', 'Clasificación Agrupada', 'Clasificación Específica', 'Transcripción'],values = None)  

    if  len(foda_s) == 0:
        st.markdown('Resultados:')
        st.caption('🥕 No hay información seleccionada')
    else:
        st.caption('Explora las respuestas del FODA interactuando con el gráfico solar. Puedes partir por seleccionar tu dimensión de interés.')
        st.plotly_chart(fig2)
        with st.expander("Ver detalle"):
            st.table(df_foda_summary)
            st.caption('Fuente: Metodología Participativa, 2do Encuentro MAU (3/12/2022)')
st.markdown("""---""")

#_________________________________________________________________

st.subheader("🌽 Análisis de Sistematización y Mapeo ✨")
#_________________________________________________________________
st.markdown('Aquí podra conocer a las organizaciones, huertas y colectivos que forman la red del MAU. La información se organiza por territorios. ')
#st.caption('')

col1, col2 = st.columns((1,1))

with col1:
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

df_bbdd_summary = df_bbdd_filtered[['Organización_Huerta_Colectivo', \
                                    'Localidad','Relación con la agroecología',]]

df_bbdd_summary.rename(columns = {'Organización_Huerta_Colectivo'                :'Nombre Organización, Huerta y/o Colectivo',
                                  'Nombre_representante'                         :'Nombre persona representante',},  inplace = True)
if  len(Territorio) == 0:
    st.markdown('Resultados')
    st.caption('🥕 No hay información seleccionada')
else:
    col1, col2, col3, col4, col5 = st.columns((1.5,1,1,1,2))

    col1.metric("Nº Organizaciones, Huertas y/o Comunidades",total_members_f)
    col2.metric("Nº Personas representantes",total_individuals_f)
    col3.metric("Nº Territorios identificados",total_localidad_f)
    col4.metric("Nº Redes sociales",total_inst_f)            
            
    #st.write(df_bbdd_summary['Nombre Organización, Huerta y/o Colectivo'].unique())
    st.markdown('Información general de las Organizaciones, Huertas y/o Colectivo en el territorio seleccionado*.')
    st.write(df_bbdd_summary.to_html(), unsafe_allow_html=True)
    st.caption('*Se espera que aquí se visualice información de las organizaciones, huertas y/o colectivos en el MAU que tenga carácter público y que contribuyan positivamente a los objetivos del MAU')
    st.caption('Fuente de la información: Formularios de participación en 1er y 2do Encuentro MAU 2022')

st.markdown("""---""")
#______________________________

st.subheader('✨🌼 Formulario de Retroalimentación 🐝✨')
#______________________________
st.markdown("[Comparte tu visión y experiencia con esta Web App respondiendo al formulario de retroalimentación aquí](https://forms.gle/fwULxu8f7kdrKDVFA)")
st.markdown('Las preguntas ahí ayudaran a :\n- Explorar la experiencia de usuario con el Prototipo Web App 1.0 - MAU 2023.\n- Caracterizar las diferentes visiones sobre el potencial de uso para una herramienta como el Prototipo Web App 1.0 - MAU 2023.\n- Identificar potenciales contenidos a considerar en futuras etapas de sistematización y mapeo.\n- Identificar contenidos que deben considerarse dentro de la esfera pública del MAU y aquellos que sólo deban estar disponibles para la gestión interna del MAU.')
st.markdown('De antemano, muchas gracias.\nEquipo de sistematización y mapeo – MAU\nEnero 2023')
st.markdown("""----""")

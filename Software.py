import datetime
import time
import streamlit as st
import plotly_express as px
import pandas as pd
from PIL import Image

#DISEÑO
def design():
    st.set_option('deprecation.showfileUploaderEncoding',False)
    title_container = st.container()
    col1, col3 = st.columns([15, 5])
    image = Image.open(r'C:\Users\josma\Documents\CarpetaVisualStudio\cecytem.jpg')
    logmx = Image.open(r'C:\Users\josma\Documents\CarpetaVisualStudio\mx2.jpg')
    with title_container:
        with col1:
                st.image(image, width=150)
        with col3:
                st.image(logmx, width=150)
    st.markdown("<h1 style='text-align: center; color: white;'>Colegio de Estudios Científicos y Tecnológicos del Estado de México</h1>", unsafe_allow_html=True)

#BARRA AJUSTES Y LECTURA ARCHIVO
def lectura_archivo():
    st.subheader("INSERTAR ARCHIVO:")
    # CARGA DE ARCHIVOS
    archivo_cargado = st.file_uploader(label="Sube aqui tus archivos CSV o Excel.",
                         type=['csv','xlsx'])
    global datos
    # si el archivo cargado no es ninguno
    if archivo_cargado is not None:
        print(archivo_cargado)
        try:
            datos = pd.read_csv(archivo_cargado)
        except Exception as e:
            print(e)
            datos = pd.read_excel(archivo_cargado)
    global cols_num
    try:
        st.write(datos)# tipos de datos del df, seleccion de columns
        cols_num = list(datos.select_dtypes(['float','int','object']).columns)
        #cols_numNoNumericas = list(datos.select_dtypes(['object']).columns)
    except Exception as e:
        print(e)
        st.write("Porfavor suba su archivo a la aplicación")

    #SELECCIONAR GRAFICO
    sel_graf = st.selectbox("Selecciona el tipo de gráfico: ",["Barras","Histograma"])

    if sel_graf == 'Barras':
            st.subheader("Gráfico de barras:")
    try:
            x_val = st.selectbox('Seleccione x: ', options = cols_num)
            y_val = st.selectbox('Seleccione y: ', options = cols_num)
            plot = px.bar(data_frame=datos, x=x_val,y=y_val,width=600, height=400)
            st.plotly_chart(plot)
    
    except Exception as e:
        print(e)

#BD BASA EN DISCO
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

def seguridad():
    design()
    menu = ["Acceder", "SignUp", "Cerrar Sesión"]
    choice = st.sidebar.selectbox("MENU", menu)

    if choice == "Cerrar Sesión":
        st.info("Has cerrado sesión")

    elif choice == "Acceder":
        username = st.sidebar.text_input("Nombre de usuario")
        password = st.sidebar.text_input("Contraseña", type = 'password')
        if st.sidebar.checkbox("Acceder"):
            #CONTRASENA
            create_usertable()
            result = login_user(username,password)
            if result:
                st.success("Te has logeado como: {}".format(username))                          
                lectura_archivo()
                #task = st.selectbox("Opciones:", ["Add Post", "Analytics", "Profiles"])
                #if task == "Add Post":
                 #   st.subheader("Add Your Post")
                #elif task == "Analytics":
                #    st.subheader("Analytics")
                #elif task == "Profiles":
                 #   st.subheader("User Profiles")
                 #   user_result = view_all_users()
                  #  clean_db = pd.DataFrame(user_result,columns = ["Username", "Password"])
                  #  st.dataframe(clean_db)
            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create new account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, new_password)
            st.success("New account")
            st.info("Go to login menu, to login")

#USUARIO Y CONTRASEÑA
def autorizacion():
    usuario = st.text_input("Usuario:", "")
    password = st.text_input("Contrasena:")
    while True:
        if usuario == "yo" and password == "contra":
            
            break

#FUNCION PRINCIPAL        
seguridad()
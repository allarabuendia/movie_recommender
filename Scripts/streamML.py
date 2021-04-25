import os
import joblib
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import streamlit as st
from bokeh.models.widgets import ColorPicker
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.imagenet_utils import preprocess_input
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image
from skimage.transform import resize
import ML as ml
import clean as cl
import cv2


matplotlib.use('Agg')

import tensorflow as tf
load_model = tf.keras.models.load_model('model4.h5')

def main():
    st.title('Streamlit Proyects')

    menu = ['Home', 'Movie recommender', 'Color picker', 'Login', 'SingUp']

    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        st.subheader('Bienvenido a Streamlit Proyects: ')
        st.text('Iré subiendo proyectos a la plataforma a la vez que voy aprendiendo')
        st.text('nuevas herramientas y librerías relaccionadas con la cienca de datos.')
        st.subheader('Welcome to Streamlit Proyects: ')
        st.text('I will upload projects to the platform while I am learning')
        st.text('new tools and libraries related to data science.')




    elif choice == 'Login':
        username = st.sidebar.text_input('Username')
        password = st.sidebar.text_input('Password', type='password')
        if st.sidebar.checkbox('Login'):
            if password == '12345':
                st.success('Bienvenido {}'.format(username))

        else:
            st.warning('Usuario o contraseña incorrecta')

    elif choice == 'SingUp':
        new_username = st.text_input('User name')
        new_password = st.text_input('Password', type='password')
        confirm_password = st.text_input('Confirm Password', type='password')
        if new_password == confirm_password:
            st.success('Password confirmed')
        else:
            st.warning('Passwords not the same')

        if st.button('Submit'):
            pass

    elif choice == 'Movie recommender':

        st.subheader('Movie recommender')

        menu2 = ['Por encuesta', 'Por coincidencia']
        choice2 = st.selectbox('¿Cómo quieres encontrar tu película?', menu2)

        if choice2 == 'Por encuesta':

            time = ['Menos de 1h30','Entre 1h30 y 2h', 'Entre 2h y 2h30', 'Más de 2h30']
            genero = ['drama', 'action', 'comedy', 'adventure', 'fantasy', 'sciencefiction', 'family', 'horror',
                      'romance', 'thriller', 'crime', 'western']
            rating = ['Si, hoy estoy sibarita', 'No, hoy todo vale']
            select = ['Con foto', 'Manual']
            animo2 = ['He tenido un buen día, ¡hoy me atevo con todo!', 'Dia duro, necesito desconectar ...']


            st.text('Bienvenido/a al recomendador de películas por encuesta.')
            st.text(' Completa la encuesta para obtener tu recomendación personalizada:')

            time_choice = st.selectbox('¿De cuanto tiempo dispones?', time)

            genero_choice = st.multiselect('¿Qué géneros prefieres?, (Elige entre 1 y 3 géneros)', genero)

            if len(genero_choice) == 0:
                st.warning('Debes poner entre 1 y 3 géneros')
            if len(genero_choice) > 3:
                st.warning('Debes poner entre 1 y 3 géneros')


            rating_choice = st.selectbox('¿Te apetece una película con buenas críticas?', rating)

            st.subheader('Veamos tu estado de ánimo')

            sen_animo = st.selectbox('¿Cómo quieres contestar?', select)

            if sen_animo == 'Con foto':

                sen_choice3 = st.file_uploader('Bien, sube una foto de tu rostro de frente, vamos a ver qué tal te ha ido el día', type='jpg')


                image1 = Image.open(sen_choice3).convert('L')
                image2 = np.array(image1)
                st.text(image2.shape)

                try:

                    st.image(sen_choice3)

                except:

                    pass

                labels = {'angry': 0,'disgust': 1,'fear': 2,'happy': 3,'neutral': 4,'sad': 5,'surprise': 6}

                sen_choice3 = cv2.resize(image2, (48, 48))/255.0

                sen_choice3 = sen_choice3.reshape(1, 48, 48, 1)

                pred = np.argmax(load_model.predict(sen_choice3))


                if pred == 3 or 4 or 6:
                    st.text('¡Parece que tienes un buen día!')
                    sen_choice2 = 0

                else:
                    st.text('Vaya carita me traes colega, necesitas desconectar...')
                    sen_choice2 = 1

                if rating_choice == 'Si, hoy estoy sibarita':
                    rating_choice2 = 'Buena'
                else:
                    rating_choice2 = 'Mala'

                mascara1 = cl.df_palabras1['duracion'] == time_choice

                if len(genero_choice) == 1:
                    mascara2 = (cl.df_palabras1['generos'].str.contains(genero_choice[0]))
                elif len(genero_choice) == 2:
                    mascara2 = (cl.df_palabras1['generos'].str.contains(genero_choice[0])) | (cl.df_palabras1['generos'].str.contains(genero_choice[1]))
                elif len(genero_choice) == 3:
                    mascara2 = (cl.df_palabras1['generos'].str.contains(genero_choice[0])) | (cl.df_palabras1['generos'].str.contains(genero_choice[1])) | (cl.df_palabras1['generos'].str.contains(genero_choice[2]))

                mascara3 = cl.df_palabras1['rate'] == rating_choice2
                mascara4 = cl.df_palabras1['sentimiento'] == sen_choice2

                lista_pelis = st.button('Ver mi recomendación(hasta 5 peliculas)')

                if lista_pelis:

                    st.text('Esta es tu recomendación personalizada:')

                    cl.df_palabras1[mascara1 & mascara2 & mascara3 & mascara4]['titulo'][:5:]

                lista_pelis2 = st.button('Ver mi recomendación(hasta 10 peliculas)')

                if lista_pelis2:

                    st.text('Esta es tu recomendación personalizada:')

                    cl.df_palabras1[mascara1 & mascara2 & mascara3 & mascara4]['titulo'][:10:]

            else:

                pregunta = st.selectbox('¿Como te ha ido el día?', animo2)

                if pregunta == 'He tenido un buen día, ¡hoy me atevo con todo!':
                    sen_choice5 = 0
                else:
                    sen_choice5 = 1

                if rating_choice == 'Si, hoy estoy sibarita':
                    rating_choice2 = 'Buena'
                else:
                    rating_choice2 = 'Mala'

                mascara1 = cl.df_palabras1['duracion'] == time_choice

                if len(genero_choice) == 1:
                    mascara2 = (cl.df_palabras1['generos'].str.contains(genero_choice[0]))
                elif len(genero_choice) == 2:
                    mascara2 = (cl.df_palabras1['generos'].str.contains(genero_choice[0])) | (cl.df_palabras1['generos'].str.contains(genero_choice[1]))
                elif len(genero_choice) == 3:
                    mascara2 = (cl.df_palabras1['generos'].str.contains(genero_choice[0])) | (cl.df_palabras1['generos'].str.contains(genero_choice[1])) | (cl.df_palabras1['generos'].str.contains(genero_choice[2]))

                mascara3 = cl.df_palabras1['rate'] == rating_choice2
                mascara4 = cl.df_palabras1['sentimiento'] == sen_choice5

                lista_pelis = st.button('Ver mi recomendación(hasta 5 peliculas)')

                if lista_pelis:

                    st.text('Esta es tu recomendación personalizada:')

                    cl.df_palabras1[mascara1 & mascara2 & mascara3 & mascara4]['titulo'][:5:]

                lista_pelis2 = st.button('Ver mi recomendación(hasta 10 peliculas)')

                if lista_pelis2:

                    st.text('Esta es tu recomendación personalizada:')

                    cl.df_palabras1[mascara1 & mascara2 & mascara3 & mascara4]['titulo'][:10:]



        elif choice2 == 'Por coincidencia':

            peliselect = st.selectbox('Selecciona una película que hayas visto',cl.df_palabras1['titulo'])

            if st.button('Predecir'):

                st.text('He encontrado estas películas')

                st.table(ml.recomendador(peliselect))



    elif choice == 'Color picker':
        st.subheader('Color picker')
        color_picker = ColorPicker(color="#ff4466", title="Choose color:", width=200)
        st.bokeh_chart(color_picker)


if __name__ == '__main__':
    main()

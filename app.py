# Para crear el requirements.txt ejecutamos 
# pipreqs --encoding=utf8 --force

# Primera Carga a Github
# git init
# git add .
# git commit -m "primer commit"
# git remote add origin https://github.com/nicoig/chat-sales.git
# git push -u origin master

# Actualizar Repo de Github
# git add .
# git commit -m "Se actualizan las variables de entorno"
# git push origin master

# Para eliminar un repo cargado
# git remote remove origin

# En Render
# agregar en variables de entorno
# PYTHON_VERSION = 3.9.12

# Pasando a master
# git checkout -b master
# git push origin master



###############################################################


# app.py

# Importar Librerías
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Cargar Datos
df = pd.read_excel("adidas.xlsx")

from langchain.llms import OpenAI
from langchain.agents import create_pandas_dataframe_agent

# Crear el Agente
agent = create_pandas_dataframe_agent(OpenAI(temperature=0.1), df, verbose=False)

# Ajustes de Streamlit
st.title("💰 Chatea con tus Ventas 💰")

st.subheader("Haz preguntas y obtén insights sobre tus datos de ventas, como:")
st.write("- Haz un top 10 de los productos más vendidos.")
st.write("- ¿Cuáles son las ventas totales del último mes?")
st.write("- Compara las ventas de este mes con las del mes pasado.")

# Cree una sección expandible para mostrar los primeros 10 registros del DataFrame
with st.expander("Haga clic aquí para ver los primeros 5 registros"):
    st.write(df.head(5))

# Inicializa el historial de chat si aún no lo está set
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes de chat del historial en cada repetición de la aplicación
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Aceptar la entrada del usuario
if prompt := st.chat_input("Realiza tu consulta:"):
    # Agregar mensaje de usuario al historial de chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Mostrar mensaje de usuario en el contenedor de mensajes de chat
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Procesar la entrada con el agente y obtener la respuesta
    agent_response = agent.run(prompt)

    # Verificar si hay una figura activa en matplotlib
    if plt.gcf().get_axes():
        # Crear un objeto BytesIO para capturar la imagen del gráfico
        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)

        # Mostrar el gráfico en Streamlit
        with st.chat_message("assistant"):
            st.image(buf.getvalue(), caption="Gráfico generado")
            
            # Agregar botón para descargar la imagen
            st.download_button(
                label="Descargar imagen",
                data=buf.getvalue(),
                file_name="grafico.png",
                mime="image/png"
            )

            st.markdown(agent_response)
            st.session_state.messages.append({"role": "assistant", "content": agent_response})
    else:
        # Si no hay gráfico, simplemente mostramos la respuesta en texto
        with st.chat_message("assistant"):
            st.markdown(agent_response)
            st.session_state.messages.append({"role": "assistant", "content": agent_response})

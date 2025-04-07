import streamlit as st
import requests
from deep_translator import GoogleTranslator
from PIL import Image
import pytesseract

# ---------------------------------------------
st.title("🤖 Tu asistente IA - Chat + OCR + Traducción")
st.write("Consulta cualquier cosa y traduce tus imágenes.")

# 1) API KEY Gestión 
import os

api_key = os.environ.get("API_KEY")
assert api_key is not None, "API_KEY no encontrada en secrets"

# ---------------------------------------------
# 2) Función para consultar OpenRouter
def get_gpt_response(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",     # Cambia al modelo compatible con tu API Key
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# ---------------------------------------------
# 3) Función traducción inglés → español usando Deep Translator
def traducir_al_espanol(texto):
    traductor = GoogleTranslator(source='auto', target='es')
    return traductor.translate(texto)

# ---------------------------------------------
# 4) Interfaz APP

menu = st.sidebar.selectbox("Elige opción", ["Chat IA", "OCR Imagen"])

# Chatbot IA
if menu == "Chat IA":
    st.subheader("🗨️ Chatea con el Asistente AI")
    pregunta = st.text_area("Escribe aquí tu pregunta en inglés o español:")

    if st.button("Preguntar a la IA"):
        if pregunta.strip() != "":
            # Siempre se envía en inglés, lo traducimos si hace falta
            try:
                respuesta = get_gpt_response(pregunta)
                st.write("**Respuesta en inglés:**", respuesta)
                
                traduccion = traducir_al_espanol(respuesta)
                st.write("**Traducción al español:**", traduccion)
            except Exception as e:
                st.error(f"Error obteniendo respuesta: {e}")
        else:
            st.warning("Por favor, escribe algo para preguntar.")

# OCR de imagen
elif menu == "OCR Imagen":
    st.subheader("📷 Sube una imagen para extraer texto")
    imagen_subida = st.file_uploader("Elige una foto", type=["png", "jpg", "jpeg"])

    if imagen_subida:
        image = Image.open(imagen_subida)
        st.image(image, caption='Imagen subida', use_column_width=True)
        
        texto_extraido = pytesseract.image_to_string(image)
        st.write("**Texto detectado:**")
        st.write(texto_extraido)
        
        if texto_extraido.strip() != "":
            traduccion = traducir_al_espanol(texto_extraido)
            st.write("**Traducción al español:**")
            st.write(traduccion)
        else:
            st.info("No se detectó texto en la imagen.")


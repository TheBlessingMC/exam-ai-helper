import streamlit as st
import requests
from deep_translator import GoogleTranslator
from PIL import Image
import pytesseract
import os

st.set_page_config(page_title="Mi Asistente AI")
st.title("🤖 Tu Asistente AI Multimodal")

# API KEY desde secrets
api_key = os.environ.get("API_KEY")
assert api_key is not None, "API_KEY no encontrada en secrets."

# -----------------
# Función para pedir respuesta al modelo
def get_gpt_response(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",   # Cambia por el modelo compatible con tu API key si quieres
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error consultando OpenRouter: {str(e)}"

# -----------------
# Función traducción con control errores
def traducir_al_espanol(texto):
    try:
        traductor = GoogleTranslator(source='auto', target='es')
        traduccion = traductor.translate(texto)
        return traduccion
    except Exception:
        return "(⚠️ Traducción no disponible por ahora)"

# -----------------
# Menú lateral
opcion = st.sidebar.selectbox("Elige modo", ("Chat IA", "OCR Imagen"))

if opcion == "Chat IA":
    st.header("💬 Chat con la IA")

    pregunta = st.text_area("Escribe algo para preguntarle:")

    if st.button("Enviar pregunta"):
        if pregunta.strip() != "":
            respuesta = get_gpt_response(pregunta)
            st.write("### Respuesta original (inglés):")
            st.write(respuesta)

            traduccion = traducir_al_espanol(respuesta)
            st.write("### Traducción al español:")
            st.write(traduccion)
        else:
            st.warning("✍️ Escribe una pregunta para continuar.")

# -----------------
elif opcion == "OCR Imagen":
    st.header("🖼️ Reconocer Texto en Imagen")
    archivo = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"])

    if archivo:
        imagen = Image.open(archivo)
        st.image(imagen, caption="Imagen subida", use_column_width=True)

        # Obtener texto con pytesseract
        try:
            texto_detectado = pytesseract.image_to_string(imagen)
        except:
            texto_detectado = ""

        st.write("### Texto detectado:")
        if texto_detectado.strip() != "":
            st.write(texto_detectado)

            traduccion = traducir_al_espanol(texto_detectado)
            st.write("### Traducción a español:")
            st.write(traduccion)
        else:
            st.warning("No se detectó texto para traducir.")

# -----------------
st.caption("Desarrollado con ❤️ usando OpenRouter, Deep Translator y Tesseract OCR")

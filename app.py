import streamlit as st
import requests

st.set_page_config(page_title="Examen AI Helper", page_icon="📚", layout="centered")

st.title("📚 Examen AI Helper")

st.write("Sube la imagen (solo si tienes OCR en local) o copia aquí la pregunta en inglés:")

tipo = st.radio("¿Cómo quieres ingresar la pregunta?", ["Escribir texto", "Subir imagen"])

api_key = st.secrets["API_KEY"] if "API_KEY" in st.secrets else "TU_API_KEY_AQUI"

if tipo == "Escribir texto":
    texto = st.text_area("Escribe o pega aquí tu pregunta en inglés:")

else:
    uploaded_file = st.file_uploader("Sube imagen", type=["jpg", "jpeg", "png"])
    texto = ""
    if uploaded_file:
        from PIL import Image
        img = Image.open(uploaded_file)
        st.image(img, caption="Imagen subida")
        st.warning("El OCR no funciona en la versión en la nube. Mejor escribe el texto.")

if st.button("Resolver con IA"):
    if texto.strip() == "":
        st.warning("Añade alguna pregunta.")
    else:
        prompt = f"""
Responde la siguiente pregunta de opción múltiple:

{texto}

Devuelve:
- La letra correcta (A, B, C,...).
- Una breve justificación.
- Un ejemplo sencillo.

Responde en inglés.
"""
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "openrouter/quasar-alpha",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500,
        }
        with st.spinner("Pensando..."):
            r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                              headers=headers, json=data)
            response = r.json()
            try:
                result = response['choices'][0]['message']['content']
            except:
                result = f"Error o sin respuesta: {response}"

        st.subheader("Respuesta en inglés:")
        st.write(result)

        with st.spinner("Traduciendo al español..."):
            trad = requests.post(
                "https://libretranslate.de/translate",
                params={"q": result, "source": "en", "target": "es"})
            try:
                traduccion = trad.json()["translatedText"]
            except:
                traduccion = "Error en traducción."

        st.subheader("Traducción:")
        st.write(traduccion)

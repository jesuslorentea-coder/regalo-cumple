import streamlit as st
import replicate
import os
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# 1. Configuración de la página
st.set_page_config(page_title="Mi Cumpleaños Mágico", page_icon="🎂")

# 2. Conexión segura con el Token
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("⚠️ Error: No se encuentra el Token. Ve a Settings -> Secrets en Streamlit.")

# --- CONFIGURACIÓN DE TU FOTO ---
# Sube tu foto a GitHub, ábrela, clic derecho "Copiar dirección de imagen" y pégala aquí:
URL_MI_FOTO = "TU_URL_DE_IMAGEN_AQUI" 

# 3. Interfaz de usuario
st.title("🎂 ¡Hagamos un recuerdo juntos!")
st.write("Dime dónde te gustaría que estuviéramos y la IA nos pondrá allí.")

lugar_propuesto = st.text_input("¿Dónde quieres que nos hagamos la foto?", 
                               placeholder="Ej: Tomando un mojito en una cascada")

foto_amigo = st.camera_input("Hazte un selfie para nuestro recuerdo")

# 4. Magia de la IA
if foto_amigo and lugar_propuesto:
    if st.button("✨ ¡Crear Recuerdo!"):
        with st.spinner("Cocinando nuestra foto... Esto tarda unos 20-30 segundos"):
            try:
                # Paso 1: Generar la escena y mezclar caras
                # Usamos un modelo avanzado que respeta el 'prompt' del lugar
                output = replicate.run(
                    "tencentarc/photomaker:ddfc2b6a",
                    input={
                        "prompt": f"A realistic photo of two happy friends, a man and another person, {lugar_propuesto}, high quality, cinematic lighting",
                        "input_image": URL_MI_FOTO,
                        "input_image2": foto_amigo,
                        "num_steps": 30,
                        "style_name": "Photographic",
                        "negative_prompt": "bad quality, blurry, distorted faces"
                    }
                )

                # El resultado suele ser una lista de imágenes
                resultado_url = output[0] if isinstance(output, list) else output

                # Paso 2: Mostrar y celebrar
                st.image(resultado_url, caption=f"Nosotros: {lugar_propuesto}")
                
                # Mensaje final grande
                st.markdown("### 🎈 ¡GRACIAS POR FELICITARME. ABRAZOS!!")
                st.balloons()
                
                # Botón de descarga
                response = requests.get(resultado_url)
                st.download_button(label="📥 Descargar nuestro recuerdo", 
                                   data=response.content, 
                                   file_name="nuestro_recuerdo.jpg", 
                                   mime="image/jpeg")

            except Exception as e:
                st.error(f"Hubo un problema técnico: {e}")

st.divider()
st.caption("Hecho con ❤️ para celebrar mi cumple")

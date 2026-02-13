import streamlit as st
import replicate
import os
import requests

# 1. Configuración de la página
st.set_page_config(page_title="Mi Cumpleaños Mágico", page_icon="🎂")

# 2. Conexión con el Token (Secrets)
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("⚠️ Falta el API Token en los Secrets de Streamlit.")

# 3. Dirección de tu foto en GitHub
URL_MI_FOTO = "https://raw.githubusercontent.com/jesuslorentea-coder/regalo-cumple/main/fotojesus.png"

# 4. Interfaz de usuario
st.title("🎂 ¡Hagamos un recuerdo juntos!")
st.write("Dime dónde te gustaría que estuviéramos y la IA nos pondrá allí.")

lugar_propuesto = st.text_input("¿Dónde quieres que nos hagamos la foto?", placeholder="Ej: Jugando al golf")
foto_amigo = st.camera_input("Hazte un selfie para nuestro recuerdo")

# 5. Lógica de generación
if foto_amigo and lugar_propuesto:
    if st.button("✨ ¡Crear Recuerdo!"):
        with st.spinner("Cocinando nuestra foto... Esto tarda unos 30 segundos"):
            try:
                # Usamos la versión de InstantID más estable y compatible
                output = replicate.run(
                    "lucataco/instantid:e7530869",
                    input={
                        "face_image": foto_amigo,
                        "image": URL_MI_FOTO,
                        "prompt": f"Two happy friends {lugar_propuesto}, realistic photograph, high quality, cinematic lighting",
                        "negative_prompt": "bad quality, blurry, distorted faces, naked",
                        "adapter_strength": 0.8,
                        "identity_net_strength": 0.8
                    }
                )

                resultado_url = output[0] if isinstance(output, list) else output
                st.image(resultado_url, caption=f"Nosotros: {lugar_propuesto}")
                st.balloons()
                st.success("¡GRACIAS POR FELICITARME! ¡ABRAZOS!")
                
                img_data = requests.get(resultado_url).content
                st.download_button("📥 Descargar foto", img_data, "recuerdo.jpg", "image/jpeg")

            except Exception as e:
                st.error(f"Hubo un problema técnico: {e}")

st.divider()
st.caption("Hecho con ❤️ para celebrar mi cumple")

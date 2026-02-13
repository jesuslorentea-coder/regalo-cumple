import streamlit as st
import replicate
import os
import requests

# 1. Configuración básica
st.set_page_config(page_title="Cumple de Jesús", page_icon="🎂")

# 2. Token de Seguridad
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("Falta el Token en Secrets.")

# 3. Tu foto de GitHub
URL_MI_FOTO = "https://raw.githubusercontent.com/jesuslorentea-coder/regalo-cumple/main/fotojesus.png"

st.title("🎂 ¡Nuestro recuerdo de cumple!")
st.write("Sube un selfie y nos pondré a los dos juntos.")

# 4. Entradas del usuario
lugar = st.text_input("¿Dónde quieres que estemos?", "jugando al golf")
foto_amigo = st.camera_input("Hazte un selfie")

if foto_amigo and st.button("✨ ¡Crear Magia!"):
    with st.spinner("Generando nuestra foto..."):
        try:
            # Este modelo es el más fiable para cambiar caras rápidamente
            output = replicate.run(
                "lucataco/faceswap:9a42989210f12d371465829672688ec8930e1596e1a47343b9d0b0051d95ec87",
                input={
                    "target_image": URL_MI_FOTO,
                    "swap_image": foto_amigo,
                }
            )
            
            st.image(output, caption=f"Nosotros {lugar}")
            st.balloons()
            st.success("¡GRACIAS POR FELICITARME! ¡ABRAZOS!")
            
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Nota: Revisa si has activado el 'Billing' en tu cuenta de Replicate.")

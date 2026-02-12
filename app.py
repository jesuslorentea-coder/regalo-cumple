import streamlit as st
import replicate
import os

# CONFIGURACIÓN: Pega aquí tu token de Replicate
os.environ["REPLICATE_API_TOKEN"] = "TU_TOKEN_AQUÍ"

st.set_page_config(page_title="Regalo de Cumpleaños", layout="centered")

st.title("🎂 ¡Hagamos un recuerdo juntos!")
st.write("Dime dónde quieres que estemos y subiré nuestra foto allí.")

# URL de tu foto (debe estar en alta calidad)
URL_MI_FOTO = "https://tu-web.com/tu_cara.jpg"

# Entradas del usuario
lugar = st.text_input("¿Dónde nos imaginas?", placeholder="Ej: En un concierto de rock")
foto_amigo = st.camera_input("Hazte un selfie")

if foto_amigo and lugar:
    if st.button("✨ Generar Magia"):
        with st.spinner("Cocinando nuestra foto..."):
            try:
                # PASO 1: Generar la base con el lugar
                prompt_base = f"Two best friends, high quality, realistic, laughing, at {lugar}"
                
                # Usamos un modelo de FaceSwap (ejemplo: InstantID o similares)
                output = replicate.run(
                    "lucataco/faceswap:9a429892", # Ejemplo de modelo de swap
                    input={
                        "target_image": URL_MI_FOTO, # Tu cara
                        "swap_image": foto_amigo,   # La cara del amigo
                    }
                )
                
                # PASO 2: Mostrar resultado
                st.image(output, caption="¡Mira qué bien salimos!")
                st.success("GRACIAS POR FELICITARME. ABRAZOS!!")
                
            except Exception as e:
                st.error(f"Ups, algo falló: {e}")
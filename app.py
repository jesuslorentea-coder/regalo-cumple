import streamlit as st
import replicate
import os

# 1. Configuración de la página
st.set_page_config(page_title="Mi Cumple", page_icon="🎂")

# 2. Conexión con el Token (Secrets)
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("⚠️ Falta el API Token en los Secrets de Streamlit. Ve a Settings -> Secrets y añádelo.")

# 3. Interfaz Visual
st.title("🎂 ¡Nuestro recuerdo de cumple!")
st.write("Sube un selfie y dime dónde quieres que estemos celebrando.")

# --- AQUÍ DEBES PONER EL LINK DE TU FOTO QUE SUBISTE A GITHUB ---
URL_TU_FOTO = "https://TU_LINK_DE_GITHUB_AQUI.jpg" 

# 4. Entradas del amigo (Esto es lo que activará la cámara y el texto)
lugar = st.text_input("¿Dónde quieres nuestro recuerdo?", placeholder="Ej: Tomando un mojito en una cascada")
foto_amigo = st.camera_input("Hazte un selfie para la foto")

# 5. Lógica de generación
if foto_amigo and lugar:
    if st.button("✨ ¡Crear Magia!"):
        with st.spinner("Generando nuestro recuerdo... esto tarda unos 20 segundos"):
            try:
                # Usamos el modelo de FaceSwap de Replicate
                output = replicate.run(
                    "lucataco/faceswap:9a429892",
                    input={
                        "target_image": URL_TU_FOTO,
                        "swap_image": foto_amigo,
                    }
                )
                
                # Resultado
                st.image(output, caption=f"Nosotros {lugar}")
                st.balloons()
                st.success("GRACIAS POR FELICITARME. ABRAZOS!!")
                
            except Exception as e:
                st.error(f"Hubo un error con la IA: {e}")

st.divider()
st.caption("Hecho con ❤️ para mi cumple")

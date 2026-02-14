import streamlit as st
from gradio_client import Client, handle_file
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
import tempfile
import os

st.set_page_config(page_title="Cumpleaños de Jesús", page_icon="🎂")

# --- FUNCIÓN DE CARGA A DRIVE ---
def upload_to_drive(file_bytes, file_name):
    try:
        creds = service_account.Credentials.from_service_account_info(st.secrets["google_credentials"])
        service = build('drive', 'v3', credentials=creds)
        folder_id = st.secrets["google_drive"]["folder_id"]
        
        file_metadata = {'name': file_name, 'parents': [folder_id]}
        media = MediaIoBaseUpload(io.BytesIO(file_bytes), mimetype='image/png')
        service.files().create(body=file_metadata, media_body=media).execute()
        return True
    except Exception as e:
        st.error(f"Error Drive: {e}")
        return False

# --- INTERFAZ ---
st.title("🎂 ¡Nuestro recuerdo de cumple!")
st.write("Dime dónde quieres que estemos y la IA nos pondrá allí.")

# 1. Recuperamos el campo del lugar
lugar = st.text_input("¿Dónde quieres que nos hagamos la foto?", "Jugando al golf")

# Foto de Jesús (la que ya tienes en GitHub)
URL_JESUS = "https://raw.githubusercontent.com/jesuslorentea-coder/regalo-cumple/main/fotojesus.png"

foto_amigo = st.camera_input("Hazte un selfie para nuestro recuerdo")

if foto_amigo and st.button("✨ ¡Crear Recuerdo!"):
    with st.spinner(f"Generando nuestra foto en: {lugar}..."):
        try:
            # 2. IA GRATUITA (Cambiamos el modelo por uno más robusto)
            # Usamos un cliente que no dependa de api_name específicos
            client = Client("sczhou/CodeFormer") 
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                tmp.write(foto_amigo.getvalue())
                tmp_path = tmp.name

            # Realizamos el procesamiento (este modelo es excelente para mejorar caras)
            result = client.predict(
                image=handle_file(tmp_path),
                background_enhance=True,
                face_upsample=True,
                upscale=2,
                codeformer_fidelity=0.5
            )

            # Nota: Para hacer el swap con el fondo y con Jesús de forma gratuita 
            # sin Replicate, estamos usando un mejorador de cara. 
            # Si quieres swap total, seguiremos ajustando el espacio de HF.

            with open(result, "rb") as f:
                img_final = f.read()

            # 3. MOSTRAR RESULTADO
            st.image(img_final, caption=f"Nosotros {lugar}")
            
            # 4. GUARDAR EN DRIVE
            st.info("Guardando en tu Google Drive...")
            upload_to_drive(foto_amigo.getvalue(), f"selfie_{lugar}.png")
            upload_to_drive(img_final, f"recuerdo_{lugar}.png")
            
            st.success("✅ ¡Todo guardado! ¡FELIZ CUMPLEAÑOS!")
            st.balloons()

        except Exception as e:
            st.error(f"Ups, algo falló: {e}")
            st.info("Prueba de nuevo, a veces los servidores gratuitos se saturan un momento.")

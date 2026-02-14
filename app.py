import streamlit as st
from gradio_client import Client, handle_file
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
import tempfile
import os

st.set_page_config(page_title="Cumpleaños de Jesús", page_icon="🎂")

# --- CONEXIÓN CON GOOGLE DRIVE ---
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

# --- UI ---
st.title("🎂 ¡Nuestro recuerdo de cumple!")
st.write("Sube tu selfie. ¡La IA es gratis y guardaré la foto en tu Drive!")

# Foto de Jesús (la que ya tienes en GitHub)
URL_JESUS = "https://raw.githubusercontent.com/jesuslorentea-coder/regalo-cumple/main/fotojesus.png"

foto_amigo = st.camera_input("Hazte un selfie")

if foto_amigo and st.button("✨ ¡Generar y Guardar!"):
    with st.spinner("Cocinando la magia..."):
        try:
            # 1. IA GRATUITA (Usando Gradio/HuggingFace)
            client = Client("tonyassi/face-swap")
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                tmp.write(foto_amigo.getvalue())
                tmp_path = tmp.name

            result = client.predict(
                source_image=handle_file(tmp_path),
                target_image=handle_file(URL_JESUS),
                api_name="/predict"
            )

            # 2. MOSTRAR Y GUARDAR
            with open(result, "rb") as f:
                img_final = f.read()

            st.image(img_final, caption="¡Quedamos genial!")
            
            # Guardamos ambos en Drive
            upload_to_drive(foto_amigo.getvalue(), "selfie_invitado.png")
            upload_to_drive(img_final, "recuerdo_final.png")
            
            st.success("✅ ¡Fotos guardadas en tu Google Drive!")
            st.balloons()

        except Exception as e:
            st.error(f"Ups, algo falló: {e}")

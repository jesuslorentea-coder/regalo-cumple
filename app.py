import streamlit as st
from gradio_client import Client, handle_file
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
import tempfile

st.set_page_config(page_title="Cumpleaños de Jesús", page_icon="🎂")

# --- FUNCIÓN DRIVE ---
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
lugar = st.text_input("¿Dónde quieres que nos hagamos la foto?", "Jugando al golf")

# Foto de Jesús (GitHub)
URL_JESUS = "https://raw.githubusercontent.com/jesuslorentea-coder/regalo-cumple/main/fotojesus.png"

foto_amigo = st.camera_input("Hazte un selfie")

if foto_amigo and st.button("✨ ¡Crear Recuerdo!"):
    with st.spinner(f"Cocinando la foto... Esto puede tardar hasta 2 minutos si hay mucha gente usándolo."):
        try:
            # CAMBIO DE MOTOR: Este está público y funcionando
            client = Client("tuan2308/face-swap")
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                tmp.write(foto_amigo.getvalue())
                tmp_path = tmp.name

            # El motor 'tuan2308' usa estos parámetros
            result = client.predict(
                source_file=handle_file(tmp_path), # Tu selfie
                target_file=handle_file(URL_JESUS), # Foto de Jesús
                do_face_restoration=True # Para que quede guapo
            )

            # El resultado es una lista, cogemos el primer elemento (la imagen)
            img_path = result[0] if isinstance(result, list) else result
            
            with open(img_path, "rb") as f:
                img_final = f.read()

            st.image(img_final, caption=f"¡Míranos en {lugar}!")
            
            # Guardar
            upload_to_drive(foto_amigo.getvalue(), f"selfie_{lugar}.png")
            upload_to_drive(img_final, f"recuerdo_{lugar}.png")
            st.success("✅ ¡Guardado en Drive!")
            st.balloons()

        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Si el error dice 'Queue full', espera 30 segundos y dale otra vez.")

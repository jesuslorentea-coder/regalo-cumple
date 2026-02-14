import streamlit as st
from gradio_client import Client, handle_file
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
import tempfile

st.set_page_config(page_title="Cumpleaños de Jesús", page_icon="🎂")

# --- CONEXIÓN CON DRIVE ---
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

# Recuperamos la pregunta del lugar
lugar = st.text_input("¿Dónde quieres que nos hagamos la foto?", "Jugando al golf")

# Foto de Jesús (GitHub)
URL_JESUS = "https://raw.githubusercontent.com/jesuslorentea-coder/regalo-cumple/main/fotojesus.png"

foto_amigo = st.camera_input("Hazte un selfie para nuestro recuerdo")

if foto_amigo and st.button("✨ ¡Crear Recuerdo!"):
    with st.spinner(f"Cocinando nuestra foto en {lugar}... (Esto puede tardar 1-2 min si hay cola)"):
        try:
            # Usamos un modelo de Face Swap más sencillo y estable
            client = Client("ghostman/face-swap") 
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                tmp.write(foto_amigo.getvalue())
                tmp_path = tmp.name

            # Llamada directa sin 'api_name' para evitar el error anterior
            result = client.predict(
                source_image=handle_file(tmp_path),
                target_image=handle_file(URL_JESUS)
            )

            # El resultado suele ser una ruta de archivo local en el servidor
            with open(result, "rb") as f:
                img_final = f.read()

            # MOSTRAR Y GUARDAR
            st.image(img_final, caption=f"¡Míranos en {lugar}!")
            
            upload_to_drive(foto_amigo.getvalue(), f"selfie_{lugar}.png")
            upload_to_drive(img_final, f"recuerdo_{lugar}.png")
            
            st.success("✅ ¡Guardado en tu Google Drive!")
            st.balloons()

        except Exception as e:
            st.error(f"Hubo un pequeño bache: {e}")

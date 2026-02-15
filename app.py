import streamlit as st
from gradio_client import Client, handle_file
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
import tempfile
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Regalo de Jesús", page_icon="🎂")

# Función para subir a Drive (Confirmada tu folder_id)
def upload_to_drive(file_bytes, file_name):
    try:
        creds_info = st.secrets["google_credentials"]
        creds = service_account.Credentials.from_service_account_info(creds_info)
        service = build('drive', 'v3', credentials=creds)
        
        folder_id = st.secrets["google_drive"]["folder_id"]
        file_metadata = {'name': file_name, 'parents': [folder_id]}
        
        media = MediaIoBaseUpload(io.BytesIO(file_bytes), mimetype='image/png')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return file.get('id')
    except Exception as e:
        st.error(f"Error subiendo a Drive: {e}")
        return None

# --- INTERFAZ ---
st.title("🎁 Creador de Recuerdos Mágicos")
st.markdown("Generaremos una foto tuya con Jesús en el lugar que elijas.")

# 1. Entrada de datos
lugar = st.text_input("¿Dónde quieres que estéis?", "Jugando al golf en el espacio")
foto_amigo = st.camera_input("Hazte un selfie")

# Foto de referencia de Jesús
URL_JESUS = "https://raw.githubusercontent.com/jesuslorentea-coder/regalo-cumple/main/fotojesus.png"

if foto_amigo and st.button("✨ Generar y Guardar en Drive"):
    with st.status("🚀 Procesando tu regalo...", expanded=True) as status:
        try:
            # Preparar archivos temporales
            status.write("📸 Analizando tu selfie...")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                tmp.write(foto_amigo.getvalue())
                selfie_path = tmp.name

            # MOTOR DE IA: Usamos un FaceSwap altamente disponible
            status.write("🤖 Conectando con el servidor de IA (esto puede tardar por la cola)...")
            # Este motor es más estable para llamadas externas
            client = Client("tonyassi/face-swap")
            
            # Realizar el intercambio (Swap)
            # Nota: Usamos predict sin api_name para que el servidor elija la función principal automáticamente
            result = client.predict(
                source_image=handle_file(selfie_path), # Tu cara
                target_image=handle_file(URL_JESUS),   # Cara de Jesús / Escenario
            )

            # El resultado suele ser la ruta a la imagen generada
            img_path = result if isinstance(result, str) else result[0]
            
            with open(img_path, "rb") as f:
                img_final = f.read()

            # Mostrar resultado
            status.write("🎨 ¡Recuerdo generado!")
            st.image(img_final, caption=f"¡Juntos en: {lugar}!", use_container_width=True)

            # GUARDAR EN DRIVE
            status.write("📂 Guardando en tu Google Drive...")
            # Guardamos el selfie original
            upload_to_drive(foto_amigo.getvalue(), f"selfie_{lugar}.png")
            # Guardamos el resultado final
            id_final = upload_to_drive(img_final, f"recuerdo_{lugar}.png")

            if id_final:
                status.update(label="✅ ¡Todo guardado correctamente!", state="complete")
                st.balloons()
            
        except Exception as e:
            status.update(label="❌ El servidor de IA está saturado", state="error")
            st.error(f"Error técnico: {e}")
            st.info("💡 Como es un servicio gratuito, a veces hay mucha cola. Espera 1 minuto e inténtalo de nuevo.")
        finally:
            if os.path.exists(selfie_path):
                os.remove(selfie_path)

# --- REQUISITOS (asegúrate de que tu requirements.txt tenga esto) ---
# streamlit
# gradio_client
# google-api-python-client
# google-auth

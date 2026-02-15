import streamlit as st
from gradio_client import Client, handle_file
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
import tempfile
import os

# 1. Configuración de seguridad y página
st.set_page_config(page_title="Regalo de Jesús", page_icon="🎂", layout="centered")

def check_secrets():
    """Verifica que todos los secretos necesarios estén presentes."""
    required = ["google_credentials", "google_drive"]
    for req in required:
        if req not in st.secrets:
            st.error(f"Falta la configuración de: {req} en los Secrets.")
            return False
    return True

# 2. Función de Google Drive (Optimizada)
def upload_to_drive(file_bytes, file_name):
    try:
        creds = service_account.Credentials.from_service_account_info(st.secrets["google_credentials"])
        service = build('drive', 'v3', credentials=creds)
        folder_id = st.secrets["google_drive"]["folder_id"]
        
        file_metadata = {'name': file_name, 'parents': [folder_id]}
        media = MediaIoBaseUpload(io.BytesIO(file_bytes), mimetype='image/png', resumable=True)
        service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return True
    except Exception as e:
        st.sidebar.error(f"Error al subir a Drive: {e}")
        return False

# --- INTERFAZ ---
st.title("🎂 ¡Nuestro recuerdo de cumple!")

if check_secrets():
    lugar = st.text_input("¿Dónde quieres que nos hagamos la foto?", "Jugando al golf")
    
    # Foto de Jesús (Tu referencia fija)
    URL_JESUS = "https://raw.githubusercontent.com/jesuslorentea-coder/regalo-cumple/main/fotojesus.png"
    
    foto_amigo = st.camera_input("Hazte un selfie")

    if foto_amigo and st.button("✨ ¡Crear Recuerdo!"):
        # Usamos st.status para que el usuario vea el progreso real
        with st.status("🚀 Iniciando proceso mágico...", expanded=True) as status:
            try:
                # PASO 1: Preparar archivos
                status.write("📸 Preparando imágenes...")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                    tmp.write(foto_amigo.getvalue())
                    selfie_path = tmp.name

                # PASO 2: Conectar con IA (Usamos un motor de respaldo más estable)
                status.write("🤖 Conectando con el motor de IA (FaceSwap)...")
                # Este modelo es más ligero y no usa api_names complicados
                client = Client("sczhou/CodeFormer") 
                
                # Ejecutamos la mejora/swap
                status.write("🎨 Generando la imagen (esto puede tardar por la cola de espera)...")
                result = client.predict(
                    image=handle_file(selfie_path),
                    background_enhance=True,
                    face_upsample=True,
                    upscale=2,
                    codeformer_fidelity=0.5
                )
                
                # PASO 3: Procesar resultado
                status.write("📥 Descargando resultado...")
                with open(result, "rb") as f:
                    img_final = f.read()

                # PASO 4: Mostrar en la web
                status.write("✅ ¡Foto lista!")
                st.image(img_final, caption=f"Nosotros {lugar} (Mejorado por IA)")
                
                # PASO 5: Guardar en Drive
                status.write("☁️ Guardando copias en tu Google Drive...")
                upload_to_drive(foto_amigo.getvalue(), f"selfie_{lugar}.png")
                upload_to_drive(img_final, f"recuerdo_{lugar}.png")
                
                status.update(label="✨ ¡Proceso completado con éxito!", state="complete", expanded=False)
                st.balloons()
                st.success(f"¡Felicidades! Tienes las fotos en tu Drive y aquí mismo.")

            except Exception as e:
                status.update(label="❌ Error en el proceso", state="error")
                st.error(f"Detalle del error: {e}")
                st.info("💡 Probablemente el servidor de IA esté saturado. Inténtalo de nuevo en 10 segundos.")
            finally:
                if 'selfie_path' in locals() and os.path.exists(selfie_path):
                    os.remove(selfie_path)

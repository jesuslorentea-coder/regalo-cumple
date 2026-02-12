import streamlit as st
import replicate
import os
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

# Configuración de API
os.environ["REPLICATE_API_TOKEN"] = "TU_TOKEN_AQUÍ"

def agregar_texto(imagen_url):
    # Descargar la imagen generada
    response = requests.get(imagen_url)
    img = Image.open(BytesIO(response.content))
    draw = ImageDraw.Draw(img)
    
    # Configurar el mensaje
    mensaje = "GRACIAS POR FELICITARME. ABRAZOS!!"
    
    # Intentar poner un texto simple en la parte inferior
    # (En una app real, podrías subir una fuente .ttf para que sea más bonita)
    width, height = img.size
    draw.text((width//10, height-100), mensaje, fill="white")
    
    return img

st.title("🎂 ¡Nuestro recuerdo de cumple!")

# Aquí va el resto del código de antes (lugar, selfie, etc.)
# ... (cuando obtengas el 'output' de Replicate) ...

# if output:
#    imagen_final = agregar_texto(output)
#    st.image(imagen_final)

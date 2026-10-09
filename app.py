import os
import streamlit as st
import base64
from openai import OpenAI

# Function to encode the image to base64
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# Streamlit page setup with centered layout
st.set_page_config(
    page_title="GalleryCritique - Curador de Arte y Diseño", 
    page_icon="🎨", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Custom CSS for an artistic, editorial, and sophisticated aesthetic (NO font changes)
st.markdown("""
    <style>
        /* Main background with a subtle artistic mesh/gradient */
        .stApp {
            background: linear-gradient(135deg, #090d16 0%, #121826 50%, #1a1025 100%);
            color: #f1f5f9;
        }
        
        /* Artistic Header Hero Card */
        .artistic-header {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(88, 28, 135, 0.25) 100%);
            padding: 2.5rem 2rem;
            border-radius: 20px;
            border: 1px solid rgba(236, 72, 153, 0.2);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
        }
        
        .artistic-header::after {
            content: "";
            position: absolute;
            top: -50px;
            right: -50px;
            width: 150px;
            height: 150px;
            background: radial-gradient(circle, rgba(236,72,153,0.15) 0%, rgba(0,0,0,0) 70%);
            border-radius: 50%;
        }

        /* Floating glassmorphism cards for sections */
        .glass-panel {
            background: rgba(18, 24, 38, 0.65);
            backdrop-filter: blur(12px);
            padding: 1.8rem;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.07);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            margin-bottom: 1.5rem;
        }
        
        /* Custom inputs styling */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            background-color: #0b0f19 !important;
            color: #f8fafc !important;
            border: 1px solid #3b4252 !important;
            border-radius: 10px !important;
            padding: 12px !important;
        }
        
        /* File uploader artistic styling */
        [data-testid="stFileUploadDropzone"] {
            background-color: rgba(11, 15, 25, 0.5) !important;
            border: 2px dashed rgba(236, 72, 153, 0.4) !important;
            border-radius: 14px !important;
        }
        
        /* Creative Gradient Button */
        .stButton > button {
            background: linear-gradient(135deg, #db2777 0%, #7c3aed 100%) !important;
            color: white !important;
            border-radius: 12px !important;
            border: none !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 600 !important;
            width: 100%;
            box-shadow: 0 4px 15px rgba(219, 39, 119, 0.3);
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            opacity: 0.9;
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
        }
        
        /* Toggle & Expander polish */
        .stExpander {
            background-color: rgba(18, 24, 38, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
        }
    </style>
""", unsafe_allow_html=True)

# Artistic Header Presentation
st.markdown("""
    <div class="artistic-header">
        <h1 style="margin: 0; font-size: 2.2rem; color: #ffffff; letter-spacing: -0.5px;">Análisis de Imagen:🤖🏞️</h1>
        <p style="margin: 8px 0 0 0; color: #cbd5e1; font-size: 1.05rem;">Plataforma de análisis visual y evaluación conceptual para piezas de diseño y obras digitales.</p>
    </div>
""", unsafe_allow_html=True)

# Credentials container (Glassmorphic panel)
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
st.markdown("#### 🔑 Credenciales de Acceso")
ke = st.text_input('Ingresa tu Clave', type="password", placeholder="sk-proj-...")
os.environ['OPENAI_API_KEY'] = ke
st.markdown('</div>', unsafe_allow_html=True)

# Retrieve the OpenAI API Key from secrets
api_key = os.environ['OPENAI_API_KEY']

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

# File uploader section inside an artistic wrapper
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
st.markdown("#### 🖼️ Repositorio de Piezas Gráficas")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    # Display the uploaded image inside an organized aesthetic wrapper
    with st.expander("👁️ Vista Previa de la Pieza", expanded = True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

# Configuration and context options panel
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
st.markdown("#### ⚙️ Parámetros de Evaluación")
show_details = st.toggle("Pregunta algo específico sobre la imagen", value=False)

if show_details:
    # Text input for additional details about the image, shown only if toggle is True
    additional_details = st.text_area(
        "Adiciona contexto de la imagen aqui:",
        disabled=not show_details,
        placeholder="Ej: Analiza la composición tipográfica, el contraste cromático y el equilibrio simétrico..."
    )
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Button to trigger the analysis
analyze_button = st.button("Analiza la imagen", type="secondary")

# Check if an image has been uploaded, if the API key is available, and if the button has been pressed
if uploaded_file is not None and api_key and analyze_button:

    with st.spinner("Analizando pieza gráfica en curso..."):
        # Encode the image
        base64_image = encode_image(uploaded_file)
    
        prompt_text = ("Describe what you see in the image in spanish")
    
        if show_details and additional_details:
            prompt_text += (
                f"\n\nAdditional Context Provided by the User:\n{additional_details}"
            )
    
        # Create the payload for the completion request - CORRECTED FORMAT
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                ],
            }
        ]
    
        # Make the request to the OpenAI API
        try:
            # Stream the response
            full_response = ""
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📋 Dictamen y Análisis Crítico:")
            
            st.markdown('<div class="glass-panel" style="border-left: 4px solid #db2777;">', unsafe_allow_html=True)
            message_placeholder = st.empty()
            
            for completion in client.chat.completions.create(
                model="gpt-4o", messages=messages,  
                max_tokens=1200, stream=True
            ):
                # Check if there is content to display
                if completion.choices[0].delta.content is not None:
                    full_response += completion.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            # Final update to placeholder after the stream ends
            message_placeholder.markdown(full_response)
            st.markdown('</div>', unsafe_allow_html=True)
    
        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    # Warnings for user action required
    if not uploaded_file and analyze_button:
        st.warning("Please upload an image.")
    if not api_key:
        st.warning("Por favor ingresa tu API key.")

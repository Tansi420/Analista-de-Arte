import os
import streamlit as st
import base64
from openai import OpenAI

# Function to encode the image to base64
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# Streamlit page setup with curated gallery layout
st.set_page_config(
    page_title="GalleryCritique - Curador de Arte y Diseño", 
    page_icon="🎨", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Custom CSS for an artistic, editorial, and gallery-like aesthetic (NO font changes)
st.markdown("""
    <style>
        /* Main background - warm editorial dark tone */
        .stApp {
            background-color: #121110;
            color: #E6E2DD;
        }
        
        /* Artistic Card Wrapper */
        .art-gallery-card {
            background-color: #1A1816;
            padding: 2.2rem;
            border-radius: 4px;
            border: 1px solid #2E2A26;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
            margin-bottom: 2rem;
            position: relative;
        }
        
        /* Subtle aesthetic banner */
        .art-header {
            border-bottom: 1px solid #2E2A26;
            padding-bottom: 1.5rem;
            margin-bottom: 2rem;
        }
        
        /* Inputs & Textareas styled like a notebook/studio tool */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            background-color: #161412 !important;
            color: #F4F1EA !important;
            border: 1px solid #38332E !important;
            border-radius: 3px !important;
            padding: 12px !important;
        }
        
        /* Artistic button styling - terracotta/gold accents */
        .stButton > button {
            background-color: #C86D51;
            color: #FFFFFF;
            border-radius: 3px;
            border: none;
            padding: 0.7rem 1.5rem;
            font-weight: 500;
            letter-spacing: 0.05em;
            width: 100%;
            transition: background 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: #B25A3F;
        }
        
        /* File uploader artistic frame */
        [data-testid="stFileUploadDropzone"] {
            background-color: #161412 !important;
            border: 1px dashed #4D453E !important;
            border-radius: 4px !important;
        }
        
        /* Expander customization */
        .streamlit-expanderHeader {
            background-color: #1A1816 !important;
            border: 1px solid #2E2A26 !important;
            border-radius: 4px !important;
        }
        
        /* Alerts */
        .stAlert {
            background-color: #1A1816 !important;
            border: 1px solid #38332E !important;
            border-radius: 4px !important;
            color: #E6E2DD !important;
        }
    </style>
""", unsafe_allow_html=True)

# App Title and presentation header (Artistic gallery layout)
st.markdown("""
    <div class="art-header">
        <h1 style="letter-spacing: -0.02em; font-weight: 400; color: #F4F1EA; margin-bottom: 0.5rem;">🎨 GalleryCritique: Diagnóstico y Curaduría Gráfica</h1>
        <p style='color: #9E968D; font-size: 1.05rem; margin: 0;'>Plataforma de análisis visual y evaluación conceptual para piezas de diseño y obras digitales.</p>
    </div>
""", unsafe_allow_html=True)

# Credentials container
with st.container():
    st.markdown("#### 🔑 Credenciales de Acceso")
    ke = st.text_input('Ingresa tu Clave', type="password", placeholder="sk-proj-...")
    os.environ['OPENAI_API_KEY'] = ke

# Retrieve the OpenAI API Key from secrets
api_key = os.environ['OPENAI_API_KEY']

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

st.markdown("<br>", unsafe_allow_html=True)

# File uploader section
st.markdown("#### 🖼️ Repositorio de Piezas Gráficas")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Display the uploaded image inside an artistic canvas wrapper
    with st.expander("👁️ Vista Previa de la Pieza", expanded = True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Configuration and context options
st.markdown("#### ⚙️ Parámetros de Evaluación")
show_details = st.toggle("Pregunta algo específico sobre la imagen", value=False)

if show_details:
    # Text input for additional details about the image, shown only if toggle is True
    additional_details = st.text_area(
        "Adiciona contexto de la imagen aqui:",
        disabled=not show_details,
        placeholder="Ej: Analiza la composición tipográfica, el contraste cromático y el equilibrio simétrico..."
    )

st.markdown("<br>", unsafe_allow_html=True)

# Button to trigger the analysis
analyze_button = st.button("Analiza la imagen", type="secondary")

# Check if an image has been uploaded, if the API key is available, and if the button has been pressed
if uploaded_file is not None and api_key and analyze_button:

    with st.spinner("Interpretando la obra y generando lectura crítica..."):
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
            
            st.markdown("<br>### 📋 Dictamen y Análisis Crítico:", unsafe_allow_html=True)
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
    
        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    # Warnings for user action required
    if not uploaded_file and analyze_button:
        st.warning("Please upload an image.")
    if not api_key:
        st.warning("Por favor ingresa tu API key.")

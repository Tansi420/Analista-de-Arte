import os
import streamlit as st
import base64
from openai import OpenAI

# Function to encode the image to base64
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# Streamlit page setup with centered artistic layout
st.set_page_config(
    page_title="Atelier Visual | Curaduría y Análisis", 
    page_icon="🎨", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Custom CSS for an artistic, gallery-style aesthetic (NO font changes)
st.markdown("""
    <style>
        /* Main dark artistic canvas background */
        .stApp {
            background-color: #0c0a09;
            color: #f5f5f4;
        }
        
        /* Artistic Header Banner */
        .art-header {
            background: linear-gradient(145deg, #1c1917 0%, #0c0a09 100%);
            padding: 2.5rem 2rem;
            border-radius: 16px;
            border: 1px solid rgba(245, 245, 244, 0.08);
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 20px 40px -15px rgba(0,0,0,0.7);
        }
        
        /* Gallery Card Container */
        .gallery-card {
            background: rgba(28, 25, 23, 0.6);
            backdrop-filter: blur(12px);
            padding: 1.8rem;
            border-radius: 14px;
            border: 1px solid rgba(245, 245, 244, 0.06);
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
            margin-bottom: 1.5rem;
        }
        
        /* Inputs & Textareas artistic refinement */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            background-color: #1c1917 !important;
            color: #f5f5f4 !important;
            border: 1px solid #44403c !important;
            border-radius: 8px !important;
        }
        
        .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
            border-color: #d97706 !important;
            box-shadow: 0 0 0 1px #d97706 !important;
        }
        
        /* Artistic button styling */
        .stButton > button {
            background: linear-gradient(135deg, #b45309 0%, #78350f 100%);
            color: #ffffff;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.1);
            padding: 0.6rem 1.2rem;
            font-weight: 500;
            width: 100%;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
            border-color: rgba(255,255,255,0.2);
        }
        
        /* File uploader artistic styling */
        [data-testid="stFileUploadDropzone"] {
            background-color: rgba(28, 25, 23, 0.4) !important;
            border: 2px dashed #57534e !important;
            border-radius: 12px !important;
        }
        
        /* Alerts styling */
        .stAlert {
            background-color: #1c1917 !important;
            color: #f5f5f4 !important;
            border: 1px solid #44403c !important;
            border-radius: 10px !important;
        }
    </style>
""", unsafe_allow_html=True)

# Artistic Page Header
st.markdown("""
    <div class="art-header">
        <h1 style="margin: 0; font-weight: 400; letter-spacing: 1px; color: #fafaf9;">ATELIER VISUAL 👁️✨</h1>
        <p style="margin: 10px 0 0 0; color: #a8a29e; font-size: 1rem; letter-spacing: 0.5px;">Espacio experimental de crítica, deconstrucción y análisis estético de obra gráfica.</p>
    </div>
""", unsafe_allow_html=True)

# Credentials container (Artistic style)
with st.container():
    st.markdown("##### 🔑 Llave de Acceso al Salón")
    ke = st.text_input('Ingresa tu Clave', type="password", placeholder="Inserta credencial de OpenAI...")
    os.environ['OPENAI_API_KEY'] = ke

# Retrieve the OpenAI API Key from secrets
api_key = os.environ['OPENAI_API_KEY']

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

st.markdown("---")

# File uploader section
st.markdown("##### 🖼️ Bastidor de Carga (Objeto Visual)")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Display the uploaded image inside an artistic frame container
    with st.expander("👁️ Exposición de la Pieza", expanded = True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

st.markdown("---")

# Configuration and context options
st.markdown("##### ✍️ Criterios Curatoriales")
show_details = st.toggle("Pregunta algo específico sobre la imagen", value=False)

if show_details:
    # Text input for additional details about the image, shown only if toggle is True
    additional_details = st.text_area(
        "Adiciona contexto de la imagen aqui:",
        disabled=not show_details,
        placeholder="Ej: Reflexiona sobre la paleta cromática, el ritmo visual y la atmósfera emocional de esta pieza..."
    )

st.markdown("<br>", unsafe_allow_html=True)

# Button to trigger the analysis
analyze_button = st.button("Analiza la imagen", type="secondary")

# Check if an image has been uploaded, if the API key is available, and if the button has been pressed
if uploaded_file is not None and api_key and analyze_button:

    with st.spinner("Contemplando y analizando la obra..."):
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
            
            st.markdown("##### 📜 Memoria Crítica y Lectura Estética:")
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

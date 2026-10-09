import os
import streamlit as st
import base64
from openai import OpenAI

# Function to encode the image to base64
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# Streamlit page setup with wide layout for better visual cards
st.set_page_config(
    page_title="GalleryCritique - Curador de Arte y Diseño", 
    page_icon="🎨", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Custom CSS for aesthetics (organization, cards, color palette - NO font changes)
st.markdown("""
    <style>
        /* Main background & container styling */
        .stApp {
            background-color: #0F172A;
            color: #F8FAFC;
        }
        
        /* Card container wrapper */
        .art-card {
            background-color: #1E293B;
            padding: 1.8rem;
            border-radius: 14px;
            border: 1px solid #334155;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
            margin-bottom: 1.5rem;
        }
        
        /* Inputs & Textareas enhancement */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            background-color: #0F172A !important;
            color: #F8FAFC !important;
            border: 1px solid #475569 !important;
            border-radius: 8px !important;
        }
        
        /* Primary button styling */
        .stButton > button {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            width: 100%;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        }
        
        /* Alerts & Warnings */
        .stAlert {
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# App Title and presentation header
st.title("🎨 GalleryCritique: Diagnóstico y Curaduría Gráfica")
st.markdown("<p style='color: #94a3b8; margin-bottom: 2rem;'>Plataforma de análisis visual y evaluación conceptual para piezas de diseño y obras digitales.</p>", unsafe_allow_html=True)

# Credentials container
with st.container():
    st.markdown("#### 🔑 Credenciales de Acceso")
    ke = st.text_input('Ingresa tu Clave', type="password", placeholder="sk-proj-...")
    os.environ['OPENAI_API_KEY'] = ke

# Retrieve the OpenAI API Key from secrets
api_key = os.environ['OPENAI_API_KEY']

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

st.markdown("---")

# File uploader section
st.markdown("#### 🖼️ Repositorio de Piezas Gráficas")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Display the uploaded image inside an organized aesthetic wrapper
    with st.expander("👁️ Vista Previa de la Pieza", expanded = True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

st.markdown("---")

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
            
            st.markdown("### 📋 Dictamen y Análisis Crítico:")
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

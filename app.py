import streamlit as st
import google.generativeai as genai

# 🌟 CONFIGURACIÓN ESTÉNTICA DE ALTA GAMA
st.set_page_config(
    page_title="Heaven App", 
    page_icon="🕊️", 
    layout="centered"
)

# 🎨 INYECCIÓN DE DISEÑO PERSONALIZADO (CSS)
st.markdown("""
    <style>
    /* Cambiar el fondo general a un tono oscuro profundo y elegante */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    
    /* Estilizar las tarjetas de información superiores */
    .stAlert {
        border-radius: 16px !important;
        border: 1px solid #334155 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Separador estético */
    hr {
        border-top: 1px solid #334155 !important;
    }
    
    /* Estilizar la barra de entrada de texto inferior */
    .stChatInputContainer {
        border-radius: 24px !important;
        border: 1px solid #334155 !important;
        background-color: #1E293B !important;
    }
    
    /* Ajustes en los títulos */
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado Minimalista y Moderno
st.markdown("<h1 style='text-align: center; color: #38BDF8; margin-bottom: 0;'>🕊️ Heaven App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 1.1rem; margin-top: 5px;'>Consejería Espiritual & Reflexión Profunda</p>", unsafe_allow_html=True)
st.markdown("---")

# 📌 TARJETAS DE BIENVENIDA ESTILIZADAS
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div style='background-color: #1E293B; padding: 20px; border-radius: 16px; border: 1px solid #334155; height: 100%;'>
            <h4 style='color: #38BDF8; margin-top:0;'>📖 Base Teológica</h4>
            <p style='color: #94A3B8; font-size: 0.95rem; margin-bottom:0;'>Respuestas guiadas bajo el rigor y la belleza de la <b>Reina Valera 1960</b>.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div style='background-color: #1E293B; padding: 20px; border-radius: 16px; border: 1px solid #334155; height: 100%;'>
            <h4 style='color: #34D399; margin-top:0;'>🧠 Memoria Activa</h4>
            <p style='color: #94A3B8; font-size: 0.95rem; margin-bottom:0;'>Nuestra conversación fluye manteniendo el hilo de cada detalle que compartas.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

st.write("") # Espacio estético

# Conectar con la API de Gemini de forma segura
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
else:
    st.error("⚠️ Por favor, configura tu GEMINI_KEY en los secretos de Streamlit.")
    st.stop()

# Instrucciones estrictas de comportamiento
PROMPT_SISTEMA = (
    "Eres un consejero espiritual, teológico y filosófico altamente empático, paciente y sabio. "
    "Tu objetivo es escuchar los problemas de los usuarios (como crisis de pareja, ansiedad o dudas) "
    "y responder de forma fluida, analítica y profundamente reflexiva. "
    "REGLA OBLIGATORIA: Todas las citas bíblicas, referencias, versículos, historias o principios "
    "que menciones deben basarse ÚNICA Y EXCLUSIVAMENTE en la traducción Reina Valera 1960 (RVR1960). "
    "Está terminantemente prohibido usar otras versiones como la NVI, DHH, TLA o cualquier otra. "
    "Cuando cites un texto, añade al final de la cita '(RVR1960)' para dar certeza al usuario. "
    "Entrelaza estas citas de forma natural para iluminar el problema del usuario, sin sonar rígido o acusador. "
    "Mantén un tono de diálogo cercano, recuerda los detalles de la conversación y cierra con preguntas abiertas."
)

# Inicializar modelo
@st.cache_resource
def iniciar_modelo():
    return genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=PROMPT_SISTEMA
    )

model = iniciar_modelo()

# Historial de conversación
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Mostrar mensajes previos con burbujas y avatares finos
for message in st.session_state.chat_session.history:
    if message.role == "model":
        with st.chat_message("assistant", avatar="🕊️"):
            st.markdown(f"<div style='background-color: #1E293B; padding: 12px 16px; border-radius: 14px; color: #E2E8F0;'>{message.parts[0].text}</div>", unsafe_allow_html=True)
    else:
        with st.chat_message("user", avatar="👤"):
            st.markdown(f"<div style='background-color: #0284C7; padding: 12px 16px; border-radius: 14px; color: #FFFFFF;'>{message.parts[0].text}</div>", unsafe_allow_html=True)

# Entrada de texto del usuario
if pregunta_usuario := st.chat_input("Escribe tu dilema o reflexión aquí..."):
    with st.chat_message("user", avatar="👤"):
        st.markdown(f"<div style='background-color: #0284C7; padding: 12px 16px; border-radius: 14px; color: #FFFFFF;'>{pregunta_usuario}</div>", unsafe_allow_html=True)
    
    with st.chat_message("assistant", avatar="🕊️"):
        with st.spinner("Reflexionando bajo la RVR1960..."):
            response = st.session_state.chat_session.send_message(pregunta_usuario)
            st.markdown(f"<div style='background-color: #1E293B; padding: 12px 16px; border-radius: 14px; color: #E2E8F0;'>{response.text}</div>", unsafe_allow_html=True)

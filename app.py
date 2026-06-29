import streamlit as st
import google.generativeai as genai

# 🌟 CONFIGURACIÓN ESTÉTICA PREMIUM
st.set_page_config(
    page_title="Heaven App", 
    page_icon="🕊️", 
    layout="centered"
)

# Aplicar un toque de estilo con Markdown para centrar y embellecer el encabezado
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🕊️ Heaven App</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #7F8C8D;'>Tu Asistente de Consejería y Reflexión</h3>", unsafe_allow_html=True)
st.markdown("---")

# 📌 PANEL DE BIENVENIDA (Tarjetas de presentación)
# Usamos columnas para que se vea ordenado y elegante
col1, col2 = st.columns(2)

with col1:
    st.info(
        "### 📖 Base Teológica\n"
        "Respuestas guiadas **única y exclusivamente** bajo la traducción de la **Reina Valera 1960**."
    )

with col2:
    st.success(
        "### 🧠 Memoria Activa\n"
        "Esta IA analiza tus dilemas a fondo y **recuerda todo el hilo** de nuestra conversación."
    )

st.write("") # Espacio en blanco estético

# Conectar con el cerebro de Google usando tu API Key de forma segura
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
else:
    st.error("⚠️ Por favor, configura tu GEMINI_KEY en los secretos de Streamlit.")
    st.stop()

# Instrucciones de personalidad para la IA (System Instructions)
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

# Inicializar el modelo inteligente con su rol definido
@st.cache_resource
def iniciar_modelo():
    return genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=PROMPT_SISTEMA
    )

model = iniciar_modelo()

# Inicializar el historial de conversación en la memoria de la página
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 💬 CONTENEDOR DEL CHAT ESTILIZADO
# Mostrar los mensajes anteriores en la pantalla con avatares personalizados
for message in st.session_state.chat_session.history:
    if message.role == "model":
        role = "assistant"
        avatar = "🕊️"  # Icono para la IA
    else:
        role = "user"
        avatar = "👤"  # Icono para el usuario
        
    with st.chat_message(role, avatar=avatar):
        st.markdown(message.parts[0].text)

# Capturar la entrada del usuario
if pregunta_usuario := st.chat_input("Escribe tu dilema o reflexión aquí..."):
    # Mostrar el mensaje del usuario
    with st.chat_message("user", avatar="👤"):
        st.markdown(pregunta_usuario)
    
    # Enviar el mensaje al cerebro de Gemini con indicador de carga elegante
    with st.chat_message("assistant", avatar="🕊️"):
        with st.spinner("Reflexionando profundamente bajo la RVR1960..."):
            response = st.session_state.chat_session.send_message(pregunta_usuario)
            st.markdown(response.text)

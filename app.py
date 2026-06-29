import streamlit as st
import google.generativeai as genai

# Configuración estética de la app
st.set_page_config(page_title="Heaven App", page_icon="🤖", layout="centered")
st.title("🤖 Heaven App")
st.subheader("Tu Asistente de Consejería y Reflexión")
st.caption("Una IA real con memoria para conversar profundamente sobre tus dilemas y reflexiones.")

# Conectar con el cerebro de Google usando tu API Key de forma segura
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
else:
    st.error("Por favor, configura tu GEMINI_KEY en los secretos de Streamlit.")
    st.stop()

# Instrucciones de personalidad para la IA
PROMPT_SISTEMA = (
    "Eres un consejero espiritual, teológico y filosófico altamente empático, paciente y sabio. "
    "Tu objetivo es escuchar los problemas de los usuarios (como crisis de pareja, ansiedad o dudas) "
    "y responder de forma fluida, analítica y profundamente reflexiva. "
    "Siempre debes entrelazar de forma natural principios, historias o citas bíblicas relevantes "
    "para iluminar el problema del usuario, pero sin sonar rígido o acusador. "
    "Mantén un tono de diálogo cercano, recuerda los detalles que el usuario te cuenta a lo largo "
    "de la conversación y cierra tus respuestas con preguntas abiertas que lo inviten a profundizar."
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

# Mostrar los mensajes anteriores en la pantalla
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Capturar la entrada del usuario
if pregunta_usuario := st.chat_input("Escribe tu mensaje o problema aquí..."):
    # Mostrar el mensaje del usuario en la pantalla
    with st.chat_message("user"):
        st.markdown(pregunta_usuario)
    
    # Enviar el mensaje al cerebro de Gemini y esperar la respuesta razonada
    with st.chat_message("assistant"):
        with st.spinner("Pensando profundamente..."):
            response = st.session_state.chat_session.send_message(pregunta_usuario)
            st.markdown(response.text)

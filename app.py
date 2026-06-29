%%writefile app.py
import urllib.request
import json
import re
import streamlit as st

# Configuración estética de la aplicación
st.set_page_config(page_title="Heaven App", page_icon="🤖", layout="centered")
st.title("🤖 Heaven App")
st.subheader("Tu Asistente de Reflexión y Consejería")
st.caption("Conversa libremente sobre tus dudas, problemas o pasajes bíblicos.")

# Base de datos conceptual interna de la IA para consultas abiertas
CONOCIMIENTO_TEMATICO = {
    "comunicacion": "(Santiago 1:19 & Efesios 4:26) Todo hombre sea pronto para oír, tardo para hablar, tardo para airarse. No se ponga el sol sobre vuestro enojo, ni deis lugar al diablo. Hablad verdad cada uno con su prójimo.",
    "pareja": "(1 Corintios 13:4-7) El amor es sufrido, es benigno; el amor no tiene envidia... Todo lo sufre, todo lo cree, todo lo espera, todo lo soporta. El amor nunca deja de ser.",
    "amor": "(1 Corintios 13:4-5) El amor es paciente y muestra bondad. El amor no es celoso, no se jacta, no es orgulloso, no actúa indebidamente ni busca sus propios intereses.",
    "ansiedad": "(Filipenses 4:6) Por nada estéis afanosos, sino sean conocidas vuestras peticiones delante de Dios en toda oración y ruego, con acción de gracias.",
    "tristeza": "(Salmo 34:18) Cercano está Jehová a los quebrantados de corazón; y salva a los contritos de espíritu."
}

def consultar_api_biblia(libro, capitulo, versiculo=None):
    libro_url = libro.lower().replace(" ", "")
    url = f"https://bible-api.com/{libro_url}+{capitulo}?translation=rvr1960"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            datos = json.loads(response.read().decode('utf-8'))
            if versiculo:
                for v in datos.get('verses', []):
                    if v.get('verse') == int(versiculo):
                        return f"({libro} {capitulo}:{versiculo}) {v.get('text').strip()}"
            return " ".join([v.get('text').strip() for v in datos.get('verses', [])[:3]])
    except:
        return None

# Manejo de memoria del chat para sostener la conversación
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hola. Soy tu asistente de reflexión. Estoy aquí para escucharte, conversar contigo y buscar guía en las escrituras. ¿Qué tienes en mente hoy?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Captura del mensaje enviado por el usuario
if pregunta_usuario := st.chat_input("Escribe tu mensaje o problema aquí..."):
    with st.chat_message("user"):
        st.markdown(pregunta_usuario)
    st.session_state.messages.append({"role": "user", "content": pregunta_usuario})

    # Analizar si contiene una cita bíblica directa
    patron = r"([1-3]?\s?[A-Za-záéíóúÁÉÍÓÚñÑ]+)\s?(\d+)(?::(\d+))?"
    coincidencia = re.search(patron, pregunta_usuario)
    
    contexto = None
    tema_detectado = None
    
    if coincidencia and any(libro in pregunta_usuario.lower() for libro in ["genesis", "exodo", "mateo", "juan", "salmo", "lucas", "marcos", "romanos", "corintios", "efesios", "filipenses", "santiago"]):
        contexto = consultar_api_biblia(coincidencia.group(1).strip(), coincidencia.group(2), coincidencia.group(3) if coincidencia.group(3) else None)
    else:
        # Analizar palabras clave emocionales
        texto_limpio = pregunta_usuario.lower()
        for clave, pasaje in CONOCIMIENTO_TEMATICO.items():
            if clave in texto_limpio:
                contexto = pasaje
                tema_detectado = clave
                break

    # Generar respuesta de consejería fluida
    with st.chat_message("assistant"):
        if contexto and tema_detectado:
            respuesta = (
                f"Lamento mucho escuchar que estás pasando por esta situación. La falta de **{tema_detectado}** en una relación "
                f"puede generar mucha distancia y dolor, pero reconocer el problema es el primer gran paso.\n\n"
                f"Desde una perspectiva de sabiduría y reflexión, las escrituras nos ofrecen un principio muy valioso para estos momentos:\n\n"
                f"*\"{contexto}\"*\n\n"
                f"Este consejo nos invita a analizar cómo nos acercamos al otro: a veces, restaurar la relación empieza por estar "
                f"completamente dispuestos a escuchar con paciencia, bajando las defensas y buscando un momento de paz para hablar con honestidad.\n\n"
                f"¿Sientes que el obstáculo principal para hablar es el temor a discutir, o simplemente el distanciamiento mutuo?"
            )
        elif contexto:
            respuesta = f"He encontrado el pasaje que mencionas para guiar nuestro diálogo:\n\n*\"{contexto}\"*\n\n¿Qué reflexión te genera este texto en tu vida actual?"
        else:
            respuesta = (
                f"Agradezco mucho que compartas esto conmigo. Te escucho atentamente. Aunque no detecté una palabra clave específica "
                f"en mi base de datos para darte una cita textual exacta en este segundo, quiero decirte que mantener la calma y buscar espacios de "
                f"diálogo constructivo siempre es el camino correcto. Cuéntame un poco más, ¿qué crees que inició este silencio en tu entorno?"
            )
        st.markdown(respuesta)
    st.session_state.messages.append({"role": "assistant", "content": respuesta})

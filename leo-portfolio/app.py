import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import plotly.express as px
import pandas as pd
import os
from groq import Groq
from PIL import Image, ImageDraw

# --- Page Configuration ---
st.set_page_config(
    page_title="Leonardo Nieto | AI Engineer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom Styling (Modern Bento Layout) ---
st.markdown(
    """
    <style>
    /* Modern Reset & Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Background */
    .stApp {
        background-color: #050505; /* Deepest Black/Grey */
        background-image: radial-gradient(circle at top right, #1a1a2e, #050505 40%);
        color: #e0e0e0;
    }
    
    /* Headers - Clean & Bold */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    
    h1 {
        background: linear-gradient(90deg, #6c5ce7, #a29bfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        padding-bottom: 0.2rem;
    }
    
    /* Bento Grid Card Style */
    .css-card {
        background-color: #111111;
        border: 1px solid #222;
        border-radius: 16px;
        padding: 30px;
        transition: transform 0.2s, border-color 0.2s;
        height: 100%;
    }
    
    .css-card:hover {
        border-color: #6c5ce7;
        transform: translateY(-2px);
    }
    
    .css-card h3, .css-card h4 {
        margin-top: 0;
        color: #fff !important;
    }
    
    /* Sidebar - Minimalist & Fixed */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 1px solid #222;
    }
    
    /* RESPONSIBLE LAYOUT CONTROL */
    /* Desktop (PC > 992px): Fixed Left Sidebar Logic */
    @media (min-width: 992px) {
        /* We DO NOT hide the 'CollapsedControl' (Open Button). 
           If the sidebar accidentally closes (resize from mobile), we need this button to reopen it.
           Once open, the 'Close Button' below is hidden, making it 'Fixed'. 
        */
        
        /* Hide the "Close Sidebar" button inside the sidebar to force it fixed */
        section[data-testid="stSidebar"] > div > div:first-child button {
            display: none !important;
        }
    }
    
    /* Mobile & Tablet (< 992px): Shows "MENU" Button */
    @media (max-width: 991px) {
        /* Container acts as position anchor */
        [data-testid="stSidebarCollapsedControl"] {
            display: block !important;
            margin: 10px;
            width: auto !important;
            z-index: 100;
        }
        
        /* The actual clickable button gets the style */
        [data-testid="stSidebarCollapsedControl"] button {
            display: flex !important;
            align-items: center;
            justify-content: center;
            background-color: #6c5ce7 !important; /* Purple Brand Color */
            color: white !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            border: 1px solid #7d6df0 !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
            width: auto !important;
            height: auto !important;
            transition: transform 0.1s;
        }
        
        [data-testid="stSidebarCollapsedControl"] button:active {
            transform: scale(0.95);
        }
        
        /* Add text label "MENÚ" inside the button */
        [data-testid="stSidebarCollapsedControl"] button::after {
            content: "MENÚ";
            font-family: 'Inter', sans-serif;
            font-weight: 800;
            font-size: 14px;
            margin-left: 8px;
            color: white;
            letter-spacing: 1px;
        }
        
        /* Icon Styling */
        [data-testid="stSidebarCollapsedControl"] button svg {
            fill: white !important;
            width: 20px !important;
            height: 20px !important;
        }
    }
    
    /* Buttons - Solid & Rounded */
    .stButton > button {
        background-color: #6c5ce7;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: background 0.2s;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #5b4cc4;
        color: white;
        box-shadow: 0 4px 12px rgba(108, 92, 231, 0.3);
    }
    
    /* Expander - Clean */
    .streamlit-expanderHeader {
        background-color: #111;
        border: 1px solid #222;
        border-radius: 8px;
        color: #e0e0e0;
    }
    
    /* inputs */
    .stTextInput > div > div, .stTextArea > div > div {
        background-color: #111;
        border-color: #333;
        color: white;
        border-radius: 8px;
    }
    
    /* Chart Container match */
    div[data-testid="metric-container"] {
        background-color: #111;
        border: 1px solid #222;
        border-radius: 12px;
        padding: 20px;
    }

    /* Navigation Adjustment */
    iframe {
        margin-top: 2rem;
    }

    /* Hide default elements */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Sidebar Navigation ---
with st.sidebar:
    st.image("https://api.dicebear.com/7.x/shapes/svg?seed=Leo&backgroundColor=6c5ce7", width=80) 
    st.markdown("""
        <div style="margin-top: 20px; margin-bottom: 40px;">
            <h2 style="font-size: 24px; margin: 0; padding: 0;">Leonardo Nieto</h2>
            <p style="color: #888; font-size: 14px; margin-top: 5px;">AI Solutions Engineer</p>
        </div>
    """, unsafe_allow_html=True)
    
    selected_page = option_menu(
        menu_title=None, # Clean look
        options=["Inicio", "Chatbot IA", "Visión Artificial", "Analytics", "Contacto"],
        icons=["grid", "chat-square-text", "eye", "graph-up", "envelope"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#6c5ce7", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "10px 0",
                "color": "#888",
                "background-color": "transparent"
            },
            "nav-link-selected": {
                "background-color": "#111", 
                "color": "#fff", 
                "border-left": "4px solid #6c5ce7",
                "border-radius": "0 8px 8px 0"
            },
        },
    )
    
    st.markdown("<div style='margin-top: 50px; color: #444; font-size: 12px;'>v2.4.0 • System Online</div>", unsafe_allow_html=True)

    # --- MOBILE UX: Auto-Close Sidebar on Selection ---
    # This JavaScript checks if we are on mobile/tablet (< 992px) and programmatically 
    # clicks the "Close Sidebar" button to mimic native app navigation behavior.
    # --- MOBILE UX: Auto-Close Sidebar on Selection ---
    # JavaScript injected via components.html ensures execution on every re-run
    # This targets Mobile (< 992px) and clicks the sidebar Close button automatically.
    components.html("""
    <script>
        const closeSidebar = () => {
            // CRITICAL FIX: Use window.parent.matchMedia because this runs in an iframe
            const mediaQuery = window.parent.matchMedia('(max-width: 991px)');
            if (mediaQuery.matches) {
                const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
                if (sidebar) {
                    const button = sidebar.querySelector('button');
                    if (button) {
                        button.click();
                    }
                }
            }
        }
        // Execute after a short delay to allow UI to settle
        setTimeout(closeSidebar, 350);
    </script>
    """, height=0, width=0)

# --- Page: HOME (About Me) ---
# --- Page: HOME (About Me) ---
def show_home():
    # Hero Section - Clean & Bold
    st.markdown("<h1 style='font-size: 3.5em; margin-bottom: 0.2em;'>Ingeniería de IA Aplicada</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: #888; margin-bottom: 2rem;'>Soluciones de Inteligencia Artificial para el mundo real.</h4>", unsafe_allow_html=True)
    
    # Bento Grid Row 1: Mission & Stack
    col1, col2 = st.columns([1.5, 1], gap="medium")
    
    with col1:
        st.markdown("""
        <div class="css-card">
            <h3>Sobre el Portafolio</h3>
            <p style="color: #ccc; line-height: 1.6;">
                Este sitio es una <strong>Proof of Concept (PoC)</strong> interactiva. 
                Interactúa con agentes de IA reales, sistemas de visión artificial y tableros predictivos 
                conectados a modelos LLM.
            </p>
            <p style="color: #ccc; margin-top: 15px;">
                <strong>Misión:</strong> Automatizar procesos complejos con tecnología de vanguardia.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="css-card">
            <h3>Stack Tecnológico</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 15px;">
                <span style="background:#222; padding: 6px 12px; border-radius: 6px; border: 1px solid #333; font-size: 13px; color: #fff;">Python 3.12</span>
                <span style="background:#222; padding: 6px 12px; border-radius: 6px; border: 1px solid #333; font-size: 13px; color: #fff;">Groq API</span>
                <span style="background:#222; padding: 6px 12px; border-radius: 6px; border: 1px solid #333; font-size: 13px; color: #fff;">Llama 3</span>
                <span style="background:#222; padding: 6px 12px; border-radius: 6px; border: 1px solid #333; font-size: 13px; color: #fff;">Streamlit</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    
    # Bento Grid Row 2: Services
    st.markdown("### Áreas de Especialización")
    s1, s2, s3 = st.columns(3, gap="medium")
    
    with s1:
        st.markdown("""
        <div class="css-card">
            <h4 style="color: #6c5ce7 !important;">Asistentes RAG</h4>
            <p style="font-size: 14px; color: #888;">
                Chatbots corporativos que responden consultas usando tus propios PDF y bases de datos.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with s2:
        st.markdown("""
        <div class="css-card">
            <h4 style="color: #6c5ce7 !important;">Computer Vision</h4>
            <p style="font-size: 14px; color: #888;">
                Detección automática de defectos y control de calidad 24/7 en líneas de producción.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with s3:
        st.markdown("""
        <div class="css-card">
            <h4 style="color: #6c5ce7 !important;">Predicción de Datos</h4>
            <p style="font-size: 14px; color: #888;">
                Modelos de ML que analizan tendencias históricas para optimizar inventarios.
            </p>
        </div>
        """, unsafe_allow_html=True)

# --- Page: AI CHAT SOLUTIONS ---
def show_chat():
    st.title("Asistente Corporativo (RAG Demo)")
    st.markdown("#### Consultas sobre Recursos Humanos e Inventario")
    
    # Context / Explanation Expander
    # Context / Explanation Expander
    with st.expander("¿Cómo funciona este módulo? (Detalles Técnicos)", expanded=True):
        st.markdown("""
        **Tecnología Subyacente:**
        Este chat utiliza **Llama 3.3 (70B)** alojado en **Groq** para una latencia mínima.
        
        **Arquitectura Simulada (RAG - Retrieval Augmented Generation):**
        1.  **Input:** El usuario hace una pregunta (ej. "¿Cuántas vacaciones tengo?").
        2.  **Retrieval (Simulado):** El sistema buscaría en una base de datos vectorial documentos relevantes (políticas de RH, tablas de inventario).
        3.  **Augmentation:** Se inyecta esa información en el "prompt" del modelo.
        4.  **Generación:** Llama 3 genera una respuesta natural y precisa basada *solo* en los datos de la empresa.
        
        **Capacidades del Bot:** En esta demo, el bot tiene "instrucciones de sistema" para actuar como un experto en Inventarios y RH.
        """)
    
    st.divider()

    col_chat, col_info = st.columns([3, 1])
    
    with col_info:
        st.info("**Prueba preguntar:**")
        st.markdown("- *'¿Cuál es el stock de material Pino?'*")
        st.markdown("- *'¿Cuántos días de vacaciones me tocan?'*")
        st.markdown("- *'Necesito un resumen del inventario.'*")
        
        api_key = st.secrets.get("GROQ_API_KEY")
        if api_key:
            st.success("✅ **Groq API Conectada**\n\nModelo: `llama-3.3-70b`")
        else:
            st.warning("⚠️ **Modo Demo (Sin API Key)**\n\nRespuestas simuladas.")

    with col_chat:
        # Initialize Messages
        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": "Hola. Soy el asistente IA de Leonardo. Tengo acceso a los datos de RH e Inventarios. ¿En qué te ayudo?"}
            ]

        # Display Chat
        for msg in st.session_state.messages:
            avatar = "🤖" if msg["role"] == "assistant" else "👤"
            with st.chat_message(msg["role"], avatar=avatar):
                st.write(msg["content"])

        # Chat Logic
        if prompt := st.chat_input("Escribe tu mensaje aquí..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user", avatar="👤").write(prompt)
            
            response_text = ""
            
            # Logic
            api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
            
            if api_key:
                try:
                    client = Groq(api_key=api_key)
                    # System prompt to define behavior
                    system_prompt = {
                        "role": "system",
                        "content": "Eres un asistente corporativo experto en dos áreas: Inventarios y RH. \nDatos de Inventario: Pino (500u), Roble (200u), Cedro (150u). \nDatos de RH: Política de vacaciones es 12 días al año. Bonos se pagan trimestralmente. \nResponde de forma profesional, concisa y amable."
                    }
                    
                    messages_for_api = [system_prompt] + [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ]
                    
                    chat_completion = client.chat.completions.create(
                        messages=messages_for_api,
                        model="llama-3.3-70b-versatile",
                        temperature=0.5,
                        max_tokens=500,
                    )
                    response_text = chat_completion.choices[0].message.content
                except Exception as e:
                    response_text = f"❌ Error de conexión: {str(e)}"
            else:
                # Fallback Simulation
                prompt_lower = prompt.lower()
                response_text = "⚠️ **Respuesta Simulada (Falta API Key):**\n\n"
                if "inventario" in prompt_lower or "stock" in prompt_lower or "pino" in prompt_lower:
                    response_text += "Según la base de datos de Almacén: \n- **Pino**: 500 unidades \n- **Roble**: 200 unidades."
                elif "rh" in prompt_lower or "vacaciones" in prompt_lower:
                    response_text += "Según la política vigente de RH, te corresponden **12 días de vacaciones** por año trabajado."
                else:
                    response_text += "Lo siento, en modo demo solo puedo responder sobre Inventarios o RH específicos."
                
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            st.chat_message("assistant", avatar="🤖").write(response_text)

# --- Page: COMPUTER VISION ---
def show_vision():
    st.title("Visión por Computadora Industrial")
    st.markdown("#### Automatización de Calidad y Diseño")

    with st.expander("Detalles Técnicos y Propósito de la Demo", expanded=True):
        st.markdown("""
        **¿Qué simula este módulo?**
        Esta es una demostración conceptual del flujo de trabajo de un sistema de **Inspección de Calidad (QA)** industrial. En un entorno de producción real, este proceso ocurre en milisegundos para filtrar piezas defectuosas automáticamente.
        
        **Stack Tecnológico (Implementación Real):**
        *   **Algoritmos:** Detección de objetos con redes neuronales convolucionales (**YOLOv8**, **Faster R-CNN**) o librerías de visión clásica (**OpenCV**).
        *   **Hardware:** Cámaras industriales de alta velocidad + GPUs (NVIDIA Tesla/Jetson) en el borde (Edge Computing) para inferencia sin latencia.
        *   **Beneficio de Negocio:** Elimina el error humano, permite operación 24/7 y reduce costos por devoluciones de productos defectuosos.
        
        **⚠️ Nota sobre esta Demo:**
        *Por limitaciones de un entorno web ligero, esta página no ejecuta un modelo de PyTorch/TensorFlow pesado en tiempo real. En su lugar, ilustra la **experiencia de usuario** y la **lógica de decisión** (Aprobar/Rechazar) que implementaríamos en una solución de fábrica real.*
        """)

    tabs = st.tabs(["Detección de Defectos (Demo QC)", "Generación de Variaciones (Demo Diseño)"])
    
    with tabs[0]:
        st.subheader("Control de Calidad Automatizado")
        st.info("Simulación: Sube una foto de un producto. El sistema 'escaneará' buscando anomalías.")
        
        # Simulation Controls for Demo
        st.markdown("##### Controles de Simulación (Demo)")
        sim_mode = st.radio("Resultado Esperado:", ["Aleatorio", "Forzar Defecto (Fallo)", "Forzar Aprobado (OK)"], horizontal=True)
        
        uploaded_file = st.file_uploader("Sube imagen de producto para inspección", type=["jpg", "png", "jpeg"], key="vision_upload")
        
        if uploaded_file:
            col_orig, col_proc = st.columns(2)
            image = Image.open(uploaded_file)
            
            with col_orig:
                st.image(image, caption="Imagen de Entrada (Cámara de Línea)", use_container_width=True)
            
            with col_proc:
                if st.button("Ejecutar Inspección IA"):
                    with st.spinner("Analizando geometría y textura..."):
                        import random
                        # Determine outcome based on selection
                        if sim_mode == "Forzar Defecto (Fallo)":
                            has_defect = True
                        elif sim_mode == "Forzar Aprobado (OK)":
                            has_defect = False
                        else:
                            has_defect = random.choice([True, False])
                        
                        img_draw = image.copy()
                        draw = ImageDraw.Draw(img_draw)
                        w, h = img_draw.size
                        
                        if has_defect:
                            # Draw bounding box simulating detection
                            draw.rectangle([w*0.4, h*0.4, w*0.6, h*0.6], outline="#ff0000", width=8)
                            st.image(img_draw, caption="Fallo Detectado [Confianza: 98.4%]", use_container_width=True)
                            st.error("❌ ALERTA: Defecto crítico en zona central. Pieza rechazada.")
                        else:
                            # Draw green border indicating Pass
                            draw.rectangle([0, 0, w, h], outline="#00ff00", width=15)
                            st.image(img_draw, caption="Análisis Completado [Confianza: 99.1%]", use_container_width=True)
                            st.success("✅ CALIDAD APROBADA. Pieza lista para envío.")
                        
    with tabs[1]:
        st.subheader("Prototipado Rápido con IA")
        st.info("Simulación: Visualiza cómo quedaría un producto con otro material sin fabricarlo.")
        
        if st.button("Generar Variante (Madera Oscura)"):
            st.warning("⚠️ Nota: Esta función requiere conectar Stable Diffusion API. (Placeholder visual)") 
            # Placeholder for visual feedback
            st.markdown("*[Aquí aparecería la imagen generada por IA con el nuevo estilo]*")

# --- Page: DATA ANALYTICS ---
def show_analytics():
    st.title("Business Intelligence & Predicción")
    st.markdown("#### Tableros Interactivos para Toma de Decisiones Estratégicas")
    
    # Improved Context / Explanation
    # Improved Context / Explanation
    with st.expander("¿Por qué usar Predicción con IA y de dónde salen los datos?", expanded=True):
        st.markdown("""
        **1. El Problema Real:**
        Las empresas suelen mirar "al retrovisor" (lo que ya vendieron). El problema es que saber que vendiste mucho Pino en Enero no te ayuda a saber cuánto comprar para Febrero si el mercado cambia.
        
        **2. La Solución (Predicción IA):**
        Utilizamos algoritmos de *Machine Learning* (como Prophet o ARIMA) que analizan años de historial para detectar **patrones estacionales** y **tendencias ocultas**. 
        *   *Ejemplo:* "El modelo detectó que cada Mayo sube la demanda de Cedro un 15%, por lo que sugiere aumentar stock hoy para no perder ventas mañana."
        
        **3. Fuente de Datos (Simulación):**
        En un entorno real, este tablero se conecta en tiempo real a tu **ERP (SAP, Oracle)** o Base de Datos **SQL**. Aquí simulamos una extracción segura de esos datos transaccionales.
        """)

    st.divider()

    # Filters
    col_filter, col_metrics = st.columns([1, 3])
    
    with col_filter:
        st.markdown("##### Configuración de Vista")
        material_filter = st.selectbox("Seleccionar Material:", ["Todos", "Pino", "Roble", "Cedro"])
        st.caption("Filtra los datos del gráfico y del chat de análisis.")
    
    # Mock Data Generation
    data = {
        "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"] * 3,
        "Material": ["Pino"]*12 + ["Roble"]*12 + ["Cedro"]*12,
        "Ventas Reales": [
            100, 120, 115, 130, 140, 150, 160, 155, 140, 130, 120, 110, # Pino
            80, 85, 90, 95, 110, 115, 120, 125, 130, 125, 110, 100,     # Roble
            60, 65, 70, 75, 80, 85, 90, 95, 100, 110, 120, 130          # Cedro
        ],
        "Ventas Predichas": [
            105, 118, 120, 135, 145, 155, 165, 160, 145, 135, 125, 115, # Pino Forecast
            82, 88, 92, 98, 115, 120, 125, 130, 135, 130, 115, 105,     # Roble Forecast
            62, 68, 72, 78, 85, 90, 95, 100, 108, 118, 128, 138         # Cedro Forecast
        ]
    }
    df_full = pd.DataFrame(data)
    
    # Filter Logic
    if material_filter != "Todos":
        df = df_full[df_full["Material"] == material_filter]
    else:
        df = df_full

    with col_metrics:
        # Dynamic KPI Calculation
        total_sales = df["Ventas Reales"].sum()
        avg_pred_accuracy = 100 - (abs(df["Ventas Reales"] - df["Ventas Predichas"]).mean() / df["Ventas Reales"].mean() * 100)
        top_month = df.loc[df["Ventas Reales"].idxmax()]["Mes"]
        
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric(label="Ventas Totales (Periodo)", value=f"{total_sales:,.0f} u", delta="Acumulado")
        kpi2.metric(label="Precisión del Modelo IA", value=f"{avg_pred_accuracy:.1f}%", delta="Alta Confianza")
        kpi3.metric(label="Mes Pico de Venta", value=top_month, delta="Estacionalidad", delta_color="off")

    # Plotly Chart
    fig = px.line(df, x="Mes", y=["Ventas Reales", "Ventas Predichas"], 
                  title=f"Tendencia de Ventas vs. Proyección IA ({material_filter})",
                  markers=True,
                  color_discrete_sequence=["#00eeff", "#bd00ff"]) # Electric Blue & Purple
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(14, 17, 23, 0.5)",
        font_color="#c9d1d9",
        xaxis_title="Ciclo Anual 2024-2025",
        yaxis_title="Unidades Vendidas",
        legend_title="Comparativa",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # --- DATA CHAT FEATURE ---
    st.markdown("---")
    st.subheader("Analista de Datos IA (Chat con tu Tabla)")
    st.caption("Pregunta directamente sobre los datos mostrados arriba. La IA tiene acceso a las filas exactas.")

    if "analytics_messages" not in st.session_state:
        st.session_state["analytics_messages"] = [
            {"role": "assistant", "content": "Hola. He analizado los datos del gráfico. ¿Qué quieres saber? (Ej: '¿Qué madera se vendió más?', '¿Cuál es la tendencia del Pino?')"}
        ]

    for msg in st.session_state.analytics_messages:
        with st.chat_message(msg["role"], avatar="📊" if msg["role"] == "assistant" else "👤"):
            st.write(msg["content"])

    if prompt := st.chat_input("Pregunta sobre los datos...", key="analytics_input"):
        st.session_state.analytics_messages.append({"role": "user", "content": prompt})
        st.chat_message("user", avatar="👤").write(prompt)
        
        response_text = ""
        api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
        
        if api_key:
            try:
                # Prepare context specifically for the Data Agent
                data_context = df.to_csv(index=False)
                
                client = Groq(api_key=api_key)
                system_prompt = {
                    "role": "system",
                    "content": f"Eres un Analista de Datos Experto. Tienes acceso al siguiente dataset (formato CSV) que corresponde a las ventas de madera:\n\n{data_context}\n\nInstrucciones:\n1. Responde basándote ÚNICAMENTE en estos datos.\n2. Sé breve y directo.\n3. Si te preguntan por totales, súmalos.\n4. Si te preguntan por tendencias, compara los meses."
                }
                
                messages = [system_prompt] + [
                    {"role": m["role"], "content": m["content"]} 
                    for m in st.session_state.analytics_messages
                ]
                
                chat = client.chat.completions.create(
                    messages=messages,
                    model="llama-3.3-70b-versatile",
                    temperature=0.1, # Low temperature for factual data analysis
                    max_tokens=600,
                )
                response_text = chat.choices[0].message.content
            except Exception as e:
                response_text = f"Error analizando datos: {str(e)}"
        else:
            response_text = "⚠️ **Modo Demo**: Para chatear con tus datos reales, configura la API Key. \n\n*Respuesta simulada:* El Pino tuvo su pico de ventas en Julio con 160 unidades."
            
        st.session_state.analytics_messages.append({"role": "assistant", "content": response_text})
        st.chat_message("assistant", avatar="📊").write(response_text)

def show_contact():
    st.title("Contacto Profesional")
    
    st.markdown("""
    <div class="css-card">
        <h4 style="margin-top:0;">¿Listo para innovar?</h4>
        <p style="color: #c9d1d9;">Estoy disponible para proyectos de transformación digital, desarrollo de MVPs de IA y consultoría técnica.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_info, col_form = st.columns([1, 1], gap="large")
    
    with col_info:
        st.subheader("Datos de Contacto")
        
        # WhatsApp Direct Link
        st.markdown("📱 **WhatsApp Directo:**")
        st.markdown(
            """<a href="https://wa.me/525615410755" target="_blank" style="text-decoration: none;">
                <button style="background-color: #25D366; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%;">
                    💬 Abrir Chat (+52 56 1541 0755)
                </button>
            </a>""", 
            unsafe_allow_html=True
        )
        
        st.write("")
        st.markdown("📧 **Email Profesional:**")
        st.write("leo_nieto_cortes@hotmail.com")
        
        st.write("")
        st.markdown("📍 **Ubicación:**")
        st.write("San Juan del Río, Qro. / Ecatepec, Edo. Méx.")
        
        st.divider()
        st.subheader("📄 Currículum Vitae")
        
        # CV Download Logic
        cv_path = "rec/CV_Leonardo_Nieto_AI_Engineer.pdf"
        try:
            with open(cv_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                st.download_button(
                    label="📥 Descargar CV (PDF)",
                    data=pdf_bytes,
                    file_name="CV_Leonardo_Nieto_AI_Engineer.pdf",
                    mime="application/pdf"
                )
        except FileNotFoundError:
            st.error(f"Archivo CV no encontrado en: {cv_path}")
        
    with col_form:
        st.subheader("Envíame un mensaje rápido")
        st.markdown("Elige tu canal preferido para iniciar la prosprección:")
        
        with st.container(border=True):
            name = st.text_input("Tu Nombre / Empresa")
            msg = st.text_area("Asunto o Mensaje", height=100)
            
            # Message encoding
            import urllib.parse
            encoded_msg_wa = urllib.parse.quote(f"Hola Leonardo, soy {name}. {msg}")
            encoded_subject = urllib.parse.quote(f"Contacto Portafolio: {name}")
            encoded_body = urllib.parse.quote(f"Hola Leonardo,\n\nSoy {name}.\n\n{msg}")
            
            col_wa, col_email = st.columns(2)
            
            with col_wa:
                st.markdown(
                    f"""<a href="https://wa.me/525615410755?text={encoded_msg_wa}" target="_blank" style="text-decoration: none;">
                        <button style="background-color: transparent; border: 1px solid #25D366; color: #25D366; padding: 8px 15px; border-radius: 5px; cursor: pointer; width: 100%;">
                            📲 Enviar por WhatsApp
                        </button>
                    </a>""",
                    unsafe_allow_html=True
                )
            
            with col_email:
                st.markdown(
                    f"""<a href="mailto:leo_nieto_cortes@hotmail.com?subject={encoded_subject}&body={encoded_body}" style="text-decoration: none;">
                        <button style="background-color: transparent; border: 1px solid #00eeff; color: #00eeff; padding: 8px 15px; border-radius: 5px; cursor: pointer; width: 100%;">
                            📧 Enviar por Correo
                        </button>
                    </a>""",
                    unsafe_allow_html=True
                )

# --- Main Routing ---
if selected_page == "Inicio":
    show_home()
elif selected_page == "Chatbot IA":
    show_chat()
elif selected_page == "Visión Artificial":
    show_vision()
elif selected_page == "Analytics":
    show_analytics()
elif selected_page == "Contacto":
    show_contact()

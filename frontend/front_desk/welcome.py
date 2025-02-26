import streamlit as st

def show():
    # Custom CSS for centering text and button
    st.markdown("""
        <style>
        .centered {
            text-align: center;
        }
        .big-title {
            font-size: 42px;
            font-weight: bold;
        }
        .description {
            font-size: 18px;
            line-height: 1.6;
            max-width: 700px;
            margin: 0 auto;
        }
        .button-container {
            display: flex;
            justify-content: center;
            margin-top: 30px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Centering content
    st.markdown('<h1 class="big-title centered">Welcome to Pueblos 🌾</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <p class="description">
    Lorem Ipsum es simplemente el texto de relleno de las imprentas y archivos de texto. Lorem Ipsum ha sido el 
    texto de relleno estándar de las industrias desde el año 1500, cuando un impresor desconocido usó una galería 
    de textos y los mezcló de tal manera que logró hacer un libro de textos especimen. 
    </p>
    <p class="description">
    No sólo sobrevivió 500 años, sino que también ingresó como texto de relleno en documentos electrónicos, 
    quedando esencialmente igual al original. Fue popularizado en los 60s con la creación de las hojas "Letraset" 
    y más recientemente con software de autoedición como Aldus PageMaker.
    </p>
    """, unsafe_allow_html=True)

    # Centered Button
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Let's Go 🎒", key="start_button"):
            st.session_state.page = "get_user_preferences_map"
            st.rerun()  # Reload the app to show the main page
    st.markdown('</div>', unsafe_allow_html=True)

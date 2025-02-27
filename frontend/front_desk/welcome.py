import streamlit as st

def show():
    # Custom CSS for vertical and horizontal centering
    st.markdown("""
        <style>
        .full-page {
            align-items: center;
            height: 12vh;
        }
        .centered {
            text-align: center;
        }
        .big-title {
            font-size: 42px;
            font-weight: bold;
        }
        }
        .button-container {
            display: flex;
            justify-content: center;
            margin-top: 30px;
            margin-left: 100px;
            width: 500px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Wrap all content inside a flexbox container
    st.markdown('<div class="full-page">', unsafe_allow_html=True)

    # Centered Title
    st.markdown('<h1 class="big-title centered">Welcome to Pueblos 🌾 </h1>', unsafe_allow_html=True)
    st.markdown('<div></dvi>', unsafe_allow_html=True)

    # Centered Text
    st.markdown("""
    <p style="font-size: 18px; line-height: 1.6; max-width: 700px; margin: 0 auto; text-align: center;">
    Lorem Ipsum es simplemente el texto de relleno de las imprentas y archivos de texto. Lorem Ipsum ha sido el 
    texto de relleno estándar de las industrias desde el año 1500, cuando un impresor desconocido usó una galería 
    de textos y los mezcló de tal manera que logró hacer un libro de textos especimen. 
    </p>
    <p style="font-size: 18px; line-height: 1.6; max-width: 700px; margin: 0 auto; text-align: center;">
    No sólo sobrevivió 500 años, sino que también ingresó como texto de relleno en documentos electrónicos, 
    quedando esencialmente igual al original. Fue popularizado en los 60s con la creación de las hojas "Letraset" 
    y más recientemente con software de autoedición como Aldus PageMaker.
    </p>
    """, unsafe_allow_html=True)
    st.markdown('<div></dvi>', unsafe_allow_html=True)
    # Centered Button
    st.markdown('<div>', unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 2, 1, 1, 1])
    with col4:
        if st.button("Let's Go :school_satchel:", key="start_button", use_container_width=True):
            st.session_state.page = "get_user_preferences_map"
            st.rerun()  # Reload the app to show the main page
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # Close the full-page div
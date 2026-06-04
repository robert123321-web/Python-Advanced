import stramlit as st

tab1,tab2,tab3 = st.tabs(["Tab1","Tab2","Tab3"])

with tab1:
    st.header("Contect for Tab 1")
    st.write("this is the content of the first tab")

with tab2:
    st.header("Contect for Tab 2")
    st.write("this is the content of the first tab")

with tab3:
    st.header("Contect for Tab 3")
    st.write("this is the content of the first tab")
import streamlit as st

CSS = """
<style>
.block-container {padding-top: 1rem !important;}
.small {font-size: 0.85rem; color: #9aa3ae;}
.kpi {background: #0ea5e914; border: 1px solid #0ea5e980; padding: 0.75rem 1rem; border-radius: 14px;}
.caption {color:#9aa3ae; font-size: 0.9rem;}
</style>
"""
#push issue 

def inject():
    st.markdown(CSS, unsafe_allow_html=True)
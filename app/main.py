"""App dedicada exclusivamente al ejercicio 1 del set."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
import streamlit as st
from app.exercise1 import render_exercise1

def main():
    st.set_page_config(page_title='PRE-POST 2.0 | Ejercicio 1',layout='wide')
    render_exercise1()

if __name__=='__main__':main()

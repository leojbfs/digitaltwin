import streamlit as st
import openai
import os
import json
from datetime import date

# Configurar API Key
openai.api_key = st.secrets["openai_key"]

# Funções auxiliares
def criar_estrutura_base(caminho, nome):
    estrutura = {
        "nome": nome,
        "diario": []
    }
    with open(caminho, "w") as f:
        json.dump(estrutura, f, indent=2)

def carregar_dados(caminho):
    with open(caminho, "r") as f:
        return json.load(f)

def salvar_dados(caminho, dados):
    with open(caminho, "w") as f:
        json.dump(dados, f, indent=2)

# Interface
st.title("🧠 Diário Digital com IA")
usuario = st.text_input("Digite seu nome:")

if usuario:
    os.makedirs("usuarios", exist_ok=True)
    caminho = f"usuarios/{usuario.lower()}.json"

    if not os.path.exists(caminho):
        criar_estrutura_base(caminho, usuario)

    dados = carregar_dados(caminho)
    entrada = st.text_area("O que você quer registrar hoje?", height=200)

    if st.button("Interpretar e Salvar"):
        if entrada:
            with st.spinner("Consultando IA..."):
                resposta = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Organize o texto em tarefas, metas, aprendizados e compromissos."},
                        {"role": "user", "content": entrada}
                    ]
                ).choices[0].message.content

            novo_registro = {
                "data": str(date.today()),
                "entrada": entrada,
                "interpretacao": resposta
            }

            dados["diario"].append(novo_registro)
            salvar_dados(caminho, dados)

            st.success("Registrado com sucesso!")
            st.markdown("### IA sugeriu:")
            st.write(resposta)

    if st.checkbox("Ver histórico"):
        for reg in reversed(dados["diario"]):
            st.markdown(f"**{reg['data']}**")
            st.markdown(f"> {reg['entrada']}")
            st.markdown(f"🧠 {reg['interpretacao']}")
            st.markdown("---")
else:
    st.info("Digite seu nome para iniciar.")

import streamlit as st
import os
import json
from datetime import datetime
from openai import OpenAI

# Carrega a chave da API do Streamlit Secrets
client = OpenAI(api_key=st.secrets["openai_key"])

# Interface do app
st.title("📓 Diário Inteligente com IA")
usuario = st.text_input("Digite seu nome ou identificador:")

if usuario:
    caminho_arquivo = f"usuarios/{usuario.lower()}.json"

    # Cria pasta se necessário
    os.makedirs("usuarios", exist_ok=True)

    # Cria arquivo do usuário se ainda não existir
    if not os.path.exists(caminho_arquivo):
        estrutura_inicial = {
            "nome": usuario,
            "rotina_diaria": {
                "saude": [],
                "educacao": [],
                "trabalho": [],
                "tarefas": []
            },
            "metas": [],
            "acordos": [],
            "ativos": [],
            "relacionamentos": [],
            "diario": []
        }
        with open(caminho_arquivo, "w") as f:
            json.dump(estrutura_inicial, f, indent=2)

    # Carrega os dados existentes
    with open(caminho_arquivo, "r") as f:
        dados = json.load(f)

    # Entrada do diário
    entrada = st.text_area("O que você gostaria de registrar hoje?", height=150)

    if st.button("Salvar e Interpretar"):
        if entrada.strip():
            # Chama o modelo de linguagem
            resposta = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente que ajuda a organizar um diário pessoal e interpretar a entrada."},
                    {"role": "user", "content": entrada}
                ]
            )

            interpretacao = resposta.choices[0].message.content

            registro = {
                "data": datetime.now().isoformat(),
                "entrada": entrada,
                "interpretacao": interpretacao
            }

            # Adiciona ao diário
            dados["diario"].append(registro)

            # Salva no arquivo
            with open(caminho_arquivo, "w") as f:
                json.dump(dados, f, indent=2)

            st.success("Entrada salva com sucesso!")
            st.markdown("### 📌 Interpretação da IA:")
            st.write(interpretacao)
        else:
            st.warning("Digite algo para registrar.")

    # Mostrar histórico
    if dados["diario"]:
        st.markdown("## 📖 Histórico do Diário")
        for item in reversed(dados["diario"][-10:]):
            st.markdown(f"**🗓 {item['data']}**")
            st.markdown(f"**Você:** {item['entrada']}")
            st.markdown(f"**IA:** {item['interpretacao']}")
            st.markdown("---")

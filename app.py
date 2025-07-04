# app.py
import streamlit as st
from interpretador import interpretar_entrada
from diario_twin_db import obter_ou_criar_usuario, salvar_interacao, buscar_historico
from config import OPENAI_API_KEY

# Título do app
st.title("Diário Digital Twin")

# Campos de entrada
nome_usuario = st.text_input("Seu nome (ou apelido)")
chave_api_input = st.text_input("Sua chave de API (opcional)", type="password")
provedor = st.selectbox("Escolha o provedor de IA", ["openai", "openrouter", "gemini"])

# Entrada de texto
mensagem = st.text_area("Escreva algo para registrar ou refletir:")

# Botão de envio
if st.button("Enviar"):
    if not nome_usuario:
        st.warning("Por favor, digite seu nome.")
    elif not mensagem:
        st.warning("Escreva alguma mensagem antes de enviar.")
    else:
        # Usa a chave fornecida ou a padrão (em config.py, vinda do Streamlit secrets)
        chave_api = chave_api_input or OPENAI_API_KEY

        # Garante que o usuário existe no banco
        usuario_id = obter_ou_criar_usuario(nome_usuario, chave_api, provedor)

        # Envia a mensagem para o interpretador
        resposta = interpretar_entrada(mensagem, chave_api, provedor)

        # Mostra a resposta na tela
        st.markdown("### Resposta da IA:")
        st.markdown(resposta)

        # Salva no banco de dados
        salvar_interacao(usuario_id, mensagem, resposta)

        # Histórico
        st.markdown("### Histórico de interações:")
        historico = buscar_historico(usuario_id)
        for entrada in historico:
            st.markdown(f"**Você:** {entrada[0]}")
            st.markdown(f"**IA:** {entrada[1]}")
            st.markdown("---")

# app.py
import streamlit as st
from interpretador import interpretar_entrada
from diario_twin_db import obter_ou_criar_usuario, salvar_interacao, buscar_historico

st.set_page_config(page_title="Diário Twin", layout="wide")
st.title("🧠 Diário Twin - Registro Inteligente")

# Sessão do usuário
with st.sidebar:
    st.header("🔐 Identificação")
    nome_usuario = st.text_input("Seu nome ou apelido")
    chave_api = st.text_input("Sua chave de API", type="password")
    provedor = st.selectbox("Escolha o provedor de IA", ["openai", "openrouter", "gemini"])
    if st.button("Entrar"):
        if nome_usuario and chave_api:
            usuario_id = obter_ou_criar_usuario(nome_usuario, chave_api, provedor)
            st.session_state["usuario_id"] = usuario_id
            st.session_state["chave_api"] = chave_api
            st.session_state["provedor"] = provedor
            st.success("Usuário autenticado.")
        else:
            st.error("Preencha todos os campos.")

# Verifica se o usuário está autenticado
if "usuario_id" not in st.session_state:
    st.warning("Autentique-se para usar o diário.")
    st.stop()

# Campo de entrada
st.subheader("✍️ Escreva seu pensamento, tarefa ou interação:")
mensagem = st.text_area("Digite abaixo...", height=150)

if st.button("Enviar"):
    if mensagem.strip():
        st.info("Processando com IA...")
        resposta = interpretar_entrada(
            mensagem,
            st.session_state["chave_api"],
            st.session_state["provedor"]
        )

        salvar_interacao(
            usuario_id=st.session_state["usuario_id"],
            entrada=mensagem,
            resposta=resposta
        )
        st.success("Interação salva!")
        st.markdown("### 🤖 Resposta:")
        st.markdown(resposta)
    else:
        st.warning("Digite algo para registrar.")

# Exibe histórico
st.subheader("📜 Últimos registros")
historico = buscar_historico(st.session_state["usuario_id"])
for h in historico:
    with st.expander(f"🕒 {h['data_criacao'].strftime('%d/%m %H:%M')}"):
        st.markdown(f"**Você:** {h['entrada']}")
        st.markdown(f"**IA:** {h['resposta']}")

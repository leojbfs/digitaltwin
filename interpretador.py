# interpretador.py
import openai
import requests
import os
import streamlit as st
import google.generativeai as genai

def interpretar_entrada(mensagem, chave_api, provedor):
    if not chave_api:
        return "Nenhuma chave de API fornecida."

    if provedor == "openai":
        try:
            client = openai.OpenAI(api_key=chave_api)
            resposta = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": mensagem}]
            )
            return resposta.choices[0].message.content.strip()
        except Exception as e:
            return f"[OpenAI] Erro: {str(e)}"

    elif provedor == "openrouter":
        try:
            headers = {
                "Authorization": f"Bearer {chave_api}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "openrouter/openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": mensagem}]
            }
            resposta = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )
            if resposta.status_code == 200:
                return resposta.json()["choices"][0]["message"]["content"].strip()
            else:
                return f"[OpenRouter] Erro: {resposta.status_code} - {resposta.text}"
        except Exception as e:
            return f"[OpenRouter] Erro: {str(e)}"

    elif provedor == "gemini":
        try:
            genai.configure(api_key=chave_api)
            modelo = genai.GenerativeModel("gemini-pro")
            resposta = modelo.generate_content(mensagem)
            return resposta.text.strip()
        except Exception as e:
            return f"[Gemini] Erro: {str(e)}"

    return "Provedor de IA não reconhecido."

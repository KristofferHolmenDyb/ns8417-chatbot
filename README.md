
# 🤖 NS 8417 Chatbot

En AI-drevet chatbot som svarer på spørsmål basert på innholdet i NS 8417-kontrakten.  
Utviklet som en del av BYG509-oppgave ved bruk av OpenAI og LangChain.

## 🚀 Kom i gang

### 1. Installer avhengigheter
```bash
pip install streamlit openai langchain-community faiss-cpu
```

### 2. Sett inn din OpenAI API-nøkkel
Åpne `ns8417_chatbot_web_inline_key.py` og lim inn nøkkelen på denne linjen:
```python
openai_api_key = "sk-din-api-nøkkel-her"
```

### 3. Start appen
```bash
streamlit run ns8417_chatbot_web_inline_key.py
```

Appen åpner seg i nettleseren. Skriv inn spørsmål og få svar basert på kontrakten.

## 📄 Filer
- `ns8417_chatbot_web_inline_key.py`: Hovedfilen for chatboten
- `ns8417_chunks.txt`: Innholdet fra NS 8417 som chatboten er trent på (rediger denne med ekte innhold)
- `README.md`: Denne filen

## 🧠 Teknologi
- Python
- LangChain
- OpenAI (GPT-4)
- Streamlit

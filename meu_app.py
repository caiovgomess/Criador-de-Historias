import streamlit as st
import google.generativeai as genai

# --- CONFIGURAÇÃO DA PÁGINA E DA API ---

st.set_page_config(
    page_title="Gerador de Histórias",
    page_icon="📖",
    layout="centered"
)

# --- CONFIGURAÇÃO SEGURA DA API KEY ---
try:
    # Carrega a chave de API dos segredos do Streamlit
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

except (KeyError, Exception) as e:
    # Mensagem de erro amigável se a chave não for encontrada ou for inválida
    st.error("Chave de API do Gemini não configurada ou inválida.")
    st.info("Por favor, adicione sua chave de API ao arquivo `secrets.toml` no diretório `.streamlit` do seu projeto.")
    st.code("""
# Exemplo para o arquivo .streamlit/secrets.toml
GEMINI_API_KEY = "SUA_CHAVE_DE_API_AQUI"
    """, language="toml")
    st.stop()

st.title("Gerador de Histórias com IA 📖")
st.header("Crie o começo da sua próxima aventura!")

st.markdown("---")

# 1. Nome do Protagonista
nome_protagonista = st.text_input(
    "Qual é o nome do(a) protagonista?",
    placeholder="Ex: Alistair, o Bravo"
)

# 2. Gênero Literário
genero = st.selectbox(
    "Escolha um gênero literário:",
    ("Fantasia", "Ficção Científica", "Mistério", "Aventura", "Terror")
)

# 3. Local Inicial
local_inicial = st.radio(
    "Selecione o local inicial da história:",
    ("Uma floresta antiga", "Uma cidade futurista", "Um castelo assombrado", "Uma nave espacial à deriva"),
    captions=["Florestas densas e magia esquecida.", "Arranha-céus de neon e carros voadores.", "Corredores escuros e segredos do passado.", "O silêncio do vácuo e painéis de controle piscando."]
)

# 4. Frase de Efeito ou Desafio
frase_desafio = st.text_area(
    "Adicione uma frase de efeito ou um desafio inicial:",
    placeholder="Ex: O mapa indicava um perigo iminente bem aqui."
)

st.markdown("---")

# 5. Botão para Gerar a História
if st.button("Gerar Início da História ✨"):
    # Validação para garantir que os campos de texto não estão vazios
    if nome_protagonista and frase_desafio:
        with st.spinner("A criatividade da IA está a todo vapor... Por favor, aguarde."):
            # 6. Lógica de Prompt Engineering
            prompt_final = (
                f"Crie um parágrafo de introdução para uma história de '{genero}' "
                f"com o protagonista chamado '{nome_protagonista}'. "
                f"A história começa em '{local_inicial}'. "
                f"Incorpore de forma criativa a seguinte frase ou desafio no início da narrativa: '{frase_desafio}'"
            )

            try:
                # 7. Exibir a história gerada
                response = model.generate_content(prompt_final)
                st.subheader(f"O Início da Aventura de {nome_protagonista}")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Ocorreu um erro ao gerar a história: {e}")

    else:
        st.warning("Por favor, preencha o nome do protagonista e a frase de desafio.")
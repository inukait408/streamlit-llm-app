from dotenv import load_dotenv

load_dotenv()
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# タイトルとアプリの概要
st.set_page_config(page_title="LLM専門家相談アプリ", layout="centered")
st.title("🧠 LLM専門家相談アプリ")
st.write("""
このアプリでは、選択した専門分野のAI専門家に質問できます。  
以下のステップでご利用ください。

1. 専門家の種類を選択してください  
2. 質問を入力して送信してください  
3. 回答が画面下部に表示されます
""")

# 専門家の選択
expert_type = st.radio(
    "相談したい専門家のタイプを選んでください：",
    ("キャリアコンサルタント", "育児アドバイザー", "健康アドバイザー")
)

# ユーザー入力
user_input = st.text_input("あなたの質問を入力してください:")

# 温度設定
temperature = st.slider("温度を設定:", 0.0, 1.0, 0.5)

# LLM呼び出し関数
def get_response_from_llm(input_text: str, expert_role: str) -> str:
    expert_prompts = {
        "キャリアコンサルタント": "あなたは経験豊富なキャリアコンサルタントです。転職や職場での悩みに対して、丁寧かつ具体的にアドバイスしてください。",
        "育児アドバイザー": "あなたは保育士資格を持つ育児アドバイザーです。子育てに関する悩みに対して、やさしく具体的に答えてください。",
        "健康アドバイザー": "あなたは栄養学と運動生理学の専門家です。健康や生活習慣に関する相談に対して、科学的根拠に基づいたアドバイスをしてください。"
    }

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=temperature)

    try:
        messages = [
            SystemMessage(content=expert_prompts[expert_role]),
            HumanMessage(content=input_text)
        ]
        response = llm(messages)
        return response.content
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# 入力がある場合に処理を実行
if user_input:
    if not user_input.strip():
        st.warning("質問を入力してください。")
    else:
        with st.spinner("AIが考えています..."):
            result = get_response_from_llm(user_input, expert_type)
        st.success("AIの回答:")
        st.write(result)
import os
import streamlit as st
from openai import OpenAI

def main():
    # 设置页面标题和配置
    st.set_page_config(page_title="AI智能问答助手", page_icon="🤖", layout="wide")

    # 页面标题
    st.title("🤖 AI智能问答助手")
    st.markdown("---")

    # 初始化会话状态来存储聊天历史
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "你是一个有帮助的AI助手，用中文回答问题"}
        ]

    # 创建侧边栏用于API设置
    with st.sidebar:
        st.header("⚙️ 设置")

        # 安全的API密钥获取方式
        api_key = get_api_key()

        if not api_key:
            st.error("❌ 未检测到API密钥配置")
            st.info("""
            🔐 **安全提示**：
            - API密钥不会被提交到GitHub
            - 支持多种安全配置方式
            - 推荐使用环境变量
            """)

            # 提供配置指导
            st.markdown("### 配置方法")
            st.markdown("""
            **1. 环境变量（推荐）**            
            **2. .env文件（开发环境）**
            创建 `.env` 文件：            """)

            # 显示当前工作目录
            st.text(f"当前目录: {os.getcwd()}")
            return

        # 模型选择
        model = st.selectbox(
            "选择模型",
            ["deepseek-chat"],
            index=0,
            help="deepseek-chat: 通用对话模型"
        )

        # 清除聊天历史按钮
        if st.button("🗑️ 清除聊天记录"):
            st.session_state.messages = [
                {"role": "system", "content": "你是一个有帮助的AI助手，用中文回答问题"}
            ]
            st.rerun()

        st.markdown("---")
        st.info("""
        🌐 **部署说明**
        
        本项目已配置安全机制：
        - `secrets.toml` 和 `.env` 已添加到 .gitignore
        - API密钥永远不会上传到GitHub
        - 支持云端密钥管理
        """)

    # 显示聊天历史
    for message in st.session_state.messages[1:]:  # 跳过系统消息
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # 用户输入区域
    user_input = st.chat_input("请输入你的问题...")

    if user_input:
        # 添加用户消息到历史
        st.session_state.messages.append({"role": "user", "content": user_input})

        # 在界面上显示用户输入
        with st.chat_message("user"):
            st.write(user_input)

        # 显示AI思考中的状态
        with st.chat_message("assistant"):
            with st.spinner("AI正在思考，请稍候..."):
                try:
                    # 创建OpenAI客户端
                    client = OpenAI(
                        api_key=api_key,
                        base_url="https://api.deepseek.com"
                    )

                    # 获取AI响应
                    response = client.chat.completions.create(
                        model=model,
                        messages=st.session_state.messages,
                        stream=False,
                        temperature=0.7,
                        max_tokens=2048
                    )

                    # 获取并显示AI回复
                    ai_response = response.choices[0].message.content
                    st.write(ai_response)

                    # 将AI回复添加到消息历史
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": ai_response
                    })

                except Exception as e:
                    error_msg = f"❌ 发生错误：{str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"很抱歉，遇到了一个问题：{str(e)}。请检查你的API密钥是否正确，或者稍后再试。"
                    })

    # 底部信息
    st.markdown("---")
    st.caption("💡 提示：刷新页面会清除所有聊天记录 | Powered by DeepSeek & Streamlit")

def get_api_key():
    """
    安全获取API密钥的多种方式
    按优先级顺序尝试
    """
    # 1. 首先尝试从Streamlit secrets（云端部署）
    try:
        import streamlit as st
        if hasattr(st, 'secrets'):
            return st.secrets.get("DEEPSEEK_API_KEY")
    except:
        pass

    # 2. 从环境变量获取
    env_key = os.environ.get('DEEPSEEK_API_KEY')
    if env_key and env_key.strip() and env_key != "your_actual_api_key_here":
        return env_key

    # 3. 从.env文件读取（仅限本地开发）
    try:
        from dotenv import load_dotenv
        load_dotenv()
        dot_env_key = os.getenv('DEEPSEEK_API_KEY')
        if dot_env_key and dot_env_key.strip():
            return dot_env_key
    except ImportError:
        pass
    except:
        pass

    # 4. 最后尝试直接在代码中定义（不推荐，仅作演示）
    # 注意：这个值不应该包含真实密钥
    fallback_key = "your_actual_api_key_here"
    if fallback_key != "your_actual_api_key_here":
        return fallback_key

    return None

if __name__ == "__main__":
    main()



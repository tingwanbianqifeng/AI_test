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

        # 方法1: 直接在代码中设置API密钥（不推荐用于共享代码）
        # 请将 'your-api-key-here' 替换为你的实际API密钥
        API_KEY = "DEEPSEEK_API_KEY"

        # 方法2: 从环境变量获取API密钥（推荐）
        # 在系统中设置环境变量：DEEPSEEK_API_KEY=your_actual_key
        api_key = os.environ.get('DEEPSEEK_API_KEY', API_KEY)

        # 如果API密钥是默认值，显示警告
        if api_key == "your-api-key-here":
            st.warning("⚠️ 请在代码中替换API密钥或设置环境变量")

        # 显示当前使用的API密钥前缀（出于安全考虑，只显示前几位）
        if api_key != "your-api-key-here":
            st.success(f"✅ API密钥已配置")

        # 模型选择
        model = st.selectbox(
            "选择模型",
            ["deepseek-chat"],
            index=0,
            help="deepseek-chat: 通用对话模型 | deepseek-coder: 编程专用模型"
        )

        # 清除聊天历史按钮
        if st.button("🗑️ 清除聊天记录"):
            st.session_state.messages = [
                {"role": "system", "content": "你是一个有帮助的AI助手，用中文回答问题"}
            ]
            st.rerun()

        st.markdown("---")
        # st.info("""
        # 📝 使用说明：
        # 1. 配置API密钥（见下方说明）
        # 2. 选择合适的模型
        # 3. 在下方输入框中提问
        # 4. 等待AI回复
        #
        # 🔐 安全提示：
        # - 推荐使用环境变量方式配置API密钥
        # - 如果直接在代码中写入，请勿分享此文件
        # """)

        # st.markdown("### 🔧 API密钥配置方法")
        # st.markdown("""
        # **方法一：环境变量（推荐）**
        #
        # **方法二：直接在代码中设置**
        # 修改第25行的 `API_KEY` 变量值
        # """)

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
                    # 验证API密钥
                    if not api_key or api_key == "your-api-key-here":
                        st.error("❌ 请先配置API密钥！")
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": "请先配置API密钥。可以在侧边栏查看配置方法。"
                        })
                    else:
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

if __name__ == "__main__":
    main()

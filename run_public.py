from pyngrok import ngrok
import subprocess
import time
import os

def main():
    # 设置API密钥（请替换为你的实际DeepSeek API密钥）
    os.environ['DEEPSEEK_API_KEY'] = 'your_actual_api_key_here'

    print("正在启动AI助手...")

    try:
        # 检查streamlit是否已安装
        result = subprocess.run(["streamlit", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ 错误：未找到streamlit命令")
            print("请先安装streamlit：pip install streamlit")
            return

        # 启动Streamlit应用
        process = subprocess.Popen([
            "streamlit", "run", "D:\\Python\\测试\\测试\\AI测试\\ai_assistant.py",
            "--server.port=8501",
            "--server.address=0.0.0.0",
            "--server.headless=true"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True)

        # 等待一段时间让服务器启动
        time.sleep(3)

        # 检查进程是否还在运行
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print(f"❌ Streamlit启动失败")
            print(f"错误信息: {stderr}")
            return

        # === 关键步骤：配置ngrok认证 ===
        try:
            # 1. 访问 https://dashboard.ngrok.com/signup 注册账号
            # 2. 登录后访问 https://dashboard.ngrok.com/get-started/your-authtoken 获取你的authtoken
            # 3. 将下面的 'your_ngrok_authtoken_here' 替换为你的实际authtoken

            NGROK_AUTHTOKEN = "your_ngrok_authtoken_here"

            if NGROK_AUTHTOKEN == "your_ngrok_authtoken_here":
                print("❌ 错误：请先配置ngrok authtoken！")
                print("\n配置步骤：")
                print("1. 访问 https://dashboard.ngrok.com/signup 注册账号")
                print("2. 登录后访问 https://dashboard.ngrok.com/get-started/your-authtoken")
                print("3. 复制你的authtoken")
                print("4. 替换代码第25行的 'your_ngrok_authtoken_here'")
                return

            # 设置ngrok authtoken
            ngrok.set_auth_token(NGROK_AUTHTOKEN)

            # 创建HTTP隧道
            public_url = ngrok.connect(8501, "http")
            print(f"🌐 AI助手已启动！")
            print(f"公网访问地址: {public_url}")
            print(f"本地访问地址: http://localhost:8501")
            print("\n按 Ctrl+C 停止服务")

            # 保持程序运行
            process.wait()

        except Exception as e:
            print(f"❌ ngrok连接失败: {e}")
            print("\n常见问题：")
            print("1. authtoken不正确或已过期")
            print("2. 网络连接问题")
            print("3. 防火墙阻止连接")
            process.terminate()

    except FileNotFoundError as e:
        print(f"❌ 找不到命令: {e}")
        print("请确保已安装必要的包：")
        print("pip install streamlit openai pyngrok")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main()

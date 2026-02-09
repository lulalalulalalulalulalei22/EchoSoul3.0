"""
EchoSoul - 情绪伴侣 AI 网页版
基于 Streamlit 和 OpenAI API 构建
"""
import streamlit as st
from openai import OpenAI
import html
from datetime import datetime
from ai_brain import generate_system_prompt
from ui_style import apply_theme

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="EchoSoul - 你的情绪伴侣",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 自定义样式 ====================

apply_theme(bg_image="D:\Echosoulaicompanion\assets\background.png")
# ==================== API 配置 (完善版) ====================

# 1. 这里的第二个参数千万不能放真实的 Key，只能放空字符串 "" 或者 None
API_KEY = st.secrets.get("DEEPSEEK_API_KEY", "") 

# 2. 这里的 URL 和 MODEL 放默认值没关系，因为它们不是秘密
BASE_URL = st.secrets.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
MODEL = st.secrets.get("DEEPSEEK_MODEL", "deepseek-chat")

# 3. 这里的报错逻辑会帮你拦截：如果读取不到 Key，程序就会报错停止
if not API_KEY:
    st.error("🔑 未检测到 API 密钥！请检查本地 .streamlit/secrets.toml 或云端 Secrets 配置。")
    st.stop()



# ==================== 初始化 Session State ====================
def init_session_state():
    """初始化会话状态"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "user_desc" not in st.session_state:
        st.session_state.user_desc = ""
    if "comfort_style" not in st.session_state:
        st.session_state.comfort_style = "温暖陪伴"
    if "word_limit" not in st.session_state:
        st.session_state.word_limit = 0
    if "forbidden_phrases" not in st.session_state:
        st.session_state.forbidden_phrases = "我只是一个AI"


init_session_state()

# ==================== 侧边栏 ====================
@st.fragment
def sidebar_settings():
    st.markdown("### 🌙 EchoSoul 设置")
    st.markdown("<p class='subtitle'>你的情绪伴侣 AI</p>", unsafe_allow_html=True)
    st.divider()
    
    # 一句话描述
    st.markdown("**一句话描述此刻的你**")
    user_desc = st.text_input(
        label="一句话描述此刻的你",
        label_visibility="collapsed",
        placeholder="例如：最近工作压力很大，感到有些疲惫...",
        value=st.session_state.user_desc,
        key="user_desc_input"
    )
    st.session_state.user_desc = user_desc
    
    st.divider()
    
    # 安慰风格选择
    st.markdown("**安慰风格**")
    comfort_style = st.radio(
        label="选择安慰风格",
        label_visibility="collapsed",
        options=["温暖陪伴", "犀利点拨", "温和鼓励", "理性分析"],
        index=["温暖陪伴", "犀利点拨", "温和鼓励", "理性分析"].index(st.session_state.comfort_style),
        key="comfort_style_radio"
    )
    st.session_state.comfort_style = comfort_style
    
    st.divider()
    
    # 字数限制
    st.markdown("**单次回复字数限制**")
    word_limit = st.select_slider(
        label="字数限制",
        label_visibility="collapsed",
        options=list(range(0, 501, 50)),
        value=st.session_state.word_limit,
        format_func=lambda x: "无限制" if x == 0 else f"{x} 字",
        key="word_limit_slider"
    )
    if word_limit == 0:
        st.caption("💡 拖动滑块设置字数限制，0 表示无限制")
    st.session_state.word_limit = word_limit
    
    st.divider()
    
    # 禁止用语
    st.markdown("**禁止出现的短语**")
    forbidden_phrases = st.text_input(
        label="禁止短语",
        label_visibility="collapsed",
        placeholder="用逗号分隔，例如：我只是一个AI, 我不知道",
        value=st.session_state.forbidden_phrases,
        key="forbidden_phrases_input"
    )
    st.session_state.forbidden_phrases = forbidden_phrases
    
    st.divider()
    
    # 重启记忆按钮
    st.markdown("**对话管理**")
    if st.button("🔄 重启 / 清空记忆", type="secondary", use_container_width=True, key="reset_button"):
        st.session_state.messages = []
        st.rerun()

with st.sidebar:
    sidebar_settings()
    
    st.divider()
    
    # API 配置提示
    with st.expander("⚙️ API 配置"):
        st.markdown("""
        **当前配置：**
        - 模型：`deepseek-chat`
        - Base URL：`https://api.deepseek.com`
        
        **设置 API Key：**
        1. 点击右上角 ⋮ → Settings
        2. 选择 Secrets
        3. 添加 `DEEPSEEK_API_KEY`
        """)

# ==================== 主界面 ====================
# 标题区域
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h1 style='text-align: center;'>🌙 EchoSoul</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.6);'>我在这里，愿意倾听你的一切</p>", unsafe_allow_html=True)

st.divider()

# 显示当前设置摘要（可选，可注释掉以完全隐藏系统信息）
if st.session_state.user_desc:
    st.info(f"💭 此刻的你：{st.session_state.user_desc}")

# ==================== 聊天界面 ====================

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入
if prompt := st.chat_input("想对我说点什么吗？"):
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 准备 API 调用
    try:
        # 检查 API Key
        api_key = API_KEY or st.secrets.get("DEEPSEEK_API_KEY", "")
        if not api_key:
            st.error("⚠️ 请先配置 DEEPSEEK_API_KEY！点击侧边栏的「API 配置」查看设置方法。")
        else:
            # 初始化客户端
            client = OpenAI(
                api_key=api_key,
                base_url=BASE_URL
            )
            
            # 生成系统提示词
            system_messages = generate_system_prompt(
                user_desc=st.session_state.user_desc,
                comfort_style=st.session_state.comfort_style,
                word_limit=st.session_state.word_limit,
                forbidden_phrases=st.session_state.forbidden_phrases
            )
            
            # 构建完整消息列表（system + history）
            api_messages = system_messages + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
            
            # 调用 API
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # 流式响应
                stream = client.chat.completions.create(
                    model=MODEL,
                    messages=api_messages,
                    stream=True,
                    temperature=0.8,
                    max_tokens=2048
                )
                
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
            
            # 保存 AI 回复
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    except Exception as e:
        st.error(f"❌ 出错了：{str(e)}")
        st.info("💡 请检查 API Key 是否正确，或稍后重试。")

# ==================== 空状态提示 ====================
if not st.session_state.messages:
    st.markdown("""
    <div style='text-align: center; padding: 60px 20px; color: rgba(255,255,255,0.5);'>
        <p style='font-size: 18px; margin-bottom: 20px;'>👋 你好，我是 EchoSoul</p>
        <p style='font-size: 14px; line-height: 2;'>
            无论你此刻是什么心情，都可以告诉我<br>
            开心、难过、困惑、疲惫... 我都在听
        </p>
        <br>
        <p style='font-size: 12px; opacity: 0.7;'>
            💡 在左侧设置中描述一下此刻的你，让我更好地理解你
        </p>
    </div>
    """, unsafe_allow_html=True)

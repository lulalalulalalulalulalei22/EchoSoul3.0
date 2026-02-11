# ui_style.py
import streamlit as st
import base64
from pathlib import Path


def _get_base64_image(image_path: str) -> str | None:
    """读取本地图片并转为 base64 字符串"""
    path = Path(image_path)
    if path.exists() and path.is_file():
        return base64.b64encode(path.read_bytes()).decode()
    return None


def inject_ui_styles(bg_image_rel_path: str = "assets/background.png"):
    """
    全局 UI 注入：背景 + 侧边栏 + 输入框 + 按钮

    bg_image_rel_path: 相对 app.py 的图片路径，例如 "assets/background.png"
    """
    b64 = _get_base64_image(bg_image_rel_path)

    if b64:
        # 使用你 assets 里的星空图
        bg_css = (
            f'background-image: url("data:image/png;base64,{b64}") !important;'
        )
    else:
        # 找不到图片时兜底用渐变
        bg_css = (
            "background: radial-gradient(circle at 50% 50%, #1a1a3a 0%,"
            " #0f0c29 100%) !important;"
        )

    st.markdown(
        f"""
    <style>
    /* 1. 别隐藏整个 header，只把背景变透明，把线去掉 */
    [data-testid="stHeader"] {{
        background-color: rgba(0,0,0,0) !important;
        border-bottom: none !important;
    }}
    
    /* 2. 专门把左上角那个展开/折叠按钮颜色变亮，确保能看见 */
    button[data-testid="stSidebarCollapseButton"] {{
        color: #ffffff !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 50% !important;
    }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* 背景：优先使用本地星空图 */
    .stApp {{
        {bg_css}
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}

    /* 全局文字颜色 */
    .stApp, .stMarkdown, p, li, label, h1, h2, h3 {{
        color: #e0e0ff !important; 
        font-weight: 300 !important;
    }}

    /* 侧边栏磨砂效果 */
    section[data-testid="stSidebar"] {{
        background: rgba(15, 12, 41, 0.8) !important;
        border-right: 1px solid rgba(139, 125, 212, 0.3) !important;
        backdrop-filter: blur(20px) !important;
    }}

    section[data-testid="stSidebar"] .stTextInput input {{
        background-color: #ffffff !important; 
        color: #000000 !important; 
        border: 2px solid #8b7dd4 !important;
        border-radius: 10px !important;
        caret-color: #000000 !important; 
    }}

        /* 5. 底部聊天输入框（极致 1:1 还原图二质感） */
    
    /* 1. 最底部的整体大背景：纯黑底色，托住输入框 */
    [data-testid="stBottom"] {{
        background-color: #050505 !important; 
    }}
    [data-testid="stBottom"] > div {{
        background-color: transparent !important;
        background-image: none !important;
    }}

    /* 2. 输入框的主体容器：高级深灰黑 + 圆角 */
    [data-testid="stChatInput"] {{
        background-color: #242426 !important; /* 图二的高级深灰色 */
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 20px !important;
        padding: 4px 6px !important;
    }}

    /* 3. 杀掉 Streamlit 内部自带的恶心白底板和外发光 */
    [data-testid="stChatInput"] [data-baseweb="textarea"],
    [data-testid="stChatInput"] [data-baseweb="textarea"] > div {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}
    [data-testid="stChatInput"] [data-baseweb="textarea"]:focus-within {{
        box-shadow: none !important;
        background-color: transparent !important;
    }}

    /* 4. 打字区域：文字颜色与占位符 */
    [data-testid="stChatInput"] textarea {{
        color: #ffffff !important;
        caret-color: #ffffff !important;
        background-color: transparent !important;
        padding-left: 12px !important;
        margin-top: 4px !important;
    }}
    [data-testid="stChatInput"] textarea::placeholder {{
        color: #888888 !important; /* 图二的浅灰色提示字 */
    }}

        /* 5. 底部聊天输入框（地毯式轰炸：强杀黑条、白底、红边） */
    
    /* 1. 彻底干掉最底部那个违和的黑色大长条背景，让它完全透明，融入星空 */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div {{
        background-color: transparent !important;
        background-image: none !important;
        border: none !important;
    }}

    /* 2. 杀掉 Streamlit 自带的容器背景，重塑我们想要的高级深灰色 */
    [data-testid="stChatInput"] {{
        background-color: transparent !important;
    }}
    
    /* 这里才是真正包裹输入框的那一层，给它上色 */
    [data-testid="stChatInput"] > div {{
        background-color: #242426 !important; /* 图二的高级深灰色 */
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 20px !important;
        padding: 4px 6px !important;
    }}

    /* 3. 强制杀掉内部所有的白底、丑陋红边框、蓝边框和发光阴影！ */
    [data-testid="stChatInput"] * {{
        box-shadow: none !important; 
    }}
    
    [data-testid="stChatInput"] [data-baseweb="textarea"],
    [data-testid="stChatInput"] [data-baseweb="textarea"] > div {{
        background-color: transparent !important;
        border: none !important;
    }}
    
    /* 针对点击输入框时冒出来的红色/蓝色边框，进行致命一击 */
    [data-testid="stChatInput"] [data-baseweb="textarea"]:focus-within {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }}

    /* 4. 打字区域文字设置 */
    [data-testid="stChatInput"] textarea {{
        background-color: transparent !important;
        color: #ffffff !important; /* 你打的字变成白色 */
        caret-color: #ffffff !important; /* 光标变成白色 */
        padding-left: 12px !important;
        margin-top: 4px !important;
        border: none !important;
        outline: none !important;
    }}
    
    /* 提示词颜色 ("在这片星空中...") */
    [data-testid="stChatInput"] textarea::placeholder {{
        color: #888888 !important; 
    }}

    /* 5. 发送按钮：专属暗紫色 */
    [data-testid="stChatInputSubmitButton"] {{
        background-color: #382a47 !important; /* 图二的暗紫底色 */
        border-radius: 14px !important;
        height: 40px !important;
        width: 40px !important;
        margin-right: 4px !important;
        border: none !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    
    /* 发送按钮内的纸飞机颜色 */
    [data-testid="stChatInputSubmitButton"] svg {{
        fill: #9586aa !important;
        stroke: #9586aa !important;
    }}

    /* 发送按钮鼠标悬停效果 */
    [data-testid="stChatInputSubmitButton"]:hover {{
        background-color: #4a385d !important;
    }}
    [data-testid="stChatInputSubmitButton"]:hover svg {{
        fill: #ffffff !important;
        stroke: #ffffff !important;
    }}
    /* 按钮美化 */
    .stButton > button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 15px !important;
        transition: all 0.3s ease !important;
    }}
    /* ========== 6. 侧边栏组件美化：100% 消灭红色，蓝紫渐变风格 ========== */

    /* 🔹 侧边栏背景：蓝紫磨砂渐变 */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(20, 28, 70, 0.95), rgba(45, 25, 80, 0.95)) !important;
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(107, 147, 255, 0.25) !important;
    }}

    /* ====================================== */
    /* 🟣 第一部分：单选框（安慰风格） 蓝紫色清晰可见 */
    /* ====================================== */
    /* ✅ 最高优先级：直接修改单选框原生主题色，强制覆盖红色 */
    [data-testid="stSidebar"] input[type="radio"] {{
        accent-color: #6366f1 !important; /* 靛蓝色，足够清晰 */
    }}
    /* 未选中状态的外圈 */
    [data-testid="stSidebar"] [role="radio"] {{
        border-color: rgba(255,255,255, 0.35) !important;
    }}
    /* 选中状态：蓝紫色 + 发光效果，清晰醒目，干掉白色内点 */
    [data-testid="stSidebar"] [role="radio"][aria-checked="true"] {{
        background-color: #6366f1 !important;
        border-color: #6366f1 !important;
        box-shadow: 0 0 12px rgba(99, 102, 241, 0.6) !important;
    }}
    [data-testid="stSidebar"] [role="radio"][aria-checked="true"]::before {{
        background-color: #6366f1 !important; /* 把内部难看的白点也改成蓝色 */
    }}
    /* 选项文字颜色 */
    [data-testid="stSidebar"] [data-testid="stRadio"] p {{
        color: #e0e7ff !important;
        font-size: 15px !important;
    }}


    /* ====================================== */
    /* 🟣 第二部分：滑块（字数限制） 蓝紫渐变 */
    /* ====================================== */
    /* ✅ 干掉默认红色，替换为蓝紫渐变进度条 */
    [data-testid="stSidebar"] [data-testid="stSlider"] > div > div > div:first-child {{
        background: linear-gradient(90deg, #3b82f6, #8b5cf6) !important;
        height: 6px !important;
        border-radius: 3px !important;
        box-shadow: 0 0 12px rgba(99, 102, 241, 0.4) !important;
    }}
    /* ✅ 缩小滑块拖拽圆点，蓝紫色发光 */
    [data-testid="stSidebar"] div[role="slider"] {{
        background-color: #7c9dff !important;
        height: 26px !important;
        width: 26px !important;
        border: none !important;
        box-shadow: 0 0 16px rgba(99, 102, 241, 0.7) !important;
    }}
    /* ✅ 把红色的数值文字（比如 350字）改成蓝紫渐变 */
    [data-testid="stSidebar"] [data-testid="stSlider"] + div p {{
        background: linear-gradient(90deg, #60a5fa, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 500 !important;
        font-size: 18px !important;
    }}
    /* 滚动条 */
    ::-webkit-scrollbar {{ width: 5px; }}
    ::-webkit-scrollbar-thumb {{
        background: rgba(139, 125, 212, 0.3); border-radius: 10px;
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


def render_message(text: str, role: str, time_str: str = ""):
    """
    自定义聊天气泡：用户靠右，AI 靠左，无头像，带时间
    """
    if role == "user":
        align = "flex-end"
        bg_color = "rgba(40, 42, 54, 0.7)"
        border = "1px solid rgba(255, 255, 255, 0.1)"
    else:
        align = "flex-start"
        bg_color = (
            "linear-gradient(135deg, rgba(30, 20, 60, 0.8) 0%,"
            " rgba(40, 35, 90, 0.7) 100%)"
        )
        border = "1px solid rgba(100, 100, 255, 0.2)"

    html = f"""
    <div style="display: flex; flex-direction: column; align-items: {align};
                width: 100%; margin-bottom: 20px;">
        <div style="
            max-width: 75%;
            background: {bg_color};
            border: {border};
            backdrop-filter: blur(12px);
            padding: 14px 20px;
            border-radius: 20px;
            color: #ffffff;
            font-size: 15px;
            line-height: 1.6;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            font-family: 'Inter', 'PingFang SC', sans-serif;
        ">
            {text}
        </div>
        <div style="
            font-size: 11px;
            color: rgba(255, 255, 255, 0.4);
            margin-top: 6px;
            margin-left: 10px;
            margin-right: 10px;
        ">
            {time_str}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
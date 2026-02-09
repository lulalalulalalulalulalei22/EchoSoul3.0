# ui_style.py
# 统一管理 EchoSoul 的背景 + 侧边栏 + 聊天气泡 + 输入框样式

import streamlit as st
import base64
import os
from typing import Optional


def _img_to_b64(path: str) -> Optional[str]:
    """把本地图片转成 base64，做背景用；读不到就返回 None。"""
    if not path or not os.path.exists(path):
        return None
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        return None


def apply_theme(bg_image: Optional[str] = None) -> None:
    """
    应用 EchoSoul 的整体 UI 主题：
    - 右侧主区域：星空背景（图片或渐变兜底）
    - 聊天气泡：深蓝长条气泡（覆盖 stChatMessage）
    - 左侧侧边栏：深色背景 + 白字 + 白底黑字输入框
    - 底部聊天输入框：白底黑字
    - 按钮 / 滚动条 / 菜单隐藏 等
    """
    b64 = _img_to_b64(bg_image) if bg_image else None

    if b64:
        bg_css = f"""
        .stApp {{
            background: url("data:image/png;base64,{b64}") center/cover fixed no-repeat !important;
        }}
        """
    else:
        # 没有背景图时的深邃星空渐变保底
        bg_css = """
        .stApp {
            background: radial-gradient(circle at 50% 50%, #1a1a3a 0%, #0f0c29 100%) !important;
            background-attachment: fixed;
        }
        """

    css = f"""
    <style>
    /* 1. 整体背景 */
    {bg_css}

    /* 叠一层轻微暗罩，增加层次感 */
    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        background: radial-gradient(circle at 20% 0%, rgba(66, 82, 178, 0.35), transparent 45%),
                    radial-gradient(circle at 80% 100%, rgba(24, 60, 150, 0.55), transparent 40%),
                    rgba(0, 0, 0, 0.35);
        pointer-events: none;
        z-index: 0;
    }}

    .block-container {{
        position: relative;
        z-index: 1;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }}

    /* 2. 全局文字颜色 */
    .stApp, .stMarkdown, p, li, label, h1, h2, h3 {{
        color: #e0e0ff !important;
        font-weight: 300 !important;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
    }}

    /* 3. 顶部 Header 透明 */
    [data-testid="stHeader"] {{
        background: transparent !important;
        box-shadow: none !important;
    }}

    /* 4. 侧边栏样式（背景 + 白底黑字输入框） */
    section[data-testid="stSidebar"] {{
        background: rgba(15, 12, 41, 0.8) !important;
        border-right: 1px solid rgba(139, 125, 212, 0.3) !important;
        backdrop-filter: blur(16px);
    }}

    /* 侧边栏标题 / 文本颜色 */
    section[data-testid="stSidebar"] * {{
        color: #e3e7ff !important;
    }}

    /* 侧边栏输入框：白底黑字 */
    section[data-testid="stSidebar"] .stTextInput input {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #8b7dd4 !important;
        border-radius: 10px !important;
        caret-color: #000000 !important;
    }}

    /* 5. 底部聊天输入框：白底黑字 */
    .stChatInputContainer {{
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #8b7dd4 !important;
        border-radius: 25px !important;
        padding: 5px !important;
    }}

    .stChatInputContainer textarea {{
        color: #000000 !important;
        caret-color: #000000 !important;
    }}

    /* 6. 聊天气泡样式（覆盖 stChatMessage） */
    .stChatMessage {{
        background: rgba(17, 19, 40, 0.92) !important;
        border-radius: 24px !important;
        padding: 15px 24px !important;
        margin: 18px 0 !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.6) !important;
    }}

    /* 聊天气泡内部文字 */
    .stChatMessage div[data-testid="stChatMessageContent"] {{
        color: #f4f5ff !important;
        font-size: 15px;
        line-height: 1.6;
    }}

    /* 你如果还想区分用户 / AI 的颜色，可以按 role 加判断再写更精细的 CSS，
       或用 nth-child(odd/even)，和你之前那段类似 */

    /* 7. 按钮美化（全局 st.button） */
    .stButton > button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 15px !important;
        transition: all 0.3s ease !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.45);
    }}

    /* 8. 隐藏 Streamlit 菜单 / footer */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* 9. 滚动条美化 */
    ::-webkit-scrollbar {{ width: 5px; }}
    ::-webkit-scrollbar-thumb {{ background: rgba(139, 125, 212, 0.3); border-radius: 10px; }}
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)
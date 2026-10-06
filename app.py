import streamlit as st
import random
import time
import os
from PIL import Image

# Cấu hình trang
st.set_page_config(page_title="Oẳn Tù Tì với AN NHI", page_icon="💖", layout="centered")

# Nhạc nền tự động
AUDIO_URL = "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=game-music-7408.mp3"
st.markdown(f"""
    <audio autoplay loop hidden>
        <source src="{AUDIO_URL}" type="audio/mp3">
    </audio>
""", unsafe_allow_html=True)

# Khởi tạo trạng thái game (Session State)
if 'p1_hp' not in st.session_state:
    st.session_state.p1_hp = 100
if 'cpu_hp' not in st.session_state:
    st.session_state.cpu_hp = 100
if 'last_p1_move' not in st.session_state:
    st.session_state.last_p1_move = "✊"
if 'last_cpu_move' not in st.session_state:
    st.session_state.last_cpu_move = "✊"
if 'result_text' not in st.session_state:
    st.session_state.result_text = "Thách bạn thắng được AN NHI đấy! 😏"

MOVES = {
    "Búa (A)": "✊",
    "Bao (S)": "✋",
    "Kéo (D)": "✌️"
}

# Thuật toán gian lận: Tỷ lệ thắng P1 chỉ 10%
def get_an_nhi_move(p1_move):
    r = random.random()
    # 10% P1 Thắng (AN NHI ra nước bị khắc chế)
    if r < 0.10:
        if p1_move == "✊": return "✌️"
        if p1_move == "✋": return "✊"
        if p1_move == "✌️": return "✋"
    # 10% Hòa
    elif r < 0.20:
        return p1_move
    # 80% AN NHI Thắng (AN NHI bắt bài P1)
    else:
        if p1_move == "✊": return "✋"
        if p1_move == "✋": return "✌️"
        if p1_move == "✌️": return "✊"

def play(user_choice_key):
    if st.session_state.p1_hp <= 0 or st.session_state.cpu_hp <= 0:
        return

    p1_move = MOVES[user_choice_key]
    cpu_move = get_an_nhi_move(p1_move)

    # Hiệu ứng đếm ngược 1... 2... 3...
    countdown_box = st.empty()
    for count in ["1...", "2...", "3...", "RA CHIÊU! 💥"]:
        countdown_box.markdown(f"""
            <div style="text-align: center; font-size: 40px; font-weight: bold; color: yellow; text-shadow: 2px 2px 4px #000;">
                {count}
            </div>
        """, unsafe_allow_html=True)
        time.sleep(0.4)
    countdown_box.empty()

    st.session_state.last_p1_move = p1_move
    st.session_state.last_cpu_move = cpu_move

    # Xử lý kết quả
    if p1_move == cpu_move:
        st.session_state.result_text = "🤝 HÒA RỒI! AN NHI tha cho bạn hiệp này!"
    elif (p1_move == "✊" and cpu_move == "✌️") or \
         (p1_move == "✋" and cpu_move == "✊") or \
         (p1_move == "✌️" and cpu_move == "✋"):
        damage = random.randint(15, 25)
        st.session_state.cpu_hp = max(0, st.session_state.cpu_hp - damage)
        st.session_state.result_text = f"🔥 HỮU DUYÊN! Bạn hên thắng được AN NHI! Gây {damage} sát thương!"
    else:
        damage = random.randint(20, 30)
        st.session_state.p1_hp = max(0, st.session_state.p1_hp - damage)
        st.session_state.result_text = f"💥 AN NHI BẮT BÀI! Bạn bị vả {damage} HP!"

def reset_game():
    st.session_state.p1_hp = 100
    st.session_state.cpu_hp = 100
    st.session_state.last_p1_move = "✊"
    st.session_state.last_cpu_move = "✊"
    st.session_state.result_text = "Ván mới bắt đầu! Cố lên nhé!"

# CSS Giao diện Nền Hồng Cánh Sen & Thiết kế Avatar
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #FF1493 0%, #FF69B4 50%, #FFB6C1 100%);
    }
    .header-title {
        text-align: center;
        font-weight: 900;
        font-size: 34px;
        color: #FFFFFF;
        text-shadow: 3px 3px 6px #8B008B;
        margin-bottom: 15px;
    }
    .hp-bar-container {
        background-color: #555;
        border-radius: 12px;
        border: 2px solid #FFF;
        overflow: hidden;
        height: 22px;
        margin-top: 5px;
    }
    .hp-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #00FF7F, #3CB371);
        transition: width 0.3s ease;
    }
    .hand-display {
        font-size: 90px;
        text-align: center;
    }
    .result-box {
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #C71585;
        padding: 12px;
        background-color: #FFF0F5;
        border-radius: 15px;
        border: 2px solid #FF1493;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        margin: 15px 0;
    }
    .avatar-img img {
        border-radius: 50%;
        border: 4px solid white;
        object-fit: cover;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-title">💖 OẮN TÙ TÌ CÙNG AN NHI 💖</div>', unsafe_allow_html=True)

# Hiển thị Avatar & Thanh Máu
col1, col_mid, col2 = st.columns([4, 1, 4])

with col1:
    st.markdown("<h3 style='color: white; text-align: center;'>🐶 P1 (BẠN)</h3>", unsafe_allow_html=True)
    if os.path.exists("p1.jpg"):
        st.image("p1.jpg", use_container_width=True)
    st.markdown(f"""
    <div class="hp-bar-container">
        <div class="hp-bar-fill" style="width: {st.session_state.p1_hp}%;"></div>
    </div>
    <p style="text-align: center; font-weight: bold; color: white;">HP: {st.session_state.p1_hp}/100</p>
    """, unsafe_allow_html=True)

with col_mid:
    st.markdown("<h2 style='text-align: center; color: yellow; margin-top: 50px;'>VS</h2>", unsafe_allow_html=True)

with col2:
    st.markdown("<h3 style='color: white; text-align: center;'>👧 AN NHI</h3>", unsafe_allow_html=True)
    if os.path.exists("cpu.jpg"):
        st.image("cpu.jpg", use_container_width=True)
    st.markdown(f"""
    <div class="hp-bar-container">
        <div class="hp-bar-fill" style="width: {st.session_state.cpu_hp}%;"></div>
    </div>
    <p style="text-align: center; font-weight: bold; color: white;">HP: {st.session_state.cpu_hp}/100</p>
    """, unsafe_allow_html=True)

st.divider()

# Hiển thị Nước đi
hand_col1, hand_col2 = st.columns(2)
with hand_col1:
    st.markdown(f'<div class="hand-display">{st.session_state.last_p1_move}</div>', unsafe_allow_html=True)
with hand_col2:
    st.markdown(f'<div class="hand-display" style="transform: scaleX(-1);">{st.session_state.last_cpu_move}</div>', unsafe_allow_html=True)

# Hiển thị Kết quả
st.markdown(f'<div class="result-box">{st.session_state.result_text}</div>', unsafe_allow_html=True)

# Thắng / Thua
if st.session_state.p1_hp <= 0:
    st.error("💀 BẠN ĐÃ THUA AN NHI TÂM PHỤC KHẨU PHỤC!")
    st.snow()
    if st.button("Chơi lại để gỡ gạc 🔄", use_container_width=True):
        reset_game()
        st.rerun()
elif st.session_state.cpu_hp <= 0:
    st.success("🎉 BÁ ĐẠO! Bạn đã đánh bại AN NHI (dù tỷ lệ thắng chỉ 10%)!")
    st.balloons()
    if st.button("Chơi ván nữa 🔄", use_container_width=True):
        reset_game()
        st.rerun()
else:
    st.markdown("<h4 style='color: white; text-align: center;'>🎯 Chọn nước đi của bạn:</h4>", unsafe_allow_html=True)
    btn1, btn2, btn3 = st.columns(3)

    with btn1:
        if st.button("✊ Búa (A)", use_container_width=True):
            play("Búa (A)")
            st.rerun()
    with btn2:
        if st.button("✋ Bao (S)", use_container_width=True):
            play("Bao (S)")
            st.rerun()
    with btn3:
        if st.button("✌️ Kéo (D)", use_container_width=True):
            play("Kéo (D)")
            st.rerun()

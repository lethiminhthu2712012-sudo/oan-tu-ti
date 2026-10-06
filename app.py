import streamlit as st
import random
import time

# Cấu hình trang
st.set_page_config(page_title="Oẳn Tù Tì Đối Kháng", page_icon="✊", layout="centered")

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
    st.session_state.result_text = "Hãy chọn chiêu để bắt đầu!"

MOVES = {
    "Búa (A)": {"icon": "✊", "name": "Búa"},
    "Bao (S)": {"icon": "✋", "name": "Bao"},
    "Kéo (D)": {"icon": "✌️", "name": "Kéo"}
}

def play(user_choice_key):
    if st.session_state.p1_hp <= 0 or st.session_state.cpu_hp <= 0:
        return

    p1_move = MOVES[user_choice_key]["icon"]
    cpu_move_key = random.choice(list(MOVES.keys()))
    cpu_move = MOVES[cpu_move_key]["icon"]

    st.session_state.last_p1_move = p1_move
    st.session_state.last_cpu_move = cpu_move

    # Xử lý kết quả
    if p1_move == cpu_move:
        st.session_state.result_text = "🤝 HÒA RỒI!"
    elif (p1_move == "✊" and cpu_move == "✌️") or \
         (p1_move == "✋" and cpu_move == "✊") or \
         (p1_move == "✌️" and cpu_move == "✋"):
        damage = random.randint(15, 25)
        st.session_state.cpu_hp = max(0, st.session_state.cpu_hp - damage)
        st.session_state.result_text = f"🔥 BẠN THẮNG! Gây {damage} sát thương lên CPU!"
    else:
        damage = random.randint(15, 25)
        st.session_state.p1_hp = max(0, st.session_state.p1_hp - damage)
        st.session_state.result_text = f"💥 CPU THẮNG! Bạn bị trừ {damage} HP!"

def reset_game():
    st.session_state.p1_hp = 100
    st.session_state.cpu_hp = 100
    st.session_state.last_p1_move = "✊"
    st.session_state.last_cpu_move = "✊"
    st.session_state.result_text = "Game mới đã bắt đầu!"

# Tùy chỉnh CSS giao diện game đối kháng
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #87CEEB 0%, #E0F6FF 100%);
    }
    .header-title {
        text-align: center;
        font-weight: bold;
        font-size: 32px;
        color: #1E3A8A;
        margin-bottom: 10px;
    }
    .hp-bar-container {
        background-color: #ddd;
        border-radius: 10px;
        border: 2px solid #333;
        overflow: hidden;
        height: 25px;
    }
    .hp-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #10B981, #059669);
        transition: width 0.3s ease;
    }
    .hand-display {
        font-size: 100px;
        text-align: center;
    }
    .result-box {
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        padding: 10px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-title">OẮN TÙ TÌ 3 - ĐỐI KHÁNG</div>', unsafe_allow_html=True)

# Thanh Máu (Health Bars)
col1, col_mid, col2 = st.columns([4, 1, 4])

with col1:
    st.markdown("### 🥷 P1 (BẠN)")
    st.markdown(f"""
    <div class="hp-bar-container">
        <div class="hp-bar-fill" style="width: {st.session_state.p1_hp}%;"></div>
    </div>
    <p style="text-align: right; font-weight: bold;">HP: {st.session_state.p1_hp}/100</p>
    """, unsafe_allow_html=True)

with col_mid:
    st.markdown("<h2 style='text-align: center;'>VS</h2>", unsafe_allow_html=True)

with col2:
    st.markdown("### 🤖 CPU")
    st.markdown(f"""
    <div class="hp-bar-container">
        <div class="hp-bar-fill" style="width: {st.session_state.cpu_hp}%;"></div>
    </div>
    <p style="text-align: left; font-weight: bold;">HP: {st.session_state.cpu_hp}/100</p>
    """, unsafe_allow_html=True)

st.divider()

# Hiển thị bàn tay ra chiêu
hand_col1, hand_col2 = st.columns(2)
with hand_col1:
    st.markdown(f'<div class="hand-display">{st.session_state.last_p1_move}</div>', unsafe_allow_html=True)
with hand_col2:
    # Lật ngược icon bàn tay của CPU cho giống đối kháng
    st.markdown(f'<div class="hand-display" style="transform: scaleX(-1);">{st.session_state.last_cpu_move}</div>', unsafe_allow_html=True)

# Hiển thị thông báo kết quả
st.markdown(f'<div class="result-box">{st.session_state.result_text}</div>', unsafe_allow_html=True)

# Kiểm tra thắng/thua
if st.session_state.p1_hp <= 0:
    st.error("💀 BẠN ĐÃ THẤT BẠI!")
    st.balloons()
    if st.button("Chơi lại 🔄", use_container_width=True):
        reset_game()
        st.rerun()
elif st.session_state.cpu_hp <= 0:
    st.success("🏆 BẠN ĐÃ CHIẾN THẮNG CPU!")
    st.balloons()
    if st.button("Chơi lại 🔄", use_container_width=True):
        reset_game()
        st.rerun()
else:
    # Các nút chọn nước đi
    st.markdown("### 🎯 Chọn chiêu của bạn:")
    btn_col1, btn_col2, btn_col3 = st.columns(3)

    with btn_col1:
        if st.button("✊ Búa (A)", use_container_width=True):
            play("Búa (A)")
            st.rerun()
    with btn_col2:
        if st.button("✋ Bao (S)", use_container_width=True):
            play("Bao (S)")
            st.rerun()
    with btn_col3:
        if st.button("✌️ Kéo (D)", use_container_width=True):
            play("Kéo (D)")
            st.rerun()
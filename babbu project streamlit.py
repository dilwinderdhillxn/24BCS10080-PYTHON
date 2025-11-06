import streamlit as st
import random
import time
from datetime import datetime


# ---------------- Page config (must be first Streamlit call) ----------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
        
        /* ROOT VARIABLES */
        :root {
            --vibrant-blue: #2a5298; /* Soft Blue */
            --deep-purple: #6a1b9a; /* Purple */
            --neon-pink: #ff006e;  /* Vibrant Pink */
            --electric-blue: #00bcd4; /* Electric Blue */
            --neon-green: #39ff14; /* Neon Green */
            --white: #ffffff; /* Pure White */
            --soft-blue: #1e3c72; /* Smooth Blue */
        }

        /* SOLID BACKGROUND GRADIENT */
        /* SEXY, ATTRACTIVE BACKGROUND */
.stApp {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(270deg, #1e3c72, #2a5298, #6a1b9a, #ff006e, #00bcd4);
    background-size: 1000% 1000%;
    animation: gradientShift 20s ease infinite;
}

/* ANIMATION FOR MOVING GRADIENT */
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

        /* GLASSMORPHISM CONTAINER */
        .glass-container {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 32px;
            margin: 20px 0;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            transition: all 0.3s ease;
        }

        .glass-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 48px 0 rgba(31, 38, 135, 0.5);
        }

        /* HEADER STYLING */
        .app-header {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 60px 20px;
            margin-bottom: 40px;
            background: rgba(255, 255, 255, 0.15); /* Transparent white background */
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
            animation: fadeInDown 1s ease-out;
            position: relative;
            overflow: hidden;
        }

        
        @keyframes textGlow {
            from { filter: drop-shadow(0 0 5px var(--neon-pink)); }
            to { filter: drop-shadow(0 0 20px var(--neon-green)); }
        }

        /* NUMBER GUESSING GAME FONT (STYLISH) */
        .game-title {
            font-size: 40px;
            font-weight: 700;
            text-transform: uppercase;
            color: var(--white);
            letter-spacing: 1px;
            margin-top: 20px;
            text-align: center;
            font-family: "Gill Sans", sans-serif;
            /* Simple & Bold */
        }

        /* HEADER ENTRY ANIMATION */
        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* BUTTON STYLING */
        .stButton > button {
            background: linear-gradient(135deg, var(--neon-pink) 0%, var(--electric-blue) 100%);
            color: var(--white);
            border: none;
            border-radius: 16px;
            padding: 14px 32px;
            font-weight: 800;
            font-size: 18px;
            box-shadow: 0 4px 20px rgba(255, 0, 123, 0.3);
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(255, 0, 123, 0.6);
        }

        .stButton > button:active {
            transform: translateY(0);
        }

        /* RESPONSIVE ADJUSTMENTS */
        @media (max-width: 768px) {
            .title { font-size: 48px; }
            .glass-container { padding: 20px; }
            .stat-value { font-size: 22px; }
            .app-header img { max-width: 150px; }
            .game-title { font-size: 28px; }
        }

    </style>
    """,
    unsafe_allow_html=True,
)





# ---------------- Difficulty settings ----------------
difficulty_config = {
    "🟢 Easy": {"range": (1, 50), "hints": 3, "max_attempts": 10, "emoji": "🟢"},
    "🟡 Medium": {"range": (1, 100), "hints": 4, "max_attempts": 12, "emoji": "🟡"},
    "🔴 Hard": {"range": (1, 200), "hints": 6, "max_attempts": 15, "emoji": "🔴"}
}


# ---------------- Session state init ----------------
def init_session():
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = "🟡 Medium"
    if "secret_number" not in st.session_state:
        st.session_state.secret_number = None
    if "attempts" not in st.session_state:
        st.session_state.attempts = 0
    if "guess_history" not in st.session_state:
        st.session_state.guess_history = []
    if "message" not in st.session_state:
        st.session_state.message = ""
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "hints_left" not in st.session_state:
        st.session_state.hints_left = difficulty_config[st.session_state.difficulty]["hints"]
    if "max_attempts" not in st.session_state:
        st.session_state.max_attempts = difficulty_config[st.session_state.difficulty]["max_attempts"]
    if "best_scores" not in st.session_state:
        st.session_state.best_scores = {"🟢 Easy": "N/A", "🟡 Medium": "N/A", "🔴 Hard": "N/A"}
    if "leaderboard" not in st.session_state:
        st.session_state.leaderboard = []
    if "wins" not in st.session_state:
        st.session_state.wins = 0
    if "losses" not in st.session_state:
        st.session_state.losses = 0
    if "guess_input" not in st.session_state:
        st.session_state.guess_input = 1
    if "closeness" not in st.session_state:
        st.session_state.closeness = 0
    if st.session_state.secret_number is None:
        reset_game(initial=True)


# ---------------- Reset / Start game ----------------
def reset_game(initial=False):
    difficulty = st.session_state.get("difficulty", "🟡 Medium")
    min_val, max_val = difficulty_config[difficulty]["range"]
    st.session_state.secret_number = random.randint(min_val, max_val)
    st.session_state.attempts = 0
    st.session_state.guess_history = []
    st.session_state.message = ""
    st.session_state.game_over = False
    st.session_state.hints_left = difficulty_config[difficulty]["hints"]
    st.session_state.max_attempts = difficulty_config[difficulty]["max_attempts"]
    st.session_state.guess_input = 1
    st.session_state.closeness = 0
    if not initial:
        st.success("✨ New game started! Good luck!")


# ---------------- Hint generator with better logic ----------------
def give_hint():
    if st.session_state.game_over:
        return "🎮 Game already finished — start new game to get hints."
    if st.session_state.hints_left <= 0:
        return "❌ No hints left! You're on your own now."
    
    st.session_state.hints_left -= 1
    secret = st.session_state.secret_number
    min_val, max_val = difficulty_config[st.session_state.difficulty]["range"]
    
    # Multiple hint types for variety
    hint_type = st.session_state.hints_left % 3
    
    if hint_type == 0:
        # Range hint
        span = max_val - min_val
        margin = max(1, span // 6)
        low = max(min_val, secret - margin)
        high = min(max_val, secret + margin)
        return f"💡 The number is between **{low}** and **{high}**. (Hints left: {st.session_state.hints_left})"
    
    elif hint_type == 1:
        # Parity hint
        if secret % 2 == 0:
            return f"💡 The number is **even**. (Hints left: {st.session_state.hints_left})"
        else:
            return f"💡 The number is **odd**. (Hints left: {st.session_state.hints_left})"
    
    else:
        # Divisibility hint
        for div in [5, 3, 7]:
            if secret % div == 0:
                return f"💡 The number is divisible by **{div}**. (Hints left: {st.session_state.hints_left})"
        
        # Last digit hint
        last_digit = secret % 10
        return f"💡 The last digit is **{last_digit}**. (Hints left: {st.session_state.hints_left})"


# ---------------- Calculate closeness (temperature) ----------------
def calculate_closeness(guess, secret, min_val, max_val):
    distance = abs(guess - secret)
    max_distance = max_val - min_val
    closeness = max(0, 100 - (distance / max_distance * 100))
    return closeness


# ---------------- Initialize ----------------
init_session()


# ---------------- Header ----------------
svg_url = "https://vectorseek.com/wp-content/uploads/2023/09/Chandigarh-University-CU-Logo-Vector.svg-.png"
st.markdown(
    f"""
    <div class="app-header">
        <img src="{svg_url}" width="120" />
        <div>
            <h1 class="title">🎯 Number Guessing Game</h1>
            <div class="subtitle">Made by <b>Dilwinder Singh</b> • Chandigarh University</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------- Main Glass Container ----------------
st.markdown("<div class='glass-container'>", unsafe_allow_html=True)


# ---------------- Controls Row ----------------
col_a, col_b, col_c = st.columns([3, 2, 2])

with col_a:
    new_diff = st.selectbox(
        "🎚️ Select Difficulty Level",
        list(difficulty_config.keys()),
        index=list(difficulty_config.keys()).index(st.session_state.difficulty),
        help="Choose your challenge level"
    )
    if new_diff != st.session_state.difficulty:
        st.session_state.difficulty = new_diff
        reset_game()

with col_b:
    if st.button("🔄 New Game", use_container_width=True):
        reset_game()

with col_c:
    if st.button("💡 Hint", use_container_width=True):
        hint_text = give_hint()
        st.info(hint_text)


# ---------------- Info Box ----------------
min_val, max_val = difficulty_config[st.session_state.difficulty]["range"]
st.markdown(
    f"<div class='info-box'>🎲 Guess a number between <b>{min_val}</b> and <b>{max_val}</b></div>",
    unsafe_allow_html=True
)


# ---------------- Closeness Meter (Temperature Gauge) ----------------
if st.session_state.closeness > 0:
    st.write("🌡️ **Temperature Meter**")
    progress_color = "🔥" if st.session_state.closeness > 80 else "🔸" if st.session_state.closeness > 50 else "🧊"
    st.progress(st.session_state.closeness / 100)
    
    if st.session_state.closeness > 90:
        st.markdown("**🔥 On Fire! You're extremely close!**")
    elif st.session_state.closeness > 70:
        st.markdown("**🌟 Getting hot! Very close!**")
    elif st.session_state.closeness > 50:
        st.markdown("**🔸 Warm! You're making progress.**")
    elif st.session_state.closeness > 30:
        st.markdown("**❄️ Cool. Keep trying!**")
    else:
        st.markdown("**🧊 Ice cold! Way off.**")


# ---------------- Input Section ----------------
st.markdown("---")
guess = st.number_input(
    "📝 Your Guess",
    min_value=min_val,
    max_value=max_val,
    value=st.session_state.guess_input,
    step=1,
    key="guess_input",
    help="Enter your guess here"
)


# ---------------- Action Buttons ----------------
col1, col2 = st.columns([3, 1])

with col1:
    submit = st.button("✅ Submit Guess", use_container_width=True, type="primary")

with col2:
    reveal = st.button("🔎 Reveal", use_container_width=True)

if reveal:
    st.info(f"🔍 Secret: **{st.session_state.secret_number}**")


# ---------------- Game Logic ----------------
if submit and not st.session_state.game_over:
    st.session_state.attempts += 1
    st.session_state.guess_history.append(guess)
    
    # Calculate closeness
    st.session_state.closeness = calculate_closeness(guess, st.session_state.secret_number, min_val, max_val)
    
    # Comparison
    if guess < st.session_state.secret_number:
        difference = st.session_state.secret_number - guess
        if difference > 20:
            st.session_state.message = "📉 Way too low! Try much higher!"
        else:
            st.session_state.message = "📉 A bit low! Try a higher number!"
    
    elif guess > st.session_state.secret_number:
        difference = guess - st.session_state.secret_number
        if difference > 20:
            st.session_state.message = "📈 Way too high! Try much lower!"
        else:
            st.session_state.message = "📈 A bit high! Try a lower number!"
    
    else:
        # WIN!
        st.session_state.message = f"🎉 **CORRECT!** You found it in **{st.session_state.attempts}** attempts!"
        st.session_state.game_over = True
        st.session_state.wins += 1
        
        # Update best score
        current_best = st.session_state.best_scores.get(st.session_state.difficulty, "N/A")
        if current_best == "N/A" or st.session_state.attempts < current_best:
            st.session_state.best_scores[st.session_state.difficulty] = st.session_state.attempts
        
        # Update leaderboard
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.leaderboard.append({
            "attempts": st.session_state.attempts,
            "time": now,
            "difficulty": st.session_state.difficulty
        })
        st.session_state.leaderboard = sorted(st.session_state.leaderboard, key=lambda x: x["attempts"])[:10]
    
    # Check max attempts loss
    if (not st.session_state.game_over) and (st.session_state.attempts >= st.session_state.max_attempts):
        st.session_state.message = f"❌ **Game Over!** Out of attempts. The number was **{st.session_state.secret_number}**."
        st.session_state.game_over = True
        st.session_state.losses += 1


# ---------------- Feedback Display ----------------
if st.session_state.message:
    if st.session_state.game_over and "CORRECT" in st.session_state.message:
        st.markdown(f"<div class='success-message'>{st.session_state.message}</div>", unsafe_allow_html=True)
        st.balloons()
        
        # Celebration animation
        prog = st.progress(0)
        for i in range(0, 101, 5):
            time.sleep(0.02)
            prog.progress(i)
        prog.empty()
    
    elif st.session_state.game_over:
        st.error(st.session_state.message)
    
    else:
        st.markdown(f"<div class='warning-message'>{st.session_state.message}</div>", unsafe_allow_html=True)


# ---------------- Statistics Section ----------------
st.markdown("---")
st.markdown("### 📊 Game Statistics")

stat_col1, stat_col2, stat_col3 = st.columns(3)

with stat_col1:
    st.markdown(
        f"""
        <div class='stat-card'>
            <div class='stat-label'>Attempts</div>
            <div class='stat-value'>{st.session_state.attempts}/{st.session_state.max_attempts}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with stat_col2:
    st.markdown(
        f"""
        <div class='stat-card'>
            <div class='stat-label'>Hints Left</div>
            <div class='stat-value'>💡 {st.session_state.hints_left}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with stat_col3:
    win_rate = (st.session_state.wins / max(1, st.session_state.wins + st.session_state.losses)) * 100
    st.markdown(
        f"""
        <div class='stat-card'>
            <div class='stat-label'>Win Rate</div>
            <div class='stat-value'>{win_rate:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------- Guess History ----------------
if st.session_state.guess_history:
    st.markdown("### 📜 Your Guesses")
    history_display = " → ".join([f"**{g}**" for g in st.session_state.guess_history])
    st.markdown(history_display)


# ---------------- Win/Loss Record ----------------
st.markdown("### 🏆 Your Record")
record_col1, record_col2 = st.columns(2)

with record_col1:
    st.markdown(
        f"""
        <div class='stat-card'>
            <div class='stat-label'>✅ Wins</div>
            <div class='stat-value' style='color: #38ef7d;'>{st.session_state.wins}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with record_col2:
    st.markdown(
        f"""
        <div class='stat-card'>
            <div class='stat-label'>❌ Losses</div>
            <div class='stat-value' style='color: #f45c43;'>{st.session_state.losses}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------- Best Scores ----------------
st.markdown("### 🏆 Best Scores")
best_scores_data = []
for diff, score in st.session_state.best_scores.items():
    emoji = difficulty_config[diff]["emoji"]
    best_scores_data.append({"Difficulty": f"{emoji} {diff}", "Best Score": score})

if best_scores_data:
    st.table(best_scores_data)


# ---------------- Leaderboard ----------------
if st.session_state.leaderboard:
    st.markdown("### 🥇 Leaderboard (Top 10)")
    lb_rows = []
    for idx, item in enumerate(st.session_state.leaderboard, start=1):
        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
        lb_rows.append({
            "Rank": medal,
            "Attempts": item["attempts"],
            "Difficulty": item["difficulty"],
            "Date": item["time"]
        })
    st.table(lb_rows)


st.markdown("</div>", unsafe_allow_html=True)


# ---------------- Footer ----------------
st.markdown(
    """
    <div class='footer'>
        <p>Made with ❤️ by <b>Dilwinder Singh</b></p>
        <p>🎓 Computer Science Student • Chandigarh University</p>
        <p style='font-size: 13px; opacity: 0.8;'>Enhanced with modern UI/UX design trends 2025</p>
    </div>
    """,
    unsafe_allow_html=True
)
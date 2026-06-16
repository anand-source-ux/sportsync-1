import streamlit as st
import pandas as pd
import uuid
import qrcode
from PIL import Image
import os

st.set_page_config(
    page_title="SportSync",
    page_icon="🏆",
    layout="wide"
)
st.markdown("""
<style>

div[data-testid="metric-container"] {
    background-color: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 50px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)
# ---------------------------
# Initialize Files
# ---------------------------

if not os.path.exists("bookings.csv"):
    pd.DataFrame(columns=[
        "BookingCode",
        "Username",
        "Role",
        "Sport",
        "Date",
        "Slot"
    ]).to_csv("bookings.csv", index=False)

if not os.path.exists("performance.csv"):
    pd.DataFrame(columns=[
        "BookingCode",
        "Sport",
        "PerformanceData",
        "CoachInsights"
    ]).to_csv("performance.csv", index=False)

# ---------------------------
# App Title
# ---------------------------

st.markdown("""
<div style='text-align:center;padding:20px;'>

<h1 style='color:#00C896;'>
🏆 SportSync
</h1>

<h3>
Train • Track • Triumph
</h3>

<p>
Book facilities, monitor progress, and level up your game.
</p>

</div>
""", unsafe_allow_html=True)

# ---------------------------
# Login Page
# ---------------------------

with st.sidebar:

    st.markdown("## 🏆 SportSync")

    choice = st.selectbox(
        "Navigate",
        [
            "🔐 Login",
            "📅 Book Slot",
            "📈 Track Performance"
        ]
    )

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if choice == "🔐 Login":

    st.header("Login Portal")

    role = st.selectbox(
        "Choose Portal",
        ["Student", "Coach"]
    )

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role
            st.success(f"Welcome {username}!")
        else:
            st.error("Enter username and password")

# ---------------------------
# Book Slot
# ---------------------------

elif choice == "📅 Book Slot":
    st.header("📊 Dashboard")
    st.success(
        f"🔥 Welcome back, {st.session_state.username}! Ready to train today?"
    )
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🏆 Total Bookings",
            len(pd.read_csv("bookings.csv"))
        )

    with col2:
        st.metric(
            "👤 Active User",
            st.session_state.username
        )

    with col3:
        st.metric(
            "🎯 Sports Available",
            8
        )

    st.markdown("---")
    if not st.session_state.logged_in:
        st.warning("Please login first")
        st.stop()

    st.header("📅 Book Sports Facility")

    sports = [
        "🏀 Basketball",
        "⚽ Football",
        "🏏 Cricket",
        "🏋️ Gym",
        "🏊 Swimming",
        "🏓 Table Tennis",
        "🎾 Tennis",
        "🎱 Snooker"
    ]
    
    sport = st.selectbox("Select Sport", sports)

    booking_date = st.date_input("Date")

    slot = st.selectbox(
        "Time Slot",
        [
            "6AM-7AM",
            "7AM-8AM",
            "4PM-5PM",
            "5PM-6PM",
            "6PM-7PM"
        ]
    )

    bookings = pd.read_csv("bookings.csv")

    slot_count = len(
        bookings[
            (bookings["Sport"] == sport)
            & (bookings["Date"] == str(booking_date))
            & (bookings["Slot"] == slot)
        ]
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "👥 Players Registered",
            slot_count
        )

    with col2:
        st.metric(
            "🎯 Available Spots",
            20 - slot_count
        )

    st.progress(slot_count / 20)
    if slot_count >= 20:
        st.error("Slot Full!")
    else:
        if st.button("Book Slot"):

            booking_code = str(uuid.uuid4())[:8]

            new_booking = pd.DataFrame({
                "BookingCode":[booking_code],
                "Username":[st.session_state.username],
                "Role":[st.session_state.role],
                "Sport":[sport],
                "Date":[str(booking_date)],
                "Slot":[slot]
            })

            bookings = pd.concat(
                [bookings, new_booking],
                ignore_index=True
            )

            bookings.to_csv("bookings.csv", index=False)

            # QR Code Generation
            qr = qrcode.make(booking_code)
            qr_file = f"{booking_code}.png"
            qr.save(qr_file)

            st.success("Booking Successful!")

            st.write("Booking Code:")
            st.code(booking_code)

            st.image(qr_file, width=200)

# ---------------------------
# Track Performance
# ---------------------------

elif choice == "📈 Track Performance":

    if not st.session_state.logged_in:
        st.warning("Please login first")
        st.stop()

    st.header("📈 Performance Tracker")

    booking_code = st.text_input("Enter Booking Code")

    bookings = pd.read_csv("bookings.csv")

    if booking_code:

        booking_match = bookings[
            bookings["BookingCode"] == booking_code
        ]

        if len(booking_match) > 0:

            sport = booking_match.iloc[0]["Sport"]

            st.success(f"Sport: {sport}")

            performance = st.text_area(
                "Performance Data",
                placeholder="Goals scored, laps completed, gym weights, etc."
            )

            coach_insight = st.text_area(
                "Coach Insights",
                placeholder="Coach feedback"
            )

            if st.button("Save Performance"):

                performance_df = pd.read_csv(
                    "performance.csv"
                )

                new_record = pd.DataFrame({
                    "BookingCode":[booking_code],
                    "Sport":[sport],
                    "PerformanceData":[performance],
                    "CoachInsights":[coach_insight]
                })

                performance_df = pd.concat(
                    [performance_df, new_record],
                    ignore_index=True
                )

                performance_df.to_csv(
                    "performance.csv",
                    index=False
                )

                st.success("Performance Saved!")

        else:
            st.error("Invalid Booking Code")

# ---------------------------
# Dashboard
# ---------------------------

if st.session_state.logged_in:

    st.sidebar.markdown("---")
    st.sidebar.write(
        f"Logged in as: {st.session_state.username}"
    )
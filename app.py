import streamlit as st
import pandas as pd
import uuid
import qrcode
import os
from PIL import Image

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="SportSync",
    page_icon="🏆",
    layout="wide"
)

# -----------------------------
# CUSTOM STYLING
# -----------------------------

st.markdown("""
<style>

.stApp {
    background-color: #DFC4DA;
}

h1,h2,h3,h4,h5,h6,p,label {
    color:#2B2D6E !important;
}

div[data-testid="metric-container"]{
    background:white;
    border-radius:15px;
    padding:15px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.15);
}

.stButton > button{
    background-color:#6667AB;
    color:white;
    border:none;
    border-radius:10px;
    height:50px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# FILES
# -----------------------------

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

if not os.path.exists("users.csv"):
    pd.DataFrame(columns=[
        "Username",
        "Password",
        "Role"
    ]).to_csv("users.csv", index=False)

# -----------------------------
# SESSION STATE
# -----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

if "banner" not in st.session_state:
    st.session_state.banner = 0

# -----------------------------
# NAVBAR
# -----------------------------

col1, col2 = st.columns([6,1])

with col1:
    st.markdown(
        "<h1 style='color:#2B2D6E;'>🏆 SportSync</h1>",
        unsafe_allow_html=True
    )

with col2:
    if st.session_state.logged_in:
        st.success(st.session_state.username)

st.divider()

choice = st.radio(
    "",
    [
        "🏠 Home",
        "🔐 Login",
        "📅 Book Slot",
        "📈 Performance",
        "ℹ️ About"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

st.divider()

# -----------------------------
# HOME PAGE
# -----------------------------

if choice == "🏠 Home":

    banners = [
        "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=1600",
        "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=1600",
        "https://images.unsplash.com/photo-1531415074968-036ba1b575da?w=1600",
        "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=1600"
    ]

    col1, col2, col3 = st.columns([1,8,1])

    with col1:
        if st.button("⬅️"):
            st.session_state.banner = (
                st.session_state.banner - 1
            ) % len(banners)

    with col2:
        st.image(
            banners[st.session_state.banner],
            use_container_width=True
        )

    with col3:
        if st.button("➡️"):
            st.session_state.banner = (
                st.session_state.banner + 1
            ) % len(banners)
        st.markdown(
            """
            <div style='text-align:center;padding:20px;'>

            <h1>Train • Track • Triumph</h1>

            <h3>
            Book facilities instantly and
            improve with coach insights.
            </h3>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.button("📅 Book Now")

        st.markdown("## 🚀 Features")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.success("🏀 Facility Booking")

        with c2:
            st.success("📈 Performance Tracking")

        with c3:
            st.success("📱 QR Access")

        with c4:
            st.success("👨‍🏫 Coach Insights")

        st.markdown("## 🔥 Popular Sports")

        s1, s2, s3, s4 = st.columns(4)

        with s1:
            st.metric("🏀 Basketball", "Available")

        with s2:
            st.metric("⚽ Football", "Available")

        with s3:
            st.metric("🏏 Cricket", "Available")

        with s4:
            st.metric("🎾 Tennis", "Available")

    # -----------------------------
    # LOGIN
    # -----------------------------

elif choice == "🔐 Login":

    st.header("🔐 Login Portal")

    users = pd.read_csv("users.csv")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user = users[
            (users["Username"] == username)
            & (users["Password"].astype(str) == str(password))
        ]

        if len(user) > 0:

            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = user.iloc[0]["Role"]

            st.success(f"Welcome {username}!")

        else:
            st.error("Invalid credentials")

# -----------------------------
# BOOK SLOT
# -----------------------------

elif choice == "📅 Book Slot":

    if not st.session_state.logged_in:
        st.warning("Please login first")
        st.stop()

    bookings = pd.read_csv("bookings.csv")
    performance = pd.read_csv("performance.csv")

    st.header("📊 Dashboard")

    d1, d2, d3, d4, d5 = st.columns(5)

    with d1:
        st.metric(
            "Bookings",
            len(bookings)
        )

    with d2:
        st.metric(
            "Performance Records",
            len(performance)
        )

    with d3:
        st.metric(
            "Active User",
            st.session_state.username
        )

    with d4:
        st.metric(
            "Sports Available",
            8
        )

    with d5:
        st.metric(
            "QR Codes Generated",
            len(bookings)
        )

    st.divider()

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

    st.subheader("📅 Book Facility")

    sport = st.selectbox(
        "Sport",
        sports
    )

    booking_date = st.date_input(
        "Booking Date"
    )

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

    slot_count = len(
        bookings[
            (bookings["Sport"] == sport)
            &
            (bookings["Date"] == str(booking_date))
            &
            (bookings["Slot"] == slot)
        ]
    )

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Players Registered",
            slot_count
        )

    with c2:
        st.metric(
            "Available Spots",
            20 - slot_count
        )

    st.progress(slot_count / 20)

    if slot_count >= 20:

        st.error("🚫 Slot Full")

    else:

        if st.button("Confirm Booking"):

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

            bookings.to_csv(
                "bookings.csv",
                index=False
            )

            qr = qrcode.make(booking_code)

            qr_file = f"{booking_code}.png"

            qr.save(qr_file)

            st.balloons()

            st.success(
                "🎉 Booking Successful!"
            )

            st.code(booking_code)

            st.image(
                qr_file,
                width=250
            )

    if st.session_state.role == "Coach":

        st.divider()

        st.subheader(
            "👨‍🏫 Coach Dashboard"
        )

        st.dataframe(bookings)

# -----------------------------
# PERFORMANCE
# -----------------------------

elif choice == "📈 Performance":

    if not st.session_state.logged_in:
        st.warning("Please login first")
        st.stop()

    st.header("📈 Performance Tracker")

    booking_code = st.text_input(
        "Booking Code"
    )

    bookings = pd.read_csv(
        "bookings.csv"
    )

    if booking_code:

        booking_match = bookings[
            bookings["BookingCode"]
            == booking_code
        ]

        if len(booking_match) > 0:

            sport = booking_match.iloc[0]["Sport"]

            st.success(
                f"Sport: {sport}"
            )

            performance_data = st.text_area(
                "Performance Data"
            )

            coach_insight = st.text_area(
                "Coach Insights"
            )

            if st.button(
                "Save Performance"
            ):

                performance_df = pd.read_csv(
                    "performance.csv"
                )

                new_record = pd.DataFrame({
                    "BookingCode":[booking_code],
                    "Sport":[sport],
                    "PerformanceData":[performance_data],
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

                st.success(
                    "Performance Saved"
                )

            if st.session_state.role == "Coach":

                st.subheader(
                    "All Performance Records"
                )

                st.dataframe(
                    pd.read_csv(
                        "performance.csv"
                    )
                )

        else:

            st.error(
                "Invalid Booking Code"
            )

# -----------------------------
# ABOUT
# -----------------------------

elif choice == "ℹ️ About":

    st.header("🏆 About SportSync")

    st.write("""
SportSync is a university sports
facility management platform.

Features:

• Facility Booking

• QR Code Generation

• Performance Tracking

• Coach Feedback

• Slot Management

• Student & Coach Portals

• Real-Time Capacity Tracking
""")
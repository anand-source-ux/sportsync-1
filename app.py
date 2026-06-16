import streamlit as st
import pandas as pd
import uuid
import qrcode
import os

# --------------------------
# PAGE CONFIG
# --------------------------

st.set_page_config(
    page_title="SportSync",
    page_icon="🏆",
    layout="wide"
)

# --------------------------
# STYLING
# --------------------------

st.markdown("""
<style>

.stApp {
    background-color: #F1F5F9;
}

h1,h2,h3,h4,h5,h6,p,label {
    color:#1E293B !important;
}

div[data-testid="metric-container"]{
    background:white;
    border-radius:20px;
    padding:20px;
    border:1px solid #E2E8F0;
    box-shadow:0px 2px 8px rgba(0,0,0,0.08);
            }
.stButton > button{
    background:#CBB7E8;
    color:#2E2A68;
    border:none;
    border-radius:15px;
    height:55px;
    width:100%;
    font-weight:bold;
    font-size:16px;
    transition:0.3s;
            box-shadow:0 4px 12px rgba(46,42,104,0.15);
}

.stButton > button:hover{
    background:#B79DDE;
    color:#2E2A68;
    transform:translateY(-3px);
}
div[data-testid="metric-container"] {
    background:white;
    border-radius:20px;
    padding:20px;
    box-shadow:0 4px 12px rgba(46,42,104,0.08);
    
}
            div[data-testid="metric-container"]:hover {
    transform: translateY(-5px);
    transition: 0.3s;
}
</style>
""", unsafe_allow_html=True)

# --------------------------
# CREATE FILES
# --------------------------

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

# --------------------------
# SESSION STATE
# --------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

if "banner" not in st.session_state:
    st.session_state.banner = 0
import time

st.session_state.banner = (
    st.session_state.banner + 1
) % 4
# --------------------------
# NAVBAR
# --------------------------

st.markdown("""
<div style='text-align:center;padding:40px;'>

<h1 style='font-size:90px;color:#1E293B;margin-bottom:0;'>
🏆 SportSync
</h1>

<h3 style='color:#475569;'>
Train • Track • Triumph
</h3>

</div>
""", unsafe_allow_html=True)

if st.session_state.logged_in:
    st.success(
        f"Logged in as: {st.session_state.username}"
    )

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()
        
nav1, nav2, nav3, nav4, nav5 = st.columns(5)

if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

with nav1:
    if st.button("🏠 Home"):
        st.session_state.page = "🏠 Home"

with nav2:
    if st.button("🔐 Login"):
        st.session_state.page = "🔐 Login"

with nav3:
   if st.button("📅 Book Now", key="home_book"):
    st.session_state.page = "📅 Book Slot"
    st.rerun()

with nav4:
    if st.button("📈 Performance"):
        st.session_state.page = "📈 Performance"

with nav5:
    if st.button("ℹ️ About"):
        st.session_state.page = "ℹ️ About"

choice = st.session_state.page

# --------------------------
# HOME PAGE
# --------------------------

if choice == "🏠 Home":

    banners = [
        "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=1600",
        "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=1600",
        "https://images.unsplash.com/photo-1531415074968-036ba1b575da?w=1600",
        "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=1600"
    ]

    st.image(
        banners[st.session_state.banner],
        use_container_width=True
    )

    st.markdown("""
<div style="
background:linear-gradient(135deg,#D8CCE8,#CBB7E8);
padding:60px;
border-radius:30px;
text-align:center;
box-shadow:0 10px 30px rgba(0,0,0,0.15);
">

<h1 style="
font-size:60px;
margin-bottom:20px;
color:#2E2A68;
">
🚀 Welcome to SportSync
</h1>

<p style="
font-size:24px;
font-weight:500;
color:#3D356B;
line-height:1.8;
max-width:900px;
margin:auto;
margin-top:25px;
">
Train smarter. Book faster. Improve continuously.
</p>

</div>
""", unsafe_allow_html=True)

    st.markdown(
        "<h1 style='text-align:center;margin-top:20px;'>Train • Track • Triumph</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h3 style='text-align:center;'>Book facilities instantly and improve with coach insights.</h3>",
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns([2,1,2])

    with col2:
        if st.button("📅 Book Now", key="hero_book"):
            st.session_state.page = "📅 Book Slot"
            st.rerun()

    st.markdown("## 📊 SportSync Live")

    a, b, c, d = st.columns(4)

    with a:
        st.metric(
            "🏀 Facilities",
            "8"
        )

    with b:
        st.metric(
            "👥 Users",
            "250+"
        )

    with c:
        st.metric(
            "📅 Bookings",
            "1200+"
        )

    with d:
        st.metric(
            "🏆 Coaches",
            "15"
        )

    st.divider()

    st.markdown("## 🚀 Features")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div style="
        background:white;
        padding:25px;
        border-radius:20px;
        text-align:center;
        box-shadow:0 4px 12px rgba(46,42,104,0.12);
        min-height:180px;
        ">
        <h3>🏀</h3>
        <h4>Facility Booking</h4>
        <p>Book courts and facilities instantly.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div style="
        background:#D8CCE8;
        padding:25px;
        border-radius:20px;
        text-align:center;
        box-shadow:0 4px 12px rgba(46,42,104,0.12);
        min-height:180px;
        ">
        <h3>📈</h3>
        <h4>Performance Tracking</h4>
        <p>Monitor progress and achievements.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div style="
        background:white;
        padding:25px;
        border-radius:20px;
        text-align:center;
        box-shadow:0 4px 12px rgba(46,42,104,0.12);
        min-height:180px;
        ">
        <h3>📱</h3>
        <h4>QR Access</h4>
        <p>Generate QR codes for bookings.</p>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div style="
        background:#D8CCE8;
        padding:25px;
        border-radius:20px;
        text-align:center;
        box-shadow:0 4px 12px rgba(46,42,104,0.12);
        min-height:180px;
        ">
        <h3>👨‍🏫</h3>
        <h4>Coach Insights</h4>
        <p>Receive feedback from coaches.</p>
        </div>
        """, unsafe_allow_html=True)

    i1, i2, i3, i4 = st.columns(4)

    with i1:
        st.image("https://images.unsplash.com/photo-1546519638-68e109498ffc?w=500")

    with i2:
        st.image("https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=500")

    with i3:
        st.image("https://images.unsplash.com/photo-1531415074968-036ba1b575da?w=500")

    with i4:
        st.image("https://images.unsplash.com/photo-1518611012118-696072aa579a?w=500")
        s1, s2, s3, s4 = st.columns(4)

    st.markdown("""
    <div style='text-align:center;
    font-size:22px;
    font-weight:bold;
    color:#6B5CA5;
    margin-top:15px;'>

    🏀 Basketball &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    ⚽ Football &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    🏏 Cricket &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    🏋️ Fitness

    </div>
    """, unsafe_allow_html=True)
    st.markdown("## 🏆 Achievements")

    a1, a2, a3 = st.columns(3)

    with a1:
        st.success("🥇 First Booking")

    with a2:
        st.success("🔥 Active Athlete")

    with a3:
        st.success("🏆 Consistent Performer")

    st.divider()
  
   
 # --------------------------
# LOGIN PAGE
# --------------------------

elif choice == "🔐 Login":

    st.header("🔐 Login Portal")

    users = pd.read_csv("users.csv")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user = users[
            (users["Username"] == username)
            &
            (users["Password"].astype(str) == str(password))
        ]

        if len(user) > 0:

            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = user.iloc[0]["Role"]

            st.success(
                f"Welcome {username}!"
            )

        else:
            st.error("Invalid Username or Password")

# --------------------------
# BOOK SLOT
# --------------------------

elif choice == "📅 Book Slot":

    if not st.session_state.logged_in:
        st.warning("Please login first")
        st.stop()

    bookings = pd.read_csv("bookings.csv")

    st.header("📊 Dashboard")
    st.success(
        f"Welcome back, {st.session_state.username} 👋"
    )
    st.markdown("""
### 🎯 Today's Activity

Keep booking, training and improving.
""")
    d1, d2, d3, d4, d5 = st.columns(5)

    with d1:
        st.metric(
            "Bookings",
            len(bookings)
        )

    with d2:
        st.metric(
            "Active User",
            st.session_state.username
        )

    with d3:
        st.metric(
            "Sports Available",
            8
        )

    with d4:
        st.metric(
            "QR Codes",
            len(bookings)
        )

    with d5:
        st.metric(
            "Role",
            st.session_state.role
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

    sport = st.selectbox(
        "Choose Sport",
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

    st.metric(
        "Players Registered",
        slot_count
    )

    st.progress(slot_count / 20)

    if slot_count < 20:
        if st.button("📅 Confirm Booking"):

            booking_code = str(
                uuid.uuid4()
            )[:8]

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

            qr = qrcode.make(
                booking_code
            )

            qr_file = f"{booking_code}.png"

            qr.save(qr_file)

            st.balloons()

            st.success(
                "Booking Successful!"
            )

            st.code(
                booking_code
            )

            st.image(
                qr_file,
                width=250
            )
    else:
        st.warning("This slot is full. Please select a different time or date.")

    if st.session_state.role == "Coach":

        st.subheader(
            "👨‍🏫 Coach Dashboard"
        )

        st.dataframe(
            bookings
        )

        st.divider()

        st.subheader("📜 My Booking History")

        user_bookings = bookings[
            bookings["Username"] ==
            st.session_state.username
        ]

        st.dataframe(user_bookings)
        st.divider()

    st.subheader("📋 Recent Bookings")

    recent = bookings.tail(5)

    st.dataframe(
        recent,
        use_container_width=True
)
# --------------------------
# PERFORMANCE
# --------------------------

elif choice == "📈 Performance":

    if not st.session_state.logged_in:
        st.warning("Please login first")
        st.stop()

    st.header("📈 Performance Tracker")

    performance_df = pd.read_csv(
        "performance.csv"
    )

    st.metric(
        "Total Records",
        len(performance_df)
    )

    st.divider()

    booking_code = st.text_input(
        "Booking Code"
    )

    if booking_code:

        performance_data = st.text_area(
            "Performance Data"
        )

        coach_insight = st.text_area(
            "Coach Insights"
        )

        if st.button(
            "Save Performance"
        ):

            new_record = pd.DataFrame({
                "BookingCode":[booking_code],
                "Sport":["General"],
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
                "Performance Saved!"
            )

    st.divider()

    st.subheader(
        "📊 Previous Records"
    )

    st.dataframe(
        performance_df
    )
# --------------------------
# ABOUT
# --------------------------

elif choice == "ℹ️ About":

    st.header("🏆 About SportSync")

    st.write("""
SportSync is a sports facility
booking and performance
tracking platform.

Features:

• QR Booking

• Performance Tracking

• Coach Feedback

• Real Time Capacity Tracking

• Student & Coach Portals
""")
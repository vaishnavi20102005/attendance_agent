import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Attendance & Engagement Agent", layout="wide")
st.title("Multimodal Attendance & Engagement Agent")

# ---------- Load data ----------
if not os.path.exists("session_report.csv"):
    st.warning("No session found yet. Run `python main.py` first, then refresh.")
    st.stop()

report = pd.read_csv("session_report.csv")
scores = report["score"]

# ---------- Top numbers ----------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Average engagement", round(scores.mean(), 1))
c2.metric("Peak", int(scores.max()))
c3.metric("Lowest", int(scores.min()))
c4.metric("Frames analyzed", len(report))

# ---------- Engagement timeline ----------
st.subheader("Engagement timeline")
st.line_chart(report.set_index("time")["score"])

left, right = st.columns(2)

with left:
    st.subheader("Engagement levels")
    st.bar_chart(report["level"].value_counts())

with right:
    st.subheader("Speech activity")
    st.line_chart(report.set_index("time")["speech_ratio"])

# ---------- Suggestions ----------
st.subheader("Instructor suggestions")
avg = scores.mean()
last = scores.tail(10).mean()
if avg < 40:
    st.warning("Engagement was low overall. Try an interactive activity or a quick question.")
if last < avg - 15:
    st.warning("Attention dropped towards the end. Consider a short break.")
if report["speech_ratio"].sum() == 0:
    st.info("No discussion was detected. Invite questions or a short discussion.")
if avg >= 70:
    st.success("Engagement was high. The current approach is working well.")
if 40 <= avg < 70 and last >= avg - 15:
    st.info("Engagement was stable. Maintain the current pace.")

# ---------- Attendance ----------
st.subheader("Attendance records")
if os.path.exists("attendance_log.csv"):
    attendance = pd.read_csv("attendance_log.csv")
    st.dataframe(attendance, use_container_width=True)
else:
    st.info("No attendance records yet.")

# ---------- Raw data ----------
with st.expander("Show raw session data"):
    st.dataframe(report, use_container_width=True)
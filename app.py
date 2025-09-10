import streamlit as st
import speech_recognition as sr
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from prophet import Prophet
import joblib

from db import add_expense, get_expenses, get_total_spent, get_category_summary, backup_database
from voice_parser import parse_voice_text

# Offline recognizer setup
def recognize_voice_offline():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Please speak your expense (e.g., 'I spent 500 on food yesterday')")
        audio = r.listen(source, timeout=7, phrase_time_limit=7)
    try:
        text = r.recognize_sphinx(audio)
        st.success(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        st.error("Sorry, could not understand the audio.")
    except sr.RequestError:
        st.error("Speech recognition service is unavailable.")
    return None

st.set_page_config(page_title="Spend Vision", layout="wide")
st.title("💰 Spend Vision - AI-powered Expense Tracker")

tab1, tab2, tab3 = st.tabs(["➕ Add Expense", "📜 Expense History", "📊 Reports"])

with tab1:
    st.subheader("Add New Expense")

    use_voice = st.checkbox("🎤 Use Voice Input")

    if use_voice:
        if st.button("Start Recording"):
            voice_text = recognize_voice_offline()
            if voice_text:
                amount, category, description, date = parse_voice_text(voice_text)
                st.write(f"**Parsed:** Amount: ₹{amount}, Category: {category}, Description: {description}, Date: {date}")

                with st.form("confirm_expense"):
                    amount_inp = st.number_input("Amount (₹)", value=amount if amount else 0.0, format="%.2f")
                    category_inp = st.text_input("Category", value=category)
                    description_inp = st.text_area("Description", value=description)
                    date_inp = st.date_input("Date", value=datetime.fromisoformat(date).date())
                    submit = st.form_submit_button("Save Expense")

                    if submit:
                        add_expense(amount_inp, category_inp, description_inp, date_inp.isoformat())
                        st.success("✅ Expense added successfully!")
    else:
        with st.form("manual_expense"):
            amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
            category = st.selectbox("Category", ["food", "transport", "shopping", "bills", "entertainment", "other"])
            description = st.text_input("Description")
            date = st.date_input("Date", datetime.now())
            submit = st.form_submit_button("Add Expense")

            if submit:
                if amount > 0:
                    add_expense(amount, category, description, date.isoformat())
                    st.success("✅ Expense added successfully!")
                else:
                    st.error("❌ Please enter a valid amount.")

with tab2:
    st.subheader("Expense History")
    expenses = get_expenses()
    st.dataframe(expenses, use_container_width=True)

    total = get_total_spent()
    st.metric("💵 Total Spent", f"₹ {total:.2f}")

    st.download_button(
        label="💾 Backup Database",
        data=backup_database(),
        file_name="expenses_backup.db",
        mime="application/octet-stream"
    )

with tab3:
    st.subheader("Category-wise Spending Report")
    category_data = get_category_summary()

    if category_data:
        categories = [row[0] for row in category_data]
        amounts = [row[1] for row in category_data]

        fig, ax = plt.subplots()
        ax.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140)
        ax.axis("equal")
        st.pyplot(fig)
    else:
        st.info("No expenses recorded yet.")


# -------------------------
# TAB 4: ANOMALY DETECTION
# -------------------------
with st.expander("🔍 Anomaly Detection"):
    st.subheader("Detect Unusual Expenses")
    expenses = get_expenses()
    if not expenses:
        st.info("No expense data available.")
    else:
        df = pd.DataFrame(expenses, columns=["id", "amount", "category", "description", "date"])
        amounts = df['amount'].values.reshape(-1, 1)
        
        iso = IsolationForest(contamination=0.05, random_state=42)
        preds = iso.fit_predict(amounts)
        df['anomaly'] = preds
        
        anomalies = df[df['anomaly'] == -1]
        if anomalies.empty:
            st.success("No anomalies detected!")
        else:
            st.warning(f"Found {len(anomalies)} anomalous transactions:")
            st.dataframe(anomalies[["date", "amount", "category", "description"]])

        # Plot
        fig, ax = plt.subplots()
        ax.plot(df.index, df['amount'], label='Amount')
        ax.scatter(anomalies.index, anomalies['amount'], color='red', label='Anomalies')
        ax.set_title("Anomaly Detection in Expenses")
        ax.set_xlabel("Transaction Index")
        ax.set_ylabel("Amount")
        ax.legend()
        st.pyplot(fig)

# -------------------------
# TAB 5: FORECASTING
# -------------------------
with st.expander("📈 Forecast Next Month Expenses"):
    st.subheader("Forecast using Prophet Model")
    expenses = get_expenses()
    if not expenses:
        st.info("No expense data available.")
    else:
        df = pd.DataFrame(expenses, columns=["id", "amount", "category", "description", "date"])
        df['date'] = pd.to_datetime(df['date'])
        daily_sum = df.groupby(df['date'].dt.date)['amount'].sum().reset_index()
        daily_sum.columns = ['ds', 'y']

        model = Prophet()
        model.fit(daily_sum)

        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)

        st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30))

        fig2 = model.plot(forecast)
        st.pyplot(fig2)

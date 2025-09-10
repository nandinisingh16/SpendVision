
#  SpendVision - AI-powered Expense Tracker
SpendVision is a **Streamlit-powered expense tracker** with AI features. It helps you manage your expenses, visualize category-wise spending, detect anomalies, and forecast future expenses using machine learning.

##  Features

*  **Add Expense**
  * Manual entry (amount, category, description, date)
  *  Voice input support (offline speech recognition)

*  **Expense History**
  * View all past expenses in a table format, Track **total money spent**, Export/backup database

*  **Reports**
  * Category-wise spending pie chart
*  **Anomaly Detection** -  Detect unusual expenses using **Isolation Forest**
    
*  **Expense Forecasting**
  * Predict next month’s expenses using **Facebook Prophet**
---
##  Screenshots

###  Add Expense
<img width="1362" height="580" alt="Screenshot 2025-09-10 165929" src="https://github.com/user-attachments/assets/d82712dd-2c54-4cad-8815-22f538d9fed0" />
###  Expense History
<img width="1313" height="513" alt="Screenshot 2025-09-10 170013" src="https://github.com/user-attachments/assets/36908be3-8b55-44e1-8768-b90438691977" />

###  Reports
<img width="974" height="568" alt="Screenshot 2025-09-10 170034" src="https://github.com/user-attachments/assets/06c9528d-0414-4b4d-8877-3a225ed6ae4c" />
---
##  Tech Stack

* **Frontend/UI** → [Streamlit](https://streamlit.io/)
* **Database** → SQLite (local storage)
* **Visualization** → Matplotlib, Plotly
* **Machine Learning** →
  * Isolation Forest (Anomaly Detection)
  * Prophet (Time Series Forecasting)
* **Voice Recognition** → SpeechRecognition (CMU Sphinx offline)
---

## 📂 Project Structure
```
SpendVision/
│── app.py                  # Main Streamlit app
│── db.py                   # Database functions
│── voice_parser.py          # Parse voice inputs
│── requirements.txt         # Dependencies
│── expenses.db              # SQLite database
│── spend_vision/            # Additional modules
│── screenshots/             # App screenshots
```
---

## ⚙️ Installation
1. Clone the repository:

   ```bash
   git clone https://github.com/nandinisingh16/SpendVision.git
   cd SpendVision
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:

   ```bash
   streamlit run app.py
   ```
---

## 🎯 Future Improvements
* Add **user authentication**
* Deploy app on **Streamlit Cloud / Heroku**
* Support **multiple currencies**
* Add **budget goals & alerts**
---

## 🙌 Credits

Developed by **Raj Nandini Singh** 💡

---


# Deployment Instructions for Book Recommendation System

This document provides instructions to deploy the Book Recommendation System.

---

## 1. Requirements

* **Python 3.9+**
* **Packages**: Streamlit, Pandas, scikit-learn (installed via `requirements.txt`)
* **Project structure** intact:

```
book-recommendation-system/
├── README.md
├── requirements.txt
├── data/
│   └── books.csv
├── backend/
├── frontend/
└── deployment/
```

---

## 2. Install Dependencies

```bash
# Create a virtual environment (optional but recommended)
python -m venv venv

# Activate environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

---

## 3. Run Locally

Navigate to the frontend folder and start the Streamlit app:

```bash
cd frontend
streamlit run app.py
```

* The application will open in your default browser.
* Default URL: `http://localhost:8501`

---

## 4. Notes

* Ensure `books.csv` is present in the `data/` folder; otherwise, the app will show a warning.
* Maximum number of books shown in search, genre, and random recommendations is limited to 10.
* Backend and frontend paths assume the structure above; do not rename folders unless you update `sys.path` in `app.py`.

---

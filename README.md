# Book Recommendation System

A Python project that recommends books using multiple approaches:

- **Random Recommendations**
- **Genre-Based Filtering**
- **Search-Based Filtering**
- **Content-Based Recommendations** using TF-IDF and Cosine Similarity

A live version of the app has been deployed and can be accessed [here](https://book-rec-system.streamlit.app).

---

## Project Structure

```
book-recommendation-system/
├── README.md
├── requirements.txt
├── data/
│   └── books.csv
├── backend/
│   ├── __init__.py
│   ├── data_processing.py
│   └── recommendations.py
├── frontend/
│   └── app.py
└── deployment/
    └── deploy_instructions.md
```

---

## Setup

1. Clone the repository:

```bash
git clone https://github.com/0utc/book-recommendation-system.git
cd book-recommendation-system
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run Locally

```bash
streamlit run frontend/app.py
```

- The app will open in your browser at `http://localhost:8501`.

---

## Deployment

- The app is deployed online and accessible at: [https://book-rec-system.streamlit.app](https://book-rec-system.streamlit.app)  
- Deployment was done using Streamlit's hosting platform.  

---

## License

MIT License

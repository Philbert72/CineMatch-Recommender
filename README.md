# 🎬 CineMatch: Content-Based Movie Recommender

CineMatch is a full-stack machine learning application that provides personalized movie recommendations. By analyzing movie metadata—including plot overviews and genres—the system identifies similarities between titles to suggest films you'll likely enjoy.

---

## 🚀 Features
- **Smart Recommendations**: Uses Cosine Similarity to find movies with similar themes and genres.
- **Dynamic UI**: A sleek, dark-themed interface built with **Streamlit** featuring a featured movie carousel and responsive search.
- **Live Data**: Integrates with the **TMDB API** to fetch real-time posters and movie details.
- **Optimized Performance**: Pre-computed similarity matrices ensure near-instant recommendation results.

## 🛠️ Tech Stack
- **Language**: Python
- **ML Libraries**: Pandas, Scikit-learn (CountVectorizer, Cosine Similarity)
- **Frontend**: Streamlit
- **API**: The Movie Database (TMDB)

## 📁 Project Structure
- `app.py`: The main Streamlit application logic and UI.
- `Main.ipynb`: Jupyter Notebook containing data preprocessing, feature engineering, and model training.
- `dataset.csv`: The raw dataset of 10,000 movies.
- `movies_list.pkl` & `similarity.pkl`: Serialized model files (tracked via Git LFS).

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/Philbert72/CineMatch-Recommender.git](https://github.com/Philbert72/CineMatch-Recommender.git)
cd CineMatch-Recommender
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. API Configuration
To see movie posters, you will need a TMDB API Key:
1. Get a free key at [themoviedb.org](https://www.themoviedb.org/).
2. Open `app.py`.
3. Replace `YOUR_TMDB_API_KEY_HERE` with your actual key.

### 4. Run the App
```bash
streamlit run app.py
```

## 🧠 How It Works
1. **Vectorization**: Movie tags (combined genres and overviews) are converted into vectors using `CountVectorizer`.
2. **Similarity Score**: We calculate the **Cosine Similarity** between vectors to determine the mathematical "distance" between movies.
3. **Ranking**: When a movie is selected, the system retrieves the top 5 movies with the highest similarity scores.

---
*Developed as part of a Semester 4 Machine Learning Project.*
```

# ⚡ SOMA | Elite Performance Engine

SOMA is a high-speed, AI-driven medical performance coach. It is designed for users who need a high-top-score approach to body optimization, nutritional timing, and physiological recovery.

## 🎯 What SOMA Does
SOMA transforms raw biometrics into a high-performance roadmap. Unlike standard fitness apps, SOMA focuses on:
* **Precision Bio-Analysis:** Compares current weight against calculated physiological power ranges.
* **Nutritional Chronobiology:** Maps out "Fuel" and "Alternative" meals with exact timestamps (HH:MM) to match energy demands.
* **Advanced Training Logic:** Delivers specific exercise sets, reps, and alternatives based on physiological benefits, removing time-based gym clutter.
* **CNS Optimization:** Analyzes sleep and lifestyle to provide specific recovery tips for the Central Nervous System.

## 🛠️ Technology Stack
* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (High-performance Python)
* **Intelligence:** [OpenAI GPT-4o-mini](https://openai.com/) (Speed-optimized LLM)
* **Frontend:** HTML5 / CSS3 with **Glassmorphism UI**
* **Deployment:** [Render](https://render.com/)

## 🚀 Deployment (Render)
To deploy this high-speed app:
1.  **Repository:** Push your code to GitHub.
2.  **Web Service:** Create a new Web Service on Render.
3.  **Environment Variables:** Add `OPENAI_API_KEY` in the Render dashboard.
4.  **Build Command:** `pip install -r requirements.txt`
5.  **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 💻 Local Installation
1.  Clone the repository:
    ```bash
    git clone [https://github.com/yourusername/soma.git](https://github.com/yourusername/soma.git)
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Set up your `.env` file with your OpenAI Secret Key.
4.  Launch the engine:
    ```bash
    uvicorn main:app --reload
    ```

## 📁 Project Architecture
```text
.
├── main.py              # Application Logic & AI Integration
├── requirements.txt     # Dependency Manifest
├── .gitignore           # Security Configuration
├── README.md            # Product Documentation
├── static/              # Assets (CSS, Images)
└── templates/           # UI Layout (HTML)
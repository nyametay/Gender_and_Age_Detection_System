# 👤 Gender and Age Detection System

An AI-powered web application that analyzes facial images to predict a person's **gender** and **estimated age** using a facial analysis API.  
Built with **Flask**, **REST APIs**, **OpenCV**, and **Tailwind CSS**.

This system combines **computer vision** and **artificial intelligence** to provide an intuitive way to analyze facial attributes from images. Whether you're a **developer**, **student**, **researcher**, or **AI enthusiast**, the platform demonstrates how modern AI APIs can be integrated into web applications to perform real-time facial analysis with minimal setup.

The application processes uploaded images, securely communicates with a facial analysis API, and presents accurate predictions through a clean, responsive interface. It showcases practical API integration, image processing, and full-stack web development.

---

## 🧭 Key Highlights

- 👤 **AI-Powered Gender Detection** — Predicts the gender of individuals from facial images.
- 🎂 **Age Estimation** — Estimates a person's age using advanced facial analysis.
- 🖼️ **Image Upload Support** — Analyze facial images directly from your device.
- ⚡ **Real-Time Analysis** — Receive predictions within seconds through API integration.
- 🌙 **Modern & Responsive UI** — Built with Tailwind CSS and optimized for desktop and mobile devices.
- 🔗 **REST API Integration** — Demonstrates secure communication with external AI services.
- 📱 **Cross-Platform Experience** — Responsive interface for multiple screen sizes.
- 🔒 **Secure Configuration** — API credentials managed using environment variables.

---

## 🧠 Tech Stack

| Category | Tools |
|-----------|--------|
| **Frontend** | HTML5, Jinja2, Tailwind CSS, JavaScript |
| **Backend** | Flask (Python) |
| **AI Service** | [FaceAnalyzer AI API](https://rapidapi.com/) via `requests`  |
| **Image Processing** | OpenCV |
| **API Communication** | Requests |
| **Database** | SQLite / SQLAlchemy *(optional for storing analysis history)* |
| **Environment Management** | Python-Dotenv |
| **Deployment** | Render / Railway / Heroku |

---

## 🧩 Folder Structure

```text
Gender_and_Age_Detection_System/
│
├── app.py                   # Main Flask entry point
├── data/                    # Application package
│   ├── static/               # CSS, JS, Images
│   ├── templates/            # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── history.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── profile.html
│   ├── routes.py             # All Flask routes
│   ├── models.py             # SQLAlchemy models
│   ├── modules.py            # Helper modules/functions
│   └── __init__.py           # App factory & DB initialization
│
├── requirements.txt          # Dependencies
├── README.md                 # Project README
└── data.db                   # SQLite database (auto-generated)
```
```

---

# 🚀 Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/nyametay/Gender_and_Age_Detection_System.git
cd Gender_and_Age_Detection_System
```

## 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Configure Environment Variables

Create a `.env` file in the project root.

```ini
API_KEY=your_api_key
API_URL=your_api_endpoint
```

## 5️⃣ Run the Application

```bash
python app.py
```

Visit:

```text
http://127.0.0.1:5000
```

---

# 🧩 How It Works

- The user uploads a facial image.
- OpenCV performs basic image preprocessing.
- The backend sends the image securely to the facial analysis API.
- The API analyzes facial features and predicts the person's age and gender.
- Flask processes the API response and displays the results through Jinja templates.
- (Optional) Analysis history can be stored for future reference.

---

# 🧪 Example Output (JSON)

```json
{
  "prediction": {
    "gender": "Male",
    "gender_confidence": 99.2,
    "estimated_age": 27,
    "age_range": "25-30",
    "processing_time": "0.83s"
  }
}
```

---

# 📡 API Integration

We use the FaceAnalyzer AI API from RapidAPI:

```bash
# Endpoint:
POST https://faceanalyzer-ai.p.rapidapi.com/faceanalysis

# Example:

import requests

url = "https://faceanalyzer-ai.p.rapidapi.com/faceanalysis"
files = {"image": ("face.jpg", open("face.jpg", "rb"), "image/jpeg")}
headers = {
    "x-rapidapi-key": "YOUR_RAPIDAPI_KEY",
    "x-rapidapi-host": "faceanalyzer-ai.p.rapidapi.com"
}

response = requests.post(url, files=files, headers=headers)
print(response.json())
```

# 📜 Requirements

```text
Flask
opencv-python
requests
python-dotenv
sqlalchemy
gunicorn
```

Install everything with:

```bash
pip install -r requirements.txt
```

---

# ☁️ Deployment (Render / Railway / Heroku)

- Push your project to GitHub.
- Configure your environment variables (`API_KEY`, `API_URL`) in your deployment platform.
- Use the following Procfile:

```text
web: gunicorn app:app
```

Deploy the project and your Flask application will be live.

---

# 👨‍💻 Developer Info

**Developer:** Isaac Nyame Taylor  
**Year:** 2025

---

# 📄 License

This project is licensed under the MIT License — free for personal and academic use with attribution.

---

# ⭐ Support

If you find this project useful, don't forget to **star ⭐ the repository**.

Your support encourages the development of more AI-powered web applications and open-source projects.

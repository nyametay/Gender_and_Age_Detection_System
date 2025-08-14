# 🧑‍💻 Gender And Age Detector

A Flask-powered web application that analyzes faces in uploaded images using the **FaceAnalyzer AI API**.  
The app detects **age range**, **gender**, **emotion**, and whether the person is wearing **eyeglasses**, **sunglasses**, or is **smiling** — with results stored in a user-specific prediction history.

---

## 📸 Features

✅ **User Authentication** – Sign up, log in, and maintain personalized detection history.  
✅ **Face Analysis** – Detect **age range**, **gender**, **emotion**, **eyeglasses**, **sunglasses**, and **smiling status**.  
✅ **Image Upload** – Upload an image via a form for instant AI-based prediction.  
✅ **History Page** – View past detections in a clean, card-based layout.  
✅ **Dark Mode Support** – Modern UI with light/dark themes.  
✅ **Responsive Design** – Works on desktop, tablet, and mobile.  

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML, Tailwind CSS, JavaScript  
- **Database:** SQLite (`data.db`) with SQLAlchemy ORM  
- **Task Handling:** Flask routes + session management  
- **API Integration:** [FaceAnalyzer AI API](https://rapidapi.com/) via `requests`  
- **Auth:** Flask session-based authentication  

---

## 📦 Installation

```bash
# 1️⃣ Clone the repository
git clone https://github.com/your-username/face-analyzer-app.git
cd face-analyzer-app

# 2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Set environment variables (example for Linux/Mac)
export FLASK_APP=app.py
export FLASK_ENV=development
export RAPIDAPI_KEY=your_api_key_here

# 5️⃣ Initialize database
flask shell
>>> from data import db
>>> db.create_all()
>>> exit()

# 6️⃣ Run the app
flask run
```

# 📂 Project Structure

gender age detector/
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

# 🚀 Usage

- Sign up or log in.
- Upload a face image via the form.
- Wait for AI processing (done in real-time).
- View results — including age range, gender, emotion, and accessories.
- Check your history page for past detections.

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

# 🤝 Contributing

- Fork the repository
- Create a new branch (feature/new-feature)
- Commit changes
-Push to your fork
-Create a Pull Request

# 💡 Author

👨‍💻 Isaac Nyame Taylor
📧 Contact: isaac4230220@gmail.com
🔗 GitHub: nyametay

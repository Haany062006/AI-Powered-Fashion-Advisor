 AI-Powered Fashion Advisor 👗✨

AI Fashion Advisor is a web-based application that provides personalized fashion recommendations based on user inputs like body shape and preferences. The system also includes an AI chatbot powered by Groq for interactive assistance.

 🚀 Features

* 👤 User Login System
* 📸 Upload Image / Input Details
* 🧠 AI-Based Body Shape & Recommendation Logic
* 🎨 Color & Dress Suggestions (JSON-based rules)
* 🤖 AI Chatbot (Groq API)
* 💻 Simple and Clean UI

---

🏗️ Project Structure

AI-Fashion-Advisor/
│
├── backend/
│   ├── app.py
│   ├── services/
│   │   ├── body_shape.py
│   │   ├── chatbot.py
│   │   ├── recommender.py
│   │   └── skin_tone_model.py
│   └── database/
│       └── users.json
│
├── frontend/
│   ├── css/
│   ├── images/
│   ├── js/
│   ├── index.html
│   ├── login.html
│   └── upload_body_shape.html
│
├── data/
│   ├── color_rules.json
│   └── dress_rules.json
│
├── uploads/
├── requirements.txt
├── .gitignore
└── README.md

---
 🛠️ Technologies Used

* Python (Flask)
* HTML, CSS, JavaScript
* JSON (for rules & data)
* Groq API (AI chatbot)
* Pillow (Image processing)

---

⚙️ Installation & Setup

1️⃣ Clone the repository


git clone https://github.com/YOUR_USERNAME/AI-Fashion-Advisor.git
cd AI-Fashion-Advisor


---

 2️⃣ Create virtual environment


python -m venv venv


---

3️⃣ Activate virtual environment

**Windows:**

venv\Scripts\activate

**Mac/Linux:**

source venv/bin/activate

---

 4️⃣ Install dependencies


pip install -r requirements.txt


---

5️⃣ Setup environment variables

Create a `.env` file in root folder:


GROQ_API_KEY=your_api_key_here


---

 ▶️ Run the Project


python backend/app.py


Then open your browser and access:


http://127.0.0.1:5000


---

📌 Important Notes

* Do NOT upload `.env` file to GitHub
* Do NOT upload `venv/` or `__pycache__/`
* Keep `uploads/` folder empty (use `.gitkeep` if needed)

---
 🎯 Future Improvements

* Real-time image-based body detection
* Advanced AI styling recommendations
* Mobile responsive UI
* Outfit visualization

---

👩‍💻 Author

Developed as an AI-based student project for fashion recommendation and styling assistance.

---

⭐ If you like this project

Give it a star ⭐ on GitHub!

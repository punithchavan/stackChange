# 🚀 stackChange

stackChange is an AI-powered tool that automatically converts a Django backend project into a fully functional Node.js (Express + MongoDB) backend. It is designed to help developers rapidly transition between backend stacks, improving flexibility and developer experience.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Features](#features)
- [Local Setup Instructions](#local-setup-instructions)
- [Folder Structure](#folder-structure)
- [Deployment](#deployment)
- [Contributors](#contributors)

---

## 🧩 Overview

This project enables developers to:

- Upload a Django backend (as a `.zip` file).
- Automatically convert its views, models, and routes to an Express.js + MongoDB equivalent.
- Download the converted Node.js backend ready to run.

The goal is to simplify the process of switching from Django to MERN stack (and eventually support MERN → Django).

---

## 🛠️ Tech Stack

### Frontend (React + Vite)

- React.js + Tailwind CSS
- Axios for API calls
- React Router DOM
- Hosted on [Vercel](https://vercel.com)

### Backend (Django + AI Processing)

- Django (Python)
- Custom AST parsing + prompt templating
- Google Gemini API for AI-based code generation
- File handling (upload → convert → zip)
- Hosted on [Render](https://render.com)

### Converted Stack (Output)

- Node.js
- Express.js
- MongoDB + Mongoose
- REST API design

---

## 🏗️ Architecture

 Monolithic Architecture (stackChange)

 ┌────────────┐
 │  Frontend  │  (React on Vercel)
 └────┬───────┘
      │
      ▼
 ┌────────────┐
 │  Backend   │  (Django on Render)
 ├────────────┤
 │  Uploads   │
 │  Extractor │
 │  AST Logic │
 │  Gemini AI │
 │  Zip & Send│
 └────────────┘



---

## ✨ Features

- 📤 Upload Django backend project
- 🤖 Automatic conversion via Gemini AI
- 🔁 Converts:
  - views.py → controller functions
  - models.py → Mongoose models
  - urls.py → Express routes
- 📦 Download ready-to-run Node.js project
- 🧠 Smart AST parsing for accurate conversion
- 🧪 Sample project provided for demo/testing

---

## 🧪 Local Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/stackChange.git
cd stackChange

### 2. Frontend Setup
cd frontend
npm install
npm run dev

### 3. Backend Setup
pip install -r requirements.txt
cd backend
python manage.py runserver

# Deployment
🔗 Frontend: https://stack-change.vercel.app/
🌐 Backend (Django AI Service): Hosted on Render

# 💡 Future Improvements
🔄 Add support for bidirectional conversion (MERN → Django)

🧠 Fine-tuned prompt engineering for better accuracy

🧪 Add unit testing and validation post-conversion

📦 VS Code Extension for in-editor conversion





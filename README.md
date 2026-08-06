# AI Resume Screener
Demo- https://ai-resume-screener-sable.vercel.app/

GitHub Repo: https://github.com/Maan-netizen/ai-resume-screener

Full-stack app that matches a resume against a job description using
TF-IDF + cosine similarity, and highlights matched vs missing skills.

**Stack:** React (frontend) · Flask/Python (backend + NLP) · MongoDB (storage)

---

## Project Structure

```
ai-resume-screener/
├── backend/
│   ├── app.py            # Flask API
│   ├── matcher.py        # Resume parsing + TF-IDF matching logic
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── public/index.html
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   ├── index.css
│   │   └── components/
│   │       ├── UploadForm.js
│   │       ├── ResultsDashboard.js
│   │       └── History.js
│   ├── package.json
│   └── .env.example
├── cli_scan.py            # Standalone Python script (no server needed)
└── README.md
```

---

## 1. Local Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # then edit MONGO_URI
python app.py
```
Runs on `http://localhost:5000`

### Frontend
```bash
cd frontend
npm install
cp .env.example .env          # confirm REACT_APP_API_URL
npm start
```
Runs on `http://localhost:3000`

### MongoDB
Easiest: create a free cluster at https://www.mongodb.com/cloud/atlas,
get the connection string, and put it in `backend/.env` as `MONGO_URI`.
(Local MongoDB via `mongodb://localhost:27017` also works if installed.)

### Quick CLI demo (no servers needed)
```bash
python cli_scan.py my_resume.pdf job_description.txt
```

---

## 2. Deployment (all free-tier friendly)

### Step A — Deploy MongoDB
1. Go to MongoDB Atlas → create a free M0 cluster.
2. Create a database user + password.
3. Network Access → allow access from anywhere (`0.0.0.0/0`) for simplicity.
4. Copy the connection string — you'll need it in Step B.

### Step B — Deploy Backend (Render)
1. Push this project to a GitHub repo.
2. Go to https://render.com → New → Web Service → connect your repo.
3. Root directory: `backend`
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`
6. Add environment variable `MONGO_URI` with your Atlas connection string.
7. Deploy — Render gives you a URL like `https://your-app.onrender.com`.

### Step C — Deploy Frontend (Vercel)
1. Go to https://vercel.com → New Project → import the same repo.
2. Root directory: `frontend`
3. Framework preset: Create React App (auto-detected).
4. Add environment variable `REACT_APP_API_URL` = your Render backend URL
   from Step B.
5. Deploy — Vercel gives you a live link, e.g. `https://your-app.vercel.app`.

### Step D — Final check
Open the Vercel URL, upload a resume, paste a job description, and
confirm you get a score back (this proves frontend → backend → MongoDB
are all connected).

**Put the live Vercel link + GitHub repo link on your resume/LinkedIn.**
That combination (working demo + visible code) is what recruiters
actually click on.

---

## 3. Talking points for interviews

- **Frontend:** component structure (UploadForm/Dashboard/History),
  controlled inputs, drag-and-drop file upload, axios + FormData for
  multipart uploads, environment-based API URLs.
- **Backend:** REST API design, file parsing (PyPDF2/python-docx),
  text preprocessing, TF-IDF vectorization, cosine similarity — be
  ready to explain *why* TF-IDF over plain keyword matching.
- **Database:** MongoDB schema-less document storage, storing scan
  history, sorting/limiting queries.
- **Possible extensions to mention:** JWT auth per user, spaCy for
  named-entity extraction (auto-detect candidate name/experience),
  weighting skills by frequency, using an LLM API for a more nuanced
  match explanation instead of pure TF-IDF.

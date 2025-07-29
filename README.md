# ExcusesGenerator

# AI Excuse Generator – Setup & Run

## 1. Start the Backend

```sh
cd .\backend\
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 2. Start the Frontend (in a new terminal tab)

```sh
cd ../frontend
python -m http.server 8080
```

---

## 3. Open the App

Open [http://localhost:8080/index.html](http://localhost:8080/index.html) in your browser.

---


---

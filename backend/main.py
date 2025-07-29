from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import google.generativeai as genai
from gtts import gTTS
from langdetect import detect
from time import sleep
import platform
import os
import uvicorn

# Optional playback
try:
    from playsound import playsound
except ImportError:
    print("Install playsound with: pip install playsound")

# ✅ Gemini API Configuration
GEMINI_API_KEY = "....."
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# 🎧 Convert text to speech and save
def save_excuse_audio(text, lang="en", speed=False, filename="excuse_audio.mp3"):
    path = f"static/audio/{filename}"
    tts = gTTS(text=text, lang=lang, slow=speed)
    tts.save(path)
    print(f"✅ Audio saved as '{path}'")


# 🔊 Cross-platform safe audio playback
def safe_play_audio(filename):
    try:
        playsound(filename)
    except Exception as e:
        print(f"❌ Audio playback error: {e}")
        if platform.system() == "Linux":
            print("Tip: Try installing ffplay, vlc, or use on Windows/macOS for auto playback.")

# 🎯 Generate excuse + scenario-based speech
def generate_excuse_with_audio(scenario, urgency, believability, context, audience,
                                lang_code=None, speak=False, filename="excuse_audio.mp3"):
    prompt = (
        f"Generate a highly believable and creative excuse for the following:\n"
        f"Scenario: {scenario}\nUrgency: {urgency}\nBelievability: {believability}%\n"
        f"Context: {context}\nAudience: {audience}\n"
        f"The excuse should sound natural, realistic, and convincing."
    )

    proof_prompt = (
        f"Based on this excuse: '{context}', generate a realistic proof idea like a doctor's note, "
        f"chat screenshot summary, travel ticket, or anything suitable to justify it."
    )

    try:
        response = model.generate_content(prompt)
        excuse = response.text.strip()

        response_proof = model.generate_content(proof_prompt)
        proof = response_proof.text.strip()

        # 🌐 Language detection or use given
        detected_lang = lang_code if lang_code else detect(excuse)

        # 🧠 Voice tone logic
        speed = False
        if any(word in scenario.lower() for word in ["emergency", "urgent", "accident", "immediate"]):
            speed = True  # Slightly slow for serious tone
        elif any(word in scenario.lower() for word in ["birthday", "happy", "party"]):
            speed = False  # Natural tone
        elif "emotional" in scenario.lower() or "breakdown" in scenario.lower():
            speed = True  # Calm tone

        print(f"\n📝 Excuse in {detected_lang}:\n", excuse)
        print("\n📎 Suggested Proof:\n", proof)

        # 🔉 Save and speak
        if speak:
            save_excuse_audio(excuse, lang=detected_lang, speed=speed, filename=filename)
            safe_play_audio(filename)

        return excuse, proof

    except Exception as e:
        print(f"❌ Error: {e}")
        return "", ""

# ⚙️ FastAPI App
app = FastAPI()

# ✅ Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🚀 React frontend build serving
app.mount("/fake-call", StaticFiles(directory="../frontend/fake-call", html=True), name="fake-call")
app.mount("/doc-generator", StaticFiles(directory="../frontend/doc-generator", html=True), name="doc-generator")

from fastapi.responses import FileResponse



@app.get("/fake-call/{full_path:path}")
async def serve_react_app():
    return FileResponse("../frontend/fake-call/index.html")

# ✨ Excuse generator route
@app.post("/generate_excuse")
async def generate_excuse(request: Request):
    data = await request.json()
    scenario = data.get("scenario")
    urgency = data.get("urgency")
    believability = data.get("believability")
    context = data.get("context")
    audience = data.get("audience")
    excuse_type = data.get("type")
      # Save MP3

    prompt_excuse = (
        f"Generate a highly believable and context-appropriate excuse with supporting detail.\n"
        f"Scenario: {scenario}\nUrgency: {urgency}\nBelievability: {believability}%\n"
        f"Excuse Type: {excuse_type}\nContext: {context}\nAudience: {audience}\n"
        f"The excuse should sound natural and realistic."
    )

    prompt_proof = (
        f"Based on the excuse type '{excuse_type}' and context '{context}', "
        f"generate a suitable and realistic supporting proof idea (e.g., document, screenshot, note, etc.)."
    )

    try:
        excuse_response = model.generate_content(prompt_excuse)
        proof_response = model.generate_content(prompt_proof)

        excuse = excuse_response.text.strip()
        proof = proof_response.text.strip()
        save_excuse_audio(excuse)
        return {
            "excuse": excuse,
            "proof": proof
        }

    except Exception as e:
        return {"error": str(e)}
@app.get("/get_audio")
async def get_audio():
    filename = "excuse_audio.mp3"
    if os.path.exists(filename):
        return FileResponse(filename, media_type="audio/mpeg", filename=filename)
    return {"error": "Audio file not found"}
# ✅ Run directly
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
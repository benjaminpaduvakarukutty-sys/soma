import os
import re
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# 1. LOAD AND VERIFY API KEY
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    raise ValueError("CRITICAL ERROR: OPENAI_API_KEY not found!")

client = OpenAI(api_key=api_key)

app = FastAPI()

# 2. PATH CONFIGURATION
current_dir = os.path.dirname(os.path.realpath(__file__))
static_path = os.path.join(current_dir, "static")
template_path = os.path.join(current_dir, "templates")

app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(directory=template_path)

def get_soma_ranges(height: float, sex: str):
    """Calculates physiological power range based on medical standards."""
    if sex.lower() == "male":
        base = 50 + 0.9 * (height - 152)
    else:
        base = 45.5 + 0.9 * (height - 152)
    base = max(base, height - 105)
    return round(base - 5, 1), round(base + 10, 1)

def clean_soma_output(text):
    """Strictly removes meta-talk and instructions leaked by the AI."""
    text = re.sub(r"(?i)(left side|right side|section \d|instruction|analysis & food|training & recovery|###.*content|\[TRAINING_START\])", "", text)
    return text.strip()

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    # FIXED: Using explicit keyword arguments to avoid 'unhashable dict' error
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"show_results": False}
    )

@app.post("/", response_class=HTMLResponse)
async def run_check(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    sex: str = Form(...),
    weight: float = Form(...),
    height: float = Form(...),
    sleep: float = Form(...),
    lifestyle_story: str = Form(...)
):
    min_range, max_range = get_soma_ranges(height, sex)
    
    prompt = f"""
    User: {name} | {age}y/o | {sex} | {weight}kg | {height}cm | {sleep}h Sleep.
    Lifestyle: {lifestyle_story}
    Healthy Range for this height: {min_range}kg - {max_range}kg.

    SOMA INSTRUCTIONS:
    1. [WEIGHT ANALYSIS]: Start by talking to {name} about their weight of {weight}kg. Compare it to the {min_range}-{max_range}kg range. Be human. Tell them if they are in a good spot or if they should aim lower/higher.
    2. [FOOD]: Provide a plan with specific TIME (HH:MM), Primary Fuel, an Alternative, and the EXACT Biological Why.
    3. [TRAINING]: Use specific Exercises, Sets/Reps, Alternatives, and the Physiological Benefit.
    4. [RECOVERY]: Explain why {sleep}h of sleep matters and give one specific recovery tip.
    5. [SUMMARY]: Give a final Health Grade (e.g. A, B+) and a positive, motivating closing sentence.
    """

    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": "You are SOMA, an elite performance coach. Speak like a human mentor, not a robot. You MUST separate the Food section from the Training section using the exact tag [TRAINING_START]. Part 1 is Weight & Food. Part 2 is Training, Sleep & Summary."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        ai_text = response.choices[0].message.content
        parts = ai_text.split("[TRAINING_START]")
        
        if len(parts) > 1:
            food_raw = parts[0].replace("[WEIGHT ANALYSIS]", "### YOUR STATUS").replace("[FOOD]", "### NUTRITIONAL TIMING")
            training_raw = parts[1].replace("[RECOVERY]", "### SLEEP & RECOVERY").replace("[SUMMARY]", "### FINAL HEALTH GRADE")
            food_advice = clean_soma_output(food_raw)
            exercise_advice = "### TRAINING PROTOCOL\n" + clean_soma_output(training_raw)
        else:
            food_advice = ai_text
            exercise_advice = "The coach is still refining your movement protocol."

    except Exception as e:
        food_advice = "Connection Error."
        exercise_advice = str(e)

    # FIXED: Passing context correctly using the modern FastAPI/Starlette style
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "show_results": True,
            "name": name,
            "food_advice": food_advice,
            "exercise_advice": exercise_advice
        }
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

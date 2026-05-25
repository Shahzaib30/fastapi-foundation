from fastapi import FastAPI, HTTPException
import torch
import joblib
from examples.sms_spam_classification import SpamDetector


app = FastAPI()
model = None
vocab = None


@app.on_event("startup")
def load_model():
    global model, vocab
    vocab = joblib.load("vocab.pkl")
    model = SpamDetector(len(vocab))
    model.load_state_dict(torch.load("spam_detector.pth"))
    model.eval()


def text_to_tensor(text, vocab):
    indices = [vocab.get(word, vocab["<UNK>"]) for word in text.lower().split()]
    return torch.tensor([indices])


@app.post("/classify")
async def classify_sms(message: str):
    if model is None or vocab is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    input_tensor = text_to_tensor(message, vocab)
    with torch.no_grad():
        output = model(input_tensor)

    prediction = "spam" if output.item() > 0.5 else "ham"
    return {"prediction": prediction}

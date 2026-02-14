from fastapi import FastAPI
import tensorflow as tf
import contextlib
import pickle
from pydantic import BaseModel , HttpUrl
from preprocess_url import URLPreprocessor
#لكي تتمكن اي واجهة من الاتصال بال API
from fastapi.middleware.cors import CORSMiddleware



# عشان لما نشغل السيرفر , ما يحمل كل ما اجا مستخدم بل يعمل مرة واحدة فقط
ml_model = {}
@contextlib.asynccontextmanager
async def lifespan(app : FastAPI):
    ml_model["model"] = tf.keras.models.load_model("best_url_model (2)_final.keras")
    with open(r"scaler (2).pickle","rb") as f:
        ml_model['scaler'] = pickle.load(f)
    yield
    ml_model.clear()       

app = FastAPI(lifespan=lifespan) 

class UrlRequest(BaseModel):
    url : str

@app.post("/predict")
async def pridict_url(data : UrlRequest):
    preprocessor = URLPreprocessor()
    seq , fet , domain = preprocessor.process(str(data.url))
    seq = seq.reshape(1, -1)
    fet = fet.reshape(1, -1)
    feat_scaled = ml_model["scaler"].transform(fet)
    prediction_result = ml_model["model"].predict([seq,feat_scaled],verbose = 0)
    scor = float(prediction_result[0][0])

    label = "Malicious 💀" if scor > 0.5 else "Benign ✅"
    confidence = scor if scor > 0.5 else 1 - scor

    return {"url":data.url , "label":label , "confidence":confidence}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # اسمح لأي واجهة بالاتصال (للتجربة حالياً)
    allow_methods=["*"],
    allow_headers=["*"],
)

#بعد الانتهاء يمكن عمل زر لتوضيح كيف تم عمل المودل 
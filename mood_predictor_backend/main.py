from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import joblib
from pydantic import BaseModel

from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE_URL = "sqlite:///./predictions.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#prediction table
class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    sleep_hours = Column(Float, nullable=False)
    stress_level = Column(Float, nullable=False)
    calories_burned = Column(Float, nullable=False)
    predicted_mood = Column(Float, nullable=False)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

model = joblib.load("mood_predictor.pkl")

class MoodInput(BaseModel): # to check if the input data sent by frontend is correct, specifically if they are float data type
    sleep_hours: float
    stress_level: float
    calories_burned: float

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(  #by default browsers block request from different domanins, so the frontend (vue) cant call backend (fastapi)
    CORSMiddleware,  # CORS allow vue to talk to fast api
    allow_origins=["http://localhost:8080"],  # Vue.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/") # simple test rout to see if fast api is reunning
def home():
    return {"message": "FastAPI backend is running"}


@app.post("/predict")
async def predict_mood(data: MoodInput, db: Session = Depends(get_db)): # validates data with mood input class
    try:
        input_data = [[data.sleep_hours, data.stress_level, data.calories_burned]]
        predicted_mood = model.predict(input_data)[0]  # Extract single value

        # save to db
        new_prediction = Prediction(
            sleep_hours=data.sleep_hours,
            stress_level=data.stress_level,
            calories_burned=data.calories_burned,
            predicted_mood=predicted_mood
        )
        db.add(new_prediction)
        db.commit()
        db.refresh(new_prediction)

        return {"predicted_mood": float(predicted_mood)}

    except Exception as e:
        return {"error": str(e)}

@app.get("/predictions")
async def get_predictions(db: Session = Depends(get_db)):
    predictions = db.query(Prediction).all()
    return predictions


# cd "C:\Users\hsueh\Desktop\personal analyzer\mood_predictor_backend"
# py -m uvicorn main:app --reload

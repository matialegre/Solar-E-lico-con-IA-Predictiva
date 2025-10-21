"""
Router para Machine Learning
Entrenamient

o y predicciones
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ml_predictor_service import ml_predictor

router = APIRouter(prefix="/api/ml", tags=["Machine Learning"])


class TrainRequest(BaseModel):
    """Request para entrenar modelo"""
    latitude: float
    longitude: float
    years_back: int = 10


@router.post("/train")
async def train_ml_models(request: TrainRequest):
    """
    Entrenar modelos ML con datos históricos
    
    Proceso:
    1. Obtiene 10-40 años de datos de NASA POWER API
    2. Entrena Random Forest para solar
    3. Entrena Gradient Boosting para eólico
    4. Valida con cross-validation
    5. Retorna métricas y conclusiones
    
    Tiempo estimado: 5-15 segundos
    """
    try:
        print(f"🚀 Iniciando entrenamiento ML...")
        metrics = await ml_predictor.train_models(
            latitude=request.latitude,
            longitude=request.longitude,
            years_back=min(request.years_back, 40)  # Máx 40 años
        )
        
        return {
            "status": "success",
            "message": "Modelos entrenados correctamente",
            "metrics": metrics
        }
        
    except Exception as e:
        print(f"❌ Error en entrenamiento: {e}")
        raise HTTPException(status_code=500, detail=f"Error entrenando modelos: {str(e)}")


@router.get("/metrics")
async def get_ml_metrics():
    """
    Obtener métricas del último entrenamiento
    """
    if ml_predictor.metrics is None:
        raise HTTPException(status_code=404, detail="No hay modelos entrenados")
    
    return ml_predictor.metrics


@router.post("/predict/{month}")
async def predict_month(month: int, latitude: float):
    """
    Predecir generación para un mes específico usando ML
    """
    try:
        if month < 1 or month > 12:
            raise HTTPException(status_code=400, detail="Mes debe estar entre 1 y 12")
        
        prediction = ml_predictor.predict_generation(month, latitude)
        return prediction
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en predicción: {str(e)}")

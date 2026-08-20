"""
Prediction Router Endpoint
POST /predict-image: Accepts multipart cropped image file and returns prediction JSON.
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, status
from schemas import PredictionResponse, RGBResponse, CIELABResponse
from services.color_service import extract_color_features
from services.predict_service import get_predict_service

router = APIRouter(tags=["Prediction"])


@router.post(
    "/predict-image",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict Egg Yolk Color Fan Score from cropped image"
)
async def predict_image(file: UploadFile = File(...)):
    """
    Receives a cropped egg yolk image file via multipart/form-data,
    extracts RGB and CIELAB color features, and predicts the Yolk Color Fan score (1-15).
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type '{file.content_type}'. Please upload an image file (JPEG/PNG)."
        )

    try:
        # Read uploaded image bytes
        image_bytes = await file.read()
        
        # Extract color features (RGB + CIELAB) using canonical Python color service
        color_feats = extract_color_features(image_bytes)

        # Get prediction service and calculate score
        predictor = get_predict_service()
        pred_score, raw_score = predictor.predict(
            r=color_feats['r'],
            g=color_feats['g'],
            b=color_feats['b'],
            l=color_feats['l'],
            a=color_feats['a'],
            b_lab=color_feats['b']
        )

        return PredictionResponse(
            predicted_score=pred_score,
            raw_score=raw_score,
            rgb=RGBResponse(
                r=color_feats['r'],
                g=color_feats['g'],
                b=color_feats['b']
            ),
            cielab=CIELABResponse(
                l=color_feats['l'],
                a=color_feats['a'],
                b=color_feats['b'],
                chroma=color_feats['chroma'],
                hue_angle=color_feats['hue_angle']
            )
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing image or model prediction: {str(e)}"
        )

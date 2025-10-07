from fastapi import APIRouter, UploadFile, File, HTTPException, status

from ..services.image_analyze import analyze_image


router = APIRouter()


@router.post("/analyze-image")
async def analyze_image_upload(file: UploadFile = File(...)):
    try:
        content = await file.read()
        info = analyze_image(content)
        return info
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Gecersiz veya desteklenmeyen goruntu")



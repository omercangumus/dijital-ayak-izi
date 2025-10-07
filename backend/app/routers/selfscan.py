from fastapi import APIRouter, HTTPException, status
from typing import Any, List
from pydantic import BaseModel

from ..schemas.selfscan import SelfScanRequest
from ..services.selfscan import initial_scan, detailed_scan
from ..services.risk import score_results, classify


router = APIRouter()


class DetailedScanRequest(BaseModel):
    full_name: str
    email: str | None = None
    confirmed_links: List[str] = []


@router.post("/initial-scan")
def do_initial_scan(req: SelfScanRequest) -> dict[str, Any]:
    """İlk aşama: Hızlı tarama ve onaylama"""
    try:
        print(f"[>>] Initial scan basladi: {req.full_name} / {req.email}")
        result = initial_scan(req.full_name, req.email)
        s = score_results(result.get('results', []))
        result['risk_score'] = s
        result['risk_level'] = classify(s)
        print(f"[OK] Initial scan tamamlandi: {len(result.get('results', []))} sonuc, risk: {s}")
        return result
    except Exception as e:
        print(f"[X] Initial scan hatasi: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Initial scan hatasi: {str(e)}")


@router.post("/detailed-scan")
def do_detailed_scan(req: DetailedScanRequest) -> dict[str, Any]:
    """Detaylı tarama: Onaylanan linkler için derinlemesine analiz"""
    try:
        print(f"[>>] Detailed scan basladi: {req.full_name} / {req.email}")
        print(f"[>>] Confirmed links: {req.confirmed_links}")
        result = detailed_scan(req.full_name, req.email, req.confirmed_links)
        s = score_results(result.get('results', []))
        result['risk_score'] = s
        result['risk_level'] = classify(s)
        print(f"[OK] Detailed scan tamamlandi: {len(result.get('results', []))} sonuc, risk: {s}")
        return result
    except Exception as e:
        print(f"[X] Detailed scan hatasi: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Detailed scan hatasi: {str(e)}")


@router.post("/self-scan")
def do_self_scan(req: SelfScanRequest) -> dict[str, Any]:
    """Backward compatibility için eski endpoint"""
    return do_initial_scan(req)



from fastapi import APIRouter, status

router = APIRouter(prefix="", tags=["[health]"])

from fastapi import FastAPI

app = FastAPI()


@router.get("/health", status_code=status.HTTP_200_OK, summary="estado de la API")
def get_status():
    return {"status": "OK"}

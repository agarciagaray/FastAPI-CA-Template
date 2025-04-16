# filepath: src/api/sms.py
from fastapi import APIRouter, Depends, Form

from src.auth.service import \
    get_current_user  # Ajusta la ruta según tu proyecto
from src.utils.sms_sender import send_sms

router = APIRouter(
    prefix="/sms",
    tags=["SMS"],
    dependencies=[Depends(get_current_user)]  # <-- Protección aquí
)


@router.post("/send", description="Permite enviar mensajes de texto SMS a números de celular usando servicios externos.")
async def send_sms_route(
    to: str = Form(...),
    message: str = Form(...)
):
    sid = send_sms(to, message)
    return {"message": "SMS enviado correctamente", "sid": sid}

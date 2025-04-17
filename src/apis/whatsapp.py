from fastapi import APIRouter, Form, Depends
from src.utils.whatsapp_sender import send_whatsapp
from src.auth.service import get_current_user  # Ajusta la ruta según tu proyecto

router = APIRouter(
    prefix="/whatsapp",
    tags=["WhatsApp"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/send", description="Envía mensajes de WhatsApp usando Twilio.")
async def send_whatsapp_route(
    to: str = Form(...),      # Número destino, ejemplo: +573001234567
    message: str = Form(...)
):
    sid = send_whatsapp(to, message)
    return {"message": "Mensaje de WhatsApp enviado correctamente", "sid": sid}
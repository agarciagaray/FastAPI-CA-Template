import os

from fastapi import APIRouter, Depends, File, Form, UploadFile

from src.utils.email_sender import send_email
from src.auth.service import get_current_user  # Ajusta la ruta según tu proyecto

router = APIRouter(
    prefix="/email",
    tags=["Emails"],
    dependencies=[Depends(get_current_user)]  # <-- Protección aquí
)


@router.post("/send", description="Permite enviar correos electrónicos con o sin adjuntos a través de SMTP.")
async def send_email_route(
    subject: str = Form(...),
    body: str = Form(...),
    to: str = Form(...),
    file: UploadFile = File(None)
):
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 465))

    attachment = await file.read() if file else None
    attachment_filename = file.filename if file else None

    send_email(
        subject, body, to,
        smtp_user, smtp_password, smtp_server, smtp_port,
        attachment, attachment_filename
    )
    return {"message": "Correo enviado correctamente"}

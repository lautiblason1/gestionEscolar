import qrcode
import secrets
from pathlib import Path
from django.conf import settings

def generar_token():
    return secrets.token_urlsafe(16)

def generar_qr_imagen(url, token, filename_template="qr_{token}.png"):
    # asegurar MEDIA_ROOT como Path
    media_root = Path(settings.MEDIA_ROOT)
    media_root.mkdir(parents=True, exist_ok=True)

    filename = filename_template.format(token=token)
    path = media_root / filename

    img = qrcode.make(url)
    img.save(path)

    # devolver la URL pública del archivo
    media_url = settings.MEDIA_URL.rstrip('/')
    return f"{media_url}/{filename}"


import base64
from pdf2image import convert_from_bytes
from io import BytesIO
from fastapi import HTTPException

async def convert_pdf_image(file_content: bytes) -> str:
    """
    Convierte un archivo PDF en una imagen codificada en Base64.

    Args:
        file_content (bytes): Contenido del archivo PDF en bytes.

    Returns:
        str: Imagen de la primera página del PDF codificada en Base64.

    Raises:
        HTTPException: Si ocurre un error al procesar el PDF.
    """
    try:
        # Convertir PDF a imágenes
        print("Convirtiendo PDF en imágenes...")
        images = convert_from_bytes(file_content, dpi=300)
        if not images:
            raise HTTPException(status_code=400, detail="No se pudieron generar imágenes desde el PDF.")

        # Tomar solo la primera página del PDF
        first_page = images[0]

        # Convertir la primera página a Base64
        print("Convirtiendo la primera página a Base64...")
        buffered = BytesIO()
        first_page.save(buffered, format="JPEG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        # Verificar longitud de la imagen codificada
        print("Longitud de la imagen en Base64:", len(image_base64))

        return image_base64

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al convertir PDF a imagen: {str(e)}")
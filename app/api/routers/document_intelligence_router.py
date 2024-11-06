from fastapi import APIRouter, BackgroundTasks, UploadFile, File, HTTPException, Response
from PIL import Image
from app.business.use_cases.extract_text import ExtractTextFromPDF
import pytesseract
from io import BytesIO
from app.services.document_intelligence_service import PDFExtractor  # Para PDF exclusivamente
import easyocr  # Importamos EasyOCR
import numpy as np
from autogen import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager

router = APIRouter()

############ Seccion de agentes y configuraciones ############ 
# Define llm_config to use in GroupChatManager
llm_config = {
    "cache_seed": 42,
    "temperature": 0,
    "config_list": [{'model': 'gpt-4o', 'api_key': ''}],
    "timeout": 120,
}    

# Define the different prompts
task = '''
    Task: Como asistente, debes organizar el siguiente texto extraído mediante OCR, asegurándote de que cada dato se presente en un formato de clave. El texto contiene información compleja con varias categorías y valores que se separan por saltos de línea (\n). El objetivo es proporcionar una representación clara y estructurada, para facilitar la comprensión de la información contenida en el documento. Los requisitos son los siguientes:
    Identificar y asignar cada segmento de información a una clave relevante.
    Usar nombres de clave significativos que describan claramente el contenido del valor.
    Organizar el texto para que sea fácil de entender y procesar.
    Evitar repeticiones innecesarias y categorizar correctamente los datos.
    Utilizar la estructura JSON para presentar la información.
    Mantener coherencia en la nomenclatura y ser preciso en la identificación de cada campo.
    Texto: "3920143738 9\nDECLARACION DE INGRESO\nFecha cevercimiento\nWus\nVALPARAISO\nVoncaferhandeZpollnink\nIMPORICIDO AMIIC\n..."
    Chain-of-Thought:
    Identificación de Secciones: Primero, revisa todo el texto para identificar secciones y categorías importantes. Identifica datos que pertenezcan a categorías como "Identificación", "Transporte", "Origen", etc.
    Asignación de Claves: Para cada fragmento de texto, asigna una clave que describa claramente su contenido. Las claves deben ser descriptivas, por ejemplo: "NUMERO", "CIUDAD", "LINEA_NAVIERA".
    Formato de JSON: Organiza los datos en un formato JSON, donde cada clave tiene un valor que corresponda a la información relevante extraída.
    Estandarización y Revisión: Asegúrate de que los nombres de las claves sean consistentes y los valores estén correctamente alineados con su contexto. Verifica que no haya errores tipográficos y que cada campo sea único y comprensible.
    Resultado Final: Presenta el texto original en un formato estructurado, utilizando claves descriptivas y asegurándote de que toda la información esté correctamente organizada.
    '''

validation_prompt = '''
    Task: Como agente de validación, tu objetivo es revisar y garantizar la calidad del texto estructurado generado mediante OCR, asegurándote de que se haya seguido correctamente el proceso de organización en un formato de clave. El texto estructurado se presenta en formato JSON, y debes realizar las siguientes tareas:
    Verificar que cada clave sea clara, concisa y representativa del contenido del valor.
    Comprobar que no existan errores tipográficos en las claves o valores, asegurando coherencia en la nomenclatura.
    Asegurarse de que no haya información duplicada o categorizada incorrectamente.
    Confirmar que se sigan los estándares de estructura JSON, garantizando que el formato sea consistente y fácil de procesar.
    Identificar posibles inconsistencias o faltas de alineación entre claves y valores y sugerir correcciones.
    Chain-of-Thought:
    Revisión de Claves: Revisa cada clave y asegúrate de que sea descriptiva y represente de manera precisa el valor asociado. Sugerir mejores nombres si es necesario.
    Verificación de Estructura: Comprueba que la estructura JSON esté bien formada, sin errores de sintaxis y siguiendo estándares de buena práctica.
    Control de Calidad de Datos: Verifica que no haya datos repetidos y que cada segmento de información esté correctamente categorizado.
    Validación de Consistencia: Revisa la coherencia en la nomenclatura de las claves y asegura que los valores estén alineados con el contexto que representan.
    Propuesta de Mejoras: Proporciona recomendaciones para mejorar la claridad o estructura de la información si es necesario.
    El objetivo es garantizar que el texto estructurado sea claro, preciso y siga las mejores prácticas para su uso futuro.
    '''

# Define the agent configuration
user_proxy = UserProxyAgent(
    name="supervisor",
        system_message="Humano experto en validación y organización de texto estructurado generado mediante OCR",
        code_execution_config={
            "last_n_messages": 2,  # Analyze the last 2 messages to understand context and flow
            "work_dir": "groupchat",  # Directory for handling validation and organization-related files
            "use_docker": False,  # No need for containerized execution in this context
        },
        human_input_mode="NEVER",  # Operates autonomously without requiring human input during execution
    )

validation_agent = AssistantAgent(
    name="validation_agent",
    system_message=validation_prompt,
    llm_config={"config_list": llm_config["config_list"]}
)

# State transition logic
def state_transition(last_speaker, groupchat):
    if last_speaker is user_proxy:
        return validation_agent
    elif last_speaker is validation_agent:
       return None

# Función de procesamiento en segundo plano
async def organize_extracted_text(texto_extraido: str):
    groupchat = GroupChat(
        agents=[user_proxy, validation_agent],
        messages=[],
        max_round=3,
        speaker_selection_method=state_transition,
    )
    manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
    
    user_proxy.initiate_chat(manager, message=texto_extraido)
    responses = [message["content"] for message in groupchat.messages]
    return responses   

# Función para extraer texto de un PDF en segundo plano y luego procesarlo
async def extract_text_from_pdf_background(file_content: bytes, background_tasks: BackgroundTasks):
    pdf_extractor = PDFExtractor(file_stream=file_content)
    use_case = ExtractTextFromPDF(extractor=pdf_extractor)
    try:
        texto_extraido = use_case.execute()
        background_tasks.add_task(organize_extracted_text, texto_extraido)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e)) 

# Función para extraer texto de una imagen en segundo plano y luego procesarlo
async def extract_text_from_image_background(file_content: bytes, background_tasks: BackgroundTasks, use_easyocr: bool = False):
    try:
        if use_easyocr:
            reader = easyocr.Reader(['es', 'en'])
            imagen = Image.open(BytesIO(file_content)).convert('RGB')
            imagen_np = np.array(imagen)
            result = reader.readtext(imagen_np)
            texto_extraido = "\n".join([res[1] for res in result])
        else:
            imagen = Image.open(BytesIO(file_content))
            texto_ocr = pytesseract.image_to_string(imagen)
            texto_extraido = texto_ocr

        background_tasks.add_task(organize_extracted_text, texto_extraido)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")       

@router.post("/extract-text/")
async def extract_text_from_pdf(background_tasks: BackgroundTasks,file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")

    try:
        file_content = await file.read()
        background_tasks.add_task(extract_text_from_pdf_background, file_content, background_tasks)
        return Response(content='{"status": "El texto está siendo extraído y procesado en segundo plano."}', media_type="application/json", status_code=202)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo: {str(e)}")   

# Ruta para manejar la subida de imágenes y ejecutar la extracción y procesamiento en segundo plano con pytesseract
@router.post("/extract-ocr/")
async def extract_text_from_image( background_tasks: BackgroundTasks,file: UploadFile = File(...)):
    if not file.filename.endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen (.png, .jpg, .jpeg)")

    try:
        file_content = await file.read()
        background_tasks.add_task(extract_text_from_image_background, file_content, background_tasks, False)
        return Response(content='{"status": "El texto OCR está siendo extraído y procesado en segundo plano."}', media_type="application/json", status_code=202)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo: {str(e)}")

# Ruta para manejar la subida de imágenes y ejecutar la extracción y procesamiento en segundo plano con EasyOCR
@router.post("/extract-ocr-easy/")
async def extract_text_with_easyocr(background_tasks: BackgroundTasks,file: UploadFile = File(...)):
    if not file.filename.endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen (.png, .jpg, .jpeg)")

    try:
        file_content = await file.read()
        background_tasks.add_task(extract_text_from_image_background, file_content, background_tasks, True)
        return Response(content='{"status": "El texto OCR está siendo extraído con EasyOCR y procesado en segundo plano."}', media_type="application/json", status_code=202)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo: {str(e)}")




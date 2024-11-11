from fastapi import HTTPException
from autogen import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager
from app.core.config import LLM_CONFIG as llm_config
from app.business.prompts.prompts_extract import task, validation_prompt, validation_prompt_TGR, validation_prompt_AFORO
from bson import ObjectId
from datetime import datetime
from app.db.base import mongo_db
from bson import json_util

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

validation_agent_TGR = AssistantAgent(
    name="validation_agent",
    system_message=validation_prompt_TGR,
    llm_config={"config_list": llm_config["config_list"]}
)

validation_agent_AFORO = AssistantAgent(
    name="validation_agent",
    system_message=validation_prompt_AFORO,
    llm_config={"config_list": llm_config["config_list"]}
)

# State transition logic
def state_transition(last_speaker, groupchat):
    if last_speaker is user_proxy:
        return validation_agent
    elif last_speaker is validation_agent:
       return None

# State transition logic
def state_transition_TGR(last_speaker, groupchat):
    if last_speaker is user_proxy:
        return validation_agent_TGR
    elif last_speaker is validation_agent_TGR:
       return None   

# State transition logic
def state_transition_AFORO(last_speaker, groupchat):
    if last_speaker is user_proxy:
        return validation_agent_AFORO
    elif last_speaker is validation_agent_AFORO:
       return None     

# Función de procesamiento en segundo plano
async def organize_extracted_text(texto_extraido: str, document_id: str = None, ocr_engine: str = None):
    """
    Procesa el texto extraído y actualiza el estado del documento en MongoDB si es necesario.
    """
    try:
        # Configuración de agentes y gestor de chat
        groupchat = GroupChat(
            agents=[user_proxy, validation_agent],
            messages=[],
            max_round=3,
            speaker_selection_method=state_transition,
        )
        manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

        # Procesa el texto extraído con los agentes
        user_proxy.initiate_chat(manager, message=texto_extraido)
        responses = [message["content"] for message in groupchat.messages]

        # Actualiza el estado del documento en MongoDB solo si se proporciona document_id
        if document_id and ocr_engine == "EASY-OCR":
            collection = mongo_db["extraction_requests"]
            responses = json_util.dumps(responses)  # Serializa el campo si es necesario

            update_data = {
                "status": "Terminado",
                "completed_at": datetime.utcnow(),
                "din": responses,
                "ocr_engine": ocr_engine,  # Solo se incluye si es EASY-OCR
            }

            await collection.update_one({"_id": ObjectId(document_id)}, {"$set": update_data})

        return responses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el texto: {str(e)}")


# Función de procesamiento en segundo plano
async def organize_extracted_text_TGR(texto_extraido: str):
    """
    Procesa el texto extraído y actualiza el estado del documento en MongoDB si es necesario.
    """
    try:
        # Configuración de agentes y gestor de chat
        groupchat = GroupChat(
            agents=[user_proxy, validation_agent_TGR],
            messages=[],
            max_round=3,
            speaker_selection_method=state_transition_TGR,
        )
        manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

        # Procesa el texto extraído con los agentes
        user_proxy.initiate_chat(manager, message=texto_extraido)
        responses = [message["content"] for message in groupchat.messages]

        # Actualiza el estado del documento en MongoDB solo si se proporciona document_id
        
        return responses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el texto: {str(e)}")    


# Función de procesamiento en segundo plano
async def organize_extracted_text_AFORO(texto_extraido: str):
    """
    Procesa el texto extraído y actualiza el estado del documento en MongoDB si es necesario.
    """
    try:
        # Configuración de agentes y gestor de chat
        groupchat = GroupChat(
            agents=[user_proxy, validation_agent_AFORO],
            messages=[],
            max_round=3,
            speaker_selection_method=state_transition_AFORO,
        )
        manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

        # Procesa el texto extraído con los agentes
        user_proxy.initiate_chat(manager, message=texto_extraido)
        responses = [message["content"] for message in groupchat.messages]

        # Actualiza el estado del documento en MongoDB solo si se proporciona document_id
        
        return responses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el texto: {str(e)}")

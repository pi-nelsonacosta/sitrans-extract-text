from autogen import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager
from app.core.config import LLM_CONFIG as llm_config
from app.business.prompts.prompts_extract import task, validation_prompt

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
    system_message=task + validation_prompt,
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
    # Asumimos que responses[0] contiene el JSON generado
    """ json_result = responses[0]
    
    # Crear una nueva sesión de SQL Server
    db: Session = SQLServerSessionLocal()
    
    try:
        # Reutilizar el método existente para crear un registro
        create_sqlserver_record(db=db, description='Testing')
        print("JSON guardado correctamente en SQL Server.")
    except Exception as e:
        print(f"Error al guardar en SQL Server: {e}")
        raise e
    finally:
        db.close()  """
    
    return responses
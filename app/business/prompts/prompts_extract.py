# Define the different prompts
# Prompt simplificado
prompt_aforo = """
        Analiza el contenido de esta imagen estructurada y extrae los datos en el siguiente formato JSON:
        {
            "solicitud":"", 
            "folioDIN":"", 
            "fechaAceptacion":"””", 
            "numeroEncriptado":"", 
            "codigoAgente":"””", 
            "nombreAgente":"””", 
            "codigoAduanaTramitacion":"””", 
            "tipoRevision":"””", 
            "FirmaAgencia":"””" 
        }
        """

prompt_tgr = """
        Analiza el contenido de esta imagen y devuelve únicamente los datos en el siguiente formato JSON:
        {
            "solicitud": "", 
            "rutConsignatario": "", 
            "formularioConsignatario": "", 
            "folioDIN": "", 
            "vencimientoDIN": "", 
            "monedaPago": "", 
            "totalPagado": "",
            "fechaPago": "", 
            "institucionRecaudadora": "", 
            "identificadorTransaccion": ""
        }
        """
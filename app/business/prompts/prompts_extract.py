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
prompt_din= """Como asistente, debes organizar el siguiente texto extraído mediante OCR, asegurándote de que cada dato se presente en un formato de clave. El texto contiene información compleja con varias categorías y valores que se separan por saltos de línea (\n). El objetivo es proporcionar una representación clara y estructurada, para facilitar la comprensión de la información contenida en el documento. Los requisitos son los siguientes:
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
    Al final estara un texto_extraido, para que puedas tener referencia de los campos a leer y sus valores.
    Proximo es la salida, que debe ser en este formato:
    
    { 

     "DIN":{ 
      "solicitud":"", 
      "numeroDin":"", 
      "fechaDin":"””", 
      "aduana":"", 
      "consignatarioOimportador":"””", 
      "rutConsignatario":"””", 
      "paisOrigen":"””", 
      "puertoEmbarque":"””", 
      "puertoDesembarque":"””", 
      "manifiesto":"””", 
      "doctoTransporte":"””", 
      "bultos":[ 
         { 
            "numeroBulto":"", 
            "tipoBulto":"””", 
            "cantTipoBulto":"””" 
         } 
      ], 
      "totalBultos":"””", 
      "pesoBruto":"””", 
      "observacionesBultos":"””", 
      "totalEnPesos":"””", 
      "tipoInspeccion":"””", 
      "resultado":"””", 
      "direccionConsignatario":"””" 
       } 
    } 
    """ 
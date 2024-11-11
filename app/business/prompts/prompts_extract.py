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
    Palabras claves: [
                "solicitud",
                "numeroDin",
                "fechaDin",
                "aduana",
                "consignatarioOimportador",
                "rutConsignatario",
                "paisOrigen",
                "puertoEmbarque",
                "puertoDesembarque",
                "manifiesto",
                "doctoTransporte",
                "bultos",
                "numeroBulto",
                "tipoBulto",
                "cantTipoBulto",
                "totalBultos",
                "pesoBruto",
                "observacionesBultos",
                "totalEnPesos",
                "tipoInspeccion",
                "resultado",
                "direccionConsignatario"
                ]
    Chain-of-Thought:
    Revisión de Claves: Revisa cada clave y asegúrate de que sea descriptiva y represente de manera precisa el valor asociado. Sugerir mejores nombres si es necesario.
    Verificación de Estructura: Comprueba que la estructura JSON esté bien formada, sin errores de sintaxis y siguiendo estándares de buena práctica.
    Control de Calidad de Datos: Verifica que no haya datos repetidos y que cada segmento de información esté correctamente categorizado.
    Validación de Consistencia: Revisa la coherencia en la nomenclatura de las claves y asegura que los valores estén alineados con el contexto que representan.
    Propuesta de Mejoras: Proporciona recomendaciones para mejorar la claridad o estructura de la información si es necesario.
    El objetivo es garantizar que el texto estructurado sea claro, preciso y siga las mejores prácticas para su uso futuro.
    Necesito que mejores los datos procesados y que generes un Json de la siguiente manera:
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
    '''  

validation_prompt_TGR = '''
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
    Necesito que mejores los datos procesados y que generes un Json de la siguiente manera:
    { 

     "TGR":{ 

      "solicitud":"", 

      "rutConsignatario":"", 

      "formularioConsignatario":"””", 

      "folioDIN":"", 

      "vencimientoDIN":"””", 

      "monedaPago":"””", 

      "totalPagado":"””", 

      "fechaPago":"””", 

      "institucionRecaudadora":"””", 

      "identificadorTransaccion":"””" 

   } 
    '''  
    
validation_prompt_AFORO = '''
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
    Necesito que mejores los datos procesados y que generes un Json de la siguiente manera:
    { 

   "Aforo":{ 

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

} 
    '''  
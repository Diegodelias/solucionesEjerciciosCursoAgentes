"""
EJERCICIO 1: Sistema de IA con Agentic - 3 Llamadas Secuenciales

ENUNCIADO:
----------
1. Primero, pide al LLM que elija un área de negocio que valga la pena explorar 
   para una oportunidad de IA con Agentic.

2. Después, pide al LLM que presente un problema en esa industria, algo desafiante 
   que pueda ser propicio para una solución con Agentic.

3. Finalmente, pide a la tercera convocatoria del LLM que proponga la solución 
   de IA con Agentic.

OBJETIVO:
---------
Implementar un sistema que realice 3 llamadas secuenciales al LLM, donde cada 
llamada utiliza el contexto de las anteriores para mantener coherencia en la 
conversación.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# TODO: Cargar las variables de entorno desde el archivo .env
# Pista: Usa load_dotenv()
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# TODO: Inicializar el cliente de OpenAI
# Pista: client = OpenAI(api_key=...)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))




def llamar_llm(prompt, contexto_previo=None):
    """
    Función para hacer una llamada al LLM de OpenAI
    
    Args:
        prompt: El prompt a enviar al LLM
        contexto_previo: Lista de mensajes previos (opcional)
    
    Returns:
        La respuesta del LLM como string
    """
    # TODO: Crear una lista de mensajes vacía
    mensajes = []
    
    # TODO: Si hay contexto previo, agregarlo a los mensajes
    # Pista: Usa mensajes.extend(contexto_previo)
    if contexto_previo:
        mensajes.extend(contexto_previo)
    
    
    # TODO: Agregar el nuevo prompt del usuario a los mensajes
    # Pista: El formato es {"role": "user", "content": prompt}
    mensajes.append({"role": "user", "content": prompt})
    
    # TODO: Hacer la llamada al LLM usando client.chat.completions.create()
    # Parámetros sugeridos:
    # - model: "gpt-4o-mini" o "gpt-4.1-mini"
    # - messages: la lista de mensajes
    # - temperature: 0.7
    # - max_tokens: 500
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # <-- Modelo seleccionado
        messages=mensajes,
        temperature=0.7,
        max_tokens=500
    )
    
    
    # TODO: Retornar el contenido de la respuesta
    # Pista: response.choices[0].message.content
    return response.choices[0].message.content
    

def main():
   
    print("=" * 80)
    print("EJERCICIO 1: Sistema de IA con Agentic - 3 Llamadas Secuenciales")
    print("=" * 80)
    
    # TODO: Crear una lista para mantener el historial de conversación
    historial = []
    
    # ========================================================================
    # PASO 1: Elegir un área de negocio
    # ========================================================================
    print("\n[PASO 1] Pidiendo al LLM que elija un área de negocio...\n")
    
    # TODO: Crear el prompt para que el LLM elija un área de negocio
    # El prompt debe pedir:
    # - Un área de negocio específica
    # - Que sea prometedora para IA con Agentic
    # - Una breve justificación
    prompt_1 = """
    Elige un área de negocio interesante para una solución de IA con Agentic y justifica brevemente por qué.
    """
    
    # TODO: Llamar a la función llamar_llm() con el prompt_1
    respuesta_1 = llamar_llm(prompt_1)  # Reemplaza con la llamada real
    
    print(f"Respuesta: {respuesta_1}")
    
    # TODO: Agregar el prompt y la respuesta al historial
    # Formato: {"role": "user", "content": ...} y {"role": "assistant", "content": ...}
    
    
    # ========================================================================
    # PASO 2: Presentar un problema en esa industria
    # ========================================================================
    print("\n" + "-" * 80)
    print("[PASO 2] Pidiendo al LLM que presente un problema en esa industria...\n")
    
    # TODO: Crear el prompt para que el LLM describa un problema
    # El prompt debe pedir:
    # - Un problema específico basado en el área elegida
    # - Que sea desafiante
    # - Que pueda beneficiarse de IA con Agentic
    prompt_2 = """
    # Escribe aquí tu prompt
    """
    
    # TODO: Llamar a la función llamar_llm() con el prompt_2 Y el historial
    respuesta_2 = None  # Reemplaza con la llamada real
    
    print(f"Respuesta: {respuesta_2}")
    
    # TODO: Agregar el prompt y la respuesta al historial
    
    
    # ========================================================================
    # PASO 3: Proponer la solución de IA con Agentic
    # ========================================================================
    print("\n" + "-" * 80)
    print("[PASO 3] Pidiendo al LLM que proponga una solución de IA con Agentic...\n")
    
    # TODO: Crear el prompt para que el LLM proponga una solución
    # El prompt debe pedir:
    # - Una solución detallada de IA con Agentic
    # - Cómo funcionaría el sistema agéntico
    # - Qué agentes específicos se necesitarían
    # - Cómo trabajarían de forma autónoma
    # - Beneficios concretos
    prompt_3 = """
    # Escribe aquí tu prompt
    """
    
    # TODO: Llamar a la función llamar_llm() con el prompt_3 Y el historial
    respuesta_3 = None  # Reemplaza con la llamada real
    
    print(f"Respuesta: {respuesta_3}")
    
    # Resumen final
    print("\n" + "=" * 80)
    print("RESUMEN DEL EJERCICIO COMPLETADO")
    print("=" * 80)
    print(f"\n✓ Área de negocio identificada")
    print(f"✓ Problema específico descrito")
    print(f"✓ Solución de IA con Agentic propuesta")
    print("\nEjercicio completado exitosamente!")


if __name__ == "__main__":
    main()


"""
TIPS:
----------------------

1. CONFIGURACIÓN INICIAL:
   - Asegúrate de tener instaladas las librerías: pip install openai python-dotenv
   - Crea un archivo .env con tu OPENAI_API_KEY
   - Importa las librerías necesarias

2. ESTRUCTURA DE MENSAJES:
   Los mensajes para OpenAI tienen este formato:
   {"role": "user", "content": "tu pregunta"}
   {"role": "assistant", "content": "respuesta del LLM"}

3. MANTENER CONTEXTO:
   Para que el LLM recuerde las conversaciones anteriores, debes pasar
   el historial completo en cada llamada.

4. LLAMADA A LA API:
   response = client.chat.completions.create(
       model="gpt-4o-mini",
       messages=[...],
       temperature=0.7,
       max_tokens=500
   )
   
5. OBTENER LA RESPUESTA:
   texto = response.choices[0].message.content

6. PROMPTS EFECTIVOS:
   - Sé específico en lo que pides
   - Usa instrucciones claras
   - Pide formato o estructura si es necesario
   - Usa el contexto de respuestas anteriores

¡Buena suerte!
"""

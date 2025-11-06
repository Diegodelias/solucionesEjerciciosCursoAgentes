"""
EJERCICIO 2: Agente de Información de Países con API Pública

ENUNCIADO:
----------
Crear un agente inteligente que:

1. Reciba consultas en lenguaje natural sobre países del mundo
   Ejemplo: "¿Cuál es la capital de Francia?"
   Ejemplo: "Dime la población y moneda de Argentina"

2. Use el LLM de OpenAI para:
   - ANALIZAR LA INTENCIÓN del usuario (qué aspectos le interesan)
   - Extraer el nombre del país de la consulta del usuario
   - Interpretar qué información específica se está solicitando

3. Consulte la API REST Countries (https://restcountries.com/v3.1/name/{pais})
   para obtener datos reales del país

4. Use nuevamente el LLM para:
   - Formatear la respuesta de la API en lenguaje natural
   - PERSONALIZAR la respuesta según los aspectos identificados
   - Presentar la información de forma conversacional al usuario

OBJETIVO:
---------
Implementar un agente que integre:
- LLM para procesamiento de lenguaje natural
- Análisis de intención para respuestas personalizadas (NUEVO)
- API externa para obtener datos reales
- Flujo de trabajo agéntico (percepción → análisis → acción → respuesta)

API A UTILIZAR:
---------------
REST Countries API v3.1
- URL base: https://restcountries.com/v3.1
- Endpoint: /name/{nombre_pais}
- No requiere API key
- Documentación: https://restcountries.com

DATOS DISPONIBLES:
------------------
- Capital, población, área
- Idiomas oficiales, monedas
- Región, subregión
- Países fronterizos
- Bandera (emoji y URL)
- Zona horaria, código de llamada
"""

import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv


# TODO: Cargar las variables de entorno
# Pista: load_dotenv()

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


# TODO: Inicializar el cliente de OpenAI
client = OpenAI(api_key=api_key)        


def extraer_pais(consulta_usuario):
    """
    Usa el LLM para extraer el nombre del país de la consulta del usuario.
    
    Args:
        consulta_usuario: La pregunta del usuario en lenguaje natural
    
    Returns:
        El nombre del país en inglés (para la API)
    """
    # TODO: Crear un prompt que le pida al LLM extraer el nombre del país
    # El prompt debe:
    # - Indicar que debe extraer solo el nombre del país
    # - Pedir que responda SOLO con el nombre en inglés
    # - Sin explicaciones adicionales
    
    prompt = f"""
Instrucción: Del siguiente texto, extrae únicamente el nombre del país.
Responde SOLO con el nombre del país en inglés. No incluyas ningún texto, 
explicación, puntuación o carácter adicional.

Texto: "{consulta_usuario}"

Respuesta Esperada:
"""
    
    # TODO: Hacer la llamada al LLM
    # Usa client.chat.completions.create()
    # model: "gpt-4o-mini"
    # messages: [{"role": "user", "content": prompt}]
    # temperature: 0.3 (baja para respuestas más precisas)
    mensajes = []
    
    mensajes.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
            model="gpt-4o-mini",  # <-- Modelo seleccionado
            messages=mensajes,
            temperature=0.7,
            max_tokens=500
        )
    # TODO: Retornar el nombre del país extraído
    # Pista: response.choices[0].message.content.strip()
    return response.choices[0].message.content



    

def consultar_api_paises(nombre_pais):
    """
    Consulta la API de REST Countries para obtener información del país.
    
    Args:
        nombre_pais: Nombre del país en inglés
    
    Returns:
        Diccionario con los datos del país o None si hay error
    """
    # TODO: Construir la URL de la API
    # URL base: https://restcountries.com/v3.1/name/
    # Agregar el nombre del país al final
    
    url = f"https://restcountries.com/v3.1/name/{nombre_pais}"
    
    try:
        # TODO: Hacer la petición GET a la API
        # Pista: response = requests.get(url)
        response = requests.get(url)
        
        # TODO: Verificar si la respuesta fue exitosa
        # Pista: response.status_code == 200
        if response.status_code == 200:
            # TODO: Convertir la respuesta JSON a diccionario Python
            # Pista: datos = response.json()
            # La API devuelve una lista, toma el primer elemento [0]
            datos = response.json()
            
            # TODO: Retornar los datos del país
            return datos[0]
        else:
            print(f"Error: La API respondió con código {response.status_code}")
            return None
        
    except requests.exceptions.RequestException as e:
        print(f"Error al consultar la API: {e}")
        return None


def formatear_respuesta(consulta_usuario, datos_pais):
    """
    Usa el LLM para formatear los datos del país en una respuesta natural.
    
    Args:
        consulta_usuario: La pregunta original del usuario
        datos_pais: Diccionario con los datos del país de la API
        aspectos: Lista de aspectos de interés identificados (opcional)
    
    Returns:
        Respuesta formateada en lenguaje natural
    """

    # TODO: Extraer información relevante de los datos del país
    # Algunos campos útiles:
    # - datos_pais['name']['common']: Nombre común
    # - datos_pais['capital'][0]: Capital
    # - datos_pais['population']: Población
    # - datos_pais['region']: Región
    # - datos_pais['subregion']: Subregión
    # - datos_pais['languages']: Idiomas (diccionario)
    # - datos_pais['currencies']: Monedas (diccionario)
    # - datos_pais['area']: Área en km²
    # - datos_pais['flag']: Emoji de la bandera
    
    # Convertir los datos a un formato legible para el LLM
    info_pais = f"""
    Nombre: {datos_pais.get('name', {}).get('common', 'N/A')}
    Capital: {datos_pais.get('capital', ['N/A'])[0] if datos_pais.get('capital') else 'N/A'}
    Población: {datos_pais.get('population', 'N/A'):,}
    Región: {datos_pais.get('region', 'N/A')}
    Subregión: {datos_pais.get('subregion', 'N/A')}
    Área: {datos_pais.get('area', 'N/A'):,} km²
    Bandera: {datos_pais.get('flag', '')}
    """
    
    # TODO: Agregar idiomas si existen
    # Pista: datos_pais.get('languages', {}).values()
    idiomas = datos_pais.get('languages', {})
    if idiomas:
        lista_idiomas = list(idiomas.values())
        info_pais += f"\nIdiomas: {', '.join(lista_idiomas)}"
    
    # TODO: Agregar monedas si existen
    # Pista: datos_pais.get('currencies', {})
    monedas_dict = datos_pais.get('currencies', {})
    if monedas_dict:
        # Extraer el nombre de cada moneda del diccionario
        nombres_monedas = [moneda.get('name', 'N/A') for moneda in monedas_dict.values()]
        info_pais += f"\nMonedas: {', '.join(nombres_monedas)}"
  
    # TODO: Crear un prompt que le pida al LLM formatear la respuesta
    # El prompt debe:
    # - Incluir la consulta original del usuario
    # - Incluir la información del país
    # - Pedir una respuesta natural y conversacional
    # - Responder específicamente a lo que el usuario preguntó
    
 
    prompt = f"""
**Instrucción de Rol:** Eres un asistente conversacional útil y amigable. Tu objetivo es responder directamente a la consulta original del usuario utilizando la información proporcionada a continuación.

**Requisitos de la Respuesta:**
1.  **Natural y Conversacional:** La respuesta debe sonar natural y ser amigable.
2.  **Respuesta Directa:** Responde a la pregunta del usuario de la manera más directa y concisa posible, basándote únicamente en la información que se te proporciona.
3.  **Enfoque Específico:** Prioriza la información relacionada con los aspectos de interés identificados.

---

**Consulta Original del Usuario:**
"{consulta_usuario}"

**Información Relevante Proporcionada:**
{info_pais}

---

**Respuesta:**
"""
    
    # TODO: Hacer la llamada al LLM
    # Usa client.chat.completions.create()
    # temperature: 0.7 (para respuestas más naturales)
    response = client.chat.completions.create(
            model="gpt-4o-mini",  # <-- Modelo seleccionado
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
    
    
    # TODO: Retornar la respuesta formateada
    return response.choices[0].message.content





def agente_paises(consulta_usuario):
    """
    Función principal del agente que orquesta todo el flujo.
    
    Args:
        consulta_usuario: La pregunta del usuario
    
    Returns:
        Respuesta final del agente
    """
    print(f"\n🤖 Agente: Procesando tu consulta...\n")
    
    
    
    # PASO 2: Extraer el país de la consulta
    print("📍 Paso 2: Identificando el país...")
    pais = extraer_pais(consulta_usuario)
    
    if not pais:
        return "❌ No pude identificar el país en tu consulta. ¿Podrías reformularla?"
    
    print(f"   ✓ País identificado: {pais}")
    
    # PASO 3: Consultar la API
    print("🌍 Paso 3: Consultando información del país...")
    datos = consultar_api_paises(pais)
    
    if not datos:
        return f"❌ No encontré información sobre '{pais}'. Verifica el nombre del país."
    
    print(f"   ✓ Datos obtenidos de la API")
    
    # PASO 4: Formatear la respuesta con los aspectos identificados
    print("💬 Paso 4: Generando respuesta personalizada...\n")
    respuesta = formatear_respuesta(consulta_usuario, datos)
    
    return respuesta


def main():
    print("=" * 80)
    print("🌎 AGENTE INTELIGENTE DE INFORMACIÓN DE PAÍSES")
    print("=" * 80)
    print("\nEste agente analiza tu intención y responde preguntas sobre países.")
    print("\n🧠 Características:")
    print("  ✓ Analiza qué aspectos te interesan (economía, turismo, etc.)")
    print("  ✓ Personaliza la respuesta según tu pregunta")
    print("  ✓ Obtiene datos reales de APIs")
    print("\nEjemplos:")
    print("  - ¿Cuál es la capital de Francia?")
    print("  - Dime la población de Japón")
    print("  - ¿Qué moneda usa Argentina?")
    print("  - Háblame sobre la historia de Italia")
    print("  - ¿Qué idiomas se hablan en Suiza?")
    print("\nEscribe 'salir' para terminar.")
    print("=" * 80)
    
    while True:
        # TODO: Solicitar la consulta del usuario
        consulta = input("\n👤 Tu consulta: ").strip()
        
        # TODO: Verificar si el usuario quiere salir
        if consulta.lower() in ['salir', 'exit', 'quit']:
            print("\n👋 ¡Hasta luego!")
            break
        
        # TODO: Verificar que la consulta no esté vacía
        if not consulta:
            print("⚠️  Por favor, escribe una consulta.")
            continue
        
        # TODO: Llamar al agente con la consulta
        respuesta = agente_paises(consulta)
        
        
        
        # TODO: Mostrar la respuesta
        print(f"\n🤖 Agente: {respuesta}")
        print("\n" + "-" * 80)


if __name__ == "__main__":
    main()


"""
TIPS PARA COMPLETAR EL EJERCICIO:
----------------------------------

1. ANÁLISIS DE INTENCIÓN (NUEVO):
   - Identifica qué aspectos le interesan al usuario
   - Usa temperature baja (0.3) para clasificación precisa
   - Devuelve lista de aspectos: ['capital', 'poblacion', etc.]
   - Mejora la personalización de la respuesta

2. EXTRACCIÓN DEL PAÍS:
   - Usa un prompt claro y específico
   - Pide al LLM que responda SOLO con el nombre del país
   - Usa temperature baja (0.3) para respuestas precisas

3. CONSULTA A LA API:
   - La API devuelve una lista, usa [0] para el primer resultado
   - Maneja errores con try/except
   - Verifica el status_code antes de procesar

4. FORMATEO DE RESPUESTA:
   - Incluye la consulta original en el prompt
   - Proporciona todos los datos relevantes al LLM
   - Incluye los aspectos identificados para personalizar
   - Usa temperature más alta (0.7) para respuestas naturales

5. MANEJO DE DATOS:
   - Usa .get() para acceder a campos que pueden no existir
   - Los idiomas y monedas son diccionarios anidados
   - Formatea números grandes con comas para legibilidad

6. FLUJO DEL AGENTE MEJORADO:
   Usuario → LLM (analiza intención) → LLM (extrae país) → API → LLM (formatea con aspectos) → Usuario

🎯 VENTAJAS DE ANALIZAR LA INTENCIÓN:
   ✓ Respuestas más enfocadas y relevantes
   ✓ Mejor experiencia del usuario
   ✓ El agente "entiende" qué busca el usuario
   ✓ Puede priorizar información específica

¡Buena suerte! 🚀
"""

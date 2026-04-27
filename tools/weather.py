# tools/weather.py
import requests
import os
from dotenv import load_dotenv
from config import WEATHER_API_KEY

load_dotenv()

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city: str = "Monterrey") -> str:
    """
    Consulta el clima de una ciudad.
    Devuelve un string listo para que el LLM lo lea en voz alta.
    """
    if not WEATHER_API_KEY:
        return "No tengo configurada la API key del clima."

    try:
        params = {
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric",      # Celsius
            "lang": "es"            # Descripción en español
        }

        response = requests.get(BASE_URL, params=params, timeout=5)

        if response.status_code == 404:
            return f"No encontré la ciudad '{city}'. ¿Puedes verificar el nombre?"

        if response.status_code != 200:
            return f"Hubo un error consultando el clima (código {response.status_code})."

        data = response.json()

        ciudad        = data["name"]
        pais          = data["sys"]["country"]
        temp          = data["main"]["temp"]
        sensacion     = data["main"]["feels_like"]
        humedad       = data["main"]["humidity"]
        descripcion   = data["weather"][0]["description"]
        viento        = data["wind"]["speed"]

        return (
            f"En {ciudad}, {pais}: {descripcion}. "
            f"Temperatura {temp:.1f}°C, sensación térmica {sensacion:.1f}°C. "
            f"Humedad {humedad}%, viento {viento} m/s."
        )

    except requests.exceptions.Timeout:
        return "La consulta del clima tardó demasiado. Verifica tu conexión."
    except Exception as e:
        return f"Error inesperado consultando el clima: {str(e)}"


def parse_city_from_input(user_input: str) -> str:
    """
    Extrae el nombre de ciudad del input del usuario.
    Si no encuentra ninguna, regresa la ciudad por defecto.
    """
    user_input_lower = user_input.lower()

    # Palabras clave que preceden al nombre de la ciudad
    triggers = ["clima en ", "temperatura en ", "tiempo en ", "weather in "]

    for trigger in triggers:
        if trigger in user_input_lower:
            # Toma lo que viene después del trigger
            city = user_input_lower.split(trigger)[-1].strip()
            # Limpia signos de pregunta u otros caracteres
            city = city.replace("?", "").replace("¿", "").strip()
            return city.title()  # Capitaliza correctamente

    return "Monterrey"  # Ciudad por defecto
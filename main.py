# weather_agent_openrouter.py
import os
import json
import requests
from openai import OpenAI
from langdetect import detect  # pip install langdetect
from dotenv import load_dotenv  # pip install python-dotenv

# Загружаем переменные из .env файла
load_dotenv()

# ========================
# 1️⃣ Настройка API-ключей через OpenRouter
# ========================
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")

# ===================================
# 2️⃣ Описание инструмента (tools)
# ===================================
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Получить текущую погоду в заданном городе с помощью OpenWeather API.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Название города (например, Москва, Paris, London)"
                    },
                    "lang": {
                        "type": "string",
                        "description": "Язык, на котором возвращать описание погоды (например, 'ru', 'en', 'fr')"
                    }
                },
                "required": ["city", "lang"],
            },
        }
    }
]

# ====================================
# 3️⃣ Реализация функции (tool)
# ====================================
def get_weather(city: str, lang: str) -> dict:
    if not OPENWEATHER_KEY:
        return {"error": "OpenWeather API key не установлен"}

    try:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": OPENWEATHER_KEY,
            "units": "metric",
            "lang": lang
        }
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        data = r.json()

        return {
            "city": data.get("name", city),
            "temperature": data["main"]["temp"],
            "condition": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Ошибка запроса: {str(e)}"}
    except (KeyError, IndexError):
        return {"error": "Не удалось обработать данные OpenWeather"}

# ====================================
# 4️⃣ Основной цикл работы
# ====================================
def chat():
    # Проверяем наличие API ключей
    if not os.getenv("OPENROUTER_API_KEY"):
        print("❌ Ошибка: OPENROUTER_API_KEY не установлен в .env файле")
        return
    
    if not OPENWEATHER_KEY:
        print("⚠️ Предупреждение: OPENWEATHER_API_KEY не установлен - функции погоды не будут работать")
    
    print(f"🔑 Используется модель: {os.getenv('MODEL_NAME', 'gpt-5')}")
    
    input_list = [
        {"role": "system", "content": "You are a helpful assistant. Always respond in the same language the user used."}
    ]

    print("💬 Спроси про погоду или что угодно ещё.")
    print("✏️ Чтобы выйти, введи: exit\n")

    while True:
        user_input = input("👤 Ты: ")
        if user_input.lower() in ["exit", "выход"]:
            break

        input_list.append({"role": "user", "content": user_input})

        # Определяем язык пользователя
        try:
            lang_code = detect(user_input)
        except:
            lang_code = "en"  # по умолчанию английский

        # Первый запрос модели
        try:
            response = client.chat.completions.create(
                model=os.getenv("MODEL_NAME", "gpt-5"),
                messages=input_list,
                tools=tools,
                max_tokens=1000,  # Ограничиваем количество токенов
                extra_headers={  # необязательно, но можно указать для OpenRouter
                    "HTTP-Referer": "https://example.com",
                    "X-Title": "WeatherAgent",
                }
            )
        except Exception as e:
            error_str = str(e)
            print(f"❌ Ошибка API запроса: {error_str}")
            
            if "402" in error_str or "credits" in error_str.lower():
                print("💳 Недостаточно кредитов на OpenRouter!")
                print("🔧 Решения:")
                print("   1. Пополните баланс на https://openrouter.ai/settings/credits")
                print("   2. Или измените MODEL_NAME в .env на более дешевую модель:")
                print("      - gpt-4o-mini (дешевле)")
                print("      - gpt-3.5-turbo (самая дешевая)")
            else:
                print("🔍 Проверьте:")
                print("   - Правильность OPENROUTER_API_KEY")
                print(f"   - Доступность модели {os.getenv('MODEL_NAME', 'gpt-5')}")
                print("   - Интернет соединение")
            continue

        response_message = response.choices[0].message
        input_list.append(response_message)
        
        tool_calls = response_message.tool_calls or []

        if tool_calls:
            for call in tool_calls:
                if call.function.name == "get_weather":
                    args = json.loads(call.function.arguments)
                    # Добавляем lang для OpenWeather
                    args["lang"] = lang_code
                    result = get_weather(args["city"], args["lang"])

                    input_list.append({
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": json.dumps(result, ensure_ascii=False)
                    })

            # Второй запрос модели — ответ на языке пользователя
            try:
                response = client.chat.completions.create(
                    model=os.getenv("MODEL_NAME", "gpt-5"),
                    messages=input_list,
                    tools=tools,
                    max_tokens=1000,  # Ограничиваем количество токенов
                    extra_headers={
                        "HTTP-Referer": "https://example.com",
                        "X-Title": "WeatherAgent",
                    }
                )
                print("🤖 Модель:", response.choices[0].message.content)
            except Exception as e:
                print(f"❌ Ошибка второго API запроса: {str(e)}")
                continue

        else:
            print("🤖 Модель:", response_message.content)


if __name__ == "__main__":
    chat()

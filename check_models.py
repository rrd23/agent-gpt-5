#!/usr/bin/env python3
"""
Скрипт для проверки доступных моделей в OpenRouter
"""
import os
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def check_openrouter_models():
    """Проверяет доступные модели в OpenRouter"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ OPENROUTER_API_KEY не найден в .env файле")
        return
    
    print(f"🔑 Проверяем модели для ключа: {api_key[:20]}...")
    
    # Получаем список всех моделей
    try:
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://example.com",
                "X-Title": "ModelChecker"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Найдено {len(models['data'])} моделей\n")
            
            # Популярные модели для проверки
            popular_models = [
                "gpt-5", "gpt-4o", "gpt-4o-mini", "gpt-4", "gpt-3.5-turbo",
                "claude-3-sonnet", "claude-3-haiku", 
                "gemini-pro", "llama-2-70b-chat"
            ]
            
            print("🔍 Проверяем популярные модели:")
            available_models = []
            
            for model_data in models['data']:
                model_id = model_data['id']
                if any(popular in model_id for popular in popular_models):
                    pricing = model_data.get('pricing', {})
                    prompt_cost = pricing.get('prompt', 'N/A')
                    completion_cost = pricing.get('completion', 'N/A')
                    
                    print(f"  ✅ {model_id}")
                    print(f"     💰 Prompt: ${prompt_cost}/1M tokens, Completion: ${completion_cost}/1M tokens")
                    available_models.append(model_id)
            
            print(f"\n📊 Доступно популярных моделей: {len(available_models)}")
            
            # Проверяем конкретные модели
            test_models = ["gpt-5", "gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]
            print(f"\n🧪 Тестируем модели: {', '.join(test_models)}")
            
            # Проверяем есть ли gpt-5 в списке
            gpt5_models = [m['id'] for m in models['data'] if 'gpt-5' in m['id'].lower()]
            if gpt5_models:
                print(f"\n🔍 Найденные модели gpt-5: {', '.join(gpt5_models)}")
            else:
                print(f"\n⚠️ Модели gpt-5 не найдены в списке доступных моделей")
            
            for model in test_models:
                test_model(api_key, model)
                
        else:
            print(f"❌ Ошибка получения моделей: {response.status_code}")
            print(f"Ответ: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")

def test_model(api_key, model_name):
    """Тестирует конкретную модель простым запросом"""
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://example.com",
                "X-Title": "ModelTester"
            },
            json={
                "model": model_name,
                "messages": [{"role": "user", "content": "Привет! Ответь одним словом: работаю"}],
                "max_tokens": 10
            },
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result['choices'][0]['message']['content'].strip()
            print(f"  ✅ {model_name}: {answer}")
        else:
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            print(f"  ❌ {model_name}: Ошибка {response.status_code}")
            if isinstance(error_data, dict) and 'error' in error_data:
                print(f"     {error_data['error'].get('message', 'Неизвестная ошибка')}")
            
    except Exception as e:
        print(f"  ❌ {model_name}: Исключение - {e}")

if __name__ == "__main__":
    print("🚀 Проверка моделей OpenRouter\n")
    check_openrouter_models()
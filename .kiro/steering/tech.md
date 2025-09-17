# Технический стек

## Основные технологии
- **Python 3.x** - основной язык разработки
- **OpenRouter API** - для работы с различными LLM моделями через единый интерфейс
- **OpenAI SDK** - клиент для взаимодействия с OpenRouter API
- **OpenWeather API** - для получения данных о погоде
- **requests** - для HTTP запросов к внешним API
- **langdetect** - для автоматического определения языка пользователя
- **python-dotenv** - для загрузки переменных окружения из .env файла

## Зависимости
```bash
pip install -r requirements.txt
```

Основные пакеты:
- `openai` - SDK для работы с OpenRouter API
- `requests` - HTTP клиент
- `langdetect` - определение языка
- `python-dotenv` - загрузка переменных окружения

## Переменные окружения
Проект требует настройки следующих переменных окружения:
- `OPENROUTER_API_KEY` - ключ для доступа к OpenRouter API
- `OPENWEATHER_API_KEY` - ключ для доступа к OpenWeather API
- `MODEL_NAME` - название модели для использования (по умолчанию gpt-4o)
- `DEFAULT_LANGUAGE` - язык по умолчанию (ru)
- `WEATHER_TIMEOUT` - таймаут для запросов к погодному API

## Команды для работы с проектом
```bash
# Запуск приложения
python main.py

# Установка зависимостей
pip install -r requirements.txt  # если файл существует
# или
pip install openai requests langdetect
```

## Архитектурные особенности
- Использует OpenRouter для доступа к различным LLM моделям через единый API
- Function calling для структурированного взаимодействия с внешними API
- Автоматическое определение языка для мультиязычной поддержки
- Обработка ошибок для сетевых запросов и парсинга данных
- Дополнительные заголовки для OpenRouter (HTTP-Referer, X-Title)
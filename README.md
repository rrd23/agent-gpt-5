# Weather Agent с OpenRouter

Погодный агент с автоматическим определением языка, использующий OpenRouter API для доступа к различным LLM моделям.

## Быстрый старт

### Локальный запуск

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Скопируйте и заполните файл окружения:
```bash
cp .env.example .env
# Отредактируйте .env файл, добавив ваши API ключи
```

3. Запустите приложение:
```bash
python main.py
```

### Запуск через Docker

1. Убедитесь, что заполнен .env файл с API ключами

2. Соберите и запустите контейнер:
```bash
docker-compose up --build
```

3. Для интерактивного режима:
```bash
docker-compose run --rm weather-agent
```

## Необходимые API ключи

- **OPENROUTER_API_KEY** - получите на [openrouter.ai](https://openrouter.ai)
- **OPENWEATHER_API_KEY** - получите на [openweathermap.org](https://openweathermap.org/api)

## Возможности

- 🌍 Получение погоды для любого города
- 🗣️ Автоматическое определение языка пользователя
- 🤖 Поддержка различных AI моделей через OpenRouter
- 🐳 Готовый Docker контейнер для развертывания

## Примеры использования

```
👤 Ты: Какая погода в Москве?
🤖 Модель: В Москве сейчас +15°C, облачно...

👤 You: What's the weather in London?
🤖 Model: The weather in London is currently...
```
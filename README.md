# YouTube Transcript API

Python Flask API для получения транскрибаций YouTube видео.

## Локальный запуск

```bash
pip install -r requirements.txt
python app.py
```

API будет доступен на http://localhost:5000

## Endpoints

- `GET /` - Информация об API
- `GET /health` - Проверка работоспособности
- `GET /transcript?video_id=XXX&lang=ru` - Получить транскрибацию

## Деплой на Railway

1. Создайте новый репозиторий с этими файлами
2. Подключите к Railway
3. Railway автоматически развернет API

## Пример использования

```bash
curl "https://your-api.up.railway.app/transcript?video_id=dQw4w9WgXcQ&lang=en"
```
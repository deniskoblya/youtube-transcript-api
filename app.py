#!/usr/bin/env python3
"""
YouTube Transcript API для Railway
"""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import ProxyHandler
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для всех доменов

# Получаем прокси из переменных окружения
PROXY_URL = os.environ.get('PROXY_URL')  # Формат: http://username:password@proxy:port

def get_proxy_config():
    """Получает настройки прокси из переменных окружения"""
    if PROXY_URL:
        print(f"🔄 Используем прокси: {PROXY_URL[:20]}...")
        proxies = {
            'http': PROXY_URL,
            'https': PROXY_URL
        }
        return proxies
    return None

@app.route('/transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('video_id')
    lang = request.args.get('lang', 'en')
    
    print(f"\n🔍 Запрос транскрибации: video_id={video_id}, lang={lang}")
    
    if not video_id:
        print("❌ Отсутствует video_id")
        return jsonify({'error': 'video_id is required'}), 400
    
    try:
        # Настраиваем прокси если доступен
        proxy_config = get_proxy_config()
        
        if proxy_config:
            # Создаем проксированный экземпляр API
            proxy_handler = ProxyHandler(proxy_config)
            api = YouTubeTranscriptApi(proxy_handler=proxy_handler)
        else:
            # Используем обычный API
            api = YouTubeTranscriptApi()
        
        # Пробуем разные языки
        languages_to_try = [lang, 'en', 'ru', 'es', 'fr', 'de']
        
        for try_lang in languages_to_try:
            try:
                print(f"🎯 Пробуем получить транскрибацию на языке: {try_lang}")
                
                # Используем метод fetch с экземпляром
                segments = api.fetch(video_id, languages=[try_lang])
                
                if segments and len(segments) > 0:
                    print(f"✅ Найдена транскрибация на языке {try_lang}: {len(segments)} сегментов")
                    
                    result = []
                    for seg in segments:
                        # Проверяем, это объект или словарь
                        if hasattr(seg, 'text'):
                            result.append({
                                "start": seg.start,
                                "duration": getattr(seg, "duration", 0),
                                "text": seg.text
                            })
                        else:
                            result.append({
                                "start": seg.get("start", 0),
                                "duration": seg.get("duration", 0),
                                "text": seg.get("text", "")
                            })
                    
                    print(f"✅ Транскрибация обработана: {len(result)} записей")
                    return jsonify(result)
                    
            except Exception as lang_error:
                print(f"⚠️  Не найдено на {try_lang}: {type(lang_error).__name__}: {lang_error}")
                continue
        
        # Если ни один язык не сработал, пробуем без указания языка
        try:
            print("🎯 Пробуем получить любую доступную транскрибацию...")
            segments = api.fetch(video_id)
            
            if segments and len(segments) > 0:
                print(f"✅ Найдена транскрибация (автовыбор): {len(segments)} сегментов")
                
                result = []
                for seg in segments:
                    if hasattr(seg, 'text'):
                        result.append({
                            "start": seg.start,
                            "duration": getattr(seg, "duration", 0),
                            "text": seg.text
                        })
                    else:
                        result.append({
                            "start": seg.get("start", 0),
                            "duration": seg.get("duration", 0),
                            "text": seg.get("text", "")
                        })
                
                return jsonify(result)
        except Exception as auto_error:
            print(f"⚠️  Автовыбор не сработал: {auto_error}")
        
        print("❌ Транскрибация не найдена ни на одном языке")
        return jsonify([])
            
    except Exception as e:
        print(f"❌ Общая ошибка: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/', methods=['GET'])
def home():
    proxy_status = "enabled" if PROXY_URL else "disabled"
    return jsonify({
        'name': 'YouTube Transcript API',
        'version': '1.0.0',
        'proxy': proxy_status,
        'endpoints': {
            '/health': 'Health check',
            '/transcript': 'Get video transcript (params: video_id, lang)'
        },
        'example': '/transcript?video_id=dQw4w9WgXcQ&lang=ru'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Transcript API запущен на порту {port}")
    print("📝 Пример: /transcript?video_id=r45n3Jsqu6o&lang=ru")
    app.run(host='0.0.0.0', port=port, debug=False)
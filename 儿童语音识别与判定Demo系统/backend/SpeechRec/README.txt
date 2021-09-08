1. python必须为3.6
2. 执行命令（依次）：
pip install -r requirements.txt
redis-server.exe
celery -A SpeechRec worker -l info
python manage.py runserver 0.0.0.0:8080
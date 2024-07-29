# 베이스 이미지 설정
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일들을 작업 디렉토리로 복사
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# django-cors-headers 설치
RUN pip install django-cors-headers

COPY . /app/

# 장고의 static 파일을 모음
RUN python manage.py collectstatic --noinput

# 장고 애플리케이션을 시작
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]

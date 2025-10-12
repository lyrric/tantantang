FROM python:3.11.9

WORKDIR /app

COPY requirements.txt .
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["sh", "-c", "python manage.py runserver --noreload 0.0.0.0:8000"]


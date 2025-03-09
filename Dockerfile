FROM python:3.12

COPY requirements.txt ./

RUN pip install --progress-bar off -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
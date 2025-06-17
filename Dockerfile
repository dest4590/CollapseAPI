FROM python:3.12-alpine

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

WORKDIR /app

EXPOSE 8754

RUN python manage.py collectstatic --noinput

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8754"]
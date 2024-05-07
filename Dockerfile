FROM python:3.12.2-alpine3.19

WORKDIR /shop/

COPY . /shop/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

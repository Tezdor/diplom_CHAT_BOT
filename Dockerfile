FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip install aiogram
RUN pip install matplotlib
CMD ["python", "-u", "main.py"]

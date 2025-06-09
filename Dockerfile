FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip install aiogram
RUN pip install matplotlib
RUN pip install openai
CMD ["python", "-u", "main.py"]

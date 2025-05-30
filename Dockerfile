FROM python:3.13-slim
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
ENV TOKEN=$TOKEN
ENV AI_TOKEN=$AI_TOKEN
WORKDIR /app
COPY . .
ENTRYPOINT ["python", "bot.py"]
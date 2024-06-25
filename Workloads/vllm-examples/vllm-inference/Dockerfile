# python3.8 breaks with gradio
#FROM python:3.10
FROM --platform=linux/amd64 python:3.10-slim as build

# Install dependencies from requirements.txt
COPY ./src/requirements.txt .
RUN pip install -r requirements.txt

COPY ./src /src

WORKDIR /src

EXPOSE 7860

CMD ["python", "app.py"]

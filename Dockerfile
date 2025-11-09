FROM python:3.12

WORKDIR /
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

RUN ["playwright", "install", "chromium"]
RUN ["playwright", "install-deps"]
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
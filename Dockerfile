FROM tiangolo/uvicorn-gunicorn:python3.10

COPY requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt

COPY . .

# python3 main.py

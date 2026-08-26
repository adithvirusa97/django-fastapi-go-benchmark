FROM python:3.13-slim
WORKDIR /app
RUN pip install --no-cache-dir matplotlib
COPY analyze.py .
CMD ["python", "analyze.py"]

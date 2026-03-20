FROM python:3.12-slim

WORKDIR /llm_rag

COPY . .

RUN pip install --no-cache-dir -r packages_list.txt

CMD ["python", "test_ChatNVIDIA.py"]
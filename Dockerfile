FROM python:3.11-slim

WORKDIR /app

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código e o executável
COPY qshell.py .
COPY qs-netcat.exe .

# Garante que o executável tenha permissão de execução
RUN chmod +x qs-netcat.exe

EXPOSE 5550

CMD ["python", "qshell.py"]

# Use uma imagem base Python leve
FROM python:3.9-alpine

# Instale dependências de sistema para rodar e compilar pacotes
RUN apk add --no-cache gcc musl-dev libffi-dev

# Defina o diretório de trabalho
WORKDIR /app

# Copie e instale as dependências do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação para o diretório de trabalho
COPY ./app/ .

# Exponha a porta que o Flask usará
EXPOSE 5000

# Comando para iniciar a aplicação com Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

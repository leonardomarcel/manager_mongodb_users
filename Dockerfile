# Build a partir de uma imagem já com python e o PIP
FROM python:3-alpine as base

# 1: Cria a pasta de instalação
RUN mkdir /install

# muda o diretório vigente para o de instalação /install
WORKDIR /install

# cópia do arquivo de dependências da app
COPY requirements.txt /requirements.txt

# Instalação das dependências atraves do PIP em um diretório
RUN pip install --prefix=/install -r /requirements.txt

# cria um novo estágio
FROM base

# Copia o diretório de instalação para o diretório raiz
COPY --from=base /install /usr/local

# Copia os arquivos da aplicação para o container
COPY . /app

# Define o diretório de trabalho
WORKDIR /app

# expõe a porta do container
EXPOSE 5000

# variáveis de ambiente

ENV MONGODB_USER=$MONGODB_USER
ENV MONGODB_PASSWORD=$MONGODB_PASS 
ENV MONGODB_URI=$MONGODB_URI

# Execução da app
CMD ["python", "app.py"]
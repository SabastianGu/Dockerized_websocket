FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  
RUN apt-get update \
    && install -y --no-install-recommends \
       netcat
    

RUN pip install --upgrade pip

COPY ./requirements.txt /app/

RUN pip install -r /app/requirements.txt

COPY . /app/

#-----
WORKDIR /app/WebService

COPY ./entrypoint.sh /

ENTRYPOINT [ "sh", "/entrypoint.sh" ]

EXPOSE 8080 9000 8000 80 443

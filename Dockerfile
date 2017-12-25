# use base python image with python 2.7
FROM python:latest

# add requirements.txt to the image
ADD requirements.txt /app/requirements.txt
Add TranslationCaching-8699c192e59a.json /app/TranslationCaching-8699c192e59a.json
WORKDIR /app/
RUN pip install -r requirements.txt
RUN adduser --disabled-password --gecos '' myuser

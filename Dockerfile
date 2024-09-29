FROM python:3.12

ENV PYTHONPATH /usr/src/sparkcoin

RUN mkdir -p $PYTHONPATH
RUN mkdir -p $PYTHONPATH/static
RUN mkdir -p $PYTHONPATH/media

WORKDIR $PYTHONPATH

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Add this line to export port 8000 for Django app

RUN chmod -R 755 /usr/src/sparkcoin/static/
RUN chmod -R 755 /usr/src/sparkcoin/media/

RUN apt-get update && apt-get install --no-install-recommends -y \
  # Dependencies for building Python packages
  build-essential \
  # Dependencies for psycopg2
  libpq-dev \
  # curl
  curl \
  # add ffmpeg
  ffmpeg

COPY . $PYTHONPATH
COPY ./req.txt $PYTHONPATH/


RUN pip install -r req.txt
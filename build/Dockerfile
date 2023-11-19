FROM python:3.11.6

WORKDIR /usr/src/app/

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN echo 'APT::Keep-Downloaded-Packages "false";' \
      > /etc/apt/apt.conf.d/01disable-cache

RUN apt-get update && apt-get install -y curl python3-pip python3-dev wget libpq-dev graphviz

COPY reqs.txt .
RUN pip3 install --no-cache-dir -r reqs.txt

RUN python3 -m nltk.downloader -d /usr/local/nltk_data stopwords averaged_perceptron_tagger_ru punkt
COPY lib /usr/src/app/lib/
COPY app.py .
COPY data.csv .

ENTRYPOINT ["/bin/bash"]

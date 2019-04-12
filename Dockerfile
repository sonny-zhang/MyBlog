FROM python:3.7-alpine

ENV FLASK_APP manga.py
ENV MyBlog_CONFIG product

#RUN adduser -D myblog
#USER myblog

WORKDIR /home/myblog

RUN apk update && apk add \
        libuuid \
        pcre \
        mailcap \
        gcc \
        linux-headers \
        pcre-dev

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pip install pipenv
RUN pipenv install

COPY app app
COPY migrations migrations
COPY manage.py config.py boot.sh ./

EXPOSE 5000
RUN chmod +x boot.sh
ENTRYPOINT ["./boot.sh"]

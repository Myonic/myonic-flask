FROM python:2.7.13-slim

WORKDIR /myonic-flask

COPY requirements.txt ./
RUN apt install python-imaging
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=/myonic-flask/myonic/__init__.py
ENV FLASK_DEBUG=0
ENV OAUTHLIB_INSECURE_TRANSPORT=0
ENV OAUTHLIB_RELAX_TOKEN_SCOPE=0
ENV SECRET_KEY='change_me'

ENTRYPOINT ["flask"]

EXPOSE 5000

VOLUME /myonic-flask/myonic/static
VOLUME /myonic-flask/myonic/database
VOLUME /myonic-flask/myonic/migrations

WORKDIR /myonic-flask/myonic

RUN flask db migrate
RUN flask db upgrade
CMD ["run", "--host=0.0.0.0"]

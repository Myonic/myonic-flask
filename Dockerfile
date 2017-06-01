FROM python:2.7.13-wheezy

WORKDIR /myonic/myonic

ENTRYPOINT ["flask"]

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=/myonic/myonic/__init__.py
ENV FLASK_DEBUG=0
ENV OAUTHLIB_INSECURE_TRANSPORT=0
ENV OAUTHLIB_RELAX_TOKEN_SCOPE=0

EXPOSE 5000

VOLUME /myonic/static

RUN flask db init
CMD ["run", "--host=0.0.0.0"]

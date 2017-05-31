FROM python:3

ENTRYPOINT ["flask"]

WORKDIR /myonic

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=./myonic/__init__.py
ENV FLASK_DEBUG=0
ENV OAUTHLIB_INSECURE_TRANSPORT=0
ENV OAUTHLIB_RELAX_TOKEN_SCOPE=0

EXPOSE 5000

VOLUME /myonic/static

CMD ["db init"]
CMD ["run --host=0.0.0.0"]

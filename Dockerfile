FROM python:3.8
FROM redis

RUN python -m venv venv
RUN source venv/bin/activate

CMD ["mkdir", "application"]
WORKDIR /application

RUN git clone git@github.com:TBS093A/trade-app-backend.git

RUN ./packages.sh
RUN ./migrate.sh
RUN ./run.sh
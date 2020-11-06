FROM python:3.8

RUN pip install --upgrade pip setuptools

ADD chat ./chat
ADD generalApp ./generalApp
ADD TradeApp ./TradeApp
ADD manage.py ./manage.py
ADD packages.sh ./packages.sh
ADD migrate.sh ./migrate.sh
ADD run.sh ./run.sh

RUN ./packages.sh
RUN ./migrate.sh

# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "TradeApp.wsgi"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:9090"]

FROM python:2.7
WORKDIR /data/CMDB/
COPY . /data/CMDB/
RUN pip install --upgrade pip && pip install -r requirements.txt && python  manage.py db migrate -m "Initial migration" && python  manage.py db upgrade

EXPOSE 5000
EXPOSE 5001
CMD python runweb.py

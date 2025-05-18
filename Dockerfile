FROM python:3.11

WORKDIR /opt/app

COPY re.txt /opt/app/re.txt

RUN pip install --no-cache-dir -r /opt/app/re.txt
RUN pip install psycopg2-binary

COPY . .

CMD [ "chainlit", "run", "main.py", "-w" ]
FROM python:3.12

WORKDIR /opt/app

COPY pyproject.toml .

RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-cache

COPY . .
RUN mkdir /opt/app/media

CMD [ "poetry", "run", "main.py" ]
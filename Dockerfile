FROM python:3.12

ENV APP_HOME=/app

WORKDIR $APP_HOME


COPY pyproject.toml poetry.lock ./

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --only main

COPY . .

EXPOSE 3000

ENTRYPOINT ["python", "main.py"]
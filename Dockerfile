FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN python -m pip install --no-cache-dir --upgrade pip gunicorn setuptools wheel \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && adduser --system --uid 1001 --group --home /app app \
    && chown -R app:app /app

COPY --chown=app:app . /app

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "modeling.app:create_app()"]

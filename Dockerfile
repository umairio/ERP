FROM python:3.12

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"

RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev musl-dev libjpeg-dev zlib1g-dev \
    git supervisor ffmpeg curl libffi-dev nano postgresql-client

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python -
RUN ln -s /root/.local/bin/poetry /usr/bin/poetry

# COPY pyproject.toml poetry.lock ./
# RUN poetry config virtualenvs.create false \
#     && poetry install --no-root
COPY poetry.lock pyproject.toml /app/

RUN poetry install --no-root

COPY . /app/
RUN chmod +x scripts/entrypoint.sh

CMD ["./scripts/entrypoint.sh"]

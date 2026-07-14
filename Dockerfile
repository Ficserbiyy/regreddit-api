FROM python:3.14.4-slim

RUN pip install --no-cache-dir uv

WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY pyproject.toml uv.lock ./

RUN uv venv $VIRTUAL_ENV
RUN uv sync --frozen --no-dev --active

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# Marketing Commander API stub container (Phase 3, Increment 3.2).
# Base image pinned per plan decision D3-1. Dependencies are resolved by
# pdm (pyproject.toml + pdm.lock) and installed system-wide - no virtual
# environment inside the container (Phase 3 recorded decision).
FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PDM_CHECK_UPDATE=false

RUN pip install --no-cache-dir pdm

WORKDIR /app
COPY pyproject.toml pdm.lock ./
# pdm resolves and locks; the exported pins install system-wide via pip
# (pdm sync with use_venv=false does not target system site-packages).
RUN pdm export --prod --no-hashes -o requirements.txt \
    && pip install --no-cache-dir -r requirements.txt \
    && rm requirements.txt

COPY app ./app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

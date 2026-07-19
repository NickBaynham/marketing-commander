# Marketing Commander worker stub container (Phase 3, Increment 3.3).
# Base image pinned per plan decision D3-1. Dependencies are resolved by
# pdm (pyproject.toml + pdm.lock) and installed system-wide via the
# exported pins - no virtual environment inside the container (Phase 3
# recorded decision; same pattern as apps/api).
FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PDM_CHECK_UPDATE=false

RUN pip install --no-cache-dir pdm

WORKDIR /app
COPY pyproject.toml pdm.lock ./
RUN pdm export --prod --no-hashes -o requirements.txt \
    && pip install --no-cache-dir -r requirements.txt \
    && rm requirements.txt

COPY worker ./worker

CMD ["python", "-m", "worker.main"]

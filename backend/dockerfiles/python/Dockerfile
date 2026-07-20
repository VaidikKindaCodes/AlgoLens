FROM python:3.12-slim

RUN addgroup --system sandbox && adduser --system --ingroup sandbox sandbox

WORKDIR /workspace
RUN mkdir -p /workspace && chown sandbox:sandbox /workspace

USER sandbox

ENV PYTHONUNBUFFERED=1

FROM golang:1.22-bullseye

RUN addgroup --system sandbox && adduser --system --ingroup sandbox sandbox

WORKDIR /workspace
RUN mkdir -p /workspace && chown sandbox:sandbox /workspace

USER sandbox

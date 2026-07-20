FROM openjdk:21-jdk-slim

RUN addgroup --system sandbox && adduser --system --ingroup sandbox sandbox

WORKDIR /workspace
RUN mkdir -p /workspace && chown sandbox:sandbox /workspace

USER sandbox

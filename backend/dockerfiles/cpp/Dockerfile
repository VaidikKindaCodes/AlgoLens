FROM gcc:13.2.0

RUN addgroup --system sandbox && adduser --system --ingroup sandbox sandbox

WORKDIR /workspace
RUN mkdir -p /workspace && chown sandbox:sandbox /workspace

USER sandbox

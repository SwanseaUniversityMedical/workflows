FROM ghcr.io/actions/actions-runner:2.318.0

LABEL org.opencontainers.image.source=https://github.com/SwanseaUniversityMedical/workflows

# Add missing dependencies compared to the old summerwind runners
USER root
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends \
      curl unzip jq wget python3-pip git-all && \
    rm -rf /var/lib/apt/lists/*

RUN echo 'export PATH="/home/runner/.local/bin:$PATH"' >> /etc/profile
ENV PATH="/home/runner/.local/bin:$PATH"

USER runner
ENV PATH="/home/runner/.local/bin:$PATH"


FROM ghcr.io/actions/actions-runner:2.318.0

LABEL org.opencontainers.image.source=https://github.com/SwanseaUniversityMedical/workflows

# Add missing dependencies compared to the old summerwind runners
USER root
RUN apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get -y install -y -qq --no-install-recommends \
      curl unzip jq wget python3-pip git-all && \
    rm -rf /var/lib/apt/lists/*

USER runner

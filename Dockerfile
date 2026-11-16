FROM kalilinux/kali-rolling

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 nmap gobuster wpscan ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/hackerlab
COPY . /opt/hackerlab

# The supplied Nmap wrapper uses TCP connect scans (-sT).
CMD ["bash"]

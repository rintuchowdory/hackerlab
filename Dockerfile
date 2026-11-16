FROM kalilinux/kali-rolling

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 nmap gobuster wpscan ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

# Preload WPScan's local component/fingerprint metadata so passive scans work
# in the isolated lab network without fetching updates during each run.
RUN wpscan --update

WORKDIR /opt/hackerlab
COPY . /opt/hackerlab

# The supplied Nmap wrapper uses TCP connect scans (-sT).
CMD ["bash"]

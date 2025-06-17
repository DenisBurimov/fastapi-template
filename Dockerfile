FROM registry.access.redhat.com/ubi8/ubi:latest

ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PYTHON_VERSION=3.12.0

RUN dnf install -y \
    gcc \
    make \
    openssl-devel \
    bzip2-devel \
    libffi-devel \
    zlib-devel \
    sqlite-devel \
    wget \
    tar \
    gzip \
    findutils \
    && dnf clean all

RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz \
    && tar xzf Python-${PYTHON_VERSION}.tgz \
    && cd Python-${PYTHON_VERSION} \
    && ./configure --enable-optimizations \
    && make -j $(nproc) \
    && make altinstall \
    && cd .. \
    && rm -rf Python-${PYTHON_VERSION} Python-${PYTHON_VERSION}.tgz

RUN ln -s /usr/local/bin/python3.12 /usr/local/bin/python3 \
    && ln -s /usr/local/bin/pip3.12 /usr/local/bin/pip3

RUN adduser -u 1001 --system --no-create-home appuser && \
    chown appuser /opt && \
    chmod 755 /opt
USER appuser

WORKDIR /app

RUN mkdir -p /app && chown appuser:appuser /app

COPY --chown=appuser requirements.txt .

RUN python3 -m venv /app/venv

RUN /app/venv/bin/pip install --no-warn-script-location -r requirements.txt

COPY --chown=appuser . .

EXPOSE 8007

CMD ["/app/venv/bin/python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8007"]

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /workspace

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        curl \
        git \
        latexmk \
        texlive-fonts-recommended \
        texlive-latex-base \
        texlive-latex-recommended \
        texlive-pictures \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/dlgpt-requirements.txt
RUN python -m pip install --upgrade pip \
    && python -m pip install -r /tmp/dlgpt-requirements.txt
COPY . /workspace

EXPOSE 8000

CMD ["python", "tools/course.py", "serve", "--host", "0.0.0.0", "--no-browser"]

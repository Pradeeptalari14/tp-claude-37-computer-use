FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb \
    x11vnc \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY claude_computer_operator.py screen_coordinate_mapper.py ./

ENV PYTHONUNBUFFERED=1
EXPOSE 8080 5900

CMD ["python", "claude_computer_operator.py"]

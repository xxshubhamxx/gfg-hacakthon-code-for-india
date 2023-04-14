FROM python:3.10-alpine
COPY . /app
WORKDIR /app
RUN apk add --no-cache gcc musl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del gcc musl-dev
EXPOSE 5673
CMD [ "python", "main.py" ]
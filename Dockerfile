FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY src/ ./src/
RUN pip install --no-cache-dir .

ENV OLLAMA_API_KEY=""
ENV OLLAMA_HOST="https://ollama.com"

EXPOSE 8000

ENTRYPOINT ["ollama-search-mcp"]
CMD ["--http", "--host", "0.0.0.0"]

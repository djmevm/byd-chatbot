FROM rasa/rasa:3.6.15-full

WORKDIR /app

USER root

# Cache bust: v3
RUN echo "build-v3"

RUN pip install --no-cache-dir \
    fuzzywuzzy==0.18.0 \
    python-Levenshtein==0.23.0 \
    rasa-sdk==3.6.2

COPY --chown=1001:1001 config.yml .
COPY --chown=1001:1001 domain.yml .
COPY --chown=1001:1001 endpoints.yml .
COPY --chown=1001:1001 data/ ./data/
COPY --chown=1001:1001 actions/ ./actions/
COPY --chown=1001:1001 start.sh .

RUN chmod +x start.sh

RUN rasa train --fixed-model-name byd-model

USER 1001

EXPOSE 5005

ENTRYPOINT []
CMD ["sh", "start.sh"]

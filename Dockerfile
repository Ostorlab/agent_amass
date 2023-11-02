FROM golang:1.19-alpine as amass_build
RUN apk --no-cache add git
RUN git clone --depth 1 https://github.com/OWASP/Amass.git /opt/amass \
    && cd /opt/amass \
    && go get ./... &&  \
    go install ./...


FROM python:3.11-alpine as base
FROM base as builder
RUN apk add build-base
RUN mkdir /install
WORKDIR /install
COPY requirement.txt /requirement.txt
RUN pip install --prefix=/install -r /requirement.txt


FROM base
RUN apk --no-cache add ca-certificates
COPY --from=amass_build /go/bin/amass /bin/amass
COPY --from=builder /install /usr/local
RUN mkdir -p /app/agent
ENV PYTHONPATH=/app
COPY agent /app/agent
COPY ostorlab.yaml /app/agent/ostorlab.yaml
WORKDIR /app
CMD ["python3.11", "/app/agent/amass_agent.py"]

FROM golang:1.24-bookworm AS builder

WORKDIR /app

COPY go.mod ./

RUN go mod download

COPY . .

RUN go build \
    -trimpath \
    -ldflags="-s -w" \
    -o /server .

FROM debian:bookworm-slim

WORKDIR /app

COPY --from=builder /server /server

EXPOSE 8000

CMD ["/server"]
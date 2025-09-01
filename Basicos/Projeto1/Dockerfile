#etapa de build
FROM golang:1.23.3-alpine AS build
WORKDIR /app
COPY go.mod ./
RUN go mod download && go mod verify
COPY . .
RUN go build -o server .

#Imagem final
FROM alpine:latest
WORKDIR /app
COPY --from=build /app/server /app/server
EXPOSE 8080
CMD ["./server"]
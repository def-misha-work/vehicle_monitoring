# vehicle_monitoring

### Running dev
Run docker-compose

- To build: `make docker`
- To start: `docker compose -f ./docker-compose.yml up -d`
- To stop: `docker compose -f ./docker-compose.yml down`
- To clean-up data: `docker system prune -a --volumes --filter "label=io.confluent.docker"`

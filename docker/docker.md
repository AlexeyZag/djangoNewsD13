просмотр контейнеров
docker ps
docker-compose up
docker exec -it 5965f852832d bash
psql -h localhost -p 5432 -U postgres -W

SELECT * FROM test;
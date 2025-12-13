# TgBot

Запустить телеграмм бота в docker-compose:
```sh
cp .env.example .env
# в .env добавить ваш токен от телеграмм бота
docker compose up --build -d
```

Локальный запуск:
```sh
cp .env.example .env
# в .env добавить ваш токен от телеграмм бота
poetry install
docker compose up --build -d redis
python3 src
```

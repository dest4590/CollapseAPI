docker stop collapseapi
docker rm collapseapi
git pull
docker build -t collapse/api .
docker run --name collapseapi --restart always -p 8754:8000 --volume ./media:/app/media --volume ./db.sqlite3:/app/db.sqlite3 --volume ./statistics.sqlite3:/app/statistics.sqlite3 --volume ./.env:/app/.env --volume /app/collapse:/mnt/collapse/collapse/:ro -d collapse/api

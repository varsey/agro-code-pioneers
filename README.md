# agro-code-pioneers

- Создаем контейнер
docker build --force-rm -t agro-code-pioneers -f build/Dockerfile .

- Запускаем в интерактивном режиме
docker run -it agro-code-pioneers

- Запускаем приложение с параметрами --rule - применяет правило из настроек, --shorts - включает короткие цепочки
python app.py --sample_size=252 --rule --shorts

- Сгенеренный файл лежит в папке graph в контейнере

- Оционально - запуск через докер-комоуз
docker-compose run --rm app

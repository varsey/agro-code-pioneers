# agro-code-pioneers

- Создаем контейнер
docker build --force-rm -t agro-code-pioneers -f build/Dockerfile .

- Запускаем в интерактивном режиме
docker run -it agro-code-pioneers

- Запускаем приложение с параметрами
  - --rule - применяет правило из настроек lib/custom_rule.py, 
  - --shorts - включает короткие цепочки
  - --sample_size=252 - сколько данных брать из датасета
    - python app.py --sample_size=252 --rule --shorts

- Сгенеренный файл лежит в папке graph в контейнере

- Опционально - запуск через докер-компоуз
  - docker-compose -f docker-compose.yaml up --build
  - docker-compose run --rm app

Запуск без docker'а из корня директории:
 - python3 -m venv venv
 - source venv/bin/activate
 - pip install reqs.txt
 - python app.py --sample_size=252 --rule --shorts
Результат в локальной папке graph

Основные параметры Yake:
- n - количество слов в n-gram для извлеченния ключевых слов
- top - сколько брать ключевых слов

Параметры BERT в файле main_pipe.ipynb:
минимальное количество профессий в кластере
- min_community_size=25

степень посимвольной схожести строк с профессиями
- threshold=0.75
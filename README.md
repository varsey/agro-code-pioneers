# agro-code-pioneers

docker build --force-rm -t agro-code-pioneers -f build/Dockerfile .

docker run -it agro-code-pioneers

python app.py --sample_size=252 --rule --shorts

docker-compose run --rm app

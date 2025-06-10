sudo docker build -t "diplom_bot" .
sudo docker run --restart=always -d diplom_bot
sudo docker ps -a
если остановить
sudo docker ps -a
Надо найти id контейнера и запомнить первые два символа
sudo docker stop 8d
sudo docker rm 8d
здесь 91 это первые два символа из id

git add .
git commit -m 'commit'
git push

# запуск
создать файл .env с двумя переменными
TOKEN для бота 
и
KEY для апи
``` 
py3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
py db.py
```
либо
```
py main.py
```
либо
```
sudo docker build -t "diplom_bot" .
sudo docker run --restart=always -d diplom_bot
 ```
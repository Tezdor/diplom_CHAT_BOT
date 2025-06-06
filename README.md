sudo docker build -t "diplom_bot" .
sudo docker run --restart=always -d diplom_bot
sudo docker ps -a
если остановить
sudo docker ps -a
Надо найти id контейнера и запомнить первые два символа
sudo docker stop 8d
sudo docker rm 8d
здесь 91 это первые два символа из id

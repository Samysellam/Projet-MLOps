docker container prune
docker rmi $(docker images -q)

docker build -t mon_image -f Dockerfile2 .
docker run -it -p 5000:5000 --entrypoint /bin/bash mon_image

curl http://localhost:5000/get_matches/1

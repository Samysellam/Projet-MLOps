# launcher

# create if logs does not exist
mkdir -p logs
# docker-compose up > logs/docker.log 2>&1 
docker-compose up --build > logs/docker.log 2>&1 
# monitor the execution with this cmd :
# tail -f -n 10 logs/docker.log
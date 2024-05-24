# AirBnB_clone_v3

# Change line endings to LF
find . -type f -exec dos2unix {} \;

# Make all .py files executable
find . -type f -name "*.py" -exec chmod +x {} \;



export MYSQL_UNIX_PORT=/var/run/mysqld/mysqld.sock


#!/home/ndirangu749/anaconda3/envs/alxse/bin/python

cfaae0b9-58f0-4fc3-a9ba-0395522abdc5

curl -X PUT http://0.0.0.0:5000/api/v1/states/cfaae0b9-58f0-4fc3-a9ba-0395522abdc5 -H "Content-Type: application/json" -d '{"name": "California is so cool"}'


curl -X DELETE http://0.0.0.0:5000/api/v1/states/cfaae0b9-58f0-4fc3-a9ba-0395522abdc5


curl -X GET http://0.0.0.0:5000/api/v1/states/cfaae0b9-58f0-4fc3-a9ba-0395522abdc5




Colorado

421a55f4-7d82-47d9-b54c-a76916479548

curl -X GET http://0.0.0.0:5000/api/v1/states/421a55f4-7d82-47d9-b54c-a76916479548/cities


curl -X POST http://0.0.0.0:5000/api/v1/states/421a55f4-7d82-47d9-b54c-a76916479548/cities -H "Content-Type: application/json" -d '{"name": "Alexandria"}' -vvv
c5aae732-e05a-4f26-9267-8771df3ad783

curl -X PUT http://0.0.0.0:5000/api/v1/cities/c5aae732-e05a-4f26-9267-8771df3ad783 -H "Content-Type: application/json" -d '{"name": "Bossier City"}'

curl -X DELETE http://0.0.0.0:5000/api/v1/cities/c5aae732-e05a-4f26-9267-8771df3ad783

# -Redis-with-Actors-and-Movies
🧪 Practical Exercise: Redis with Actors and Movies 

🛠️ Objective You'll:  Load data into Redis using Docker. Interact with Redis using Python. Write queries to analyze data.

🚀 Setup
1. Run Redis and RedisInsight using Docker Compose
Create a docker-compose.yml with this minimal configuration and add a Jupyter notebook image with a mounted folder for your notebooks :

version: '3'
services:
  redis:
    image: redis:latest
    container_name: redis-server
    ports:
      - "6379:6379"
    volumes:
      - ./data:/data

  redisinsight:
    image: redis/redisinsight:latest
    container_name: redis-insight
    ports:
      - "5540:5540"
    depends_on:
      - redis

volumes:
  redis_data:
The data folder should contain the files actors.redis and movies.redis.

Start it:

docker-compose up -d
📥 Load the Data
In a terminal, run:

docker exec -i redis-server redis-cli < data/actors.redis
docker exec -i redis-server redis-cli < data/movies.redis
🧪 Part 1 – Data Exploration (RedisInsight or Python)
Jupyter notebook page and install the client:

!pip install redis
import redis

# Connect
r = redis.Redis(host='redis', port=6379, decode_responses=True)
Answer to the following questions :

How many actors and movies are stored in Redis?
List 5 actors born before 1980.
Retrieve the genre and rating of the movie "The Imitation Game".
List the top 5 highest-rated movies.
How many movies have a rating above 7.5?
Update the rating of the movie "The Imitation Game" to 8.5.
Add a new actor: "Zendaya", born in 1996.
Delete the movie with title "The Room".


📌 Part 2 – Python Interaction
Write a Python script that does the following:

Connects to Redis.
Loads all actor hashes and counts how many actors have a last name starting with “P”.
Gets all movies released after 2010 with more than 100,000 votes.
Creates a new hash: top_movies_by_genre:<genre> with the highest-rated movie per genre.


🧼 Cleanup
To stop everything:

docker-compose down

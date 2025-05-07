import redis

#1/ Connects to Redis.

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


#2/ Loads all actor hashes and counts how many actors have a last name starting with “P”.
number_of_P_last_names=0
for key in  r.scan_iter(match='actor:*'):
    if r.type(key) != 'hash':

        continue
    
    last_name=r.hget(key,'last_name')
    if last_name.startswith('P'):
        number_of_P_last_names=number_of_P_last_names+1

print("The number of actors that  have a last name starting with 'P' is :", number_of_P_last_names)

#3/ Gets all movies released after 2010 with more than 100,000 votes.

moovies = []
for key in r.scan_iter(match='movie:*'):
    year = r.hget(key, 'release_year')
    numb_votes= r.hget(key, 'votes')
    
    
    release_year=int(year)
    votes=int(numb_votes)

    if release_year > 2010 and votes > 100000: 
        moovies.append({
            'key': key,
            'title': r.hget(key, 'title'),
            'release_year':release_year,
            'votes': votes})


for m in moovies:
    print(f"{m['key']} {m['title']} {m['release_year']} {m['votes']}")



#4/ Creates a new hash: top_movies_by_genre:<genre> with the highest-rated movie per genre.

top_by_genre = {}  

for key in r.scan_iter(match='movie:*'):
    # On récupère genre, note et titre 
    genre, rating, title = r.hmget(key, ['genre', 'rating', 'title'])
    if not genre or not rating:
        continue
    try:
        score = float(rating)
    except ValueError:
        continue

    # Si ce genre est nouveau ou si ce film a une note supérieure à celle stockée
    if genre not in top_by_genre or score > top_by_genre[genre]['rating']:
        top_by_genre[genre] = {
            'title': title,
            'rating': score
        }

# Écriture dans Redis
for genre, info in top_by_genre.items():
    new_key = f"top_movies_by_genre:{genre}"
   
    r.hset(new_key, mapping={
        'title':  info['title'],
        'rating': info['rating']
    })
    print(f"Créé {new_key} → {{'title': {info['title']!r}, 'rating': {info['rating']}}}")
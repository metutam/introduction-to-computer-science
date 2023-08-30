SELECT DISTINCT(name) FROM directors, ratings, people
WHERE directors.movie_id = ratings.movie_id
AND directors.person_id = people.id
AND rating >= 9.0;
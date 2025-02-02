select * from posts; -- 3, 2
select * from users; -- 1 & 4
select * from votes;
select * from alembic_version;

insert into votes (post_id, user_id) values (4, 3);
delete from votes;

select posts.*, count(votes.post_id) as likes from posts left join votes on posts.id = votes.post_id group by posts.id;

SELECT users.id, users.email, COUNT(posts.id) AS post_count
FROM users
LEFT JOIN posts
ON users.id = posts.owner_id
GROUP BY users.id;

SELECT posts.*, COUNT(votes.post_id) AS vote_count
FROM posts
LEFT JOIN votes
ON posts.id = votes.post_id
GROUP BY posts.id;

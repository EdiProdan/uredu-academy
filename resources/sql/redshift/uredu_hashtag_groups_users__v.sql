CREATE OR REPLACE VIEW "uredu-academy-final-schema".hashtag_groups_users__v AS
SELECT DISTINCT x.group_name, y.user_id
FROM "uredu-academy-final-schema".hashtag_groups_tweets__v as x
INNER JOIN "uredu-academy-final-schema".tweets as y
ON x.id = y.id

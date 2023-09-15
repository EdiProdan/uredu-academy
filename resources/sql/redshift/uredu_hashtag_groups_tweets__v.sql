CREATE OR REPLACE VIEW "uredu-academy-final-schema".hashtag_groups_tweets__v AS
SELECT DISTINCT x.group_name, y.id
FROM "uredu-academy-final-schema".hashtag_groups as x
INNER JOIN "uredu-academy-final-schema".hashtags as y
ON x.hashtag_name = y.hashtag

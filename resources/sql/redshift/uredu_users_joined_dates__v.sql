CREATE OR REPLACE VIEW "uredu-academy-final-schema".users_joined_dates__v AS
SELECT DISTINCT u.user_id, hg.group_name, min(date(t.created_at))
FROM "uredu-academy-final-schema".hashtag_group_users__v AS u
INNER JOIN "uredu-academy-final-schema"."tweets" AS t
ON t.user_id = u.user_id
INNER JOIN "uredu-academy-final-schema".hashtag_group_tweets__v AS hg
ON hg.id = t.id
GROUP BY u.user_id, hg.group_name
ORDER BY u.user_id
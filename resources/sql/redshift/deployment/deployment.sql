CREATE IF NOT EXISTS TABLE "uredu-academy-final-scheme"."users"
AS SELECT * FROM "uredu-academy-final-datalake"."users"

CREATE IF NOT EXISTS TABLE "uredu-academy-final-scheme"."tweets"
AS SELECT * FROM "uredu-academy-final-datalake"."tweets"

CREATE IF NOT EXISTS TABLE "uredu-academy-final-scheme"."user_followers"
AS SELECT * FROM "uredu-academy-final-datalake"."user_followers"

CREATE IF NOT EXISTS TABLE "uredu-academy-final-scheme"."hashtags"
AS SELECT * FROM "uredu-academy-final-datalake"."hashtags"

CREATE IF NOT EXISTS TABLE "uredu-academy-final-scheme"."user_mentions"
AS SELECT * FROM "uredu-academy-final-datalake"."user_mentions"
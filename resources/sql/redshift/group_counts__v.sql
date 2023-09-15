create or replace view "twitter_redshift_db"."uredu-academy-final-schema"."group_counts__v" as
    (SELECT
        hgt.group_name,
        count(distinct tw.id) as tweet_count,
        count(distinct tw.user_id) as user_count,
        count(distinct tw.retweet_from_user_id) as retweet_user_count,
        count(distinct tw.retweet_from_user_id)*count(distinct tw.user_id)/count(distinct tw.id) as custom_metric
    FROM
        "twitter_redshift_db"."uredu-academy-final-schema"."tweets" as tw
        inner join
        "twitter_redshift_db"."uredu-academy-final-schema"."hashtag_group_tweets__v" as hgt
        on tw.id=hgt.id
    group by
        hgt.group_name
    order by
        custom_metric desc
    )
;
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import pyspark.sql.functions as F
import boto3
from awsglue.dynamicframe import DynamicFrame
from awsglue.context import DynamicFrameCollection
from datetime import datetime
from pyspark.sql.functions import split, explode, regexp_replace, lit, col
import logging
import botocore

args = getResolvedOptions(sys.argv, ["JOB_NAME","DATABASE_LANDING","S3_BUCKET_DATA","S3_BUCKET_ADMIN","DYNAMODB_TABLE"])
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

DATABASE_LANDING = args["DATABASE_LANDING"]
S3_BUCKET_DATA = args["S3_BUCKET_DATA"]
S3_BUCKET_ADMIN = args["S3_BUCKET_ADMIN"]
DYNAMODB_TABLE = args["DYNAMODB_TABLE"]

dynamodb = boto3.client('dynamodb')
table = dynamodb.get_item(
    TableName=DYNAMODB_TABLE,
    Key={
        'name': {'S': 'tweet_dt'}
    }
)
ingestion_dttm = table['Item']['ingestion_dttm']['S']

table_name = 'tweets'
client = boto3.client('glue')
partitions = client.get_partitions(
    DatabaseName=DATABASE_LANDING,
    TableName=table_name
)

def find_all_partitions_to_ingest(partitions, ingestion_dttm):
    partitions_to_ingest = []
    
    for partition in partitions['Partitions']:
        if ingestion_dttm == '':
            partitions_to_ingest.append(partition["Values"][0])
            continue
        elif partition['Values'][0] > ingestion_dttm:
            partitions_to_ingest.append(partition["Values"][0])

    return sorted(partitions_to_ingest, key=lambda x: datetime.strptime(x, '%Y-%m-%d'))

partitions_to_ingest = find_all_partitions_to_ingest(partitions, ingestion_dttm)

latest_partition = partitions_to_ingest[-1] if partitions_to_ingest else ingestion_dttm 

def dataframe_from_partitions(partitions_to_ingest):
    dynamic_frames = []
    for partition in partitions_to_ingest:
        partition_prefix = f"tweet_dt={partition}"
        tweets_dyf = glueContext.create_dynamic_frame.from_options(
            connection_type="s3",
            connection_options={
                "paths": [f"s3://admin-academy-data/twitter/tweets/{partition_prefix}"]
            },
            format="parquet",
            transformation_ctx="tweets_dyf",
        )
        
        s3output = glueContext.getSink(
            path=f"s3://{S3_BUCKET_DATA}/twitter/landing/tweets/",
            connection_type="s3",
            updateBehavior="UPDATE_IN_DATABASE",
            partitionKeys=[],
            compression="snappy",
            enableUpdateCatalog=True,
            transformation_ctx="s3output",
        )
        s3output.setCatalogInfo(
            catalogDatabase="uredu-academy-final-landing", catalogTableName="tweets"
        )
        s3output.setFormat("glueparquet")
        s3output.writeFrame(tweets_dyf)    
        tweets_df = tweets_dyf.toDF()
        dynamic_frames.append(tweets_df)
        

    tweets_df = dynamic_frames[0] if dynamic_frames else None
    if len(dynamic_frames) > 1:
        for i in range(1, len(dynamic_frames)):
            tweets_df = tweets_df.union(dynamic_frames[i])
    return tweets_df

def transform_df(df):
    # Save only first half of the full_text column in tweets dastaframe
    tweets_df = leave_only_first_half_of_column(df, 'full_text')
    # Make all strings lower case
    tweets_df = lower_strings(tweets_df)
    # Explode columns with lists
    user_mentions_df = explode_column(tweets_df, 'user_mentions', ['id'])
    hashtags_df = explode_column(tweets_df, 'hashtags', ['id'])
    # Drop expoloded columns from dataframe
    tweets_df = tweets_df.drop('user_mentions', 'hashtags')
    # Convert user_id to bigint
    # Drop empty strings and nulls from dataframe
    user_mentions_df = user_mentions_df.filter("user_mentions != ''").na.drop()
    hashtags_df = hashtags_df.filter("hashtags != ''").na.drop()
    hashtags_df = hashtags_df.withColumnRenamed('hashtags', 'hashtag')
    return tweets_df, user_mentions_df, hashtags_df

def leave_only_first_half_of_column(df, column):
    return df.withColumn(column, F.col(column).substr(F.lit(1),  F.floor(F.length(column) / F.lit(2))))

def lower_strings(df):
    string_cols = [item[0] for item in df.dtypes if item[1].startswith('string')]
    for col_name in string_cols:
        df = df.withColumn(col_name, F.lower(F.col(col_name)))
    return df

def explode_column(df, item, column_list):
    column_list.append(item)
    df = df.select(*column_list)
    df = df.withColumn(item, F.regexp_replace(df[item], "[' ]", ""))
    df = df.withColumn(item, F.regexp_replace(df[item], "[\\[\\]]", ""))
    df = df.withColumn(item, F.split(df[item], ','))
    return df.withColumn(item, F.explode(df[item]))

def check_if_path_exists(path):
    s3 = boto3.resource('s3')

    try:
        s3.Object(S3_BUCKET_DATA, path).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            # The object does not exist.
            return False
        else:
            # Something else has gone wrong.
            raise
    else:
        # The object does exist.
        return True

if ingestion_dttm == '':
    logger.info("Ingesting the dataset for the first time")
    tweets_dyf = glueContext.create_dynamic_frame.from_catalog(
        database=DATABASE_LANDING,
        table_name=table_name,
        transformation_ctx="tweets_dyf",
    )
    # check if path already exists
    path_exists = check_if_path_exists("twitter/landing/tweets")
    if not path_exists:
        # write to s3 and data catalog
        s3output = glueContext.getSink(
            path=f"s3://{S3_BUCKET_DATA}/twitter/landing/tweets/",
            connection_type="s3",
            updateBehavior="UPDATE_IN_DATABASE",
            partitionKeys=[],
            compression="snappy",
            enableUpdateCatalog=True,
            transformation_ctx="s3output",
        )
        s3output.setCatalogInfo(
            catalogDatabase="uredu-academy-final-landing", catalogTableName="tweets"
        )
        s3output.setFormat("glueparquet")
        s3output.writeFrame(tweets_dyf)    
    
    tweets_df = tweets_dyf.toDF()
    tweets_df, user_mentions_df, hashtags_df = transform_df(tweets_df)
    
elif partitions_to_ingest == []:
    logger.info("No new partitions to ingest")
else:
    print(f"Ingesting {len(partitions_to_ingest)} new partitions")
    tweets_df = dataframe_from_partitions(partitions_to_ingest)
    # transform dataframe
    tweets_df, user_mentions_df, hashtags_df = transform_df(tweets_df)

def update_ingestion_dttm(latest_ingestion_dttm):
    dynamodb.update_item(
        TableName='uredu-academy-final-table',
        Key={
            'name': {'S': 'tweet_dt'}
        },
        UpdateExpression='SET ingestion_dttm = :ingestion_dttm',
        ExpressionAttributeValues={
            ':ingestion_dttm': {'S': latest_ingestion_dttm}
        }
    )
update_ingestion_dttm(latest_partition)


table_name = 'users'
users_dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
    database=DATABASE_LANDING,
    table_name=table_name,
    transformation_ctx=table_name + "_dynamic_frame",
)

path_exists = check_if_path_exists("twitter/landing/users")
if not path_exists:
    s3output = glueContext.getSink(
                path=f"s3://{S3_BUCKET_DATA}/twitter/landing/users/",
                connection_type="s3",
                updateBehavior="UPDATE_IN_DATABASE",
                partitionKeys=[],
                compression="snappy",
                enableUpdateCatalog=True,
                transformation_ctx="s3output",
            )
    s3output.setCatalogInfo(
                catalogDatabase="uredu-academy-final-landing", catalogTableName="users"
            )
    s3output.setFormat("glueparquet")
    s3output.writeFrame(users_dynamic_frame)    


table_name = 'user_followers'
user_followers_dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
    database=DATABASE_LANDING,
    table_name=table_name,
    transformation_ctx=table_name + "_dynamic_frame",
)
path_exists = check_if_path_exists("twitter/landing/user_followers")
if not path_exists:
    s3output = glueContext.getSink(
                path=f"s3://{S3_BUCKET_DATA}/twitter/landing/user_followers/",
                connection_type="s3",
                updateBehavior="UPDATE_IN_DATABASE",
                partitionKeys=[],
                compression="snappy",
                enableUpdateCatalog=True,
                transformation_ctx="s3output",
            )
    s3output.setCatalogInfo(
                catalogDatabase="uredu-academy-final-landing", catalogTableName="user_followers"
            )
    s3output.setFormat("glueparquet")
    s3output.writeFrame(user_followers_dynamic_frame)  

users_df = users_dynamic_frame.toDF()
user_followers_df = user_followers_dynamic_frame.toDF()

users_df = lower_strings(users_df)
# Explode columns with lists
user_followers_df = user_followers_df.withColumn('followers', F.explode(user_followers_df['followers']))

# Convert user_id to bigint
user_followers_df = user_followers_df.withColumn('user_id', F.col('user_id').cast("long"))

user_followers_df = user_followers_df.na.drop()

# transform df to dyf
users_dyf = DynamicFrame.fromDF(users_df, glueContext, "users_dyf")
s3output = glueContext.getSink(
    path=f"s3://{S3_BUCKET_DATA}/twitter/datalake/users/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    compression="snappy",
    enableUpdateCatalog=True,
    transformation_ctx="s3output",
)
s3output.setCatalogInfo(
    catalogDatabase="uredu-academy-final-datalake", catalogTableName="users"
)
s3output.setFormat("glueparquet")
s3output.writeFrame(users_dyf)
# transform df to dyf
if partitions_to_ingest != []:
    tweets_dyf = DynamicFrame.fromDF(tweets_df, glueContext, "tweets_dyf")
    s3output = glueContext.getSink(
        path=f"s3://{S3_BUCKET_DATA}/twitter/datalake/tweets/",
        connection_type="s3",
        updateBehavior="UPDATE_IN_DATABASE",
        partitionKeys=[],
        compression="snappy",
        enableUpdateCatalog=True,
        transformation_ctx="s3output",
    )
    s3output.setCatalogInfo(
        catalogDatabase="uredu-academy-final-datalake", catalogTableName="tweets"
    )
    s3output.setFormat("glueparquet")
    s3output.writeFrame(tweets_dyf)
    
    # write hashtags_df to s3 and data catalog
    
    hashtags_dyf = DynamicFrame.fromDF(hashtags_df, glueContext, "hashtags_dyf")
    s3output = glueContext.getSink(
        path=f"s3://{S3_BUCKET_DATA}/twitter/datalake/hashtags/",
        connection_type="s3",
        updateBehavior="UPDATE_IN_DATABASE",
        partitionKeys=[],
        compression="snappy",
        enableUpdateCatalog=True,
        transformation_ctx="s3output",
    )
    s3output.setCatalogInfo(
        catalogDatabase="uredu-academy-final-datalake", catalogTableName="hashtags"
    )
    s3output.setFormat("glueparquet")
    s3output.writeFrame(hashtags_dyf)
    
    # write user_mentions_df to s3 and data catalog
    user_mentions_dyf = DynamicFrame.fromDF(user_mentions_df, glueContext, "user_mentions_dyf")
    s3output = glueContext.getSink(
        path=f"s3://{S3_BUCKET_DATA}/twitter/datalake/user_mentions/",
        connection_type="s3",
        updateBehavior="UPDATE_IN_DATABASE",
        partitionKeys=[],
        compression="snappy",
        enableUpdateCatalog=True,
        transformation_ctx="s3output",
    )
    s3output.setCatalogInfo(
        catalogDatabase="uredu-academy-final-datalake", catalogTableName="user_mentions"
    )
    s3output.setFormat("glueparquet")
    s3output.writeFrame(user_mentions_dyf)

# write user_followers_df to s3 and data catalog
user_followers_dyf = DynamicFrame.fromDF(user_followers_df, glueContext, "user_followers_dyf")
s3output = glueContext.getSink(
    path=f"s3://{S3_BUCKET_DATA}/twitter/datalake/user_followers/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    compression="snappy",
    enableUpdateCatalog=True,
    transformation_ctx="s3output",
)
s3output.setCatalogInfo(
    catalogDatabase="uredu-academy-final-datalake", catalogTableName="user_followers"
)
s3output.setFormat("glueparquet")
s3output.writeFrame(user_followers_dyf)


job.commit()
import json
import boto3
import botocore
import psycopg2
from os import environ

def lambda_handler(event, context):
    secret_name = environ.get('secretName')
    
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name='eu-central-1',
    )

    try: 
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except botocore.exceptions.ClientError as e:
        raise e
    
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = get_secret_value_response['SecretBinary']

    secret_data = json.loads(secret)

    # Connect to Redshift cluster using the credentials from the secret
    connection = psycopg2.connect(**secret_data)
    # create schema
    cursor = connection.cursor()
    create_datalake_schema_sql = "CREATE EXTERNAL SCHEMA \"uredu-academy-final-datalake\" FROM DATA CATALOG DATABASE 'uredu-academy-final-datalake' IAM_ROLE 'arn:aws:iam::456582705970:role/RedshiftRole'"
    cursor.execute(create_datalake_schema_sql)
    connection.commit()
    create_landing_schema_sql = "CREATE EXTERNAL SCHEMA \"uredu-academy-final-landing\" FROM DATA CATALOG DATABASE 'uredu-academy-final-landing' IAM_ROLE 'arn:aws:iam::456582705970:role/RedshiftRole'"
    cursor.execute(create_landing_schema_sql)
    connection.commit()
    create_schema_sql = "CREATE SCHEMA \"uredu-academy-final-schema\""
    cursor.execute(create_schema_sql)
    connection.commit()
    cursor = connection.cursor()
    tables = ["users", "tweets", "user_followers", "hashtags", "user_mentions"]
    for table in tables:
        create_table_sql = f"CREATE TABLE \"uredu-academy-final-schema\".\"{table}\" AS SELECT * FROM \"uredu-academy-final-datalake\".\"{table}\""
        try:
            cursor.execute(create_table_sql)
        except psycopg2.Error as e:
            pass
    
        connection.commit()

         
    # execute query
    return { 
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

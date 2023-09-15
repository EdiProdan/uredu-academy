# AWS Pricing Calculations

## Amazon S3

### Unit Conversions
- S3 Standard Average Object Size: 16 MB x 0.0009765625 GB in a MB = 0.015625 GB

### Pricing Calculations
- 2 GB per month / 0.015625 GB average item size = 128.00 unrounded number of objects
- Round up by 1 (128.0000) = 128 number of objects
- Tiered price for: 2 GB
- 2 GB x 0.0245000000 USD = 0.05 USD
- Total tier cost = 0.0490 USD (S3 Standard storage cost)
- 300 PUT requests for S3 Standard Storage x 0.0000054 USD per request = 0.0016 USD (S3 Standard PUT requests cost)
- 300 GET requests in a month x 0.00000043 USD per request = 0.0001 USD (S3 Standard GET requests cost)
- 2 GB x 0.0008 USD = 0.0016 USD (S3 select returned cost)
- 2 GB x 0.00225 USD = 0.0045 USD (S3 select scanned cost)
- Total S3 Standard Storage, data requests, S3 select cost = 0.049 USD + 0.0001 USD + 0.0016 USD + 0.0016 USD + 0.0045 USD = 0.06 USD
- S3 Standard cost (monthly): 0.06 USD

## AWS Glue

### Duration for ETL Jobs
- Duration for Apache Spark ETL job runs: 1 minute = 0.02 hours
- Duration for Python Shell ETL job runs: 60 minutes = 1 hour

### Pricing Calculations
- Max (0.02 hours, 0.0166 hours (minimum billable duration)) = 0.02 hours (billable duration)
- Apache Spark ETL job cost: 2 DPUs x 0.02 hours x 0.44 USD per DPU-Hour = 0.02 USD
- Python Shell ETL job cost: 1 DPU x 1 hour x 0.44 USD per DPU-Hour = 0.44 USD
- ETL jobs cost (monthly): 0.46 USD

## Amazon Redshift

### Pricing Calculation for Redshift Instance
- 2 instance(s) x 0.25 USD hourly x (10 / 100 Utilized/Month) x 730 hours in a month = 47.30 USD

## Amazon Comprehend

### Pricing Calculation for Comprehend
- 280 characters per document x 300,000 documents = 84,000,000 characters per request asynchronous
- Max (84000000 characters, 300 characters) = 84,000,000.00 characters
- NLP requests are measured in units of 100 characters, with a 3 unit (300 character) minimum charge per request. Characters per request is: 84,000,000.00
- 84,000,000.00 characters / 100 characters = 840,000 units for asynchronous
- RoundUp (840000) = 840000 units rounded up to nearest 1 unit asynchronous
- Tiered price for: 840000 units
- 840000 units x 0.0001000000 USD = 84.00 USD
- Total tier cost = 84.00 USD for month
- USD for sentiment analysis (monthly): 84.00 USD

## Amazon Translate

### Pricing Calculation for Translate
- 4,000,000 characters (16800 tweets * 280 characters) x 0.000015 USD = 60.00 USD (cost for Standard Real-Time Translation)
- Standard Real-Time Translation cost (monthly): 60.00 USD

## Total Cost

### Total Cost for AWS Services
- S3 Standard cost (monthly): 0.06 USD
- ETL jobs cost (monthly): 0.46 USD
- Redshift cost (monthly): 47.30 USD
- Comprehend cost (monthly): 84.00 USD
- Translate cost (monthly): 60.00 USD
- Total cost (monthly): 191.82 USD
```
from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.functions import col, collect_list
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark.sql.functions import expr

import time

conf = SparkConf().set("spark.driver.memory", "8g")

spark = SparkSession.builder\
        .master("local[*]")\
        .config(conf=conf)\
        .appName('PySpark_Tutorial')\
        .getOrCreate()


df = spark.read.csv("custom_1988_2020.csv", sep=",", inferSchema=True, header=True)

sum_time = 0
for i in range(100):
        cur_time = time.time()
        df2 = df.withColumn("34353", col('34353')**3)

        sum_time = sum_time + time.time() - cur_time
print(sum_time/100)
df.write.parquet("./output/people.parquet")
df.write.orc("./output/people.orc")
parDF=spark.read.parquet("./output/people.parquet")
orcDF=spark.read.orc("./output/people.orc")
sum_time = 0
for i in range(100):
        cur_time = time.time()
        df2 = parDF.withColumn("34353", col('34353')**3)

        sum_time = sum_time + time.time() - cur_time
print(sum_time/100)
sum_time = 0
for i in range(100):
        cur_time = time.time()
        df3 = orcDF.withColumn("34353", col('34353')**3)

        sum_time = sum_time + time.time() - cur_time
print(sum_time/100)





time.sleep(100000)
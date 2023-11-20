from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.functions import col, collect_list
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
import time

conf = SparkConf().set("spark.driver.memory", "8g")

spark = SparkSession.builder\
        .master("local[*]")\
        .config(conf=conf)\
        .appName('PySpark_Tutorial')\
        .getOrCreate()

df = spark.read.csv("custom_1988_2020.csv", sep=",", inferSchema=True, header=True)

df.write.parquet("./output/people.parquet")
df.write.orc("./output/people.orc")
parDF=spark.read.parquet("./output/people.parquet")
orcDF=spark.read.orc("./output/people.orc")
parDF.show(1000000)
orcDF.show(1000000)

print('yes')



time.sleep(100000)
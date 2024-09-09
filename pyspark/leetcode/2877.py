from pyspark.sql import SparkSession

input = [
  [1, 15],
  [2, 11],
  [3, 11],
  [4, 20]
]

spark = SparkSession.builder.appName("2877").getOrCreate()

df = spark.createDataFrame(input, ["student_id", "age"])

df.show()

spark.stop()

# Expected output:
# +------------+-----+
# | student_id | age |
# +------------+-----+
# | 1          | 15  |
# | 2          | 11  |
# | 3          | 11  |
# | 4          | 20  |
# +------------+-----+
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql import SparkSession, Window
import  datetime

from pyspark.sql.types import BooleanType


spark = SparkSession.builder\
        .appName("job1-app")\
        .getOrCreate()


def run(): 
        BASE_PATH = '/data'
        matches = '/home/jbouhadoun/esgi/architecture/tp_spark/data/df_matches.csv'


        df_matches = spark.read \
                        .option("delimiter",",")\
                        .option("header", "true")\
                        .csv(matches)
        


        df_matches_rename= df_matches.withColumnRenamed('X4', 'match').withColumnRenamed('X6', 'competition')



        df_matches_selected=df_matches_rename.select('match','competition','adversaire','score_france','score_adversaire','penalty_france','penalty_adversaire','date')


        df_matches_penalety_adversaire = df_matches_selected.withColumn('penalty_adversaire', F.when(F.col("penalty_adversaire") == 'NA', '0').otherwise(F.col("penalty_adversaire")))
        df_matches_penalety_france= df_matches_penalety_adversaire.withColumn('penalty_france', F.when(F.col("penalty_france") == 'NA', '0').otherwise(F.col("penalty_france")))


        df_matches_date_cast = df_matches_penalety_france.withColumn('date', F.to_date(F.col('date'),"yyyy-MM-dd"))
        df_matches_date= df_matches_date_cast.filter( df_matches_date_cast.date > datetime.date(1980,3,1))



        
        domicile_udf=F.udf(lambda z: z.split('-')[0].strip() == 'France',BooleanType())

        df_domicile=df_matches_date.withColumn('domicile',domicile_udf(df_matches_date.match))
        


        nb_match_mean_france=df_domicile.groupBy('adversaire').agg(F.mean(df_domicile.score_france)).show()

        nb_match_mean_adversaire=df_domicile.groupBy('adversaire').agg(F.mean(df_domicile.score_adversaire)).show()

        nb_macth_total=df_domicile.groupBy('adversaire').count()
    
        #pourcentage= df_domicile.groupBy('adversaire').agg((df_domicile.domicile==True).count()/nb_macth_total)

        #nb_match_coupe=df_domicile.groupBy('adversaire').agg((df_domicile.competition).startswith("Coupe"))
        


        nb_max_pen=df_domicile.groupBy('adversaire').agg({"penalty_france": "max"}).collect()[0]
     


     


run()

from dagster import op
import mysql.connector
import pandas as pd


@op
def my_op(context):
    context.log.info("my operations is starting")

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="example",
        database="testdatabase"
    )

    mycursor = mydb.cursor(buffered=True)

    df = pd.read_excel("dataset.xlsx", names=None, engine='openpyxl')
    df = df.where((pd.notnull(df)), None)

    df = df.where(df != "#REF!", None)
    df = df.where(df != "!", None)
    df = df.where(df != "-", None)
    df = df.where(df != " ", None)
    df = df.where(df != "?", None)

    cols = "`,`".join([str(i).replace(' ', '_') for i in df.columns.tolist()])
    print(cols)
    i = 0
    for row in df.iterrows():
        sql = "INSERT INTO `drillingparameter`(`" + cols + "`) VALUES ({})".format(
            ','.join(['%s']*len(df.columns)))
        mycursor.execute(sql, tuple(row[1]))
        mydb.commit()
        context.log.info(f"inserting data {i} : {tuple(row[1])}")
        i += 1

import psycopg2
try:
    conn = psycopg2.connect(dbname= 'postgres', user= 'postgres',password = 'example', host='localhost', port="8070")
except:
    print ("I am unable to connect to the database.")
cur = conn.cursor()
cur.execute(
    "CREATE TABLE test3 (id serial PRIMARY KEY, num integer, data varchar);"
)
cur.execute(
    "INSERT INTO test3 (num, data) VALUES (%s, %s)",
    (100, "abc'def")
)
# Выполнить команду
cur.execute("SELECT * FROM test3;")
# Но как получить результат её выполнения?..

# А вот так. fetchone — «принести» одну строчку результата,
# fetchall — все строчки.
cur.fetchone()

# Завершить транзакцию
conn.commit()
# Закрыть курсор
cur.close()
# Закрыть подключение
conn.close()

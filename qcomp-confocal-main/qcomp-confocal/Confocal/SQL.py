import psycopg2 as pg2
from functools import wraps
import datetime


class Database:

    def generate_name():
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        now = datetime.datetime.now().strftime("%H-%M-%S")
        name = str(today)+ "-"+str(now)
        return name


    def decorator_insert(original_function):

        @wraps(original_function)
        def wrapper_function(*args,**kwargs):
            query,content = original_function(*args,**kwargs)
            conn = pg2.connect(database = 'QuantumPulse', user = 'postgres',password = 'Duttlab')
            cur = conn.cursor()
            executable = cur.mogrify(query,content)
            cur.execute(executable)
            conn.commit()
            conn.close()
        return wrapper_function

    @decorator_insert
    def QP(self,data):

        data_id = Database.generate_name()
        query = "INSERT INTO experiment_data(data_id,xcoord,ycoord,counts,time_stamp) VALUES (%s,%s,%s,%s," \
                "CURRENT_TIMESTAMP) "
        content = [data_id, data[0],data[1],data[2]]

        return (query,content)


if __name__ == '__main__':
    a = [1,2,3]
    b = [4,5,6]
    c = [7,8,9]

    data = [a,b,c]

    Database().QP(data)
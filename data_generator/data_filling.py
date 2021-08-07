import uuid
import random
from datetime import timedelta, datetime
import psycopg2

name_list = open('names.txt').read().split('\n')
lastname_list = open('lastnames.txt').read().split('\n')


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_seconds = random.randrange(int_delta)
    return start + timedelta(seconds=random_seconds)


def generate_user():

    user_list_tup = []
    wallet_list_tup = []
    history_list_tup = []

    operation_type = ['IN', 'OUT']
    for _ in range(20000):
        user_id = uuid.uuid4()
        wallet_id = uuid.uuid4()
        name = '{} {}'.format(
            random.choice(name_list),
            random.choice(lastname_list),
        )
        user_history_tup = []
        for _ in range(random.randint(5, 10)):
            if not user_history_tup:
                amount = random.randint(100, 1000)
                user_history_tup.append(
                    (
                        str(uuid.uuid4()),
                        'IN',
                        random_date(datetime(2020, 8, 1), datetime.today()),
                        amount,
                        amount,
                        str(wallet_id)
                    )
                )
            else:
                total_amount_old = user_history_tup[-1][4]
                if total_amount_old < 5:
                    type = 'IN'
                else:
                    type = random.choice(operation_type)

                if type == 'IN':
                    purchase = random.randint(1, 1000)
                else:
                    purchase = random.randint(1, total_amount_old)

                total_amount_new = total_amount_old + purchase if type == 'IN' else total_amount_old - purchase

                operation_year = user_history_tup[-1][2].year
                operation_month = user_history_tup[-1][2].month
                operation_day = user_history_tup[-1][2].day

                user_history_tup.append(
                    (
                        str(uuid.uuid4()),
                        type,
                        random_date(datetime(operation_year, operation_month, operation_day), datetime.today()),
                        purchase,
                        total_amount_new,
                        str(wallet_id)
                    )
                )

        user_list_tup.append((str(user_id), name, random_date(datetime(1950, 1, 1), datetime(2000, 12, 12))))
        wallet_list_tup.append((str(wallet_id), user_history_tup[-1][4], str(user_id)))
        history_list_tup += user_history_tup

    return user_list_tup, wallet_list_tup, sorted(history_list_tup, key=lambda k: k[2])


user_list_tup, wallet_list_tup, history_list_tup = generate_user()

con = psycopg2.connect(host='localhost', port='5432', password='test', dbname='fortin_test', user='postgres')
cur = con.cursor()

cur.executemany('INSERT INTO clients (id, name, birthday) VALUES (%s, %s, %s)', user_list_tup)
con.commit()

cur.executemany('INSERT INTO wallets (id, amount, client_id) VALUES (%s, %s, %s)', wallet_list_tup)
con.commit()

cur.executemany('INSERT INTO operations (id, type, date, operation_amount, total_amount, wallet_id) VALUES (%s, %s, %s, %s, %s, %s)', history_list_tup)
con.commit()


import  psycopg2

def main():
    conn = psycopg2.connect(database="", user="", password="")
    s = ''
    while True:
        if s == '1':
            createtables(conn)
            s = ''
        elif s == '2':
            droptables(conn)
            s = ''
        elif s == '3':
            show(conn)
            s = ''
        elif s == '4':
            addclient(conn)
            s = ''
        elif s == '5':
            addphone(conn)
            s = ''
        elif s == '6':
            update(conn)
            s = ''
        elif s == '7':
            delphone(conn)
            s = ''
        elif s == '8':
            delclient(conn)
            s = ''
        elif s == '9':
            findclient(conn)
            s = ''
        elif s == 'q':
            conn.close()
            break
            s = ''
        else:
            print("1. Создать таблицы\n"
                  "2. Удалить таблицы\n"
                  "3. Показать клиентов\n"
                  "4. Добавить клиента\n"
                  "5. Добавить номер телефона\n"
                  "6. Обновить информацию о клиенте\n"
                  "7. Удалить номер телефона\n"
                  "8. Удалить клиента\n"
                  "9. Поиск клиента\n"
                  "q. Выйти")
            s = input("Выберите действие: ")


def show(conn):
    with conn.cursor() as cur:
        cur.execute("""
                    SELECT id, first_name, last_name FROM clients;
                    """)
        res = cur.fetchall()
        for i in res:
            print(f'{i[0]}. {i[1]} {i[2]}')
        print()


def createtables(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(60) not null,
        last_name VARCHAR(60) not null,
        email VARCHAR(60) not null
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone(
        client INTEGER not null references clients(id),
        phone VARCHAR(20) not null
        );
        """)
        conn.commit()


def droptables(conn):
    with conn.cursor() as cur:
        cur.execute("""
                    DROP TABLE clients cascade;
                    """)
        cur.execute("""
                    DROP TABLE phone cascade;
                    """)
        conn.commit()


def addclient(conn):
    first_name = input("\nВведите имя: ")
    last_name = input("Введите фамилию: ")
    email = input("Введите email: ")
    with conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO clients(first_name, last_name, email)
                    VALUES (%s, %s, %s) RETURNING id, first_name
                    """, (first_name, last_name, email))
        res = cur.fetchone()
        print (f'Добавлен клиент {res[1]} с идентификатором {res[0]}\n')
        conn.commit()


def addphone(conn):
    show(conn)
    id = input("Введите id клиента: ")
    phone = input("Введите номер телефона: ")
    with conn.cursor() as cur:
        cur.execute("""
                        INSERT INTO phone(client, phone)
                        VALUES (%s, %s) RETURNING phone
                        """, (id, phone))
        res = cur.fetchone()
        print(f'Добавлен телефон {res[0]}\n')
        conn.commit()


def update(conn):
    show(conn)
    id = input("\nВведите идентификатор пользователя: ")
    first_name = input("Введите имя: ")
    last_name = input("Введите фамилию: ")
    email = input("Введите email: ")
    with conn.cursor() as cur:
        cur.execute("""
                    UPDATE clients SET first_name=%s, last_name=%s, email=%s WHERE id=%s;
                    """, (first_name, last_name, email, id))
        conn.commit()
    print("Данные обновлены успешно\n")


def delphone(conn):
    show(conn)
    id = input("Выберите идентификатор клиента: ")
    with conn.cursor() as cur:
        cur.execute("""
                    SELECT phone FROM phone
                    WHERE client=%s;
                    """, (id, ))
        res = cur.fetchall()
        counter = 1
        for i in res:
            print(f'{counter}. {i[0]}')
            counter+=1
        phone = res[int(input("Введите идентификатор номера: "))-1][0]
        cur.execute("""
                        DELETE FROM phone
                        WHERE phone=%s;
                    """, (phone,))
        conn.commit()
        print(f'Телефон {phone} успешно удалён\n')


def delclient(conn):
    show(conn)
    id = input("Выберите идентификатор клиента: ")
    with conn.cursor() as cur:
        cur.execute("""
                    DELETE FROM phone
                    WHERE client=%s;
                    """, (id,))
        conn.commit()
        cur.execute("""
                            DELETE FROM clients
                            WHERE id=%s;
                            """, (id,))
        conn.commit()
    print("Пользователь удалён успешно\n")


def find_c(conn, fname='*', lname='*', email='*', id=1):
    with conn.cursor() as cur:
        cur.execute("""
                    SELECT * FROM clients
                    WHERE first_name=%s and last_name=%s and email=%s;
                    """, (fname, lname, email))
        res = cur.fetchall()
        print(res)


def findclient(conn):
    print("\n1. По имени\n2. По фамилии\n3. По email\n4. По телефону")
    choise = input("Выберите: ")
    q = input("Введите поисковой запрос: ")
    if choise=='1':
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT * FROM clients
                        WHERE first_name=%s;
                        """, (q, ))
            res = cur.fetchall()
            for i in res:
                print(f'{i[0]}. {i[1]} {i[2]} | {i[3]}')
            print()
    elif choise=='2':
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT * FROM clients
                        WHERE last_name=%s;
                        """, (q, ))
            res = cur.fetchall()
            for i in res:
                print(f'{i[0]}. {i[1]} {i[2]} | {i[3]}')
            print()
    elif choise =='3':
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT * FROM clients
                        WHERE email=%s;
                        """, (q, ))
            res = cur.fetchall()
            for i in res:
                print(f'{i[0]}. {i[1]} {i[2]} | {i[3]}')
            print()
    elif choise =='4':
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT client FROM phone
                        WHERE phone=%s;
                        """, (q, ))
            client = cur.fetchone()[0]
            cur.execute("""
                        SELECT * FROM clients
                        WHERE id=%s;
                        """, (client,))
            i = cur.fetchone()
            print(f'{i[0]}. {i[1]} {i[2]} | {i[3]}')


if __name__ == "__main__":
    main()
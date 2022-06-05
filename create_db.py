'''
    DISCLAIMER: This file SHOULD ONLY RUN ONCE to create DB, if run again, it will delete all existing content
'''

import os # Access env variables
import psycopg2

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE users(
                    user_id INT GENERATED ALWAYS AS IDENTITY,
                    email VARCHAR(150) NOT NULL UNIQUE,
                    password VARCHAR(50) NOT NULL,
                    user_name VARCHAR(100) NOT NULL,
                    PRIMARY KEY(user_id)
        )
        """
        ,
        """
        CREATE TABLE books (
                    book_id INT GENERATED ALWAYS AS IDENTITY,
                    user_id INT,
                    title VARCHAR(150) NOT NULL,
                    author VARCHAR(150) NOT NULL,
                    quotes TEXT,
                    review TEXT,
                    date_added DATE DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY(book_id),
                        CONSTRAINT fk_user
                            FOREIGN KEY(user_id)
                                REFERENCES users(user_id)
                                ON DELETE CASCADE
        )
        """
    )
    try:
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
        
"""
    START DB initialization
"""

os.environ['DB_USERNAME'] = 'admin'
os.environ['DB_PASSWORD'] = 'PurplePine015'

# Create a connection to the DB
conn = psycopg2.connect(
        host="localhost",
        database="book_db",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations -> allows Python code to execute PostgreSQL commands in a database session.
cur = conn.cursor()

""" 
    1. Execute a command: Create new books table and users table
    (This command will execute once and delete everything)
    
"""
cur.execute('DROP TABLE IF EXISTS books;') 
cur.execute('DROP TABLE IF EXISTS users;')

create_tables()
cur = conn.cursor()

# Insert EXAMPLE-DATA into the table

cur.execute('INSERT INTO users (email, password, user_name)'
            'VALUES (%s, %s, %s)',
            (
             'lillo@gmail.com',
             'password',
             'user1')
            )

cur.execute('INSERT INTO users (email, password, user_name)'
            'VALUES (%s, %s, %s)',
            (
             'lillo2@gmail.com',
             'password',
             'user2')
            )

cur.execute('INSERT INTO books (user_id, title, author, quotes, review)'
            'VALUES (%s, %s, %s, %s, %s)',
            ('1',
             'La tabla de Flandes',
             'Arturo Pérez-Reverte',
             'Dios mueve al jugador y este a la pieza. ¿Qué Dios detrás de Dios la trama empieza de polvo y sueño y agonías...?',
             'A great classic!')
            )

cur.execute('INSERT INTO books (user_id, title, author, quotes, review)'
            'VALUES (%s, %s, %s, %s, %s)',
            ('2',
             'La tabla de Flandes',
             'Arturo Pérez-Reverte',
             'Dios mueve al jugador y este a la pieza. ¿Qué Dios detrás de Dios la trama empieza de polvo y sueño y agonías...?',
             'A great classic!')
            )



# Commit transaction, like github
conn.commit()

# Close cursor and connection
cur.close()
conn.close()

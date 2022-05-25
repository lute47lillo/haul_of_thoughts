'''
    DISCLAIMER: This file SHOULD ONLY RUN ONCE to create DB, if run again, it will delete all existing content
'''


import os # Access env variables
import psycopg2

# Create a connection to the DB
conn = psycopg2.connect(
        host="localhost",
        database="book_db",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations -> allows Python code to execute PostgreSQL commands in a database session.
cur = conn.cursor()

# Execute a command: this creates a new table
#This command will execute once and delete everything
cur.execute('DROP TABLE IF EXISTS books;') 

'''
    id serial -> The database will assign a unique value to this key for each entry. Autoincrementing integer.
    review text -> any length
    varchar(x) -> capped to x characters
    
'''
cur.execute('CREATE TABLE books (id serial PRIMARY KEY,'
                                 'title varchar (150) NOT NULL,'
                                 'author varchar (50) NOT NULL,'
                                 'quotes text,'
                                 'review text,'
                                 'read boolean NOT NULL,'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )


# Insert EXAMPLE-DATA into the table
cur.execute('INSERT INTO books (title, author, quotes, read, review)'
            'VALUES (%s, %s, %s, %s, %s)',
            ('La tabla de Flandes',
             'Arturo Pérez-Reverte',
             'Dios mueve al jugador y este a la pieza. ¿Qué Dios detrás de Dios la trama empieza de polvo y sueño y agonías...?',
             'FALSE',
             'A great classic!')
            )

# Commit transaction, like github
conn.commit()

# Close cursor and connection
cur.close()
conn.close()
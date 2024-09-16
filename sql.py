import sqlite3
from table_info import table_definitions

def create_tables(cursor):
    for table in table_definitions:
        try:
            cursor.execute(table["definition"])
            print(f"Table '{table['name']}' created successfully!")
        except Exception as e:
            print(f"Error creating table '{table['name']}': {str(e)}")


def main():
    try:
        with sqlite3.connect('Data.db') as conn:
            cursor = conn.cursor()
            create_tables(cursor)
            conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

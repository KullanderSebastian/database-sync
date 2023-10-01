'''data = []

finns det en databas? om inte:

Importera Databas (of choice, (SQLite först))

if databas:
    connecta till databas

    Hämta data ifrån "original" databasen och "hash" databasen

    Jämför nya datan med gamla:
        if ny_data inte finns i databasen:
            lägg till data
        elif ny_data finns i database:
            if ny_data != gammal_data:
                 uppdatera_data
            elif ny_data == gammal_data:
                 gör ingenting

elif !databas:
        Skapa en databas med original data
        Skapa en databas med hash strängar(för att jämföra databaserna)'''

import sqlite3
import json
import hashlib

with open("mock.json", "r") as file:
    data = json.load(file)

def connect_to_database(db_name):
    conn = sqlite3.connect(f"{db_name}.db")

    cursor = conn.cursor()

    return cursor, conn

def create_db_and_table(data, db_name, db_table_name):
    cursor, conn = connect_to_database(db_name)

    keys = data[0].keys()
    columns = []

    for key in keys:
        if isinstance(data[0][key], str):
            typeString = "TEXT"
        elif isinstance(data[0][key], int):
            typeString = "INTEGER"

        columns.append((key, typeString))
    
    columns.append(("hash", "TEXT"))

    # Build the CREATE TABLE statement
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {db_table_name} ("

    # Add column definitions
    for column_name, column_type in columns:
        create_table_sql += f"{column_name} {column_type}, "

    # Remove the trailing comma and add the closing parenthesis
    create_table_sql = create_table_sql.rstrip(", ") + ")"

    cursor.execute(create_table_sql)

    conn.commit()
    conn.close()

def create_hash(item, key_selection_array):
    contains_numbers = False
    contains_strings = False
    data = {}

    for variable_type in key_selection_array:
        if isinstance(variable_type, (int, float)):
            contains_numbers = True
        elif isinstance(variable_type, str):
            contains_strings = True

    if contains_numbers == True & contains_strings == True:
        print("The key_selection_array can only contain either ints or strings")
        return
    elif contains_numbers == True:
        for key_selector in key_selection_array:
            data[list(item)[key_selector]] = list(item.values())[key_selector]
    elif contains_strings == True:
        return

    data_json = json.dumps(data, sort_keys=True)

    sha256_hash = hashlib.sha256()
    sha256_hash.update(data_json.encode("utf-8"))
    hashed_data = sha256_hash.hexdigest()

    return hashed_data

def populate_db(data, db_name, db_table_name):
    cursor, conn = connect_to_database(db_name)

    cursor.execute(f"SELECT COUNT(*) FROM {db_table_name}")
    row_count = cursor.fetchone()[0]

    if row_count == 0:
        for item in data:
            keys = item.keys()
            table_strings = ""
            param_placeholders = ""
            data_to_insert = ()

            for key in keys:
                table_strings += f"{key}, "
                param_placeholders += "?, "
                data_to_insert += (item[key],)

            table_strings += f"hash, "
            param_placeholders += "?, "



            data_to_insert += (hashed_data,)

            table_strings = table_strings.rstrip(", ")
            param_placeholders = param_placeholders.rstrip(", ")

            print(f"INSERT INTO {db_table_name} ({table_strings}) VALUES ({param_placeholders})", data_to_insert)
            cursor.execute(f"INSERT INTO {db_table_name} ({table_strings}) VALUES ({param_placeholders})", data_to_insert)
    else:
        print("Database is already populated")

    conn.commit()
    conn.close()


#create_db_and_table(data, "buff_data", "skins")

#populate_db(data, "buff_data", "skins")

hashe = create_hash({
        "sticker_name": "Natus Vincere (Holo) | DreamHack 2014",
        "item_name": "M4A1-S | Bright Water (Minimal Wear)",
        "market_price": 203
    }, [0, 1])

print(hashe)
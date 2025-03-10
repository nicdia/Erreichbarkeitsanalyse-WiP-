from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError


def add_column_based_on_table_name(db_con):
    """
    Fügt eine Spalte 'source' mit dem passenden Wert ('metaver', 'osm', 'gmaps') 
    zu allen Tabellen hinzu, die 'meta', 'osm' oder 'gmaps' im Namen enthalten.
    
    Parameters:
    db_con (sqlalchemy.engine.Engine): Datenbankverbindung
    """
    try:
        with db_con.connect() as conn:
            with conn.begin():
                inspector = inspect(db_con)
                schemas = inspector.get_schema_names()
                
                for schema in schemas:
                    tables = inspector.get_table_names(schema=schema)
                    
                    for table in tables:
                        if "meta" in table:
                            new_column_value = "metaver" + {table}
                        elif "osm" in table:
                            new_column_value = "osm" + {table}
                        elif "gmaps" in table:
                            new_column_value = "gmaps" + {table}
                        else:
                            continue  
                        
                        # Prüfen, ob die Spalte bereits existiert
                        columns = [col["name"] for col in inspector.get_columns(table, schema=schema)]
                        if "source" not in columns:
                            alter_query = f'ALTER TABLE "{schema}"."{table}" ADD COLUMN source TEXT;'
                            conn.execute(text(alter_query))
                            print(f"Spalte 'source' zur Tabelle '{schema}.{table}' hinzugefügt.")
                        
                        update_query = f'UPDATE "{schema}"."{table}" SET source = :value;'
                        conn.execute(text(update_query), {"value": new_column_value})
                        print(f"Spalte 'source' in Tabelle '{schema}.{table}' mit Wert '{new_column_value}' aktualisiert.")
    
    except SQLAlchemyError as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


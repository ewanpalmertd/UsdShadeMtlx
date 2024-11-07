from xml_parser import MTLX_DICTIONARY
import sqlite3 as sqlite

connection = sqlite.connect("materialx.db")
print(connection.total_changes)
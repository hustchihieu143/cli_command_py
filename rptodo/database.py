"""This module provides the RP To-Do database functionality."""
# rptodo/database.py

import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from rptodo import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS

class DBResponse(NamedTuple):
    todo_list: List[Dict[str, Any]]
    error: int

class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_todos(self) -> DBResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError:  # Catch wrong JSON format
                    return DBResponse([], JSON_ERROR)
        except OSError:  # Catch file IO problems
            return DBResponse([], DB_READ_ERROR)
    
    def delete_all(self) -> None:
        try:
            with self._db_path.open("r+") as db: 
                try: 
                    db.seek(0)
                    db.truncate()
                    db.write("[]")
                    return DBResponse([], SUCCESS)
                except json.JSONDecodeError:  # Catch wrong JSON format
                    return DBResponse([], JSON_ERROR)  
        except OSError:  # Catch file IO problems
            return DBResponse([], DB_READ_ERROR)
    
    
    def write_todos(self, todo_list: List[Dict[str, Any]]) -> DBResponse:
        try:
            with self._db_path.open("w") as db:
                json.dump(todo_list, db, indent=4)
            return DBResponse(todo_list, SUCCESS)
        except OSError:  # Catch file IO problems
            return DBResponse(todo_list, DB_WRITE_ERROR)    
    
    def delete_by_uuid(self, uuid) -> None:
        try:
            with self._db_path.open("r+") as db:
                try:
                    old_data = json.load(db)
                    print("old_data: ",old_data)
                    check_exists = True
                    index = -1
                    rs = []
                    
                    for i in range(0, len(old_data)):
                        if old_data[i]["uuid"] == uuid:
                            check_exists = True
                            index = i
                            break
                        
                    if(check_exists == True and index >= 0):
                        db.seek(0)
                        db.truncate()
                        del old_data[index]
                        print("old_data: ",old_data)
                        # for i in len(old_data):
                        #   rs.append(i)
                        #   write_todos(self, rs)
                        
                        
                    return DBResponse([], SUCCESS) 
                except json.JSONDecodeError:  # Catch wrong JSON format
                    return DBResponse([], JSON_ERROR) 
        except OSError:  # Catch file IO problems
            return DBResponse([], DB_READ_ERROR)   

    

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_todo.json"
)

def get_database_path(config_file: Path) -> Path:
    """Return the current path to the to-do database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

def init_database(db_path: Path) -> int:
    """Create the to-do database."""
    try:
        db_path.write_text("[]")  # Empty to-do list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR
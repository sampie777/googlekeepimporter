import sqlite3
from typing import Optional, List

from db_objects import DbNote
from secrets import SECRET_DB_PATH

DB_TABLE_NOTES = "comhuaweiproviderNotePadbackupnote_items_new_tb"
DB_TABLE_TAGS = "comhuaweiproviderNotePadbackuptag_items_tb"
DB_TABLE_TASKS = "comhuaweiproviderNotePadbackuptask_items_tb"


class DbState:
    is_connected = False
    connection: Optional[sqlite3.Connection] = None


def db_init(state: DbState):
    db_connect(state)


def db_connect(state: DbState):
    if state.is_connected:
        return

    connection = sqlite3.connect(SECRET_DB_PATH)
    state.connection = connection


def db_get_cursor(state: DbState):
    return state.connection.cursor()


def db_get_all_notes(state: DbState) -> List[DbNote]:
    def db_row_to_note(row: tuple):
        return DbNote(*row)

    cursor = db_get_cursor(state)
    result = cursor.execute("select {0}.*, {1}.name as 'tag_name' from {0} "
                            "left join {1} on {0}.tag_id={1}.uuid "
                            "where {0}.prefix_uuid not in (select {2}.notes_id from {2})"
                            .format(DB_TABLE_NOTES, DB_TABLE_TAGS, DB_TABLE_TASKS))
    return list(map(db_row_to_note, result))

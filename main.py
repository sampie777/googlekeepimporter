from typing import Optional, List

import gkeepapi

from db import DbState, db_init, db_get_all_notes
from db_objects import DbNote
from gkeep import GkeepState, gkeep_connect, gkeep_get_or_create_label, gkeep_sync, gkeep_create_note, gkeep_notes
from secrets import SECRET_USERNAME, SECRET_PASSWORD


def create_note(gkeep_state: GkeepState, db_note: DbNote, label: Optional[gkeepapi.node.Label]):
    note = gkeep_create_note(gkeep_state, text=db_note.title)
    if label is not None:
        note.labels.add(label)
    print("    Note created: {}".format(note.text[:32]))


def create_notes(gkeep_state: GkeepState, db_notes: List[DbNote]):
    print("Parsing notes...")
    for note in db_notes:
        label: Optional[gkeepapi.node.Label] = None
        if note.tag_name is not None and len(note.tag_name) > 0:
            label = gkeep_get_or_create_label(gkeep_state, note.tag_name)

        create_note(gkeep_state, note, label)


def double_check(gkeep_state: GkeepState, db_notes: List[DbNote]):
    print("Double checking...")
    for note in db_notes:
        try:
            next(it for it in gkeep_notes(gkeep_state) if it.text == note.title)
        except StopIteration:
            print("Note not uploaded: {}".format(note.title))


def main():
    db_state = DbState()
    gkeep_state = GkeepState()

    db_init(db_state)
    db_notes = db_get_all_notes(db_state)

    gkeep_connect(gkeep_state, SECRET_USERNAME, SECRET_PASSWORD)
    create_notes(gkeep_state, db_notes)
    gkeep_sync(gkeep_state)

    double_check(gkeep_state, db_notes)

    print("Done.")


if __name__ == "__main__":
    main()

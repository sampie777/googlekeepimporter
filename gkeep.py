from typing import Optional, List

import gkeepapi
from gkeepapi.exception import LabelException


class GkeepState:
    is_connected = False
    keep: Optional[gkeepapi.Keep] = None
    username: Optional[str] = None


def gkeep_connect(state: GkeepState, username: str, password: str):
    state.keep = gkeepapi.Keep()
    print("Logging in...")
    state.is_connected = state.keep.login(username, password)
    if not state.is_connected:
        raise Exception("Could not log in to Google Keep")


def gkeep_get_or_create_label(state: GkeepState, title: str) -> Optional[gkeepapi.node.Label]:
    if len(title) == 0:
        return

    if title.startswith("sys-def-"):
        title = title.replace("sys-def-", "")

    title = title[0].upper() + title[1:]

    try:
        label = state.keep.findLabel(title, create=True)
        print("  Label created: {}".format(title))
        return label
    except LabelException:
        pass
    return None


def gkeep_sync(state: GkeepState):
    print("Syncing...")
    state.keep.sync()


def gkeep_create_note(state: GkeepState, title: Optional[str] = None, text: Optional[str] = None) -> gkeepapi.node.Note:
    return state.keep.createNote(title=title, text=text)


def gkeep_notes(state: GkeepState) -> List[gkeepapi.node.Note]:
    return state.keep.all()

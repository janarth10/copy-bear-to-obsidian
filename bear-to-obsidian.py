import datetime
from markdownify import markdownify
import sqlite3

BEAR_DB_PATH = '/Users/newdev/Library/Group Containers/9K33E3U3T4.net.shinyfrog.bear/Application Data/database.sqlite'
OBSIDIAN_DIR = '/Users/newdev/Google Drive/Folders/obsidian-vaults/janarth-vault/copied-from-bear'

class Note(object):
    def __init__(self, db, note_id):
        self.db = db
        self.note_data = self.db.execute("SELECT * FROM ZSFNOTE WHERE Z_PK=?",
                                    (note_id,)).fetchone()

    def title(self):
        return self.note_data["ZTITLE"]

    def text(self):
        return self.note_data["ZTEXT"]

    def last_modified(self):
        return datetime.datetime.fromtimestamp(
            self.note_data["ZMODIFICATIONDATE"] + apple_epoch)

class BearDb(object):

    def __init__(self):
        self.db = sqlite3.connect("file:%s?mode=ro" % BEAR_DB_PATH, uri=True)
        self.db.row_factory = sqlite3.Row

    def all_notes(self):
        ids = self.db.execute(
            "SELECT Z_PK FROM ZSFNOTE WHERE ZTRASHED != 1").fetchall()
        notes = [Note(self.db, i["Z_PK"]) for i in ids]
        return notes


print(f"Last ran { datetime.datetime.now().strftime('%c') }")
bear_db = BearDb()
notes = bear_db.all_notes()

# copy notes to Obsidian if it contains '#copy-to-obsidian'
for note in notes:
    if '#copy-to-obsidian' in note.text():
        with open(f"{OBSIDIAN_DIR}/{note.title()}.md", 'w') as obsidian_file:
            obsidian_file.write(
                markdownify(
                    note.text(),
                    heading_style='ATX',
                )
            )

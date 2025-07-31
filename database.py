from pony.orm import Database, Required, db_session

db = Database()
db.bind(provider='sqlite', filename=r'C:\Users\karinate-iyabi\Documents\videos.db', create_db=False)

class Video(db.Entity):
    _table_ = "video"
    name = Required(str)
    category = Required(str)
    description = Required(str)
    url = Required(str)
    thumbnail = Required(str)
db.generate_mapping(create_tables=False)

with db_session:
    videos = Video.select()
    for video in videos:
        print(video.name)

import os
from Model.database import Database

class ComicModel:
    def __init__(self):
        self.db = Database()

    def get_comics(self):
        return self.db.fetchall("SELECT id, tieu_de, chuyen_muc, duong_dan FROM comic")

    def get_comic_details(self, comic_id):
        comic = self.db.fetchone("SELECT tieu_de, duong_dan, chuyen_muc FROM comic WHERE id = ?", (comic_id,))
        category_name = self.db.fetchone("SELECT ten_chuyen_muc FROM category WHERE id = ?", (comic[2],))[0]
        return comic, category_name

    def get_chapter_images(self, comic_id, chapter_id):
        duong_dan_anh = self.db.fetchone("SELECT duong_dan FROM comic WHERE id = ?", (comic_id,))[0]
        chapter_dir = os.path.join(duong_dan_anh, chapter_id)
        image_files = sorted([f for f in os.listdir(chapter_dir) if f.endswith(('.jpg', '.png'))])
        return [os.path.join(chapter_dir, f) for f in image_files]
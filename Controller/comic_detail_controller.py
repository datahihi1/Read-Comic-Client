from Model.comic_model import ComicModel
import os

class ComicDetailController:
    def __init__(self, view):
        self.view = view
        self.view.controller = self
        self.model = ComicModel()

    def display_comic_details(self, comic_id):
        comic, category_name = self.model.get_comic_details(comic_id)
        self.view.display_comic_details(comic_id, comic, category_name)

    def add_chapters(self, comic_id, duong_dan_anh):
        chapter_ids = []
        if os.path.exists(duong_dan_anh):
            chapter_ids = [d for d in os.listdir(duong_dan_anh) if os.path.isdir(os.path.join(duong_dan_anh, d))]
        self.view.display_chapters(comic_id, sorted(chapter_ids))

    def show_chapter(self, comic_id, chapter_id):
        self.view.app.root.transition.direction = 'left'
        self.view.app.root.current = 'chapter_view'
        chapter_view_screen = self.view.app.root.get_screen('chapter_view').children[0]
        chapter_view_screen.controller.display_chapter(comic_id, chapter_id)

    def go_back(self):
        self.view.app.root.transition.direction = 'right'
        self.view.app.root.current = 'home'

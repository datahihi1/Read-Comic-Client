from Model.comic_model import ComicModel

class ChapterViewController:
    def __init__(self, view):
        self.view = view
        self.view.controller = self
        self.model = ComicModel()

    def display_chapter(self, comic_id, chapter_id):
        images = self.model.get_chapter_images(comic_id, chapter_id)
        self.view.display_chapter(images)

    def go_back(self):
        self.view.app.root.transition.direction = 'right'
        self.view.app.root.current = 'comic_detail'

from Model.comic_model import ComicModel

class HomeController:
    def __init__(self, view):
        self.view = view
        self.view.controller = self
        self.model = ComicModel()

    def show_comics(self):
        comics = self.model.get_comics()
        self.view.display_comics(comics)

    def show_comic_detail(self, comic_id):
        self.view.app.root.transition.direction = 'left'
        self.view.app.root.current = 'comic_detail'
        comic_detail_screen = self.view.app.root.get_screen('comic_detail').children[0]
        comic_detail_screen.controller.display_comic_details(comic_id)

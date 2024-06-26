from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen

from View.home_screen import HomeScreen
from View.comic_detail_screen import ComicDetailScreen
from View.chapter_view_screen import ChapterViewScreen
from Controller.home_controller import HomeController
from Controller.comic_detail_controller import ComicDetailController
from Controller.chapter_view_controller import ChapterViewController

class MyApp(MDApp):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)

    def build(self):
        sm = ScreenManager()
        self.add_screen(sm, 'home', HomeScreen, HomeController)
        self.add_screen(sm, 'comic_detail', ComicDetailScreen, ComicDetailController)
        self.add_screen(sm, 'chapter_view', ChapterViewScreen, ChapterViewController)
        return sm

    def add_screen(self, screen_manager, name, screen_class, controller_class):
        screen = Screen(name=name)
        view_instance = screen_class(app=self)
        controller_instance = controller_class(view_instance)
        screen.add_widget(view_instance)
        screen_manager.add_widget(screen)

if __name__ == '__main__':
    MyApp().run()

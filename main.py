import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

# Import các class từ các tệp riêng
from View.home_screen import HomeScreen
from View.comic_detail_screen import ComicDetailScreen
from View.chapter_view_screen import ChapterViewScreen

class MyApp(App):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)

    def build(self):
        sm = ScreenManager()
        self.add_screen(sm, 'home', HomeScreen)
        self.add_screen(sm, 'comic_detail', ComicDetailScreen)
        self.add_screen(sm, 'chapter_view', ChapterViewScreen)
        return sm
    
    def add_screen(self, screen_manager, name, screen_class):
        screen = Screen(name=name)
        screen.add_widget(screen_class(app=self))
        screen_manager.add_widget(screen)

if __name__ == '__main__':
    MyApp().run()

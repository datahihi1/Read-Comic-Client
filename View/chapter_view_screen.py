from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivy.core.window import Window

class ChapterViewScreen(MDFloatLayout):
    def __init__(self, app, **kwargs):
        super(ChapterViewScreen, self).__init__(**kwargs)
        self.app = app
        self.controller = None
        self.create_ui()

    def create_ui(self):
        self.action_bar = MDTopAppBar(title='Chi tiết nội dung', pos_hint={'top': 1}, elevation=10)
        self.action_bar.left_action_items = [['arrow-left', lambda x: self.controller.go_back()]]
        self.add_widget(self.action_bar)

        self.scrollview = MDScrollView(size_hint=(1, None), size=(Window.width, Window.height - self.action_bar.height))
        self.content = MDBoxLayout(orientation='vertical', size_hint_y=None)
        self.scrollview.add_widget(self.content)
        self.add_widget(self.scrollview)

    def display_chapter(self, images):
        self.content.clear_widgets()
        for img_path in images:
            chapter_image = Image(source=img_path, allow_stretch=True, keep_ratio=True, size_hint_x=1)
            chapter_image.size_hint_y = None
            chapter_image.height = Window.height - self.action_bar.height
            self.content.add_widget(chapter_image)

        self.content.height = len(images) * (Window.height - self.action_bar.height)

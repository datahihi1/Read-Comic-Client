import os
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivy.core.window import Window
from kivy.uix.image import Image

class ComicDetailScreen(MDFloatLayout):
    def __init__(self, app, **kwargs):
        super(ComicDetailScreen, self).__init__(**kwargs)
        self.app = app
        self.controller = None
        self.create_ui()

    def create_ui(self):
        action_bar = MDTopAppBar(title='Chi tiết truyện', pos_hint={'top': 1}, elevation=10)
        action_bar.left_action_items = [['arrow-left', lambda x: self.controller.go_back()]]
        self.add_widget(action_bar)

        self.content = MDBoxLayout(orientation='vertical', padding=10, size_hint_y=None)
        self.scrollview = MDScrollView(size_hint=(1, None), size=(Window.width, Window.height - action_bar.height))
        self.scrollview.add_widget(self.content)
        self.add_widget(self.scrollview)

    def display_comic_details(self, comic_id, comic, category_name):
        self.content.clear_widgets()
        tieu_de, duong_dan_anh, chuyen_muc_id = comic

        self.content.add_widget(MDLabel(text=tieu_de, font_style='H4', size_hint_y=None, height=50))

        img_path = os.path.join(duong_dan_anh, 'title.png')
        if os.path.exists(img_path):
            comic_image = Image(source=img_path, size_hint=(None, None), size=(Window.width * 0.8, Window.width * 0.8))
            comic_image_layout = MDBoxLayout(size_hint_y=None, height=comic_image.height)
            comic_image_layout.add_widget(comic_image)
            self.content.add_widget(comic_image_layout)

        self.content.add_widget(MDLabel(text=f"Chuyên mục: {category_name}", font_style='Subtitle1', size_hint_y=None, height=30, halign='left'))

        self.controller.add_chapters(comic_id, duong_dan_anh)

    def display_chapters(self, comic_id, chapter_ids):
        for chapter_id in chapter_ids:
            chapter_button = MDRaisedButton(text=f'{chapter_id}', size_hint_y=None, height=44)
            chapter_button.bind(on_release=lambda instance, comic_id=comic_id, chapter_id=chapter_id: self.controller.show_chapter(comic_id, chapter_id))
            self.content.add_widget(chapter_button)

        self.content.height = len(chapter_ids) * 44 + 70

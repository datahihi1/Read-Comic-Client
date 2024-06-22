# comic_detail_screen.py
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.actionbar import ActionBar, ActionView, ActionPrevious
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.image import Image
import sqlite3
import os

class ComicDetailScreen(FloatLayout):
    def __init__(self, app, **kwargs):
        super(ComicDetailScreen, self).__init__(**kwargs)
        self.app = app
        self.create_ui()

    def create_ui(self):
        action_bar = ActionBar(pos_hint={'top': 1})
        action_view = ActionView()
        action_previous = ActionPrevious(title='Chi tiết truyện', with_previous=True)
        action_previous.bind(on_press=self.go_back)
        action_view.add_widget(action_previous)
        action_bar.add_widget(action_view)
        self.add_widget(action_bar)

        self.content = BoxLayout(orientation='vertical', padding=10, size_hint_y=None)
        self.scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height - action_bar.height))
        self.scrollview.add_widget(self.content)
        self.add_widget(self.scrollview)

    def display_comic_details(self, comic_id):
        self.content.clear_widgets()

        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT tieu_de, duong_dan, chuyen_muc FROM comic WHERE id = ?", (comic_id,))
            comic = cursor.fetchone()
            if not comic:
                return
            comic_title, duong_dan_anh, chuyen_muc_id = comic

            cursor.execute("SELECT ten_chuyen_muc FROM category WHERE id = ?", (chuyen_muc_id,))
            ten_chuyen_muc = cursor.fetchone()[0]

        self.content.add_widget(Label(text=comic_title, font_size='20sp', size_hint_y=None, height=50))

        img_path = os.path.join(duong_dan_anh, 'title.png')
        if os.path.exists(img_path):
            comic_image = Image(source=img_path, size_hint=(None, None), size=(Window.width * 0.8, Window.width * 0.8))
            comic_image_layout = BoxLayout(size_hint_y=None, height=comic_image.height)
            comic_image_layout.add_widget(comic_image)
            self.content.add_widget(comic_image_layout)

        self.content.add_widget(Label(text=f"Chuyên mục: {ten_chuyen_muc}", font_size='14sp', size_hint_y=None, height=30, halign='left'))

        self.add_chapters(comic_id, duong_dan_anh)

    def add_chapters(self, comic_id, duong_dan_anh):
        chapter_ids = []
        chapter_dir = duong_dan_anh
        if os.path.exists(chapter_dir):
            chapter_ids = [d for d in os.listdir(chapter_dir) if os.path.isdir(os.path.join(chapter_dir, d))]

        for chapter_id in sorted(chapter_ids):
            chapter_button = Button(text=f'{chapter_id}', size_hint_y=None, height=44)
            chapter_button.bind(on_release=lambda instance, chapter_id=chapter_id: self.show_chapter(comic_id, chapter_id))
            self.content.add_widget(chapter_button)

        self.content.height = len(chapter_ids) * 44 + 70

    def show_chapter(self, comic_id, chapter_id):
        self.app.root.transition = SlideTransition(direction='left')
        self.app.root.current = 'chapter_view'
        chapter_view_screen = self.app.root.get_screen('chapter_view').children[0]
        chapter_view_screen.display_chapter(comic_id, chapter_id)

    def go_back(self, instance):
        self.app.root.transition = SlideTransition(direction='right')
        self.app.root.current = 'home'

# chapter_view_screen.py
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.actionbar import ActionBar, ActionView, ActionPrevious
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.screenmanager import SlideTransition
import sqlite3
import os

class ChapterViewScreen(FloatLayout):
    def __init__(self, app, **kwargs):
        super(ChapterViewScreen, self).__init__(**kwargs)
        self.app = app
        self.create_ui()

    def create_ui(self):
        self.action_bar = ActionBar(pos_hint={'top': 1})
        action_view = ActionView()
        action_previous = ActionPrevious(title='Chi tiết nội dung', with_previous=True)
        action_previous.bind(on_press=self.go_back)
        action_view.add_widget(action_previous)
        self.action_bar.add_widget(action_view)
        self.add_widget(self.action_bar)

        self.scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height - self.action_bar.height))
        self.content = BoxLayout(orientation='vertical', size_hint_y=None)
        self.scrollview.add_widget(self.content)
        self.add_widget(self.scrollview)

    def display_chapter(self, comic_id, chapter_id):
        self.content.clear_widgets()

        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT duong_dan FROM comic WHERE id = ?", (comic_id,))
            duong_dan_anh = cursor.fetchone()[0]

        chapter_dir = os.path.join(duong_dan_anh, chapter_id)

        # Hàm key để trích xuất số và sắp xếp
        def sort_key(filename):
            name, ext = os.path.splitext(filename)
            try:
                return int(name)
            except ValueError:
                return name

        image_files = [f for f in sorted(os.listdir(chapter_dir), key=sort_key) if f.endswith(('.jpg', '.png'))]

        for image_file in image_files:
            img_path = os.path.join(chapter_dir, image_file)
            if os.path.exists(img_path):
                chapter_image = Image(source=img_path, allow_stretch=True, keep_ratio=True)
                chapter_image.size_hint_y = None
                chapter_image.height = Window.height - self.action_bar.height
                self.content.add_widget(chapter_image)

        self.content.height = len(image_files) * (Window.height - self.action_bar.height)

    def go_back(self, instance):
        self.app.root.transition = SlideTransition(direction='right')
        self.app.root.current = 'comic_detail'

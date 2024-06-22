# home_screen.py
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.actionbar import ActionBar, ActionView, ActionPrevious, ActionButton
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import SlideTransition
import sqlite3
import os

class HomeScreen(FloatLayout):
    def __init__(self, app, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.app = app
        self.create_ui()

    def create_ui(self):
        action_bar_height = Window.height * (3 / 30)
        box_layout_height = Window.height * (27 / 30)

        action_bar = ActionBar(pos_hint={'top': 1}, size_hint=(1, None), height=action_bar_height)
        action_view = ActionView()
        action_previous = ActionPrevious(title='Trang chủ', with_previous=False)
        action_view.add_widget(action_previous)

        dropdown = DropDown()
        btn_show_list = Button(text='Hiển thị bài viết', size_hint_y=None, height=44)
        btn_show_list.bind(on_release=self.show_comics)
        dropdown.add_widget(btn_show_list)

        mainbutton = ActionButton(text='Menu')
        mainbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

        action_view.add_widget(mainbutton)
        action_bar.add_widget(action_view)

        self.add_widget(action_bar)

        self.content = BoxLayout(orientation='vertical', padding=1, size_hint=(1, None), height=box_layout_height)
        self.scrollview = ScrollView(size_hint=(1, None), size=(Window.width, box_layout_height))
        self.scrollview.add_widget(self.content)
        self.add_widget(self.scrollview)

    def show_comics(self, instance):
        self.content.clear_widgets()

        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, tieu_de, chuyen_muc, duong_dan FROM comic")
            comics = cursor.fetchall()

        for comic in comics:
            self.add_comic(comic)

        self.content.height = len(comics) * 150 + 10

    def add_comic(self, comic):
        comic_id, tieu_de, ten_chuyen_muc, duong_dan_anh = comic
        comic_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=150)

        img_path = os.path.join(duong_dan_anh, 'title.png')
        comic_image = Image(source=img_path if os.path.exists(img_path) else 'img/default.png', size_hint_x=0.3)

        comic_info = BoxLayout(orientation='vertical', padding=5, size_hint_x=0.7)
        comic_info.add_widget(Label(text=tieu_de, font_size='18sp', halign='left'))
        comic_info.add_widget(Label(text=f"Chuyên mục: {ten_chuyen_muc}", font_size='14sp', halign='left'))

        comic_layout.add_widget(comic_info)
        comic_layout.add_widget(comic_image)

        comic_button = Button(text='Chi tiết', size_hint_x=0.2)
        comic_button.bind(on_release=lambda instance, comic_id=comic_id: self.show_comic_detail(comic_id))
        comic_layout.add_widget(comic_button)

        self.content.add_widget(comic_layout)

    def show_comic_detail(self, comic_id):
        self.app.root.transition = SlideTransition(direction='left')
        self.app.root.current = 'comic_detail'
        comic_detail_screen = self.app.root.get_screen('comic_detail').children[0]
        comic_detail_screen.display_comic_details(comic_id)

from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivy.core.window import Window
from kivy.uix.image import Image
import os

class HomeScreen(MDFloatLayout):
    def __init__(self, app, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.app = app
        self.controller = None
        self.create_ui()

    def create_ui(self):
        action_bar = MDTopAppBar(title='Trang chủ', pos_hint={'top': 1}, elevation=10)
        action_bar.right_action_items = [['menu', lambda x: self.dropdown.open()]]
        self.add_widget(action_bar)

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Hiển thị bài viết",
                "on_release": lambda x="Hiển thị bài viết": self.controller.show_comics(),
            },
        ]
        self.dropdown = MDDropdownMenu(
            caller=action_bar,
            items=menu_items,
            width_mult=4,
        )

        self.content = MDBoxLayout(orientation='vertical', padding=1, size_hint=(1, None), height=Window.height * (27 / 30))
        self.scrollview = MDScrollView(size_hint=(1, None), size=(Window.width, Window.height * (27 / 30)))
        self.scrollview.add_widget(self.content)
        self.add_widget(self.scrollview)

    def display_comics(self, comics):
        self.content.clear_widgets()
        self.dropdown.dismiss()
        for comic in comics:
            self.add_comic(comic)

        self.content.height = len(comics) * 150 + 10

    def add_comic(self, comic):
        comic_id, tieu_de, ten_chuyen_muc, duong_dan_anh = comic
        comic_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=150)

        img_path = os.path.join(duong_dan_anh, 'title.png')
        comic_image = Image(source=img_path if os.path.exists(img_path) else 'img/default.png', size_hint_x=0.3)

        comic_info = MDBoxLayout(orientation='vertical', padding=5, size_hint_x=0.7)
        comic_info.add_widget(MDLabel(text=tieu_de, font_style='H6', halign='left'))
        comic_info.add_widget(MDLabel(text=f"Chuyên mục: {ten_chuyen_muc}", font_style='Subtitle1', halign='left'))

        comic_layout.add_widget(comic_info)
        comic_layout.add_widget(comic_image)

        comic_button = MDRaisedButton(text='Chi tiết', size_hint_x=0.2)
        comic_button.bind(on_release=lambda instance, comic_id=comic_id: self.controller.show_comic_detail(comic_id))
        comic_layout.add_widget(comic_button)

        self.content.add_widget(comic_layout)

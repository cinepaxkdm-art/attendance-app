from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.boxlayout import MDBoxLayout
import requests

class AttendanceApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        screen = MDScreen()

        layout = MDBoxLayout(orientation='vertical')

        # Top Bar
        toolbar = MDTopAppBar(title="MOS Cinepax Live Duty Tracker")
        layout.add_widget(toolbar)

        # Scroll View for List
        scroll = MDScrollView()
        self.list_container = MDList()
        scroll.add_widget(self.list_container)
        layout.add_widget(scroll)

        # Refresh Button
        btn = MDRaisedButton(
            text="🔄 REFRESH LIVE DUTY",
            pos_hint={'center_x': 0.5},
            size_hint=(0.9, None),
            on_release=self.fetch_duty_status
        )
        layout.add_widget(btn)

        screen.add_widget(layout)
        return screen

    def on_start(self):
        self.fetch_duty_status(None)

    def fetch_duty_status(self, instance):
        self.list_container.clear_widgets()
        FIREBASE_URL = "https://mos-attendance-default-rtdb.firebaseio.com/attendance.json"

        try:
            res = requests.get(FIREBASE_URL)
            data = res.json()

            if not data:
                self.list_container.add_widget(OneLineListItem(text="Aaj koi active attendance nahi hai."))
                return

            for emp_id, info in data.items():
                item_text = f"Emp ID: {emp_id} | In Time: {info.get('time')} | ON DUTY"
                self.list_container.add_widget(OneLineListItem(text=item_text))

        except Exception as e:
            self.list_container.add_widget(OneLineListItem(text="Network Error! Internet Check Karein."))

if __name__ == "__main__":
    AttendanceApp().run()


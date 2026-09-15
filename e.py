# ==========================================
# 1. DEPENDENCIES INSTALL KARNA
# ==========================================
!sudo apt update
!sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libffi-dev libssl-dev
!pip install --upgrade buildozer cython==0.29.33

# ==========================================
# 2. CALCULATOR APP CODE (main.py)
# ==========================================
code = '''
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class CalculatorApp(App):
    def build(self):
        self.operators = ['/', '*', '+', '-']
        self.last_was_operator = None
        
        main_layout = BoxLayout(orientation="vertical")
        self.solution = TextInput(
            multiline=False, readonly=True, halign="right", font_size=55
        )
        main_layout.add_widget(self.solution)
        
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            [".", "0", "C", "+"],
        ]
        
        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(
                    text=label, pos_hint={"center_x": 0.5, "center_y": 0.5}
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)
            
        equals_button = Button(
            text="=", pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        equals_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equals_button)
        
        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text
        
        if button_text == 'C':
            self.solution.text = ""
        else:
            if current and (self.last_was_operator and button_text in self.operators):
                return
            elif current == "" and button_text in self.operators:
                return
            else:
                self.solution.text += button_text
        self.last_was_operator = (button_text in self.operators)

    def on_solution(self, instance):
        text = self.solution.text
        if text:
            try:
                self.solution.text = str(eval(self.solution.text))
            except Exception:
                self.solution.text = "Error"

if __name__ == "__main__":
    CalculatorApp().run()
'''

with open('main.py', 'w') as f:
    f.write(code)

# ==========================================
# 3. BUILDOZER SPEC CONFIGURATION
# ==========================================
!buildozer init

# Spec file ko modify karna
with open('buildozer.spec', 'r') as file:
    spec = file.read()

spec = spec.replace('title = My Application', 'title = Python Calculator')
spec = spec.replace('package.name = myapp', 'package.name = mycalculator')
spec = spec.replace('requirements = python3,kivy', 'requirements = python3,kivy')

with open('buildozer.spec', 'w') as file:
    file.write(spec)

# ==========================================
# 4. APK BUILD KARNA & DOWNLOAD KARNA
# ==========================================
!buildozer -v android debug

# APK File Auto Download
from google.colab import files
import glob

apk_files = glob.glob('bin/*.apk')
if apk_files:
    print(f"Downloading: {apk_files[0]}")
    files.download(apk_files[0])
else:
    print("APK Build Nahi ho saki.")

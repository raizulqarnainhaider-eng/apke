from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class CalculatorApp(App):

  def build(self):
    self.expression = ""
    layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

    # Result Screen (Display)
    self.result = TextInput(
        font_size=32, readonly=True, halign="right", multiline=False
    )
    layout.add_widget(self.result)

    # Buttons layout
    buttons = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["C", "0", "=", "+"],
    ]

    for row in buttons:
      h_layout = BoxLayout(spacing=10)
      for label in row:
        button = Button(text=label, font_size=24)
        button.bind(on_press=self.on_button_press)
        h_layout.add_widget(button)
      layout.add_widget(h_layout)

    return layout

  def on_button_press(self, instance):
    text = instance.text
    if text == "C":
      self.expression = ""
      self.result.text = ""
    elif text == "=":
      try:
        self.expression = str(eval(self.expression))
        self.result.text = self.expression
      except Exception:
        self.result.text = "Error"
        self.expression = ""
    else:
      self.expression += text
      self.result.text = self.expression


if __name__ == "__main__":
  CalculatorApp().run()

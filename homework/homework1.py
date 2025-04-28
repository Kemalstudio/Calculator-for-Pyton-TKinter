import tkinter as tk
from tkinter import ttk, messagebox
import math

class AdvancedCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор")

        self.style = ttk.Style(root)
        self.style.theme_use('clam')

        self.expression = ""
        self.history = []
        self.buttons_map = {}
        self.extended = False

        self.display = ttk.Entry(root, font=('Arial', 18), justify='right', state='readonly')
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='ew')
        self.update_display()

        self.history_label = ttk.Label(root, text="История:")
        self.history_label = ttk.Label(root, text="Esc - очищает поля для ввода")
        self.history_label.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky='w')
        self.history_list = tk.Listbox(root, height=5)
        self.history_list.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')

        self.copy_result_button = ttk.Button(root, text="Копировать пример", command=self.copy_result_to_clipboard)
        self.copy_result_button.grid(row=2, column=2, padx=5, pady=5, sticky='nw')

        self.copy_expression_button = ttk.Button(root, text="Копировать ответ", command=self.copy_expression_to_clipboard)
        self.copy_expression_button.grid(row=2, column=3, padx=5, pady=5, sticky='ne')

        self.clear_history_button = ttk.Button(root, text="Очистить историю", command=self.clear_history)
        self.clear_history_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky='ew')
        self.clear_history_button.grid_remove()

        self.extend_button = ttk.Button(root, text="Развернуть", command=self.toggle_extended)
        self.extend_button.grid(row=3, column=2, columnspan=2, padx=10, pady=5, sticky='ew')

        buttons_data = [
            ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('/', 4, 3),
            ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('*', 5, 3),
            ('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('-', 6, 3),
            ('0', 7, 0), ('.', 7, 1), ('=', 7, 2), ('+', 7, 3),
            ('C', 8, 0), ('Del', 8, 1), ('(', 8, 2), (')', 8, 3)
        ]

        self.grid_buttons(buttons_data)
        self.configure_grid_weights()
        self.bind_keys()
        self.active_button = None
        self.update_clear_history_button_visibility()

        self.extended_buttons = []
        self.create_extended_buttons()
        self.hide_extended_buttons()

        root.focus_set()

    def grid_buttons(self, buttons_data):
        for (text, row, col) in buttons_data:
            command = lambda t=text: self.button_click(t)
            button = ttk.Button(self.root, text=text, command=command)
            button.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            self.buttons_map[text] = button

    def configure_grid_weights(self):
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(9):
            self.root.grid_rowconfigure(i, weight=1)

    def bind_keys(self):
        self.root.bind('<Key>', self.handle_keyboard_input)
        self.root.bind('<Return>', lambda event: self.button_click('='))

    def create_extended_buttons(self):
        extended_buttons_data = [
            ('%', 4, 4), ('sin', 5, 4), ('√', 6, 4), ('π', 7, 4),
            ('x²', 4, 5), ('cos', 5, 5), ('x³', 6, 5), ('tan', 7, 5)
        ]
        for (text, row, col) in extended_buttons_data:
            command = lambda t=text: self.extended_button_click(t)
            button = ttk.Button(self.root, text=text, command=command)
            button.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            self.extended_buttons.append(button)
            self.buttons_map[text] = button
            self.root.grid_columnconfigure(col, weight=1)
        for i in range(4, 8):
            self.root.grid_rowconfigure(i, weight=1)

    def show_extended_buttons(self):
        for button in self.extended_buttons:
            button.grid()
        self.root.geometry("") # Reset window size to accommodate new buttons
        self.extend_button.config(text="Свернуть")
        self.extended = True

    def hide_extended_buttons(self):
        for button in self.extended_buttons:
            button.grid_remove()
        self.root.geometry("") # Reset window size
        self.extend_button.config(text="Развернуть")
        self.extended = False

    def toggle_extended(self):
        if self.extended:
            self.hide_extended_buttons()
        else:
            self.show_extended_buttons()

    def highlight_button(self, text):
        if text in self.buttons_map:
            button = self.buttons_map[text]
            self.active_button = button
            button.state(['pressed'])
            self.root.after(100, self.unhighlight_button)

    def unhighlight_button(self):
        if self.active_button:
            self.active_button.state(['!pressed'])
            self.active_button = None

    def handle_keyboard_input(self, event):
        key = event.char
        if key.isdigit() or key in ['.', '+', '-', '*', '/', '(', ')']:
            self.expression += key
            self.update_display()
            self.highlight_button(key)
        elif key == '\x08':
            self.expression = self.expression[:-1]
            self.update_display()
            self.highlight_button('Del')
        elif key == '\x1b':
            self.expression = ""
            self.update_display()
            self.highlight_button('C')
        elif event.keysym == 'Return':
            self.button_click('=')
            self.highlight_button('=')

    def button_click(self, text):
        if text == '=':
            try:
                result = eval(self.expression)
                self.display.config(state='normal')
                self.display.delete(0, tk.END)
                self.display.insert(0, result)
                self.display.config(state='readonly')
                self.history.append(f"{self.expression} = {result}")
                self.update_history_list()
                self.expression = str(result)
            except Exception as e:
                self.show_error()
        elif text == 'C':
            self.expression = ""
            self.update_display()
        elif text == 'Del':
            self.expression = self.expression[:-1]
            self.update_display()
        else:
            self.expression += text
            self.update_display()
        self.update_clear_history_button_visibility()

    def extended_button_click(self, text):
        current_expression = self.expression
        if text == '%':
            try:
                result = eval(self.expression) / 100
                self.expression = str(result)
                self.update_display()
                self.history.append(f"{current_expression} % = {result}")
                self.update_history_list()
            except Exception:
                self.show_error()
        elif text == 'sin':
            try:
                angle_degrees = eval(self.expression)
                result = math.sin(math.radians(angle_degrees))
                self.expression = str(result)
                self.update_display()
                self.history.append(f"sin({current_expression}) = {result}")
                self.update_history_list()
            except Exception:
                self.show_error()
        elif text == 'cos':
            try:
                angle_degrees = eval(self.expression)
                result = math.cos(math.radians(angle_degrees))
                self.expression = str(result)
                self.update_display()
                self.history.append(f"cos({current_expression}) = {result}")
                self.update_history_list()
            except Exception:
                self.show_error()
        elif text == 'tan':
            try:
                angle_degrees = eval(self.expression)
                result = math.tan(math.radians(angle_degrees))
                self.expression = str(result)
                self.update_display()
                self.history.append(f"tan({current_expression}) = {result}")
                self.update_history_list()
            except Exception:
                self.show_error()
        elif text == '√':
            try:
                value = eval(self.expression)
                result = math.sqrt(value)
                self.expression = str(result)
                self.update_display()
                self.history.append(f"√({current_expression}) = {result}")
                self.update_history_list()
            except Exception:
                self.show_error()
        elif text == 'π':
            self.expression += str(math.pi)
            self.update_display()
        elif text == 'x²':
            try:
                value = eval(self.expression)
                result = value ** 2
                self.expression = str(result)
                self.update_display()
                self.history.append(f"{current_expression}² = {result}")
                self.update_history_list()
            except Exception:
                self.show_error()
        elif text == 'x³':
            try:
                value = eval(self.expression)
                result = value ** 3
                self.expression = str(result)
                self.update_display()
                self.history.append(f"{current_expression}³ = {result}")
                self.update_history_list()
            except Exception:
                self.show_error()
        self.update_clear_history_button_visibility()

    def update_display(self):
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)
        self.display.config(state='readonly')

    def update_history_list(self):
        self.history_list.delete(0, tk.END)
        for item in self.history:
            self.history_list.insert(tk.END, item)
        if self.history:
            self.history_list.see(tk.END)
        self.update_clear_history_button_visibility()

    def clear_history(self):
        self.history.clear()
        self.update_history_list()
        self.update_clear_history_button_visibility()

    def update_clear_history_button_visibility(self):
        if self.history:
            self.clear_history_button.grid()
        else:
            self.clear_history_button.grid_remove()

    def copy_result_to_clipboard(self):
        try:
            result = self.display.get()
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            self.root.update()
            messagebox.showinfo("Копирование", "Результат скопирован в буфер обмена.")
        except tk.TclError:
            messagebox.showerror("Ошибка", "Нет результата для копирования.")

    def copy_expression_to_clipboard(self):
        try:
            expression_to_copy = self.expression
            self.root.clipboard_clear()
            self.root.clipboard_append(expression_to_copy)
            self.root.update()
            messagebox.showinfo("Копирование", "Выражение скопировано в буфер обмена.")
        except tk.TclError:
            messagebox.showerror("Ошибка", "Нет выражения для копирования.")

    def show_error(self):
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        self.display.insert(0, "Ошибка")
        self.display.config(state='readonly')
        self.expression = ""

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedCalculator(root)
    root.mainloop()
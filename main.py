import os
from bs4 import BeautifulSoup
import subprocess
import tkinter as tk
import requests
from tkinter import filedialog, messagebox, simpledialog, ttk
import time

THEMES = {
    "default": {"bg": "white", "fg": "black"},
    "dark": {"bg": "black", "fg": "white"},
    "blue": {"bg": "#1E90FF", "fg": "white"},
    "green": {"bg": "#32CD32", "fg": "black"},
    "purple": {"bg": "#800080", "fg": "white"},
    "red": {"bg": "#FF6347", "fg": "white"},
    "yellow": {"bg": "#FFD700", "fg": "black"},
    "grey": {"bg": "#A9A9A9", "fg": "black"},
    "orange": {"bg": "#FFA500", "fg": "black"},
    "pink": {"bg": "#FF69B4", "fg": "black"},
}


def collect_information():
    def submit():
        phone_number = phone_number_entry.get()
        full_name = full_name_entry.get()
        street_city = street_city_entry.get()
        vk = vk_entry.get()
        telegram_id = telegram_entry.get()
        age = age_entry.get()
        school = school_entry.get()
        mother_name = mother_entry.get()
        father_name = father_entry.get()
        mother_phone = mother_phone_entry.get()
        father_phone = father_phone_entry.get()
        user_text = user_text_entry.get()
        ransom_amount = ransom_entry.get()

        message = (
            f"Привет, ты был задеононен by {user_text}\n"
            f"Требую извинений или откуп в размере {ransom_amount}\n"
            f"Твоя информация:\n"
            f"Номер телефона: {phone_number}\n"
            f"ФИО: {full_name}\n"
            f"Улица и город, где ты живешь: {street_city}\n"
            f"Твое ВК: {vk}\n"
            f"Твой ID Telegram: {telegram_id}\n"
            f"Твой возраст: {age}\n"
            f"Твоя школа: {school}\n"
            f"Мама: {mother_name}\n"
            f"Папа: {father_name}\n"
            f"Номер мамы: {mother_phone}\n"
            f"Номер папы: {father_phone}\n"
            f"Рекомендую поторопиться)"
        )

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, message)

    def copy_to_clipboard():
        window.clipboard_clear()
        window.clipboard_append(result_text.get(1.0, tk.END))
        messagebox.showinfo("Копирование", "Текст скопирован в буфер обмена!")

    collect_window = tk.Toplevel(window)
    collect_window.title("Генератор")

    title_label = tk.Label(collect_window, text="Введите данные для генерации", font=("Arial", 14, "bold"))
    title_label.pack(pady=10)

    fields = ["Номер телефона", "ФИО", "Улица и город", "ВК", "Telegram ID", "Возраст", "Школа", "Имя мамы", "Имя папы",
              "Номер мамы", "Номер папы", "Текст", "Сумма"]
    entries = {}

    for field in fields:
        frame = tk.Frame(collect_window)
        frame.pack(pady=5, padx=10, fill="x")
        tk.Label(frame, text=field, font=("Arial", 10)).pack(side=tk.LEFT)
        entry = tk.Entry(frame, font=("Arial", 10), width=30)
        entry.pack(side=tk.RIGHT, padx=10)
        entries[field] = entry

    phone_number_entry = entries["Номер телефона"]
    full_name_entry = entries["ФИО"]
    street_city_entry = entries["Улица и город"]
    vk_entry = entries["ВК"]
    telegram_entry = entries["Telegram ID"]
    age_entry = entries["Возраст"]
    school_entry = entries["Школа"]
    mother_entry = entries["Имя мамы"]
    father_entry = entries["Имя папы"]
    mother_phone_entry = entries["Номер мамы"]
    father_phone_entry = entries["Номер папы"]
    user_text_entry = entries["Текст"]
    ransom_entry = entries["Сумма"]

    result_text = tk.Text(collect_window, height=10, width=50, font=("Arial", 10))
    result_text.pack(pady=10, padx=10)

    button_frame = tk.Frame(collect_window)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Сгенерировать", command=submit, font=("Arial", 10, "bold"), bg="#4CAF50",
              fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Скопировать текст", command=copy_to_clipboard, font=("Arial", 10, "bold"),
              bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)


def search_in_txt_files():
    folder_path = filedialog.askdirectory()

    if not folder_path:
        messagebox.showerror("Ошибка", "Папка не выбрана!")
        return

    search_term = simpledialog.askstring("Поиск", "Введите текст для поиска:")

    if not search_term:
        messagebox.showerror("Ошибка", "Текст для поиска не введен!")
        return

    found_files = []

    progress_window = tk.Toplevel()
    progress_window.title("Поиск...")
    progress_bar = ttk.Progressbar(progress_window, mode='indeterminate')
    progress_bar.pack(padx=20, pady=20)
    progress_bar.start()

    window.update()
    time.sleep(1)

    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                if search_term in file.read():
                    found_files.append(filename)

    progress_bar.stop()
    progress_window.destroy()

    if found_files:
        messagebox.showinfo("Результаты поиска", f"Найденные файлы:\n{', '.join(found_files)}")
    else:
        messagebox.showinfo("Результаты поиска", "Файлы не найдены.")


def apply_theme(theme_name):
    theme = THEMES[theme_name]
    window.configure(bg=theme["bg"])
    for widget in window.winfo_children():
        widget.configure()

        if isinstance(widget, (tk.Label, tk.Button, tk.Entry)):
            widget.configure(fg=theme["fg"])


def search_social_media(name):
    print(f"Поиск информации о {name} в социальных сетях...")
    vk_search_url = f"https://vk.com/search?c[section]=people&q={name}"
    response = requests.get(vk_search_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        users = soup.find_all('div', class_='search_result')
        if users:
            result_text = "Найденные пользователи VK:\n"
            for user in users:
                user_name = user.find('a').text
                user_link = user.find('a')['href']
                result_text += f"- {user_name}: {user_link}\n"
            messagebox.showinfo("Результаты VK", result_text)
        else:
            messagebox.showinfo("Результаты VK", "Пользователи не найдены.")
    else:
        messagebox.showerror("Ошибка", "Ошибка при запросе к VK.")


def search_ip(ip_address):
    print(f"Поиск информации о IP {ip_address}...")
    response = requests.get(f"https://ipinfo.io/{ip_address}/json")

    if response.status_code == 200:
        data = response.json()
        message = (
            f"Информация о IP {ip_address}:\n"
            f" - Локация: {data.get('loc', 'Неизвестно')}\n"
            f" - Организация: {data.get('org', 'Неизвестно')}\n"
            f" - Город: {data.get('city', 'Неизвестно')}\n"
        )
        messagebox.showinfo("Результаты IP", message)
    else:
        messagebox.showerror("Ошибка", "Ошибка при запросе информации о IP.")


def search_google_dorks(dork):
    print(f"Поиск по Google Dork: {dork}")
    headers = {'User-Agent': 'Mozilla/5.0'}
    search_url = f"https://www.google.com/search?q={dork}"
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('h3')
        if results:
            result_text = "Найденные результаты:\n"
            for result in results:
                result_text += f"- {result.get_text()}\n"
            messagebox.showinfo("Результаты поиска", result_text)
        else:
            messagebox.showinfo("Результаты поиска", "Результаты не найдены.")
    else:
        messagebox.showerror("Ошибка", "Ошибка при запросе к Google.")


def osint_menu():
    osint_window = tk.Toplevel(window)
    osint_window.title("OSINT Инструменты")

    tk.Label(osint_window, text="Выберите инструмент:", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Button(osint_window, text="Руководство по установке Arch Linux", font=("Arial", 12),
              command=show_arch_installation_guide).pack(pady=5)
    tk.Button(osint_window, text="1 - Поиск по имени", font=("Arial", 12),
              command=lambda: search_social_media(simpledialog.askstring("Поиск", "Введите имя:"))).pack(pady=5)
    tk.Button(osint_window, text="2 - Поиск по IP-адресу", font=("Arial", 12),
              command=lambda: search_ip(simpledialog.askstring("Поиск", "Введите IP-адрес:"))).pack(pady=5)
    tk.Button(osint_window, text="3 - Поиск по Google Dork", font=("Arial", 12),
              command=lambda: search_google_dorks(simpledialog.askstring("Поиск", "Введите Google Dork:"))).pack(pady=5)
    tk.Button(osint_window, text="4 - Просмотр исходного кода сайта", font=("Arial", 12),
              command=view_source_code).pack(pady=5)
    tk.Button(osint_window, text="5 - Обход блокировки YouTube", font=("Arial", 12), command=bypass_youtube_block).pack(
        pady=5)
    tk.Button(osint_window, text="О создателе", font=("Arial", 12), command=show_about_creator).pack(pady=5)


def applyh(theme_name):
    if theme_name == "rainbow":
        rainbow_theme.start()
    else:
        rainbow_theme.stop()
        th = THEMES[theme_name]
        window.configure(bg=th["bg"])
        for widget in window.winfo_children():
            widget.configure()
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry)):
                widget.configure(fg=th["fg"])


class RainbowTheme:
    def __init__(self, window):
        self.window = window
        self.running = False
        self.current_color = [255, 0, 0]
        self.target_color = [255, 0, 0]
        self.color_step = 0
        self.color_index = 0

        self.colors = [
            [255, 0, 0],
            [50, 50, 50],
            [255, 127, 0],
            [255, 255, 0],
            [0, 255, 0],
            [200, 200, 200],
            [0, 255, 127],
            [50, 50, 50],
            [0, 255, 255],
            [0, 127, 255],
            [150, 150, 150],
            [0, 0, 255],
            [127, 0, 255],
            [255, 0, 255],
            [50, 50, 50],
            [255, 0, 127],
            [255, 0, 0],
            [200, 200, 200],
            [255, 50, 0],
            [255, 100, 0],
            [255, 150, 0],
            [255, 200, 0],
            [50, 50, 50],
            [255, 255, 0],
            [200, 255, 0],
            [100, 255, 0],
            [150, 150, 150],
            [0, 255, 0],
            [0, 255, 100],
            [150, 150, 150],
            [0, 255, 200],
            [0, 255, 255],
            [0, 150, 255],
            [50, 50, 50],
            [0, 0, 255],
            [50, 0, 255],
            [100, 0, 255],
            [150, 0, 255],
            [200, 0, 255],
            [255, 0, 255],
            [255, 0, 200],
            [50, 50, 50],
            [255, 0, 150],
            [255, 0, 100],
            [150, 150, 150],
            [255, 0, 0],
        ]

    def start(self):
        self.running = True
        self.color_step = 0
        self.animate()

    def stop(self):
        self.running = False

    def animate(self):
        if self.running:
            if self.color_step < 100:
                for i in range(3):
                    self.current_color[i] += (self.target_color[i] - self.current_color[i]) / (100 - self.color_step)
                self.color_step += 1
            else:
                self.color_index = (self.color_index + 1) % len(self.colors)
                self.target_color = self.colors[self.color_index]
                self.color_step = 0

            hex_color = "#{:02x}{:02x}{:02x}".format(int(self.current_color[0]), int(self.current_color[1]),
                                                     int(self.current_color[2]))
            self.window.configure(bg=hex_color)
            for widget in self.window.winfo_children():
                widget.configure(bg=hex_color)

            self.window.after(40, self.animate)


def bypass_youtube_block():
    youtube_url = "https://www.youtube.com"

    try:
        subprocess.Popen(['chromium', '--proxy-server=socks5://127.0.0.1:9050', youtube_url])
        messagebox.showinfo("Блокировка обойдена", "YouTube открыт через прокси в Chromium.")
    except Exception as e:
        print(f"Ошибка при запуске Chromium: {e}")
        messagebox.showerror("Ошибка", f"Не удалось открыть YouTube через прокси: {e}")


def show_terms_and_conditions():
    terms_window = tk.Toplevel(window)
    terms_window.title("Согласие с правилами")

    terms_text = (
        "Пользовательское соглашение\n\n"
        "1. Этот инструмент предназначен исключительно для образовательных целей.\n"
        "2. Мы не несем ответственности за использование данного инструмента в незаконных целях.\n"
        "3. Пожалуйста, соблюдайте законы вашей страны при использовании этого инструмента.\n"
        "4. Все действия, выполненные с помощью этого инструмента, вы делаете на свой страх и риск.\n\n"
        "Нажимая 'Согласен', вы принимаете эти условия."
    )

    tk.Label(terms_window, text=terms_text, font=("Arial", 12), justify=tk.LEFT).pack(padx=10, pady=10)

    tk.Button(terms_window, text="Согласен", command=terms_window.destroy).pack(pady=10)


def show_about_creator():
    about_window = tk.Toplevel(window)
    about_window.title("О создателе")

    tk.Label(about_window, text="Создатель: FRE1ZIK ", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(about_window, text="Discord: ssgamxi", font=("Arial", 12)).pack(pady=5)
    tk.Label(about_window, text="Версия: 1.0.3", font=("Arial", 12)).pack(pady=5)
    tk.Label(about_window, text="Описание: Продукс сделан для общего пользования.", font=("Arial", 12)).pack(pady=5)

    tk.Button(about_window, text="Закрыть", command=about_window.destroy).pack(pady=10)


def view_source_code():
    url = simpledialog.askstring("Введите URL", "Введите ссылку на сайт:")
    if not url:
        messagebox.showerror("Ошибка", "URL не введен!")
        return

    try:
        response = requests.get(url)
        response.raise_for_status()
        source_code = response.text

        code_window = tk.Toplevel(window)
        code_window.title("Исходный код")
        code_text = tk.Text(code_window, wrap=tk.WORD)
        code_text.pack(expand=True, fill='both')
        code_text.insert(tk.END, source_code)
        code_text.config(state=tk.DISABLED)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить страницу:\n{e}")


def show_arch_installation_guide():
    guide_text = (
        "Руководство по установке Arch Linux:\n\n"

        "1. Подготовка:\n"
        "   - Скачайте образ Arch Linux с официального сайта: https://archlinux.org/download/\n"
        "   - Запишите образ на USB-накопитель с помощью Rufus или dd.\n\n"

        "2. Загрузка с USB:\n"
        "   - Вставьте USB-накопитель и загрузитесь с него.\n\n"

        "3. Скачивание и настройка:\n"
        "   - Отформатируйте диски с помощью следующих команд:\n"
        "       1. Запустите `fdisk` для настройки разделов.\n"
        "       2. Используйте `mkfs.ext4` для форматирования разделов, созданных в `fdisk`.\n"
        "   - Напишите `archinstall`, когда окажетесь в командной строке.\n"
        "   - Если нет интернета, раздайте его через USB от телефона.\n\n"

        "4. Настройка дисков и монтирования:\n"
        "   - В разделе 'Диски' выберите автоматическое распределение.\n"
        "   - Обязательно смонтируйте диски:\n"
        "       1. Первый диск: `/boot`\n"
        "       2. Второй диск: `/`\n"
        "       3. Третий диск: `/home`\n\n"

        "5. Настройка пользователя и звука:\n"
        "   - Установите пароль для root.\n"
        "   - В профиле выберите Desktop → KDE Plasma (рекомендуется).\n"
        "   - В дополнительных репозиториях выберите первый пункт.\n\n"

        "Полное руководство доступно на официальном сайте Arch Linux:\n"
        "https://wiki.archlinux.org/"
    )

    guide_window = tk.Toplevel(window)
    guide_window.title("Установка Arch Linux")
    guide_text_box = tk.Text(guide_window, wrap=tk.WORD)
    guide_text_box.insert(tk.END, guide_text)
    guide_text_box.pack(expand=True, fill='both')
    guide_text_box.config(state=tk.DISABLED)


def change_theme(theme):
    colors = THEMES.get(theme, THEMES["default"])
    window.configure(bg=colors["bg"])
    for widget in window.winfo_children():
        widget.configure()


def create_button(parent, text, command):
    button = tk.Button(parent, text=text, command=command, font=("Arial", 12),
                       bg="#4CAF50", fg="white", width=20, borderwidth=2, relief="groove")

    button.bind("<Enter>", lambda e: button.configure(bg="#45a049"))
    button.bind("<Leave>", lambda e: button.configure(bg="#4CAF50"))

    button.pack(pady=5)
    return button


window = tk.Tk()
window.title("Tool by ds ssgamxi")
window.geometry("400x500")

rainbow_theme = RainbowTheme(window)

title_label = tk.Label(window, text="OSINT Tool", font=("Arial", 18, "bold"))
title_label.pack(pady=20)

button_frame = tk.Frame(window)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Генератор текста", command=collect_information, font=("Arial", 12), bg="#4CAF50",
          fg="white", width=20).pack(pady=5)
tk.Button(button_frame, text="Поиск в файлах", command=search_in_txt_files, font=("Arial", 12), bg="#4CAF50",
          fg="white", width=20).pack(pady=5)
tk.Button(button_frame, text="OSINT Инструменты", command=osint_menu, font=("Arial", 12), bg="#4CAF50", fg="white",
          width=20).pack(pady=5)
tk.Button(button_frame, text="Согласие с правилами", command=show_terms_and_conditions, font=("Arial", 12),
          bg="#f44336", fg="white", width=20).pack(pady=5)

theme_label = tk.Label(window, text="Выберите тему:", font=("Arial", 14))
theme_label.pack(pady=10)
for theme in THEMES:
    tk.Button(window, text=theme.capitalize(), command=lambda t=theme: change_theme(t), font=("Arial", 10)).pack(pady=5)

tk.Button(window, text="Rainbow", command=lambda: rainbow_theme.start(), font=("Arial", 10)).pack(pady=5)

window.mainloop()

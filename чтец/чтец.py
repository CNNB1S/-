import sys
import subprocess
import os
from importlib import util
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# Проверка и установка необходимых библиотек
def check_and_install_libraries():
    REQUIRED_LIBRARIES = [
        ('chardet', 'chardet'),
        # Для pyinstaller можно добавить:
        # ('pyinstaller', 'pyinstaller')
    ]
    
    missing_libs = []
    for (import_name, pkg_name) in REQUIRED_LIBRARIES:
        if util.find_spec(import_name) is None:
            missing_libs.append(pkg_name)
    
    if missing_libs:
        print(f"Требуются библиотеки: {', '.join(missing_libs)}")
        try:
            # Проверяем, есть ли pip
            import pip
            # Устанавливаем отсутствующие библиотеки
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing_libs])
            print("Библиотеки успешно установлены!")
            # Перезапускаем программу после установки
            os.execv(sys.executable, ['python'] + sys.argv)
        except Exception as e:
            print(f"Ошибка установки: {e}")
            response = messagebox.askyesno(
                "Ошибка",
                f"Необходимо установить библиотеки: {', '.join(missing_libs)}\n"
                "Установить автоматически? (требуются права администратора)"
            )
            if response:
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing_libs])
                    os.execv(sys.executable, ['python'] + sys.argv)
                except:
                    messagebox.showerror(
                        "Ошибка",
                        "Не удалось установить библиотеки. Установите их вручную:\n"
                        f"pip install {' '.join(missing_libs)}"
                    )
                    sys.exit(1)
            else:
                sys.exit(1)

# Проверяем библиотеки перед запуском основной программы
check_and_install_libraries()

# Теперь импортируем остальные библиотеки
import chardet

class UltimateWordReader:
    def __init__(self, root):
        self.root = root
        self.language = "ru"
        self.translations = self.load_translations()
        self.init_ui()
        self.update_language()
    
    def load_translations(self):
        return {
            "ru": {
                "title": "Улучшенный чтец текста",
                "open": "📂 Открыть файл",
                "help": "❓ Помощь",
                "language": "🌐 English",
                "speed": "Скорость:",
                "start": "▶ Старт",
                "pause": "⏸ Пауза",
                "prev": "◀ Назад",
                "next": "Вперед ▶",
                "file_loaded": "Файл загружен",
                "words_loaded": "Загружено {} слов",
                "error": "Ошибка",
                "file_error": "Не удалось загрузить файл:\n{}",
                "instructions": self.get_russian_instructions()
            },
            "en": {
                "title": "Enhanced Text Reader",
                "open": "📂 Open File",
                "help": "❓ Help",
                "language": "🌐 Русский",
                "speed": "Speed:",
                "start": "▶ Start",
                "pause": "⏸ Pause",
                "prev": "◀ Previous",
                "next": "Next ▶",
                "file_loaded": "File loaded",
                "words_loaded": "Loaded {} words",
                "error": "Error",
                "file_error": "Failed to load file:\n{}",
                "instructions": self.get_english_instructions()
            }
        }
    
    def get_russian_instructions(self):
        return """ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ:

1. ОТКРЫТИЕ ФАЙЛА
- Нажмите "📂 Открыть файл"
- Выберите текстовый файл (.txt)

2. УПРАВЛЕНИЕ
▶ "Старт/Пауза" - автоматическое чтение
◀ "Назад" - предыдущее слово
▶ "Вперед" - следующее слово

3. СКОРОСТЬ
- Регулируйте ползунком (0.5-20)

4. ПОДСКАЗКИ
- F11 - полноэкранный режим
- Esc - выход из полноэкранного режима

5. ЕСЛИ ФАЙЛ НЕ ОТКРЫВАЕТСЯ:
- Откройте в Блокноте
- Сохраните как UTF-8
- Попробуйте снова"""
    
    def get_english_instructions(self):
        return """USER INSTRUCTIONS:

1. OPENING FILES
- Click "📂 Open File"
- Select a text file (.txt)

2. CONTROLS
▶ "Start/Pause" - auto reading
◀ "Previous" - previous word
▶ "Next" - next word

3. SPEED
- Adjust with slider (0.5-20)

4. TIPS
- F11 - fullscreen mode
- Esc - exit fullscreen

5. IF FILE WON'T OPEN:
- Open in Notepad
- Save as UTF-8
- Try again"""
    
    def init_ui(self):
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Верхняя панель
        self.top_frame = tk.Frame(self.root, bg='#e0e0e0', padx=10, pady=5)
        self.top_frame.pack(fill=tk.X)
        
        # Кнопки управления
        self.btn_open = tk.Button(self.top_frame, font=('Arial', 12), bg='#4CAF50', fg='white', relief=tk.FLAT)
        self.btn_open.pack(side=tk.LEFT)
        
        self.btn_help = tk.Button(self.top_frame, font=('Arial', 12), bg='#2196F3', fg='white', relief=tk.FLAT)
        self.btn_help.pack(side=tk.LEFT, padx=5)
        
        self.btn_language = tk.Button(self.top_frame, font=('Arial', 12), bg='#FF9800', fg='white', relief=tk.FLAT)
        self.btn_language.pack(side=tk.LEFT, padx=5)
        
        # Ползунок скорости
        self.speed_frame = tk.Frame(self.top_frame, bg='#e0e0e0')
        self.speed_frame.pack(side=tk.RIGHT)
        
        self.speed_label = tk.Label(self.speed_frame, font=('Arial', 10), bg='#e0e0e0')
        self.speed_label.pack(side=tk.LEFT)
        
        self.speed_scale = tk.Scale(
            self.speed_frame,
            from_=0.5, to=20, resolution=0.5,
            orient=tk.HORIZONTAL,
            font=('Arial', 10),
            bg='#e0e0e0',
            highlightthickness=0,
            length=200
        )
        self.speed_scale.set(5)
        self.speed_scale.pack(side=tk.LEFT)
        
        # Основное текстовое поле
        self.word_label = tk.Label(
            self.root,
            font=('Arial', 82, 'bold'),
            fg='#333333',
            bg='#f0f0f0',
            wraplength=1200,
            pady=100
        )
        self.word_label.pack(expand=True)
        
        # Нижняя панель управления
        self.bottom_frame = tk.Frame(self.root, bg='#e0e0e0', padx=10, pady=10)
        self.bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Кнопки навигации
        self.nav_frame = tk.Frame(self.bottom_frame, bg='#e0e0e0')
        self.nav_frame.pack(side=tk.LEFT, expand=True)
        
        self.btn_prev = tk.Button(
            self.nav_frame,
            font=('Arial', 12),
            bg='#2196F3',
            fg='white',
            state=tk.DISABLED,
            width=10
        )
        self.btn_prev.pack(side=tk.LEFT, padx=5)
        
        self.btn_play = tk.Button(
            self.nav_frame,
            font=('Arial', 14, 'bold'),
            bg='#4CAF50',
            fg='white',
            width=10,
            height=1
        )
        self.btn_play.pack(side=tk.LEFT, padx=20)
        
        self.btn_next = tk.Button(
            self.nav_frame,
            font=('Arial', 12),
            bg='#2196F3',
            fg='white',
            state=tk.DISABLED,
            width=10
        )
        self.btn_next.pack(side=tk.LEFT, padx=5)
        
        # Инициализация переменных
        self.words = []
        self.current_word = 0
        self.file_path = ""
        self.playing = False
        self.after_id = None
        
        # Привязка команд
        self.btn_open.config(command=self.load_file)
        self.btn_help.config(command=self.show_instructions)
        self.btn_language.config(command=self.toggle_language)
        self.btn_play.config(command=self.toggle_play)
        self.btn_prev.config(command=self.prev_word)
        self.btn_next.config(command=self.next_word)
    
    def toggle_language(self):
        self.language = "en" if self.language == "ru" else "ru"
        self.update_language()
    
    def update_language(self):
        lang = self.translations[self.language]
        self.root.title(lang["title"])
        self.btn_open.config(text=lang["open"])
        self.btn_help.config(text=lang["help"])
        self.btn_language.config(text=lang["language"])
        self.speed_label.config(text=lang["speed"])
        self.btn_play.config(text=lang["pause"] if self.playing else lang["start"])
        self.btn_prev.config(text=lang["prev"])
        self.btn_next.config(text=lang["next"])
    
    def show_instructions(self):
        instr_window = tk.Toplevel(self.root)
        instr_window.title(self.translations[self.language]["help"])
        instr_window.geometry("800x600")
        
        text_area = scrolledtext.ScrolledText(
            instr_window,
            wrap=tk.WORD,
            font=('Arial', 12),
            padx=15,
            pady=15
        )
        text_area.pack(expand=True, fill=tk.BOTH)
        text_area.insert(tk.END, self.translations[self.language]["instructions"])
        text_area.config(state=tk.DISABLED)
        
        btn_close = tk.Button(
            instr_window,
            text="OK" if self.language == "en" else "Закрыть",
            command=instr_window.destroy,
            font=('Arial', 12),
            bg='#4CAF50',
            fg='white'
        )
        btn_close.pack(pady=10)
    
    def load_file(self):
        filetypes = [
            (self.translations[self.language]["file_loaded"], "*.txt"),
            ("All files", "*.*")
        ] if self.language == "en" else [
            ("Текстовые файлы", "*.txt"),
            ("Все файлы", "*.*")
        ]
        
        filepath = filedialog.askopenfilename(
            title=self.btn_open["text"],
            filetypes=filetypes
        )
        
        if not filepath:
            return
        
        try:
            with open(filepath, 'rb') as f:
                raw_data = f.read()
            
            result = chardet.detect(raw_data)
            encoding = result['encoding'] if result['confidence'] > 0.7 else 'utf-8'
            content = raw_data.decode(encoding, errors='replace')
            
            self.words = content.split()
            self.current_word = 0
            self.file_path = filepath
            
            self.update_word_display()
            self.btn_prev.config(state=tk.NORMAL)
            self.btn_next.config(state=tk.NORMAL)
            self.btn_play.config(text=self.translations[self.language]["start"])
            
            messagebox.showinfo(
                self.translations[self.language]["file_loaded"],
                self.translations[self.language]["words_loaded"].format(len(self.words))
            )
            
        except Exception as e:
            messagebox.showerror(
                self.translations[self.language]["error"],
                self.translations[self.language]["file_error"].format(str(e))
            )
    
    def update_word_display(self):
        if 0 <= self.current_word < len(self.words):
            self.word_label.config(text=self.words[self.current_word])
        else:
            self.word_label.config(text="---")
    
    def toggle_play(self):
        if not self.words:
            return
            
        self.playing = not self.playing
        lang = self.translations[self.language]
        
        if self.playing:
            self.btn_play.config(text=lang["pause"])
            self.play_next_word()
        else:
            self.btn_play.config(text=lang["start"])
            if self.after_id:
                self.root.after_cancel(self.after_id)
                self.after_id = None
    
    def play_next_word(self):
        if not self.playing:
            return
            
        if self.current_word < len(self.words) - 1:
            self.current_word += 1
            self.update_word_display()
            delay = int(1000 / self.speed_scale.get())
            self.after_id = self.root.after(delay, self.play_next_word)
        else:
            self.playing = False
            self.btn_play.config(text=self.translations[self.language]["start"])
    
    def next_word(self):
        if self.current_word < len(self.words) - 1:
            self.current_word += 1
            self.update_word_display()
            if self.playing:
                self.toggle_play()
    
    def prev_word(self):
        if self.current_word > 0:
            self.current_word -= 1
            self.update_word_display()
            if self.playing:
                self.toggle_play()

if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateWordReader(root)
    root.mainloop()
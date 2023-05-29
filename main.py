from tkinter import *
from tkinter import messagebox
import sqlite3
import traceback
import re
import psutil
import threading
import time
import sys

# Мониторинг ресурсов
def analyze_system_resources():
    cpu_percent = psutil.cpu_percent()
    mem = psutil.virtual_memory()
    mem_percent = mem.percent
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    print(f"CPU usage: {cpu_percent}%")
    print(f"Memory usage: {mem_percent}%")
    print(f"Disk usage: {disk_percent}%")

def monitor_resources():
    while True:
        analyze_system_resources()
        time.sleep(10)
monitor_thread = threading.Thread(target=monitor_resources)
monitor_thread.daemon = True
monitor_thread.start()

# Основной код


# Соединяемся с базой данных
conn = sqlite3.connect('errors.db')
c = conn.cursor()

# Создаем таблицу для ошибок, если ее еще нет
c.execute('''CREATE TABLE IF NOT EXISTS errors
             (date text, time text, error text)''')

# Функция для записи ошибок в базу данных
def log_error(error):
    # Получаем текущую дату и время
    import datetime
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    # Записываем ошибку в базу данных
    c.execute("INSERT INTO errors VALUES (?, ?, ?)", (date, time, error))
    conn.commit()


# Constants
WINDOW_WIDTH=1200
WINDOW_HEIGHT=800
MARGIN=100
BG_COLOR='grey'
LINES_COLOR = 'green'
BTN_COLOR = 'red'
TXT_COLOR='black'
SPEC_COLOR='orange'
HEAD_COLOR='YELLOW'
HAND_COLOR='PINK'
FOOT_COLOR='BROWN'
FG_COLOR='BLUE'
label_word = []
btn_aplha = []

def start_pos_man():
    line_1 = canvas.create_line(
        MARGIN, WINDOW_HEIGHT - MARGIN, MARGIN, MARGIN, width=4, fill=LINES_COLOR)
    line_2 = canvas.create_line(
        MARGIN, MARGIN, WINDOW_WIDTH // 3, MARGIN, width=4, fill=LINES_COLOR)
    line_3 = canvas.create_line(
        WINDOW_WIDTH // 3, MARGIN, WINDOW_WIDTH // 3, MARGIN * 2, width=4, fill=LINES_COLOR)

def start_pos_aplhabet():
    shift_x = shift_y = 0
    count = 0

    for c in range(ord('А'), ord('Я') + 1):
        btn = Button(text=chr(c), bg=BTN_COLOR, foreground=TXT_COLOR, font='Arial 16', relief=SOLID)
        btn.place(x=WINDOW_HEIGHT - MARGIN*2 + shift_x, y=MARGIN*4.5 - shift_y)
        btn.bind('<Button-1>', lambda event: check_alpha(event,word))
        btn_aplha.append(btn)
        shift_x += 65
        count += 1

        if (count==8):
            shift_x = count = 0
            shift_y -= 65

def get_word():
    global word, player
    word = entry.get()
    player = player_entry.get()

    # Проверяем, что введенные символы являются только русскими буквами
    if not re.match("^[А-Яа-я]+$", word):
        messagebox.showerror("Ошибка", "Вы можете вводить только русские буквы!")
        return

    wordinp.destroy()
    wordinp.quit()
    word = word.upper()


def on_closing():
    if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
        print('Вы вышли')
        time.sleep(1)
        sys.exit()


word = None
player = None
wordinp = Tk()
wordinp.title('Введите слово')
# Определяем ширину и высоту экрана
screen_width = wordinp.winfo_screenwidth()
screen_height = wordinp.winfo_screenheight()

# Определяем ширину и высоту окна
window_width = 500
window_height = 500

# Вычисляем координаты для размещения окна по центру экрана
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
wordinp.geometry('{}x{}+{}+{}'.format(window_width, window_height, x, y))

label = Label(wordinp, text='Введите имя:', font=('Arial', 14))
label.pack(pady=10)

player_entry = Entry(wordinp, font=('Arial', 14))
player_entry.pack(pady=10)

label = Label(wordinp, text='Введите слово (только русские буквы):', font=('Arial', 14))
label.pack(pady=10)

entry = Entry(wordinp, font=('Arial', 14))
entry.pack(pady=10)

button = Button(wordinp, text='Отправить', font=('Arial', 14), command=get_word)
button.pack(pady=10)

wordinp.protocol("WM_DELETE_WINDOW", on_closing)
wordinp.mainloop()

# здесь можно использовать переменные word и player
print(f'Слово: {word}, Игрок: {player}')

def start_pos_word(word):
    shift = 0
    count=0
    for i in range(len(word)):
        if count==0 or count==len(word)-1:
            label_under = Label(window, text=word[(count)], font='Arial 24', bg=BG_COLOR, fg=FG_COLOR)
            label_under.place(x=WINDOW_HEIGHT-MARGIN*2 + shift, y=MARGIN*3.5)
            shift+=50
            label_word.append(label_under)
        else:
            label_under = Label(window, text='__', font='Arial 24', bg=BG_COLOR, fg=FG_COLOR)
            label_under.place(x=WINDOW_HEIGHT-MARGIN*2 + shift, y=MARGIN*3.5)
            shift+=50
            label_word.append(label_under)
        count+=1

def draw(lifes):
    if (lifes == 4):
        head = canvas.create_oval(WINDOW_WIDTH // 3 - 60, MARGIN*1.5,
                                  WINDOW_WIDTH // 3 + 60, MARGIN*2.5, fill=HEAD_COLOR)
    elif (lifes == 3):
        body = canvas.create_oval(WINDOW_WIDTH // 3 - 25, MARGIN*2.5,
                                  WINDOW_WIDTH // 3 + 25, MARGIN*5, fill=HEAD_COLOR)
    elif (lifes==2):
        l_hand = canvas.create_line(WINDOW_WIDTH // 3 - 15, MARGIN*3.5,
                                    WINDOW_WIDTH // 3 - 105, MARGIN*2.4, width=6, fill=HAND_COLOR)
        r_hand = canvas.create_line(WINDOW_WIDTH // 3 + 15, MARGIN*3.5,
                                    WINDOW_WIDTH // 3 + 105, MARGIN*2.4, width=6, fill=HAND_COLOR)
    elif (lifes==1):
        l_foot = canvas.create_line(WINDOW_WIDTH // 3 - 15, MARGIN*4.5,
                                    WINDOW_WIDTH // 3 - 110, MARGIN*7, width=7, fill=FOOT_COLOR)
        r_foot = canvas.create_line(WINDOW_WIDTH // 3 + 15, MARGIN*4.5,
                                    WINDOW_WIDTH // 3 + 110, MARGIN*7, width=7, fill=FOOT_COLOR)
    elif (lifes==0):
        game_over('lose')
        label_text.destroy()
        label_life.destroy()


def check_alpha(event, word):
    alpha = event.widget['text']
    pos = []

    for i in range(len(word)):
        if (word[i]==alpha):
            pos.append(i)

    if (pos):
        for i in pos:
            label_word[i].config(text='{}'.format(word[i]))
        count_alpha = 0

        for i in label_word:
            if (i['text'].isalpha()):
                count_alpha += 1

        if (count_alpha==len(word)):
            game_over('win')
    else:
        lifes = int(label_life.cget('text')) - 1

        if (lifes != 0):
            label_life.config(text=' {}'.format(lifes))

        draw(lifes)
def stop_game():
    sys.exit()
def game_over(status):
    for btn in btn_aplha:
        btn.destroy()
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY, name TEXT, word TEXT, result TEXT)')
    if (status=='win'):
        canvas.create_text(canvas.winfo_width()/2 + 100, canvas.winfo_height()/2,
                           font=('Futura PT Heave', 50), text='Вы выиграли!\n     Поздравляем!', fill=SPEC_COLOR)
        result = 'WIN'
        btn = Button(text='Выйти', bg=BTN_COLOR, foreground=TXT_COLOR, font='Arial 16', relief=SOLID)
        btn.place(x=WINDOW_HEIGHT - MARGIN*2//2, y=MARGIN*4.5//1.5)
        btn.bind('<Button-1>', lambda event: stop_game())
    else:
        canvas.create_text(canvas.winfo_width() / 2 + 150, canvas.winfo_height() / 2,
                           font=('Futura PT Heave', 50),
                           text='    Вы проиграли\n    Попробуйте еще раз!', fill=SPEC_COLOR)
        result = 'LOSE'
        btn = Button(text='Выйти', bg=BTN_COLOR, foreground=TXT_COLOR, font='Arial 16', relief=SOLID)
        btn.place(x=WINDOW_HEIGHT - MARGIN*2//2, y=MARGIN*4.5//1.5)
        btn.bind('<Button-1>', lambda event: stop_game())

    cursor.execute('INSERT INTO games (name, word, result) VALUES (?, ?, ?)', (player, word, result))
    conn.commit()
    cursor.close()
    conn.close()
#main window
window = Tk()

window.title('Виселица')
window.resizable(False, False)

lifes = 5
label_playertxt = Label(window, text='Игрок:', font=('Futura PT Heave', 40), foreground=TXT_COLOR)
label_playertxt.place(x=0,y=10)
label_player = Label(window, text='{}'.format(player), font=('Futura PT Heave', 40), foreground=TXT_COLOR)
label_player.place(x=200,y=10)
label_text = Label(window, text='Жизни:', font=('Futura PT Heave', 40), foreground=TXT_COLOR)
label_text.place(x=930,y=10)
label_life = Label(window,text=' {}'.format(lifes), font=('Futura PT Heave', 40), foreground=TXT_COLOR)
label_life.place(x=1110, y=10)

canvas = Canvas(window, bg=BG_COLOR, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
canvas.place(x=0,y=70)
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
win_width = 1200
win_height = 800
x = (screen_width - win_width) // 2
y = (screen_height - win_height) // 2
window.geometry('{}x{}+{}+{}'.format(win_width, win_height, x, y))



# Пример кода с ошибкой
try:
    # Код, который может вызвать ошибку
    start_pos_man()
    start_pos_aplhabet()
    start_pos_word(word)
except Exception as e:
    # Записываем ошибку в базу данных и выводим сообщение пользователю
    log_error(traceback.format_exc())
    print("Произошла ошибка. Пожалуйста, обратитесь к разработчикам.")

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()

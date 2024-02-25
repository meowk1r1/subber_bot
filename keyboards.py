from telebot import types

def hello_kb():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(types.InlineKeyboardButton(text="🤑 Earn", callback_data="earn"),
           types.InlineKeyboardButton(text="💰 Balance", callback_data="balance"))
    
    kb.add(types.InlineKeyboardButton(text="🎲 Play", callback_data="play"),
           types.InlineKeyboardButton(text="🏦 Withdrawal", callback_data="balance")
    )
    kb.add(types.InlineKeyboardButton(text="👥 Invite friends", callback_data="invite"),
           types.InlineKeyboardButton(text="📜 Rules", callback_data="rules"))
    kb.row(types.InlineKeyboardButton(text = "💲Big Money💲", callback_data="bigmoney"))
    return kb

def admin():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(types.InlineKeyboardButton(text="💠 Add TG task", callback_data="add_tg_task"),
           types.InlineKeyboardButton(text="📤 Mailing", callback_data="sender"))
    kb.row(types.InlineKeyboardButton(text="📊 Statistics", callback_data="statistics"))
    return kb

def markup_add_tg():
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("Add✅", callback_data="add_admin_tg"), types.InlineKeyboardButton("Cancel❎", callback_data="cancel_admin"))
    return markup
def sender():
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("Send✅", callback_data="send_tg"), types.InlineKeyboardButton("Cancel❎", callback_data="cancel_admin"))
    return markup
def back_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="🏠 Home", callback_data="home"))
    return kb

def tasks_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)  # row_width=1 для вертикального расположения кнопок
    telegram_button = types.InlineKeyboardButton(text="🤖 Telegram tasks", callback_data="tg_tasks")
    instagram_button = types.InlineKeyboardButton(text="📸 Instagram tasks", callback_data="insta_tasks")
    kb.add(telegram_button)
    # kb.row(telegram_button, instagram_button)
    kb.add(types.InlineKeyboardButton(text="🏠 Home", callback_data="home"))
    return kb

def back_kb_tasks():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="🔙 Back", callback_data="earn"))
    return kb


def back_kb_tasks_earn():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="🔙 Back", callback_data="tgsex_1"))
    return kb
class PaginatedKeyboard:
    def __init__(self, items, items_per_page):
        self.items = items
        print(items)
        self.items_per_page = items_per_page
        self.total_pages = max(1, len(items) // items_per_page + (1 if len(items) % items_per_page else 0))

    def get_page(self, page):
        start = (page - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.items[start:end]

    def create_keyboard(self, page=1):
        kb = types.InlineKeyboardMarkup(row_width=3)
        rows_task = []
        for item in self.get_page(page):
            button = types.InlineKeyboardButton(text=item['name'].replace("https://t.me/",""), callback_data="tgs_"+item['_id'])
            rows_task.append(button)

        # Добавляем кнопки управления страницами
        row = []
        if page > 1:
            row.append(types.InlineKeyboardButton(text="⬅️", callback_data=f"tgsex_{page-1}"))
        if page < self.total_pages:
            row.append(types.InlineKeyboardButton(text="➡️", callback_data=f"tgsex_{page+1}"))
        kb.add(*rows_task)
        kb.row(*row)
        kb.add(types.InlineKeyboardButton(text="🏠 Home", callback_data="home"))
        return kb
    
def sub_tg(url, group_id):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="🌐 Subscribe to the channel", url=url))
    kb.add(types.InlineKeyboardButton(text="💸 Get a award", callback_data=f"tgcheck_{group_id}"))
    kb.add(types.InlineKeyboardButton(text="✖️ Skip task", callback_data=f"tgskip_{group_id}"))#✖️ Skip task
    kb.add(types.InlineKeyboardButton(text="🔙 Back", callback_data="tgsex_1"))
    return kb


def fine_task():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="✔️More tasks", callback_data="tgsex_1"))
    kb.add(types.InlineKeyboardButton(text="🔙Back to menu", callback_data=f"home"))
    return kb
import datetime
import asyncio
import text_ms as text
import config
from telebot import asyncio_filters
import keyboards as kb
from bson import ObjectId
import telebot
from telebot import types
from telebot.async_telebot import AsyncTeleBot
import database
# list of storages, you can use any storage
from telebot.asyncio_storage import StateMemoryStorage
from telebot.types import Message
# new feature for states.
from telebot.asyncio_handler_backends import State, StatesGroup


#db
db = database.db(uri=config.url_db, database_name=config.db_name)
db_tg = database.TelegramDB(uri=config.url_db, database_name=config.db_name)
db_inst = database.InstagramDB(uri=config.url_db, database_name=config.db_name)
db_coll = database.UserCollections(uri=config.url_db, database_name=config.db_name)

#asyncio.run(db_tg.create_entry(telegram_id="3231312", url="https://t.me/+YsYCRupjFFxiZDky", group_id="-1001716233239")) 
# Example usage
# db = Database(uri="mongodb://localhost:27017", database_name="yourDatabaseName")
#await db.create_user(user_id=12345, name="John Doe", referral="54321")


#connect bot
bot = AsyncTeleBot(config.api_token, state_storage=StateMemoryStorage())



# Создание StatesGroup для регистрации группы
class GroupRegistrationStates(StatesGroup):
    group_link = State()        # Состояние для ввода ссылки на группу
    group_user_id = State()     # Состояние для ввода user_id группы
# Создание StatesGroup для регистрации рассылки
class mailState(StatesGroup):
    text = State()        # Состояние для ввода ссылки на группу
    photo = State()     # Состояние для ввода user_id группы

#start handler
@bot.message_handler(commands=["start"])
async def welcome(message):
    print("start")
    try:
        referal = message.text.split(" ")[1]
        print(referal)
        have = await db.get_user_by_id(int(referal))
        print(have)
        if not have:
            referal = None
            
            await bot.send_message(message.from_user.id, "You're frend are not alive))")
    except:
        referal = None
    info = await db.create_user(message.from_user.id, message.from_user.first_name, referal, datetime.datetime.now().strftime('%d-%m-%Y'))
    if info == True:
        await db.add_balance(int(referal), 50)
        await db.add_balance(int(message.from_user.id), 50)
        await bot.send_message(chat_id=message.from_user.id, text=text.hello_text, parse_mode="Markdown", reply_markup=kb.hello_kb())
        try:
            await bot.send_message(referal, "You're a secsessful invited!")
            
        except:
            pass

        
    elif info == False:
        balance = await db.get_user_by_id(message.from_user.id)
        balance = balance['balance']
        balance = round(balance, 2)
        await bot.send_message(chat_id=message.from_user.id, text=text.hello_text_reg(message=message.from_user, balance=balance), parse_mode="Markdown", reply_markup=kb.hello_kb())
    else:
        await bot.send_message(chat_id=message.from_user.id, text=text.hello_text, parse_mode="Markdown", reply_markup=kb.hello_kb())


@bot.message_handler(commands=["admin"])
async def admin_func(message):
    if message.from_user.id in config.sudo_ids:
        await bot.send_photo(chat_id=message.from_user.id,photo="https://i.pinimg.com/564x/98/bc/95/98bc95968a45b6912c45b047b1256104.jpg", caption="You are admin!\nThis is task_tg example bot from @meowk1r1\nSelect a action:",reply_markup=kb.admin() )

# Обработчик команды /cancel для отмены регистрации
@bot.message_handler(commands=['cancel'], state="*")
async def cancel_group_registration(message):
    # Отменяем состояние
    await bot.delete_state(message.from_user.id, message.chat.id)
    await bot.send_message(message.chat.id, "Group registration is canceled.")


@bot.callback_query_handler(func=lambda call: True)
async def callback_worker(call):
    await bot.answer_callback_query(callback_query_id=call.id, show_alert=False)
    print(call.data)
    if call.data == "delete":
        await bot.delete_message(chat_id = call.from_user.id, message_id = call.message.id)
    
    if call.data == "balance":
        balance = await db.get_user_by_id(call.from_user.id)
        balance = balance['balance']
        balance = round(balance, 2)
        referal_link = f"https://t.me/url?start={call.from_user.id}"
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text.balance(balance, referal_link), reply_markup=kb.back_kb(), parse_mode="Markdown")
    
    if call.data == "home":
        balance = await db.get_user_by_id(call.from_user.id)
        balance = balance['balance']
        balance = round(balance, 2)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text.hello_text_reg(message=call.from_user, balance=balance), parse_mode="Markdown", reply_markup=kb.hello_kb())
    
    if call.data == "invite":
        referal_link = f"https://t.me/url?start={call.from_user.id}"
        bot_text = text.referal(referal_link)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=bot_text, reply_markup=kb.back_kb(), parse_mode="Markdown")
    
    if call.data == "rules":
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text.rules, reply_markup=kb.back_kb(), parse_mode="Markdown")
    
    if call.data == "earn":
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text.social, reply_markup=kb.tasks_kb(), parse_mode="Markdown")

    if call.data == "sender":
        await bot.set_state(call.from_user.id, mailState.text, call.message.chat.id)
        await bot.send_message(call.message.chat.id, "Please send me the text and photo together in one message. /cancel to back")


     #TSAKS
    if call.data =="tg_tasks":
        #await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text.work, reply_markup=kb.back_kb_tasks(), parse_mode="Markdown")
        page = 1

        # tasks = await db_tg.get_all_entries()
        user_entries = await db_coll.get_entries_by_user(call.from_user.id)
        # print(user_entries, "user_entries")
        completed_ids = {entry['id'] for entry in user_entries}
        print(completed_ids, "completed_ids")
        all_tg = await db_tg.get_all_entries()
        all_tg_entries = []
        for all in all_tg:
            print(all)
            try:
                name = await bot.get_chat(all['group_id'])
                name = name.title
            except Exception as e:
                print(e)
                name = "Not found"
            all_tg_entries.append({'_id' : all['_id'], 'group_id': all['group_id'], 'url': all['url'], 'name': name})
        tasks = [entry for entry in all_tg_entries if entry['group_id'] not in completed_ids]

        print(tasks)
        keyboard = kb.PaginatedKeyboard(tasks, 5).create_keyboard(page)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Choose a task:", reply_markup=keyboard, parse_mode="Markdown")
    
    if call.data == "insta_tasks":
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text.work, reply_markup=kb.back_kb_tasks(), parse_mode="Markdown")
    if call.data == "statistics":
        total_users = await db.count_users()
        print(f"Total users: {total_users}")
        users_with_referral = await db.count_users_with_referral()
        print(f"Users with referral: {users_with_referral}")
        await bot.send_message(chat_id=call.from_user.id, text=f"Total users: {total_users}\nUsers with referral: {users_with_referral}")

    if call.data == "add_tg_task":
        # Обработчик события нажатия кнопки "add_tg_task"
        print(call.message.chat.id, call.from_user.id)
        # Активируем состояние для регистрации группы и передаем user_id, чтобы потом его сохранить
        await bot.set_state(call.from_user.id, GroupRegistrationStates.group_link, call.from_user.id)
        await bot.send_message(call.message.chat.id, "the bot must be the admin of the group!! Please enter the link to the Telegram group:\n\n/cancel to back")
        
    if call.data == "add_admin_tg":
        chat_id = call.from_user.id
        user_id = call.from_user.id
        
        # Получаем данные из состояний
        async with bot.retrieve_data(user_id, chat_id) as data:
            group_link = data.get('group_link')
            group_user_id = data.get('group_user_id')
        
        try:
            name = await bot.get_chat(group_user_id)
            name = name.title

            await db_tg.create_entry(telegram_id=group_user_id, group_id=group_user_id, url=group_link)
            # Выводим данные в консоль
            print(f"Group Link: {group_link}")
            print(f"Group User ID: {group_user_id}")
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.id)
            # Отправляем сообщение о успешном добавлении данных
            await bot.send_message(chat_id, f"group {name} added!")
        except Exception as e:
            await bot.send_message(chat_id=call.from_user.id, text=f"FATAL ERROR : {e}")
        # Удаляем состояние
        await bot.delete_state(user_id, chat_id)
        await bot.send_photo(chat_id=call.from_user.id,photo="https://i.pinimg.com/564x/98/bc/95/98bc95968a45b6912c45b047b1256104.jpg", caption="You are admin!\nThis is task_tg example bot from @meowk1r1\nSelect a action:",reply_markup=kb.admin() )

    if call.data == "cancel_admin":
        user_id = call.from_user.id
        await bot.delete_state(user_id, user_id)
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.id)
        await bot.send_photo(chat_id=call.from_user.id,photo="https://i.pinimg.com/564x/98/bc/95/98bc95968a45b6912c45b047b1256104.jpg", caption="You are admin!\nThis is task_tg example bot from @meowk1r1\nSelect a action:",reply_markup=kb.admin() )

    if call.data == "send_tg":
        chat_id = call.from_user.id
        user_id = call.from_user.id
        async with bot.retrieve_data(user_id, chat_id) as data:
            texts = data.get('text')
            photo = data.get('photo')
        
        await bot.delete_state(user_id, chat_id)
        print(texts, photo)
        
        # Получаем массив с ID всех пользователей
        user_ids = await db.get_all_users()
        total_users = len(user_ids)
        
        msg = await bot.send_message(chat_id=call.from_user.id, text="start of mailing") 
        
        # Счетчик успешно отправленных сообщений
        successful_messages = 0

        # Проходим по каждому ID и отправляем сообщение
        for index, user_id in enumerate(user_ids, start=1):
            try:
                successful_messages += 1
                if successful_messages % 10 == 0:
                    percentage_complete = (successful_messages / total_users) * 100
                    await bot.edit_message_text(chat_id=call.from_user.id, message_id=msg.message_id, 
                                                text=f"Progress: {percentage_complete:.2f}%")
                # Отправляем сообщение каждому пользователю
                if texts and photo:
                    await bot.send_photo(chat_id=user_id, photo=photo, caption=texts)
                elif texts:
                    await bot.send_message(chat_id=user_id, text=texts)
                elif photo:
                    await bot.send_photo(chat_id=user_id, photo=photo)

                # Увеличиваем счетчик успешно отправленных сообщений
                

                # Рассчитываем процент выполнения каждые 10 успешно отправленных сообщений
                
                asyncio.sleep
                # Для управления частотой рассылки можно добавить небольшую задержку между сообщениями
                 # Например, 1 секунда
                
            except Exception as e:
                print(f"Failed to send message to user {user_id}: {e}")

    # Отправляем сообщение о завершении рассылки
        await bot.send_message(chat_id=call.from_user.id, text="Mailing completed!")


        

    if call.data == "bigmoney":
        await bot.edit_message_text(message_id=call.message.id, chat_id=call.from_user.id,text=text.bigmoney, reply_markup=kb.back_kb())
    
    if "tgsex_" in call.data:
        page = call.data.split("_")[1]
        page = int(page)
        print(page)
        # tasks = await db_tg.get_all_entries()

        user_entries = await db_coll.get_entries_by_user(call.from_user.id)
        # print(user_entries, "user_entries")
        completed_ids = {entry['id'] for entry in user_entries}
        print(completed_ids, "completed_ids")
        all_tg = await db_tg.get_all_entries()
        all_tg_entries = []
        for all in all_tg:
            print(all)
            name = await bot.get_chat(all['group_id'])
            name = name.title
            all_tg_entries.append({'_id' : all['_id'], 'group_id': all['group_id'], 'url': all['url'], 'name': name})
        tasks = [entry for entry in all_tg_entries if entry['group_id'] not in completed_ids]

        keyboard = kb.PaginatedKeyboard(tasks, 5).create_keyboard(page)

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Choose a task:", reply_markup=keyboard, parse_mode="Markdown")

    if "tgs_" in call.data:
        task_id = call.data.split("_")[1]
        print(task_id)
        full_info = await db_tg.find_by_id(task_id)
        print(full_info)
        keyboard = kb.sub_tg(url = full_info['url'], group_id = full_info['group_id'])
        name = await bot.get_chat(full_info['group_id'])
        name = name.title
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text.sub_tg(name), reply_markup=keyboard, parse_mode="Markdown")

    if "tgcheck_" in call.data:
        group_id = call.data.split("_")[1]
        print(group_id)
        try:
            chat_member = await bot.get_chat_member(group_id, call.from_user.id)
            if chat_member.status in ['member', 'administrator', 'creator']:
                print("true")
                await db.add_balance(call.from_user.id, 30)
                await db_coll.create_entry(user_id=call.from_user.id, platform_id=group_id, platform_type="tg")
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text.fine_task, reply_markup=kb.fine_task(), parse_mode="Markdown")
            else:
                print("false")
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text.not_fine_task, reply_markup=kb.back_kb_tasks_earn(), parse_mode="Markdown")
        except Exception as e:
            # Если у бота нет доступа к информации о члене чата или пользователь не найден
            print(e)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text.inactive, reply_markup=kb.back_kb_tasks(), parse_mode="Markdown")
            await db_coll.create_entry(user_id=call.from_user.id, platform_id=group_id, platform_type="tg")
    if "tgskip_" in call.data:
        group_id = call.data.split("_")[1]
        await db_coll.create_entry(user_id=call.from_user.id, platform_id=group_id, platform_type="tg")
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text.skip, reply_markup=kb.back_kb_tasks(), parse_mode="Markdown")

# Обработчик состояния для ввода ссылки на группу
@bot.message_handler(state=GroupRegistrationStates.group_link)
async def group_link_input(message):
    # Сохраняем введенную ссылку
    group_link = message.text
    # Переключаемся на состояние для ввода user_id группы
    await bot.set_state(message.from_user.id, GroupRegistrationStates.group_user_id, message.chat.id)
    await bot.send_message(message.chat.id, "Please enter the user_id of the group:")
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['group_link'] = group_link

# Обработчик состояния для ввода user_id группы
@bot.message_handler(state=GroupRegistrationStates.group_user_id)
async def group_user_id_input(message):
    # Получаем введенные данные
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        group_link = data.get('group_link')
        group_user_id = data['group_user_id'] = message.text

    # Формируем текст сообщения с введенными данными
    response_message = f"Group link: {group_link}\nGroup user ID: {group_user_id}"

    # Создаем InlineKeyboardMarkup с кнопкой "add" и зеленой галочкой
    
    
    # Отправляем сообщение с данными и клавиатурой
    await bot.send_message(message.chat.id, response_message, reply_markup=kb.markup_add_tg())

    # Удаляем состояние
    # await bot.delete_state(message.from_user.id, message.chat.id)

@bot.message_handler(content_types=['text', 'photo'], state=mailState.text)
async def text_and_photo_received(message: Message):
    print("full_right")
    # Получаем текст и фотографию из сообщения
    if message.content_type == "photo":
        if message.caption:
            text = message.caption
        else:
            text = None
        photo = message.photo[-1].file_id  # Берем последнюю фотографию из списка
        await bot.send_photo(chat_id=message.from_user.id, caption=text, photo=photo, reply_markup=kb.sender())
    elif message.content_type == "text":
        photo = None
        text = message.text
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=kb.sender())
    # Сохраняем данные в состояние
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['text'] = text
        data['photo'] = photo

    print(text, photo)
    # await bot.delete_state(message.from_user.id, message.chat.id)


# register filters

bot.add_custom_filter(asyncio_filters.StateFilter(bot))
bot.add_custom_filter(asyncio_filters.IsDigitFilter())

asyncio.run(bot.polling(skip_pending=True)) 

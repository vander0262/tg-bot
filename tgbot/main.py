from pyrogram import Client, filters
from pyrogram.types import ForceReply
import config
import keyboards
import random
from randint
from FusionBrain_AI import generate
import base64

bot = Client(
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    name="jmqBOT"

)

def button_filter(button):
   async def func(_, __, msg):
       return msg.text == button.text
   return filters.create(func, "ButtonFilter", button=button)

@bot.on_message(filters.command("start"))
async def start(bot, message):
    await message.reply("сап" ,
                        reply_markup=keyboards.kb_main
)
    await bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAENWNhnYuZ4ooauRO5tinsFWLsWrCZzhQACwBEAAmcaoErrkdFHd0JoDDYE")


query_text = "Введите запрос для генерации"
@bot.on_message(button_filter(keyboards.btn_image))
async def image_command(bot, message):
    await message.reply(query_text, reply_markup=ForceReply(True))

@bot.on_message(filters.reply)
async def reply(bot, message):
    if message.reply_to_message.text == query_text:
        query = message.text
        await message.reply_text(f"Генерирую изображение по запросу **{query}**...")
        images = await generate(query)
        if images:
            image_data = base64.b64decode(images[0])
            img_num = random.randint(1, 99)
            with open(f"images/image{img_num}.jpg", "wb") as file:
                file.write(image_data)
            await bot.send_photo(message.chat.id, f"images/image{img_num}.jpg",
                                        reply_to_message_id=message.id,
                                        reply_markup=keyboards.kb_main)
        else:
            await message.reply_text("ошибка, попробуй еще раз",
                                        reply_to_message_id=message.id,
                                        reply_markup=keyboards.kb_main)


@bot.on_message(filters.command("image"))
async def image(bot, message):
    print(1)
    if len(message.text.split()) > 1:
        query = message.text.replace("/images", "")
        await message.reply_text(f"генерирую изображение '{query}', подождите...")
        images = await generate(query)
        print(2)
        if images:
            print(3)
            image_data = base64.b64decode(images[0])
            with open(f"images/image.jpg", "wb") as file:
                file.write(image_data)
            await bot.send_photo(message.chat.id, f"images/image.jpg",
                                            reply_to_message_id=message.id)
            print(1)
        else:
            await message.reply_text("ошибка, попробуй еще раз",
                                        reply_to_message_id=message.id)
    else:
        await message.reply_text("введите запрос")

@bot.on_message(filters.command("info") | button_filter(keyboards.btn_info))
async def info(bot, message):
    await message.reply("тут описание что может этот бот")


@bot.on_message(filters.command("time"))
async def start(bot, message):
 pass



@bot.on_message(filters.command("gnumberss") | button_filter(keyboards.btn_gnumber))
async def gnumberss(bot, message):
    await message.reply(" выбери число от 1 до 100 через команду '/num' ")

@bot.on_message(filters.command("number"))
async def replyy(bot, message):
    secret_number = int(message.text.replace("/number", ""))
    guess = random.randint(1, 100)
    if guess < secret_number:
        await message.reply("Слишком низкое! Попробуй еще раз.")
    elif guess > secret_number:
        await message.reply("Слишком высокое! Попробуй еще раз.")
    else:
        await message.reply("Поздравляю! Ты угадал число! 🎉")

@bot.on_message(filters.command("game") | button_filter(keyboards.btn_games))
async def game(bot, message):
    await message.reply("твой ход", reply_markup=keyboards.kb_rps)

@bot.on_message(button_filter(keyboards.btn_rock) |
                button_filter(keyboards.btn_scissors) |
                button_filter(keyboards.btn_paper) )


async def choice_rps(bot, message):
    rock = keyboards. btn_rock .text
    scissors = keyboards.btn_scissors.text
    paper = keyboards.btn_paper.text
    user = message.text
    pc = random.choice([rock, scissors, paper])

    if user == pc:
        await message.reply("Ничья")
    elif (user == rock and pc == scissors) or (user == scissors and pc == paper) or (user == paper and pc == rock):
        await message.reply(f"Ты ВЫИГРАЛ. Бот выбрал{pc}",
                        reply_markup=keyboards.kb_rps)
    else:
        await message.reply(f"Ты проиграл. Бот выбрал {pc}",
                        reply_markup=keyboards.kb_rps)

@bot.on_message (filters.command("quest") | button_filter(keyboards.btn_quest))
async def kvest(bot, message):
    await message.reply_text("Хотите отправиться в путешествие?",
                             reply_markup=keyboards.inline_kb_start_quest)

@bot.on_callback_query()
async def handle_query(bot, query):
    await query.message.delete()
    if query.data == "start_quest":
        await bot.answer_callback_query(query.id,
            text="Добро пожаловать на квест",
            show_alert=True)

        await query.message.reply_text("какую дверь выберешь?",
                                       reply_markup=keyboards.inline_kb_choice_door)
    elif query.data == "left_door":
        await query.message.reply_text("Ты заходишь в дверь и видишь зомби, что ты сделаешь?",
                                       reply_markup=keyboards.inline_kb_left_door)
    elif query.data == "right_door":
        await query.message.reply_text("Ты заходишь в дверь и у тя 2 предмета, какой ты возьмешь?",
                                       reply_markup=keyboards.inline_kb_right_door)

    elif query.data == "zomb":
        await bot.answer_callback_query(query.id, text="Ты сражаешься с зомби, но он тя кусает и ты умираешь",
                                        show_alert=True)
    elif query.data == "run":
        await bot.answer_callback_query(query.id, text="Ты находишь камень и кидаешь его в сторону, спокойно проходя дальше",
                                        show_alert=True)
    elif query.data == "toy":
        await bot.answer_callback_query(query.id, text="Ты берешь игрушку для своей дочери, дочь очень счастлива, но у тя появляется язва желудка от недостатка еды",
                                        show_alert=True)
    elif query.data == "food":
        await bot.answer_callback_query(query.id, text="Ты берешь еду и вам с дочерью хватит его точно на месяц!",
                                        show_alert=True)
bot.run()
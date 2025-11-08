import telebot
import requests

# SENING TOKENING
TOKEN = "8587931835:AAHYZT3WCUbkokRF8OwBrFpfA522y0nYRw0"

# PAYME HISOB RAQAMING (o‘z raqamingni shu yerga yoz)
PAYME_LINK = "https://payme.uz/998901234567"  # <--- BU YERGA O‘Z PAYME RAQAMINGNI QO‘Y!

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, """
🚀 *Salom! Men Saytchi AI – 15 sekundda sayt yasayman!*

Misol uchun yozing:
"Toshkentda restoran ochyapman, sayt yasab ber"
yoki
"Onlayn do‘kon, telefon: +998 99 123 45 67"

Men darrov tayyor sayt beraman! 💻

💸 Narx: 99 000 so‘m (bir martalik)
💳 To‘lov: Payme, Click, Uzum

Hozir sinab ko‘ring! 👇
    """, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_text = message.text
    bot.reply_to(message, "⏳ Sayt tayyorlanmoqda... 20 sekund kutib turing!")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": "Bearer gsk_2FHJ0KQZJ8C9nZ7t1234567890abcdef",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.1-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": """Sen o‘zbek tilida sayt yasaydigan AI dizainersan. 
                Foydalanuvchi nima xohlasa, shu haqida zamonaviy, mobilga mos, o‘zbek tilida to‘liq sayt kodini ber.
                Faqat HTML + CSS + JS ichida, hech qanday tashqi link yo‘q. 
                Chiroyli dizayn, kontakt forma, telefon tugmasi bo‘lsin.
                Oxirida: "Sayt tayyor! To‘lovdan keyin saytchi.uz/domendingiz tayyor bo‘ladi" deb yoz."""
            },
            {"role": "user", "content": user_text}
        ],
        "temperature": 0.7,
        "max_tokens": 4000
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        ai_response = response.json()['choices'][0]['message']['content']

        bot.send_message(message.chat.id, "🎉 *Saytingiz tayyor!*", parse_mode="Markdown")
        bot.send_message(message.chat.id, ai_response, parse_mode="HTML")

        markup = telebot.types.InlineKeyboardMarkup()
        pay_button = telebot.types.InlineKeyboardButton("💸 99 000 so‘m to‘lash", url=PAYME_LINK)
        markup.add(pay_button)
        bot.send_message(message.chat.id, f"""
💳 To‘lov qiling va men darrov saytni domen bilan ulayman!

Payme: {PAYME_LINK}
Izohda: @{message.from_user.username}

To‘lov kelishi bilan saytchi.uz sayti tayyor bo‘ladi!
        """, reply_markup=markup, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, "❌ Xatolik yuz berdi. Qayta urining yoki /start bosing.")

print("🤖 @SaytchiBot ishga tushdi...")
bot.infinity_polling()

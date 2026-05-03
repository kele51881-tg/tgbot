import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from openai import OpenAI

load_dotenv()

# ================== 配置区（改这里就行）==================
TELEGRAM_TOKEN = "5354775688:AAHSVVi7cj1esoj60gdZ6l292nyic4k4bpM"
XINYUAN_API_KEY = "sk-Ez9J9BoBjZ0Jn1ImSgpop5VOuiA8IhKgsxx9hsX9rBnqFOAt"
BOT_USERNAME = "@kelefish_bot"   # 比如 @MySuperAIBot

# 鑫源API 配置（OpenAI 完全兼容）
client = OpenAI(
    api_key=XINYUAN_API_KEY,
    base_url="https://xinyuanai666.com/v1"   # ← 关键在这里！
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    text = message.text.lower()
    user_text = message.text

    # 只在私聊、@机器人、或回复机器人时才回答（防刷屏）
    if (message.chat.type == "private" or
        BOT_USERNAME.lower() in text or
        (message.reply_to_message and message.reply_to_message.from_user.username == BOT_USERNAME.replace("@", ""))):

        # 调用鑫源API
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",          # ← 这里改模型！推荐先用这个便宜又快
                # 其他可选模型示例：
                # "gpt-4o" / "claude-3-5-sonnet" / "gemini-2.0-flash" / "deepseek-r1" / "qwen-max"
                messages=[
                    {"role": "system", "content": "你是一个幽默、聪明、乐于助人的AI助手，用中文回复用户。"},
                    {"role": "user", "content": user_text}
                ],
                temperature=0.8,
                max_tokens=1024
            )
            ai_reply = response.choices[0].message.content
        except Exception as e:
            ai_reply = f"哎呀，出错了：{str(e)[:100]}... 稍后再试～"

        await message.reply_text(ai_reply)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 机器人已启动（使用鑫源API）...")
    app.run_polling()

if __name__ == "__main__":
    main()

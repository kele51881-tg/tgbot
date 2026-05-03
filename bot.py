import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

            response = client.chat.completions.create(
                model="gemini-3.1-flash-lite-preview",          # ← 这里改模型！推荐先用这个便宜又快
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

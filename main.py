# 導入Discord.py模組
import discord
from discord import app_commands
import random
import csv
import logging

# read env variables
import os
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("TOKEN")
channel_id = int(os.environ.get("CHANNEL_ID"))



def load_messages_from_csv(file_path):
    messages = []
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            messages.append({
                "title": row["title"],
                "message": row["message"],
                "final": row["final"]
            })
    return messages

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
console_handler = logging.StreamHandler()
logging.basicConfig(handlers=[handler, console_handler], level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')

# Example usage
csv_file_path = "./message.csv"
string_list = load_messages_from_csv(csv_file_path)
message_id = 0

# client是跟discord連接，intents是要求機器人的權限
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
client = discord.Client(intents=intents)

def get_sea_string():
    random.shuffle(string_list)  # 隨機打亂字串陣列
    return string_list[0] # 回傳第一個字串

class SeaButtonHandler(discord.ui.Button):
    def __init__(self, label, style):
        super().__init__(label=label, style=style)

    async def callback(self, interaction: discord.Interaction):

        message = get_sea_string()

        embed=discord.Embed(title=message["title"], description="➤ "+message["message"], color=0x007bff)
        embed.set_author(name="海港事件")

        final_lines = message["final"].split("-----")
        final_text = "\n".join(f"- {line.strip()}" for line in final_lines)
        embed.add_field(name="事件結果", value=final_text, inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        # print("Button clicked!")

class JobButtonHandler(discord.ui.Button):
    def __init__(self, label, style):
        super().__init__(label=label, style=style)

    async def callback(self, interaction: discord.Interaction):
        new_view = discord.ui.View(timeout=30)
        new_view.add_item(SeaButtonHandler(label="海港", style=discord.ButtonStyle.success))
        await interaction.response.send_message("> 去跳海吧", view=new_view, ephemeral=True)

# 調用event函式庫
@client.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {client.user}")
    
    channel = client.get_channel(channel_id)  # Fetch the channel using its ID
    if channel:
        async for msg in channel.history(limit=None):
            await msg.delete()
        
        await send_view()
    else:
        print("Channel not found!")

@client.event
async def on_resumed():
    await on_ready()

@client.event
async def on_error(event, *args, **kwargs):
    print(f"發生錯誤: {event} {args} {kwargs}")

async def edit_resend_view():
    global message_id  # 明確宣告使用全域變數
    channel = client.get_channel(channel_id)

    if channel:
        view = discord.ui.View()
        view.clear_items()
        view.add_item(JobButtonHandler(label="工作", style=discord.ButtonStyle.primary))

        async def on_timeout():
            print("View 已超時，重新生成按鈕。")
            await edit_resend_view()
        
        view.on_timeout = on_timeout
        sent_message = await channel.fetch_message(message_id)
        new_message = await sent_message.edit(view=view)
        message_id = new_message.id
        print("Message sent to channel!")

async def send_view():
    global message_id  # 明確宣告使用全域變數
    channel = client.get_channel(channel_id)

    if channel:
        view = discord.ui.View()
        view.clear_items()
        view.add_item(JobButtonHandler(label="工作", style=discord.ButtonStyle.primary))

        async def on_timeout():
            if channel:
                print("View 已超時，重新生成按鈕。")
                await edit_resend_view()
        
        view.on_timeout = on_timeout
        sent_message = await channel.send(file=discord.File("CountryState.png"), view=view)
        message_id = sent_message.id
        print("Message sent to channel!")
    else:
        print("Channel not found!")

client.run(token, log_handler=handler, log_level=logging.INFO)

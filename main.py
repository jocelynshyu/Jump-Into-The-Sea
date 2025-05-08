# 導入Discord.py模組
import discord
from discord import app_commands
import random
import csv
import logging

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
channel_id = 0000000000000000

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
        embed.add_field(name="事件結果", value="• "+message["final"], inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        # print("Button clicked!")

class JobButtonHandler(discord.ui.Button):
    def __init__(self, label, style):
        super().__init__(label=label, style=style)

    async def callback(self, interaction: discord.Interaction):
        new_view = discord.ui.View(timeout=30)
        new_view.add_item(SeaButtonHandler(label="海港", style=discord.ButtonStyle.success))
        await interaction.response.send_message("> 去跳海吧", view=new_view, ephemeral=True)

# client是跟discord連接，intents是要求機器人的權限
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)

# 調用event函式庫
@client.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {client.user}")
    view = discord.ui.View()
    view.clear_items()
    view.add_item(JobButtonHandler(label="工作", style=discord.ButtonStyle.primary))
    channel = client.get_channel(channel_id)  # Fetch the channel using its ID
    if channel:
        async for msg in channel.history(limit=None):
            await msg.delete()
        await channel.send(file=discord.File("CountryState_Yiguo.png"), view=view)
        print("Message sent to channel!")
    else:
        print("Channel not found!")

@client.event
async def on_resumed():
    await on_ready()

# @client.event
# 當頻道有新訊息
# async def on_message(message):
#     # 排除機器人本身的訊息，避免無限循環
#     if message.author == client.user:
#         return
    
#     if message.channel.id != channel_id:
#         return

#     # 新訊息包含Hello，回覆Hello, world!
#     if message.content == "Hello":
#         await send_view(message.channel)

@client.event
async def on_error(event, *args, **kwargs):
    print(f"發生錯誤: {event} {args} {kwargs}")

async def send_view(channel):
    # 創建一個 View，並設置 30 秒超時
    view = discord.ui.View(timeout = 30)
    # 添加一個 Button 到 View 中 

    # Replace the existing button with the custom ButtonHandler
    view.clear_items()
    view.add_item(JobButtonHandler(label="工作", style=discord.ButtonStyle.primary))
    await channel.send(file=discord.File("CountryState_Yiguo.png"), view=view)


client.run("你的Discord機器人token",log_handler=handler,log_level=logging.INFO)

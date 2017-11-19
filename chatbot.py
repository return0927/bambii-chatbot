import discord  # 디스코드 모듈
import general_settings  # 설정관리 모듈

Setting = general_settings.Settings()  # 설정 불러오기

app = discord.Client()  # 챗봇 지정


# --- 이벤트영역 ---
# 봇 레디
@app.event
async def on_ready():
    print(app.user.name, "(%s)" % app.user.id)
    await app.change_presence(game=discord.Game(name="Afreeca 밤비TV", type=0))


# 메세지
@app.event
async def on_message(message):
    print("Channel: %s(%s) | Author: %s(#%s) | Message: %s" % (
        message.channel, message.channel.id[:5],
        message.author.name, message.author.id[:5],
        message.content
    ))


# 봇 실행
app.run(Setting.token)

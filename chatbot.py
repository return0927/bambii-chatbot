import asyncio
import random
import discord  # 디스코드 모듈
import requests
from bs4 import BeautifulSoup as bs

import general_settings  # 설정관리 모듈

Setting = general_settings.Settings()  # 설정 불러오기

app = discord.Client()  # 챗봇 지정

bot_deleting = False

# --- 이벤트영역 ---
# 봇 레디
@app.event
async def on_ready():
    print(app.user.name, "(%s)" % app.user.id)
    await app.change_presence(game=discord.Game(name="Afreeca 밤비TV", type=0))


# 메세지
@app.event
async def on_message(message):
    if message.author.id == app.user.id: return

    print("Channel: %s(%s) | Author: %s(#%s) | Message: %s" % (
        message.channel, message.channel.id[:5],
        message.author.name, message.author.id[:5],
        message.content
    ))

    # 안내
    if "!유튜브" == message.content:
        await app.send_message(message.channel, "https://www.youtube.com/channel/UCSIdQo4-_eWYaiksJp18vQA")  # 비동기 프로그래밍
    if "!방송국" == message.content:
        await app.send_message(message.channel, "http://afreecatv.com/snowdrop1223")  # 비동기 프로그래밍
    if "!카페" == message.content:
        await app.send_message(message.channel, "http://cafe.naver.com/bambiittv")  # 비동기 프로그래밍

    # Google 이미지 보내기
    if "!검색" == message.content.split(" ")[0]:
        group = message.content.split(" ")[1]

        google_data = requests.get("https://www.google.co.kr/search?q=" + group + "&dcr=0&source=lnms&tbm=isch&sa=X")
        soup = bs(google_data.text, "html.parser")
        imgs = soup.find_all("img")

        await app.send_message(message.channel, random.choice(imgs[1:])['src'])

        del group, google_data, soup, imgs


    if "!익명" == message.content.split(" ")[0]:
        global bot_deleting

        msg = " ".join(message.content.split(" ")[1:])
        channel = message.channel

        bot_deleting = True
        await app.delete_message(message)
        bot_deleting = False

        await app.send_message(channel, msg)


# 메세지가 수정되었을 때
@app.event
async def on_message_edit(before, after):
    return

    outstring = ''
    outstring += " -- 메세지 수정이 있습니다 --" + "\n"
    outstring += " 작성자:" + before.author.name + "  메세지 작성시간:" + str(before.timestamp) + "  메세지 수정시간:" + str(
        after.edited_timestamp) + "\n"
    outstring += " 변경 전 내용:" + before.content + "\n"
    outstring += " 변경 후 내용:" + after.content + "\n"

    await app.send_message(before.channel, outstring)


# 메세지가 삭제되었을 때
@app.event
async def on_message_delete(message):
    global bot_deleting
    if bot_deleting: return
    if message.author.id == app.user.id: return

    msg = await app.send_message(message.channel, "<@%s> 왜 지우고 그래,,, 내가 이미 다 봤거든,," % message.author.id)
    await asyncio.sleep(5)  # --> 메세지를 기다리면서 5초간 멈춤 // time.sleep(5) --> 아무것도 안하면서 5초간 멈춤
    await app.delete_message(msg)
    del msg


# 새로운 멤버가 입장했을 때
@app.event
async def on_member_join(member):
    await app.send_message(app.get_channel("379288158954586113"), "반갑다우, <@%s> 동무!" % member.id)


# 봇 실행
app.run(Setting.token)

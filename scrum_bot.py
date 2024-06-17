import os
import datetime
import discord
from discord.ext import tasks
from dotenv import load_dotenv

### Environments ###
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

KOREA = datetime.timezone(datetime.timedelta(hours=9)) # UTC + 9
WEEKDAY = ['월','화','수','목','금','토','일']


### Discord Bot Logic ###
class MyClient(discord.Client):
  async def on_ready(self): # bot 실행 시 발생할 이벤트
    self.channel = self.get_channel(int(CHANNEL_ID)) # 채널 연결
    await self.change_presence(status=discord.Status.online) # 온라인 표시
    self.daily_scrum.start() # 데일리 스크럼 반복 시작

  @tasks.loop(time=datetime.time(hour=10, minute=0, second=0, tzinfo=KOREA)) # 반복할 시간: 10AM
  async def daily_scrum(self):
    thread_list = self.channel.threads # 기존 outdated 스레드를 받아와서 닫는다.
    for t in thread_list:
      await t.edit(archived=True)

    now = datetime.datetime.now() # 현재 시각

    if now.weekday() < 5: # 0-4 월-금요일만 동작
      year = now.year
      month = now.month
      day = now.day
      weekday = WEEKDAY[now.weekday()]

      tname = '📢 ' + str(year) + '년 ' + str(month) + '월 ' + str(day) + '일 (' + weekday + ') 데일리 스크럼 📢'
      tmsg = '@everyone 데일리 스크럼을 작성해 주세요!\n```어제 한 일\n- 일 1\n- 일 2\n\n오늘 할 일\n- 일 1\n- 일 2```'
      thread = await self.channel.create_thread(name=tname, auto_archive_duration=1440, type=discord.ChannelType.public_thread) # 스레드 생성
      await thread.send(tmsg)


### Run Discord Bot ###
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(BOT_TOKEN)
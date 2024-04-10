from WeiboBot import Bot
from WeiboBot.const import *
import asyncio
import datetime
import time
import re
import os
from hots import get_random_hot
from request import ask_openai

async def main():
    while True:  # 无限循环
        now = datetime.datetime.now()
        if now.hour == int(os.environ.get('HOTS')):
            question = get_random_hot()
        elif now.hour == int(os.environ.get('GENKI')):
            question = ""
        else:
            time.sleep(3600)
            continue
        myBot = Bot(cookies=os.environ.get('WEIBO_COOKIE'))
        await myBot.login()  # 登录
        for i in range(3):
            content = ask_openai(question)
            if content is not None:
                break
        if content is not None:
            tags = re.findall('#(.*?)#', question)
            if len(tags) > 0:
                content = "#" + tags[0] + "#" + content
            await myBot.post_weibo(content, visible=VISIBLE.ALL)  # 发布微博
        await myBot.close()  # 关闭浏览器
        time.sleep(3600)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

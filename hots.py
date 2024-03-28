import requests
from time import sleep
from lxml import html
import re
import os
import random 

def process_string(s):
    s = re.sub(r'\s', '', s)  # 去除空白字符
    # title = re.findall('#(.*?)#', s)
    # s = re.sub(r'#.*?#', '', s)  # 去除#...#之间的内容
    s = re.sub(r'【.*?】', '', s)  # 去除【...】之间的内容
    s = re.sub(r'L.*?视频', '', s)  # 去除"L...视频"之间的内容
    s = re.sub(r'收起.*?d$', '', s)  # 去除最后的"收起...d"
    return s

skip_words = [
    "军队", "军人",
    "国家", "政府",
    "乳房", "胸部",
]
etree = html.etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Cookie': ""
}

def get_hot_list(url):
    '''
    微博热搜页面采集，获取详情页链接后，跳转进入详情页采集
    :param url: 微博热搜页链接
    :return: None
    '''
    headers['Cookie'] = os.environ.get('WEIBO_COOKIE')
    page_text = requests.get(url=url, headers=headers).text
    tree = etree.HTML(page_text)
    tr_list = tree.xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr')
    all_bos = {}
    for tr in tr_list[1:21]:
        parse_url = tr.xpath('./td[2]/a/@href')[0]
        detail_url = 'https://s.weibo.com' + parse_url
        title = tr.xpath('./td[2]/a/text()')[0]
        try:
            rank = tr.xpath('./td[1]/text()')[0]
            hot = tr.xpath('./td[2]/span/text()')[0]
        except:
            rank = '置顶'
            hot = '置顶'
        bos = get_detail_page(detail_url, title, rank, hot)
        if bos is not None:
            all_bos.update(bos)
    return all_bos

def get_detail_page(detail_url, title, rank, hot):
    '''
    根据详情页链接，解析所需页面数据，并保存到全局变量 all_df
    :param detail_url: 详情页链接
    :param title: 标题
    :param rank: 排名
    :param hot: 热度
    :return: None
    '''
    try:
        page_text = requests.get(url=detail_url, headers=headers).text
    except:
        return None
    bos = {}
    tree = etree.HTML(page_text)
    # 爬取3条热门评论信息
    for i in range(1, 4):
        try:
            comment_time = tree.xpath(f'//*[@id="pl_feedlist_index"]/div[4]/div[{i}]/div[2]/div[1]/div[2]/p[1]/a/text()')[0]
            comment_time = re.sub('\s','',comment_time)
            user_name = tree.xpath(f'//*[@id="pl_feedlist_index"]/div[4]/div[{i}]/div[2]/div[1]/div[2]/p[2]/@nick-name')[0]
            forward_count = tree.xpath(f'//*[@id="pl_feedlist_index"]/div[4]/div[{i}]/div[2]/div[2]/ul/li[1]/a/text()')[1]
            forward_count = forward_count.strip()
            comment_count = tree.xpath(f'//*[@id="pl_feedlist_index"]/div[4]/div[{i}]/div[2]/div[2]/ul/li[2]/a/text()')[0]
            comment_count = comment_count.strip()
            like_count = tree.xpath(f'//*[@id="pl_feedlist_index"]/div[4]/div[{i}]/div[2]/div[2]/ul/li[3]/a/button/span[2]/text()')[0]
            comment = tree.xpath(f'//*[@id="pl_feedlist_index"]/div[4]/div[{i}]/div[2]/div[1]/div[2]/p[2]//text()')
            comment = ' '.join(comment).strip()
            comment = process_string(comment)
            flag = False
            for word in skip_words:
                if word in comment:
                    flag = True
                    break
            if flag:
                continue
            bos[title] = comment
        except Exception as e:
            # print(e)
            continue
    return bos

def get_random_hot():
    url = 'https://s.weibo.com/top/summary?cate=realtimehot'
    res = get_hot_list(url)
    key, value = random.choice(list(res.items()))
    # return "标题："+ key + "。内容：" + value
    return value

if __name__ == '__main__':
    url = 'https://s.weibo.com/top/summary?cate=realtimehot'
    res = get_hot_list(url)
    key, value = random.choice(list(res.items()))
    print("标题："+ key + "。内容：" + value)
    # all_df.to_excel('exam.xlsx', index=False)

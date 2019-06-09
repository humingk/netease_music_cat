# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
全局变量配置文件

"""
# ============基本信息=====================

# 需要爬取的用户的ID
user_id = "55494140"
base_url = "http://music.163.com/"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
host = "music.163.com"
language = "zh-CN,zh;q=0.9,en;q=0.8"
accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"

# ============数据库信息=======================

database_user_name = "root"
database_user_pwd = "1233"
database_name = "music"
database_charset = "utf8mb4"

table_user_name = "users"
table_user_cols_temp = {
    "user_name": "",
    "user_id": "",
    "comment_id": ""
}
table_user_cols = ",".join(table_user_cols_temp.keys())

table_comment_name = "comments"

table_comment_cols_temp = {
    "comment_id": "",
    "comment_song_name": "",
    "comment_content": "",
    "comment_time": ""
}
table_comment_cols = ",".join(table_comment_cols_temp.keys())

# 数据库操作，待集成
"""

CREATE DATABASE IF NOT EXISTS music DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_general_ci

CREATE TABLE comments (
  comment_num int PRIMARY key auto_increment,
  comment_id varchar(50) CHARACTER SET utf8mb4  NOT NULL,
  comment_song_name varchar(500) CHARACTER SET utf8mb4 NOT NULL,
  comment_content text(1000) CHARACTER SET utf8mb4  NOT NULL,
  comment_time datetime NOT NULL,
  unique key(comment_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4

CREATE TABLE users (
  user_num int PRIMARY key auto_increment,
  user_name varchar(500) CHARACTER SET utf8mb4 NOT NULL,
  user_id varchar(50) CHARACTER SET utf8mb4 NOT NULL,
  comment_id varchar(50) CHARACTER SET utf8mb4 NOT NULL,
  KEY comment_id (comment_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4

自增量起始值恢复为0
alter table users AUTO_INCREMENT=0
alter table comments AUTO_INCREMENT=0

交叉查询操作
SELECT users.user_name,comments.comment_content,comments.comment_time 
FROM users,comments
where user_name= "z09488" and users.comment_id=comments.comment_id
group by comments.comment_id;


"""
# ============解密信息=======================

user_cookie = "appver=1.5.0.75771;"

# 当前页评论页数
page_offset = "0"

# 评论页数限制
page_limit = "100"

# 根据core.js找到四个加密参数param
# first_param = "{rid:\"\", offset:" + str(page_offset) + ", total:\"true\", limit:" + str(
#     page_limit) + ", csrf_token:\"\"}"
first_param = "{rid:\"\", offset:\"0\", total:\"true\", limit:" + page_limit + ", csrf_token:\"\"}"
second_param = "010001"
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
forth_param = "0CoJUm6Qyw8W8jud"

# 排行榜cookie
cookie_ranklist = "iuqxldmzr_=32; WM_TID=iVI9x7km0Hnxl06D55xE0Zk%2F%2FMdwj0Zi; __utmz=94650624.1532444533.18.9.utmcsr=anjingwd.github.io|utmccn=(referral)|utmcmd=referral|utmcct=/AnJingwd.github.io/2017/08/19/%E5%A6%82%E4%BD%95%E4%BC%98%E9%9B%85%E7%9A%84%E7%94%9F%E6%88%90python%E5%B5%8C%E5%A5%97%E5%AD%97%E5%85%B8/; _ntes_nnid=2c566b51ddc165a326744e0503a2205d,1532534319105; _ntes_nuid=2c566b51ddc165a326744e0503a2205d; __utmc=94650624; JSESSIONID-WYYY=HAuFkIf%2BwYQmdf07n1i41pF%5Ch5DhafY1jFGxBc9uka2TJpv%2BWn%2BOJoh%5C4zlt8r5grWfkxQY%2Boi8%5CSKiZC1nNBDf2I43bg6wfnO3IpdseS%2BqFDPN%2BfGi7WqR8hgBcOKM7G4%5Cg56GO0%5C8Ts%2BsjdG6cWGWCVVe08TTgpVD%5CZIlqh%5CfUH2W0%3A1532597076858; WM_NI=X8pxijMhfASbItvnUcS0vU0yQ9ixB6Jp%2F2oZp1Sx543w4J3HnBgHcqq1VXzCN3Zf27yh4VwwgXhj9shbdgqcVkDsAO5rq7Vsf9V%2BlewnDVVxrmZFsMbBTIyplXucd2SzT0M%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb4c548bc9ab9b0cc47b5ec8db8e139ed8c9bafc94a90f100d6e63ba6babe86dc2af0fea7c3b92a9ce8c099ec628fb8aaa2d26a8bacba8fd86991f0bab6b37393e7a799c13e8ab0e1d3ee52b4ef9d99b840f1a9fcabb244ae9ea9a9e27bb3ef9ab9f9498eed9687b13dbbb8fcb7f67da588a88bbc79acbeac88f46996b58c94c445f7aebfd8d579a6e79accef6fb5b28cb7d574b2b396a7f247a29e9caafc7cb088bb84e73a91a69cd1d037e2a3; __utma=94650624.454371702.1531313810.1532586731.1532596127.25; __utmb=94650624.17.10.1532596127"

# 排行榜params
params_ranklist = "phHyJWqRgsgameCszoYt9DZHVdhIkrVrNY+WwIGv+84cdpi2I/W+ncdikcelNCc/Fv10nFX6BZkKMco5UkfGHEWI26ROmDckb/4j+60NfDmoNmZ2HBzMeuabKndea8Dro2rDHAB72cPXSy4uWsrOZvKNxRSKbKtTzEisPcYg4cElX57QksNky58hrGQ5TBYh"

# 排行榜encSecKey
encSecKey_ranklist = "a1670bbd1582893885a7bfe42c1cfd11d7844e81b5f6d385bb84d648fc248a6e806643b723d9cbe9bd6a51d0bf9ff13e11b213b5779be120e4bd34b89c29cf05cae543500cbdbdfb1cad33663743bfe5ce5157f38558e35e1e3d5a0f9c1cb6ab17cee6ca8e4aaf224351463b88618864e06ae9666c6e5b9e959af1be8a1a0512"

# 首页歌单cookie
cookie_play_lists="_iuqxldmzr_=32; WM_TID=iVI9x7km0Hnxl06D55xE0Zk%2F%2FMdwj0Zi; __utmz=94650624.1532444533.18.9.utmcsr=anjingwd.github.io|utmccn=(referral)|utmcmd=referral|utmcct=/AnJingwd.github.io/2017/08/19/%E5%A6%82%E4%BD%95%E4%BC%98%E9%9B%85%E7%9A%84%E7%94%9F%E6%88%90python%E5%B5%8C%E5%A5%97%E5%AD%97%E5%85%B8/; _ntes_nnid=2c566b51ddc165a326744e0503a2205d,1532534319105; _ntes_nuid=2c566b51ddc165a326744e0503a2205d; __utmc=94650624; JSESSIONID-WYYY=HAuFkIf%2BwYQmdf07n1i41pF%5Ch5DhafY1jFGxBc9uka2TJpv%2BWn%2BOJoh%5C4zlt8r5grWfkxQY%2Boi8%5CSKiZC1nNBDf2I43bg6wfnO3IpdseS%2BqFDPN%2BfGi7WqR8hgBcOKM7G4%5Cg56GO0%5C8Ts%2BsjdG6cWGWCVVe08TTgpVD%5CZIlqh%5CfUH2W0%3A1532597076858; WM_NI=X8pxijMhfASbItvnUcS0vU0yQ9ixB6Jp%2F2oZp1Sx543w4J3HnBgHcqq1VXzCN3Zf27yh4VwwgXhj9shbdgqcVkDsAO5rq7Vsf9V%2BlewnDVVxrmZFsMbBTIyplXucd2SzT0M%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb4c548bc9ab9b0cc47b5ec8db8e139ed8c9bafc94a90f100d6e63ba6babe86dc2af0fea7c3b92a9ce8c099ec628fb8aaa2d26a8bacba8fd86991f0bab6b37393e7a799c13e8ab0e1d3ee52b4ef9d99b840f1a9fcabb244ae9ea9a9e27bb3ef9ab9f9498eed9687b13dbbb8fcb7f67da588a88bbc79acbeac88f46996b58c94c445f7aebfd8d579a6e79accef6fb5b28cb7d574b2b396a7f247a29e9caafc7cb088bb84e73a91a69cd1d037e2a3; __utma=94650624.454371702.1531313810.1532586731.1532596127.25; __utmb=94650624.17.10.1532596127"
# 首页歌单params
params_play_lists="phHyJWqRgsgameCszoYt9DZHVdhIkrVrNY+WwIGv+84cdpi2I/W+ncdikcelNCc/Fv10nFX6BZkKMco5UkfGHEWI26ROmDckb/4j+60NfDmoNmZ2HBzMeuabKndea8Dro2rDHAB72cPXSy4uWsrOZvKNxRSKbKtTzEisPcYg4cElX57QksNky58hrGQ5TBYh",
# 首页encSecKey
encSecKey_play_lists="a1670bbd1582893885a7bfe42c1cfd11d7844e81b5f6d385bb84d648fc248a6e806643b723d9cbe9bd6a51d0bf9ff13e11b213b5779be120e4bd34b89c29cf05cae543500cbdbdfb1cad33663743bfe5ce5157f38558e35e1e3d5a0f9c1cb6ab17cee6ca8e4aaf224351463b88618864e06ae9666c6e5b9e959af1be8a1a0512"


# ==============IPProxy模块================

DBName = "proxies.db"  # 数据库名称
TabelName = "IPPORT"  # 表
Column1 = "IP_PORT"  # 列1

TestTimeOut = 1  # 检测IP可用性设置的超时，
# 对IP质量要求不高，就把值设的高一点儿。这样可用IP就会增多
MaxThreads = 512  # 最大线程数，依据电脑性能修改，性能好的电脑可以设置高一点
# 最好设置为2的n次方，别问我为什么，我也不知道，这是玄学

TestUrl = "https://www.baidu.com/"  # 用以检测的网站

# 代理IP网址和对应的正则式，正则式一定要IP和Port分开获取，例如[(192.168.1.1,80),(192.168.1.1,90),]
# 可自行添加
# 只抓取首页，想要抓取后面的可以将链接和正则式贴上来
Url_Regular = {
    "http://www.xicidaili.com/nn/": "<td>([\d\.]+)</td>\s*<td>(\d+)</td>",
    "http://www.kuaidaili.com/free/": "IP\">([\d\.]+)</td>\s*<td data-title=\"PORT\">(\d+)</td>",
    "http://www.66ip.cn/nmtq.php?getnum=512&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=0&proxytype=2&api=66ip": "([\d\.]+):(\d+)",
    "http://www.ip3366.net/free/": "<td>([\d\.]+)</td>\s*<td>(\d+)</td>",
    "http://www.proxy360.cn/Region/China": ">\s*([\d\.]+)\s*</span>\s*.*width:50px;\">\s*(\d+)\s*</span>",
    "http://www.mimiip.com/": "<tr>\s+<td>([\d\.]+)</td>\s+<td>(\d+)</td>",
    "http://www.data5u.com/free/index.shtml": "<li>([\d\.]+)</li></span>\s+<span style=\"width: 100px;\"><li class=\".*\">(\d+)</li>",
    "http://www.ip181.com/": "<tr.*>\s+<td>([\d\.]+)</td>\s+<td>([\d]+)</td>",
    "http://www.kxdaili.com/": "<tr.*>\s+<td>([\d\.]+)</td>\s+<td>([\d]+)</td>",
}

# 头部代理S
UserAgents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12",
    "Opera/9.27 (Windows NT 5.2; U; zh-cn)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13",
    "Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 ",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 ",
    "Mozilla/5.0 (Linux; U; Android 3.2; ja-jp; F-01D Build/F0001) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13 ",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; ja-jp) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B117 Safari/6531.22.7",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; da-dk) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5 ",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-US) AppleWebKit/530.9 (KHTML, like Gecko) Chrome/ Safari/530.9 ",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36"
]

## 前言

本项目实现网易云音乐的某一首歌下的所有评论进行爬取，亦可对某一个歌单下的所有音乐的评论进行爬取，甚至对某一个用户在网易云音乐中的所有评论进行爬取。

- 产品总体效果：mysql中采用sql语句查询。
- 产品功能：对某一个用户在网易云音乐中的所有评论进行爬取。
- 用户特征：网易云音乐重度用户。
- 约束：用户是否开启所有评论可查看、听歌排行是否可查看。 
- 假设与依赖关系：  
    - 只有听歌排行是否可查看开启，才能爬虫分析。
    - 无论所有评论可查看是否开启，都可爬虫分析。

![获取隐私权限允许]({{site.url}}/img/netease/first_permission.png)

## 效果图

![爬取到的结果]({{site.url}}/img/netease/final_all.png)

![对某用户进行搜索]({{site.url}}/img/netease/final_person.png)

![用户评论搜索所占比]({{site.url}}/img/netease/final_person_persent.png)

## 项目总体设计

![项目结构图]({{site.url}}/img/netease/structure.png)

## 项目详细设计

### 六个模块

1. Config模块：用户信息、数据库信息、页面解密信息。
2. Comment模块：获取每一首歌的所有评论信息。  
集成了歌单获取模块、排行榜获取模块、网页信息解密模块、歌单所有歌曲信息获取模块等等。
3. Playlist模块：某个歌单中所有的歌曲信息。  
传入歌单的ID信息，可以爬虫指定歌单界面所有的歌曲的ID，名称，类别，歌手ID，歌手名称，收录的专辑等等。
4. play_lists模块：某个用户主页所有的歌单信息。  
传入用户的ID信息，可以爬虫指定用户界面所有的歌单的ID，名称，类别，创建时间等等。
5. rank模块：某个用户主页“最近一周”和“所有时间”排行榜中所有的歌曲信息。  
传入用户的ID信息，可以爬虫指定用户主页所有排行榜中的歌曲的ID，名称，类别，歌手ID，歌手名称，收录的专辑等等。
6. decrypt模块：params和encSecKey参数信息。  
传入某首歌下某一页的页码等信息，通过crypto模块中的AES解密，可以对网易云音乐服务器端进行POST请求。
 
### 关键代码

#### 获取评论

```python
    com = comment()
    user_id = config.user_id

    # 用户首页听歌排行榜所有歌
    print("正在爬取【所有时间】排行榜...")
    print("正在爬取【最近一周】排行榜...")
    rank_songs = com.ranklist.get_ranklists_id(user_id)

    # 用户首页所有歌单
    print("正在爬取用户的歌单...")
    playlists_id = com.play_lists.get_lists_id(user_id)

    # 用户首页所有歌单的歌
    playlists_songs = []
    for i in range(len(playlists_id)):
        playlist_songs = com.playlist.get_playlist_songs_id(playlists_id[i])
        playlists_songs.extend(playlist_songs)

    # 整合所有的歌
    all_songs_2 = []
    all_songs_2.extend(rank_songs)
    all_songs_2.extend(playlists_songs)

    # 去除列表中重复的歌
    all_songs = []
    for i in all_songs_2:
        if not i in all_songs:
            all_songs.append(i)
    print("正在提取用户最可能评论的歌曲信息...")

    # 多进程
    # 代理IP库初始化
    p1 = multiprocessing.Process(target=ProxiesDataBase.InitDB())
    p1.start()
    # 代理IP库刷新
    p2 = multiprocessing.Process(target=com.flash)
    p2.start()

    #进程池
    songs_sum = len(all_songs)
    pool=multiprocessing.Pool(processes=200)
    for i in range(len(all_songs)):
        print("======================================")
        print("正在爬取中... 当前第 " + str(i) + " 首,共计 " + str(songs_sum) + " 首")
        pool.apply_async(com.get_comments,(all_songs[i],))
        pool.apply_async(com.mysql_save)
    pool.close()
    pool.join()
    com.mysql_save()
```


#### 获取某首歌下所有的评论

```python
# 获取song_id这首歌下所有的评论
    def get_comments(self, song):

        song_id = song["song_id"]
        song_name = song["song_name"]

        print("ID:    " + str(song_id))
        print("歌名:  " + str(song_name))

        # 获取第一页中header中的Form Data数据项
        first_param = config.first_param
        params_obj_1 = decrypt.get_params(first_param)
        encSecKey_obj_1 = decrypt.get_encSecKey()

        url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_" + str(song_id) + "?csrf_token="

        # 代理IP
        print("正在验证代理IP中...")
        Util.Refresh()
        # 查询IP数据库多少条数据
        conn = sqlite3.connect(config.DBName)
        cu = conn.cursor()
        ip_num = cu.execute("""SELECT * FROM {};""".format(config.TabelName)).fetchall().__len__()
        print("共 " + str(ip_num) + " 个代理IP可用...")
        cu.close()
        conn.close()

        proxies = Util.Get()
        print("匿名IP代理成功...")
        print("ip: " + str(proxies["http"]))

        # 获取第一页中response中的json数据项
        json_text_1 = decrypt.get_json(url, params_obj_1, encSecKey_obj_1, proxies)
        json_obj_1 = json.loads(json_text_1)

        # 获取第一页的置顶评论
        if json_obj_1["topComments"]:
            for item in json_obj_1["topComments"]:
                self.dict_save(item, song_name)

        # 获取第一页的热门评论
        if json_obj_1["hotComments"]:
            for item in json_obj_1["hotComments"]:
                self.dict_save(item, song_name)

        # 评论总数
        self.comment_sum = int(json_obj_1["total"])

        # 每首歌最多20000条评论
        # 循环每一页的最新评论
        page_limit = config.page_limit
        if self.comment_sum<10000:
            for offset in range(int(page_limit), int(self.comment_sum), int(page_limit)):
                    # 若给定代理IP无法获取数据，循环执行
                    flag = True
                    while flag:
                        proxies = Util.Get()
                        flag = self.get_page_comment(proxies, offset, page_limit, url, song_name)
        else:
            # 正序10000条评论
            for offset in range(int(page_limit), 10000, int(page_limit)):
                # 若给定代理IP无法获取数据，循环执行
                flag = True
                while flag:
                    proxies = Util.Get()
                    flag = self.get_page_comment(proxies, offset, page_limit, url, song_name)
            # 倒序10000条评论
            for offset in range(int(self.comment_sum), int(self.comment_sum)-10000, -int(page_limit)):
                # 若给定代理IP无法获取数据，循环执行
                flag = True
                while flag:
                    proxies = Util.Get()
                    flag = self.get_page_comment(proxies, offset, page_limit, url, song_name)

        self.mysql_save()

```

#### 循环每一页的最新评论

```python
    # 循环每一页的最新评论
    def get_page_comment(self, proxies, offset, page_limit, url, song_name):
        try:
            param_n = "{rid:\"\", offset:" + str(
                offset) + ", total:\"false\", limit:" + page_limit + ", csrf_token:\"\"}"
            # 获取第page页中header中的Form Data数据项
            params_obj_n = decrypt.get_params(param_n)
            encSecKey_obj_n = decrypt.get_encSecKey()

            # 获取第page页中response中的json数据项
            json_text_n = decrypt.get_json(url, params_obj_n, encSecKey_obj_n, proxies)
            json_obj_n = json.loads(json_text_n)
            if json_obj_n["comments"]:
                for item in json_obj_n["comments"]:
                    self.dict_save(item, song_name)
            return False
        except Exception as e:
            return True
```

## 待重构

1. 多进程改为多线程，加入线程锁
2. 改进IP可用与不可用的切换
3. 爬取、解析、存储改为多线程进行
4. cookie的获取自动化
5. 仅存储有用信息
6. 加入自定义时间限制，超出时间不予考虑


赶工完成，还有很多地方需要花时间修改。

<a href=""><img src="https://img.shields.io/github/license/mashape/apistatus.svg" alt="license"></a>
<a href=""><img src="https://img.shields.io/badge/language-python-green.svg" alt="language"></a>

---

### **[施工] 代码重构中...**

---

## 项目简介



#### 本项目的**数据来源**为网易云音乐官方API:

- weapi
- eapi



#### 本项目**实现**：

- 网易云音乐爬虫，包括：
  
  - 某用户的排行榜 
  
  - 某用户的所有歌单  (可指定歌单种类及范围)
  
  - 某用户的所有歌单的所有歌曲  (可用于备份导出)
  
  - 某歌单的所有歌曲
  
  - 某歌曲的所有热门评论
  
  - 某歌曲的最新及最旧共计一万条评论
  
  
  
- 网易云音乐听歌报告生成，包括：(开发中...)
  
  - 某用户的听歌报告生成
  - 某用户的歌曲评论信息 (包括公开及部分未公开评论)
  - ...
  
  
  
- 网易云音乐歌曲推荐，包括: (开发中...)
  
  - 基于用户的协同过滤算法
    - 基于用户排行榜 
      - 最近一周排行榜
      - 所有时间排行榜
    - 基于用户的歌单
      - 喜欢音乐歌单
      - 创建的歌单
      - 收藏的歌单
    
    影响因子
    
    排行榜种类,歌单种类,排行榜歌曲播放量,歌单播放量,歌单标签,歌曲歌手
    
  - ...

## 安装方式

```shell
"下载到本地
git clone https://github.com/humingk/netease_music


"配置依赖包
cd netease_music
pip install -r requirements.txt 


"配置数据库
cd my_tools
mysql -uroot -p < music.sql


"配置config.py

待续...
```





## 使用方式



待续...

<a href=""><img src="https://img.shields.io/github/license/mashape/apistatus.svg" alt="license"></a>
<a href=""><img src="https://img.shields.io/badge/language-python-green.svg" alt="language"></a>

本项目实现对网易云音乐的某一首歌下的所有评论进行爬取，亦可对某一个歌单下的所有音乐的评论进行爬取，甚至对某一个用户在网易云音乐中的所有评论(仅自己可见的情况下)进行爬取。

# 使用方式

```bash
git clone https://github.com/humingk/netease_music_comments



```

# 流程图

![](image/process.png)

# 效果预览

- 获取隐私权限许可
 
![](image/permission.png)

- 爬取到的结果(数据后期可做分析用)</center>

![](image/result.png)

- 在结果中对此用户进行查询</center>

![](image/search.png)

- 查询到的评论数/实际评论数 百分比

![](image/persent.png)

# 待解决的问题

1. 多进程改为多线程，加入线程锁

2. 改进IP可用与不可用的切换

3. 爬取、解析、存储改为多线程进行

4. cookie的获取自动化

5. 考虑是否仅存储有用信息

6. 加入自定义时间限制，超出时间不予考虑
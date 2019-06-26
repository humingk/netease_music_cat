# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------

class netease_main:
    """
    网易云音乐资源的集成获取

    """


if __name__ == '__main__':
    netease_main()
    comments_total = 70
    song_comments_new_max = 50
    song_comments_old_max = 40
    song_comments_page_limit = 5

    # new_pages与old_pages不相交
    if song_comments_new_max <= comments_total - song_comments_old_max:
        new_pages = list(range(0, song_comments_new_max, song_comments_page_limit))
        old_pages = list(range(comments_total - song_comments_old_max, comments_total, song_comments_page_limit))
    # 相交
    else:
        new_pages = list(range(0, comments_total, song_comments_page_limit))
        old_pages = []


    print(new_pages)
    print(old_pages)
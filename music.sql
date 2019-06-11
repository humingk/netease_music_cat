CREATE DATABASE IF NOT EXISTS netease_music DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_general_ci;


CREATE TABLE user
(
    user_id   int(15)  NOT NULL,
    user_name char(20) NOT NULL,
    primary key (user_id),
    index (user_name)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;


CREATE TABLE user_playlist
(
    user_id     int(15) NOT NULL,
    playlist_id int(15) NOT NULL,
    primary key (user_id, playlist_id),
    foreign key (user_id) references user (user_id),
    foreign key (playlist_id) references playlist (playlist_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;


CREATE TABLE playlist
(
    playlist_id         int(15)  NOT NULL,
    playlist_name       char(20) NOT NULL,
    playlist_type       int(1)   NOT NULL,
    playlist_play_count int      NOT NULL,
    primary key (playlist_id),
    index playlist_name (playlist_name),
    index playlist_type (playlist_type),
    index playlist_play_count (playlist_play_count)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

CREATE TABLE song
(
    song_id                     int(15)  NOT NULL,
    song_name                   char(20) NOT NULL,
    song_source_type            int(1)   NOT NULL,
    playlist_song_playlist_type int(1)   NOT NULL,

    primary key (playlist_id),
    index playlist_name (playlist_name),
    index playlist_type (playlist_type),
    index playlist_play_count (playlist_play_count)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;



#
# CREATE TABLE comments
# (
#     comment_num       int PRIMARY key auto_increment,
#     comment_id        varchar(50) CHARACTER SET utf8mb4  NOT NULL,
#     comment_song_name varchar(500) CHARACTER SET utf8mb4 NOT NULL,
#     comment_content   text(1000) CHARACTER SET utf8mb4   NOT NULL,
#     comment_time      datetime                           NOT NULL,
#     unique key (comment_id)
# ) ENGINE = InnoDB
#   DEFAULT CHARSET = utf8mb4;

-- # 自增量起始值恢复为0
-- alter table users AUTO_INCREMENT=0
-- alter table comments AUTO_INCREMENT=0
--
-- # 交叉查询操作
-- SELECT users.user_name,comments.comment_content,comments.comment_time
-- FROM users,comments
-- where user_name= "xxxxxxxxxx" and users.comment_id=comments.comment_id
-- group by comments.comment_id;

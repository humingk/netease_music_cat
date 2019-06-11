CREATE DATABASE IF NOT EXISTS netease_music DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_general_ci;


CREATE TABLE user
(
    user_id   int(15)  NOT NULL,
    user_name char(20) NOT NULL,
    primary key (user_id),
    index (user_name)
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


CREATE TABLE user_playlist
(
    user_id     int(15) NOT NULL,
    playlist_id int(15) NOT NULL,
    primary key (user_id, playlist_id),
    foreign key (user_id) references user (user_id),
    foreign key (playlist_id) references playlist (playlist_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;


CREATE TABLE ranklist
(
    ranklist_id   int(15) NOT NULL auto_increment,
    ranklist_type int(1)  NOT NULL,
    primary key (ranklist_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

CREATE TABLE user_ranklist
(
    user_id     int(15) NOT NULL,
    ranklist_id int(15) NOT NULL,
    primary key (user_id, ranklist_id),
    foreign key (user_id) references user (user_id),
    foreign key (ranklist_id) references ranklist (ranklist_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;


CREATE TABLE song
(
    song_id                   int(15)  NOT NULL,
    song_name                 char(20) NOT NULL,
    song_source_type          int(1)   NOT NULL,
    song_source_playlist_type int(1)   NOT NULL,
    song_source_rank_type     int(1)   NOT NULL,
    primary key (song_id),
    index song_name (song_name)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

CREATE TABLE song_playlist
(
    song_id     int(15) NOT NULL,
    playlist_id int(15) NOT NULL,
    primary key (song_id, playlist_id),
    foreign key (song_id) references song (song_id),
    foreign key (playlist_id) references playlist (playlist_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

CREATE TABLE song_ranklist
(
    song_id     int(15) NOT NULL,
    ranklist_id int(15) NOT NULL,
    primary key (song_id, ranklist_id),
    foreign key (song_id) references song (song_id),
    foreign key (ranklist_id) references ranklist (ranklist_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

CREATE TABLE user_song
(
    user_id int(15) NOT NULL,
    song_id int(15) NOT NULL,
    primary key (user_id, song_id),
    foreign key (user_id) references user (user_id),
    foreign key (song_id) references song (song_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

CREATE TABLE comment
(
    comment_id      int(18)      NOT NULL,
    comment_content varchar(200) NOT NULL,
    comment_data    int(18)      NOT NULL,
    primary key (comment_id),
    index comment_comtent (comment_content)
) ENGINE = INNODB
  DEFAULT CHARSET = UTF8MB4;

CREATE TABLE user_comment
(
    user_id    int(15) NOT NULL,
    comment_id int(18) NOT NULL,
    primary key (user_id, comment_id),
    foreign key (user_id) references user (user_id),
    foreign key (comment_id) references comment (comment_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

CREATE TABLE song_comment
(
    song_id    int(15) NOT NULL,
    comment_id int(18) NOT NULL,
    primary key (song_id, comment_id),
    foreign key (song_id) references song (song_id),
    foreign key (comment_id) references comment (comment_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

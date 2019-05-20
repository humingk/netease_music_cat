CREATE DATABASE IF NOT EXISTS music DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE comments(
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

# 自增量起始值恢复为0
alter table users AUTO_INCREMENT=0
alter table comments AUTO_INCREMENT=0

# 交叉查询操作
SELECT users.user_name,comments.comment_content,comments.comment_time
FROM users,comments
where user_name= "xxxxxxxxxx" and users.comment_id=comments.comment_id
group by comments.comment_id;

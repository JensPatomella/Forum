
CREATE DATABASE IF NOT EXISTS webbserverprogrammering;

USE webbserverprogrammering;


CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  user_id INT NOT NULL,
  topic VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
--en updatering till posts för att commentarer ska fungera
ALTER TABLE posts
ADD COLUMN parent_post_id INT NULL,
ADD CONSTRAINT FK_Parent_Post FOREIGN KEY (parent_post_id) REFERENCES posts(id) ON DELETE CASCADE;
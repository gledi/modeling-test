CREATE TABLE `users` (
  `id`   INTEGER NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `age`  INTEGER DEFAULT NULL,
  CONSTRAINT pk_users PRIMARY KEY (`id`)
)
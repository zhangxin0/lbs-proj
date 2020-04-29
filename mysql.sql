
CREATE TABLE `user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `email` varchar(200) NOT NULL DEFAULT '',
  `phone_number` varchar(200) NOT NULL DEFAULT '',
  `first_name` varchar(200) NOT NULL DEFAULT '',
  `middle_name` varchar(200),
  `last_name` varchar(200) NOT NULL DEFAULT '',
  `mail_address` varchar(200) ,
  `occupation` varchar(2000) ,
  `user_name` varchar(200) NOT NULL DEFAULT '' ,
  `password` varchar(200) NOT NULL DEFAULT '' ,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_name`(`user_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
DROP TABLE IF EXISTS `clients`;

CREATE TABLE `clients` (
  `client_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `client_key` varchar(30) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `client_secret` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`client_id`),
  UNIQUE KEY `unique_clients_client_key` (`client_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO `clients` (`client_id`, `client_key`, `client_secret`, `status`)
VALUES
	(1,'CLIENT01','SECRET01',1),
	(2,'CLIENT02','SECRET02',1),
	(3,'CLIENT03','SECRET03',1),
	(4,'CLIENT04','SECRET04',0),
	(5,'CLIENT05','SECRET05',0);

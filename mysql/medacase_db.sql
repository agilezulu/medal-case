CREATE TABLE `athlete` (
                           `id` int unsigned NOT NULL AUTO_INCREMENT,
                           `uuid` varchar(36) NOT NULL,
                           `strava_id` int unsigned NOT NULL,
                           `slug` varchar(45) DEFAULT NULL,
                           `firstname` varchar(45) DEFAULT NULL,
                           `lastname` varchar(45) DEFAULT NULL,
                           `units` enum('mi','km') NOT NULL DEFAULT 'mi',
                           `country` varchar(45) DEFAULT NULL,
                           `city` varchar(45) DEFAULT NULL,
                           `sex` enum('M','F') DEFAULT NULL,
                           `date_fmt` varchar(45) DEFAULT NULL,
                           `photo_m` varchar(255) DEFAULT NULL,
                           `photo_l` varchar(255) DEFAULT NULL,
                           `access_token` varchar(45) DEFAULT NULL,
                           `refresh_token` varchar(45) DEFAULT NULL,
                           `expires_at` int unsigned DEFAULT NULL,
                           `total_runs` int unsigned DEFAULT '0',
                           `total_distance` int unsigned DEFAULT '0',
                           `total_medals` int unsigned DEFAULT '0',
                           `c_marathon` int unsigned DEFAULT '0',
                           `c_marathon_race` int unsigned DEFAULT '0',
                           `c_50k` int unsigned DEFAULT '0',
                           `c_50k_race` int unsigned DEFAULT '0',
                           `c_50mi` int unsigned DEFAULT '0',
                           `c_50mi_race` int unsigned DEFAULT '0',
                           `c_100k` int unsigned DEFAULT '0',
                           `c_100k_race` int unsigned DEFAULT '0',
                           `c_100mi` int unsigned DEFAULT '0',
                           `c_100mi_race` int unsigned DEFAULT '0',
                           `c_extreme` int unsigned DEFAULT '0',
                           `c_extreme_race` int unsigned DEFAULT '0',
                           `created_at` datetime DEFAULT NULL,
                           `last_run_date` datetime DEFAULT NULL,
                           PRIMARY KEY (`id`),
                           UNIQUE KEY `uuid_UNIQUE` (`uuid`),
                           UNIQUE KEY `strava_id_UNIQUE` (`strava_id`),
                           UNIQUE KEY `slug_UNIQUE` (`slug`),
                           KEY `strava_IDX` (`strava_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8_general_ci;

DROP TABLE IF EXISTS `run`;
CREATE TABLE `run` (
                       `id` int unsigned NOT NULL AUTO_INCREMENT,
                       `run_class_id` int unsigned NOT NULL,
                       `user_id` int unsigned NOT NULL,
                       `strava_id` bigint unsigned NOT NULL,
                       `name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
                       `distance` decimal(10,1) NOT NULL,
                       `moving_time` int unsigned NOT NULL,
                       `elapsed_time` int unsigned NOT NULL,
                       `total_elevation_gain` decimal(6,1) DEFAULT NULL,
                       `start_date` datetime NOT NULL,
                       `start_date_local` datetime NOT NULL,
                       `utc_offset` decimal(9,1) DEFAULT NULL,
                       `timezone` varchar(45) COLLATE utf8mb4_general_ci DEFAULT NULL,
                       `location_country` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL,
                       `average_heartrate` decimal(5,1) DEFAULT NULL,
                       `average_cadence` decimal(4,1) DEFAULT NULL,
                       `race` tinyint unsigned NOT NULL,
                       `summary_polyline` text COLLATE utf8mb4_general_ci,
                       PRIMARY KEY (`id`),
                       KEY `run_class_fk_idx` (`run_class_id`),
                       KEY `user_fk` (`user_id`),
                       CONSTRAINT `run_class_fk` FOREIGN KEY (`run_class_id`) REFERENCES `run_class` (`id`),
                       CONSTRAINT `user_fk` FOREIGN KEY (`user_id`) REFERENCES `athlete` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `run_class`;
CREATE TABLE `run_class`
(
    `id`   int unsigned NOT NULL AUTO_INCREMENT,
    `name` varchar(45) DEFAULT NULL,
    `key`  varchar(45) DEFAULT NULL,
    `min`  int unsigned NOT NULL,
    `max`  int NOT NULL,
    `parent` enum('marathon', 'ultra') NOT NULL DEFAULT 'marathon',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8_general_ci;

INSERT INTO `run_class` (`name`, `key`, `min`, `max`, `parent`) values ('Marathon', 'c_marathon', 26, 29, 'marathon');
INSERT INTO `run_class` (`name`, `key`, `min`, `max`, `parent`) values ('50k', 'c_50k', 29, 48, 'ultra');
INSERT INTO `run_class` (`name`, `key`, `min`, `max`, `parent`) values ('50mi', 'c_50mi', 48, 58, 'ultra');
INSERT INTO `run_class` (`name`, `key`, `min`, `max`, `parent`) values ('100k', 'c_100k', 58, 68, 'ultra');
INSERT INTO `run_class` (`name`, `key`, `min`, `max`, `parent`) values ('100k+', 'c_100kplus', 68, 98, 'ultra');
INSERT INTO `run_class` (`name`, `key`, `min`, `max`, `parent`) values ('100mi', 'c_100mi', 98, 110, 'ultra');
INSERT INTO `run_class` (`name`, `key`, `min`, `max`, `parent`) values ('Xtreme', 'c_xtreme', 110, 1000, 'ultra');

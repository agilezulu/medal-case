CREATE TABLE `athlete`
(
    `id`              int unsigned NOT NULL AUTO_INCREMENT,
    `uuid`            varchar(36) NOT NULL,
    `strava_id`       int unsigned NOT NULL,
    `slug`            varchar(45)  DEFAULT NULL,
    `firstname`       varchar(45)  DEFAULT NULL,
    `lastname`        varchar(45)  DEFAULT NULL,
    `units`           enum('mi','km') NOT NULL DEFAULT 'mi',
    `country`         varchar(45)  DEFAULT NULL,
    `city`            varchar(45)  DEFAULT NULL,
    `sex`             enum('M','F') DEFAULT NULL,
    `date_fmt`        varchar(45)  DEFAULT NULL,
    `photo_m`         varchar(255) DEFAULT NULL,
    `photo_l`         varchar(255) DEFAULT NULL,
    `access_token`    varchar(45)  DEFAULT NULL,
    `refresh_token`   varchar(45)  DEFAULT NULL,
    `expires_at`      int unsigned DEFAULT NULL,
    `total_runs`      int unsigned DEFAULT NULL,
    `c_marathon`      int unsigned DEFAULT NULL,
    `c_marathon_race` int unsigned DEFAULT NULL,
    `c_50k`           int unsigned DEFAULT NULL,
    `c_50k_race`      int unsigned DEFAULT NULL,
    `c_50mi`          int unsigned DEFAULT NULL,
    `c_50mi_race`     int unsigned DEFAULT NULL,
    `c_100k`          int unsigned DEFAULT NULL,
    `c_100k_race`     int unsigned DEFAULT NULL,
    `c_100mi`         int unsigned DEFAULT NULL,
    `c_100mi_race`    int unsigned DEFAULT NULL,
    `c_extreme`       int unsigned DEFAULT NULL,
    `c_extreme_race`  int unsigned DEFAULT NULL,
    `created_at`      datetime     DEFAULT NULL,
    `last_run_date`   datetime     DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uuid_UNIQUE` (`uuid`),
    UNIQUE KEY `strava_id_UNIQUE` (`strava_id`),
    UNIQUE KEY `slug_UNIQUE` (`slug`),
    KEY               `strava_IDX` (`strava_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `run`
(
    `id`                   int unsigned NOT NULL AUTO_INCREMENT,
    `user_id`              int unsigned NOT NULL,
    `strava_id`            int unsigned NOT NULL,
    `name`                 varchar(255)  DEFAULT NULL,
    `distance`             decimal(10, 1) unsigned NOT NULL,
    `moving_time`          int unsigned NOT NULL,
    `elapsed_time`         int unsigned NOT NULL,
    `total_elevation_gain` decimal(6, 1) DEFAULT NULL,
    `start_date`           datetime NOT NULL,
    `start_date_local`     datetime NOT NULL,
    `utc_offset`           decimal(9, 1) DEFAULT NULL,
    `timezone`             varchar(45)   DEFAULT NULL,
    `location_country`     varchar(128)  DEFAULT NULL,
    `average_heartrate`    decimal(5, 1) DEFAULT NULL,
    `average_cadence`      decimal(4, 1) DEFAULT NULL,
    `race`                 tinyint(1) NOT NULL,
    `summary_polyline`     text,
    `athlete`              varchar(45)   DEFAULT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `user_fk` FOREIGN KEY (`id`) REFERENCES `athlete` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

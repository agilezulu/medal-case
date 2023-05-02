-- MySQL dump 10.13  Distrib 8.0.26, for macos11 (x86_64)
--
-- Host: 127.0.0.1    Database: medalcase
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `athlete`
--

DROP TABLE IF EXISTS `athlete`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `athlete` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `uuid` varchar(36) NOT NULL,
  `strava_id` bigint unsigned NOT NULL DEFAULT '0',
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
  `c_100k_plus` int DEFAULT '0',
  `c_100k_plus_race` int DEFAULT '0',
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `run`
--

DROP TABLE IF EXISTS `run`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `run` (
  `strava_id` bigint unsigned NOT NULL,
  `run_class_id` int unsigned NOT NULL,
  `user_id` int unsigned NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `distance` decimal(10,1) NOT NULL,
  `moving_time` int unsigned NOT NULL,
  `elapsed_time` int unsigned NOT NULL,
  `total_elevation_gain` decimal(6,1) DEFAULT NULL,
  `start_date` datetime NOT NULL,
  `start_date_local` datetime NOT NULL,
  `utc_offset` decimal(9,1) DEFAULT NULL,
  `timezone` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `start_latlng` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `location_country` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `location_city` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `average_heartrate` decimal(5,1) DEFAULT NULL,
  `average_cadence` decimal(4,1) DEFAULT NULL,
  `race` tinyint unsigned NOT NULL,
  `summary_polyline` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  PRIMARY KEY (`strava_id`),
  UNIQUE KEY `strava_id_UNIQUE` (`strava_id`),
  KEY `run_class_fk_idx` (`run_class_id`),
  KEY `user_fk` (`user_id`),
  CONSTRAINT `run_class_fk` FOREIGN KEY (`run_class_id`) REFERENCES `run_class` (`id`),
  CONSTRAINT `user_fk` FOREIGN KEY (`user_id`) REFERENCES `athlete` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `run_class`
--

DROP TABLE IF EXISTS `run_class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `run_class` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `key` varchar(45) DEFAULT NULL,
  `min` int unsigned NOT NULL,
  `max` int NOT NULL,
  `parent` enum('marathon','ultra') NOT NULL DEFAULT 'marathon',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `run_class`
--

LOCK TABLES `run_class` WRITE;
/*!40000 ALTER TABLE `run_class` DISABLE KEYS */;
INSERT INTO `run_class` VALUES (1,'26.2','c_marathon',26,29,'marathon'),(2,'50k','c_50k',29,48,'ultra'),(3,'50mi','c_50mi',48,58,'ultra'),(4,'100k','c_100k',58,68,'ultra'),(5,'100k+','c_100kplus',68,98,'ultra'),(6,'100mi','c_100mi',98,110,'ultra'),(7,'Xtreme','c_xtreme',110,1000,'ultra');
/*!40000 ALTER TABLE `run_class` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-25 22:09:01

-- MySQL dump 10.13  Distrib 5.7.28, for Linux (x86_64)
--
-- Host: localhost    Database: central_dogma
-- ------------------------------------------------------
-- Server version	5.7.28-0ubuntu0.18.04.4

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `game_sessions`
--

DROP TABLE IF EXISTS `game_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game_sessions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(100) NOT NULL,
  `start_time` timestamp NOT NULL,
  `owner_id` int(11) NOT NULL,
  `end_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_code` (`code`),
  KEY `fk_sess_owner` (`owner_id`),
  CONSTRAINT `fk_sess_owner` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_sessions`
--

LOCK TABLES `game_sessions` WRITE;
/*!40000 ALTER TABLE `game_sessions` DISABLE KEYS */;
INSERT INTO `game_sessions` VALUES (3,'isbretreat2019','2019-10-03 15:00:00',1,'2019-10-21 06:59:00');
/*!40000 ALTER TABLE `game_sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hyperlink_log`
--

DROP TABLE IF EXISTS `hyperlink_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hyperlink_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `url` varchar(1000) NOT NULL,
  `visited_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_link_visitor` (`user_id`),
  CONSTRAINT `fk_link_visitor` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hyperlink_log`
--

LOCK TABLES `hyperlink_log` WRITE;
/*!40000 ALTER TABLE `hyperlink_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `hyperlink_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_game_log`
--

DROP TABLE IF EXISTS `user_game_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_game_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `session_id` int(11) DEFAULT NULL,
  `level_id` varchar(100) NOT NULL,
  `score` int(11) NOT NULL,
  `sent_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `accuracy` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_gl_user` (`user_id`),
  KEY `fk_gl_session` (`session_id`),
  CONSTRAINT `fk_gl_session` FOREIGN KEY (`session_id`) REFERENCES `game_sessions` (`id`),
  CONSTRAINT `fk_gl_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_game_log`
--

LOCK TABLES `user_game_log` WRITE;
/*!40000 ALTER TABLE `user_game_log` DISABLE KEYS */;
INSERT INTO `user_game_log` VALUES (22,4,3,'0',200,'2019-10-03 20:58:01',50),(23,4,3,'1',200,'2019-10-03 20:58:15',50),(24,4,3,'2',0,'2019-10-03 21:01:47',0),(25,4,3,'0',400,'2019-10-03 21:02:14',100),(26,4,3,'1',0,'2019-10-03 21:02:28',0),(27,4,3,'2',0,'2019-10-03 21:03:18',0),(28,4,3,'2',200,'2019-10-03 21:06:41',50),(29,4,3,'0',400,'2019-10-04 17:50:35',100),(30,4,3,'1',400,'2019-10-04 17:50:50',100),(31,4,3,'2',0,'2019-10-04 18:05:17',0),(32,4,3,'0',400,'2019-10-04 20:41:45',100),(33,4,3,'1',300,'2019-10-04 20:42:00',75),(34,4,3,'0',400,'2019-10-04 20:44:08',100),(35,4,3,'1',100,'2019-10-04 20:44:23',25);
/*!40000 ALTER TABLE `user_game_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_question_log`
--

DROP TABLE IF EXISTS `user_question_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_question_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `answer_option` varchar(10) NOT NULL,
  `correctness` int(11) NOT NULL,
  `session_id` int(11) DEFAULT NULL,
  `answered_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_uql_user` (`user_id`),
  KEY `fk_uql_session` (`session_id`),
  CONSTRAINT `fk_uql_session` FOREIGN KEY (`session_id`) REFERENCES `game_sessions` (`id`),
  CONSTRAINT `fk_uql_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_question_log`
--

LOCK TABLES `user_question_log` WRITE;
/*!40000 ALTER TABLE `user_question_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_question_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `grade` int(11) DEFAULT NULL,
  `gender` char(1) DEFAULT NULL,
  `hash` varchar(512) DEFAULT NULL,
  `salt` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_uname` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin',6,'m','$argon2id$v=19$m=102400,t=2,p=8$1gJcj+O0KVRna9ERS6nFHA$hr8n/jX+4suouipyCAzoaA','6oQSBt2KOJJkpmGMqILGM0J3BR+WG1iggdBzjN32Pgo='),(4,'someone',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-12-04 13:57:06

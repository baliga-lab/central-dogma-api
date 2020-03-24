-- MySQL dump 10.13  Distrib 5.7.29, for Linux (x86_64)
--
-- Host: localhost    Database: central_dogma
-- ------------------------------------------------------
-- Server version	5.7.29-0ubuntu0.18.04.1

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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_sessions`
--

LOCK TABLES `game_sessions` WRITE;
/*!40000 ALTER TABLE `game_sessions` DISABLE KEYS */;
INSERT INTO `game_sessions` VALUES (3,'isbretreat2019','2019-10-03 15:00:00',1,'2019-10-21 06:59:00'),(4,'mysession','2020-03-16 22:04:32',1,NULL);
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
-- Table structure for table `level_types`
--

DROP TABLE IF EXISTS `level_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `level_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `level_types`
--

LOCK TABLES `level_types` WRITE;
/*!40000 ALTER TABLE `level_types` DISABLE KEYS */;
INSERT INTO `level_types` VALUES (1,'dna_replication'),(2,'codon_transcription');
/*!40000 ALTER TABLE `level_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `levels`
--

DROP TABLE IF EXISTS `levels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `levels` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `finished_at` timestamp NULL DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `process` int(11) DEFAULT NULL,
  `level_type` int(11) DEFAULT NULL,
  `speed` int(11) DEFAULT NULL,
  `rotational` int(11) DEFAULT NULL,
  `missed` int(11) DEFAULT NULL,
  `correct` int(11) DEFAULT NULL,
  `num_errors` int(11) DEFAULT NULL,
  `num_total` int(11) DEFAULT NULL,
  `level_num` int(11) DEFAULT NULL,
  `session_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `levels`
--

LOCK TABLES `levels` WRITE;
/*!40000 ALTER TABLE `levels` DISABLE KEYS */;
INSERT INTO `levels` VALUES (5,'2020-03-17 23:16:27',1,1,1,42,0,10,5,0,15,1,4,13,490),(6,'2020-03-18 00:12:38',1,1,1,42,0,8,7,0,15,1,4,13,606);
/*!40000 ALTER TABLE `levels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `processes`
--

DROP TABLE IF EXISTS `processes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `processes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `processes`
--

LOCK TABLES `processes` WRITE;
/*!40000 ALTER TABLE `processes` DISABLE KEYS */;
INSERT INTO `processes` VALUES (1,'dna replication');
/*!40000 ALTER TABLE `processes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_options`
--

DROP TABLE IF EXISTS `question_options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `question_options` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) DEFAULT NULL,
  `content` varchar(500) DEFAULT NULL,
  `option_num` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_options`
--

LOCK TABLES `question_options` WRITE;
/*!40000 ALTER TABLE `question_options` DISABLE KEYS */;
INSERT INTO `question_options` VALUES (5,2,'Click on the choice to select it',1),(6,2,'Then click submit to submit it.',2),(7,2,'A, B, and C are wrong.',3),(8,2,'Select me! I\'m the right answer.',4);
/*!40000 ALTER TABLE `question_options` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_types`
--

DROP TABLE IF EXISTS `question_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `question_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_types`
--

LOCK TABLES `question_types` WRITE;
/*!40000 ALTER TABLE `question_types` DISABLE KEYS */;
INSERT INTO `question_types` VALUES (1,'drag and drop'),(2,'multiple choice');
/*!40000 ALTER TABLE `question_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `questions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_type` int(11) DEFAULT NULL,
  `worth` int(11) DEFAULT NULL,
  `prompt` varchar(500) DEFAULT NULL,
  `correct_option` int(11) DEFAULT NULL,
  `game_session_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
INSERT INTO `questions` VALUES (2,2,200,'Every level you\'ll be given a challenge question. They can be either drag and drop, or multiple choice formats.',3,4);
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_results`
--

DROP TABLE IF EXISTS `quiz_results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_results` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `answered_at` timestamp NULL DEFAULT NULL,
  `question_id` int(11) DEFAULT NULL,
  `attempts` int(11) DEFAULT NULL,
  `num_questions_asked` int(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_results`
--

LOCK TABLES `quiz_results` WRITE;
/*!40000 ALTER TABLE `quiz_results` DISABLE KEYS */;
INSERT INTO `quiz_results` VALUES (1,'2020-03-24 17:13:30',2,1,1,200,13);
/*!40000 ALTER TABLE `quiz_results` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_game_log`
--

LOCK TABLES `user_game_log` WRITE;
/*!40000 ALTER TABLE `user_game_log` DISABLE KEYS */;
INSERT INTO `user_game_log` VALUES (36,6,NULL,'0',1500,'2019-12-13 23:29:30',NULL),(37,6,NULL,'2',1000,'2019-12-14 00:49:23',NULL),(38,7,NULL,'level1',12345,'2020-01-16 19:11:32',NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin',6,'m','$argon2id$v=19$m=102400,t=2,p=8$1gJcj+O0KVRna9ERS6nFHA$hr8n/jX+4suouipyCAzoaA','6oQSBt2KOJJkpmGMqILGM0J3BR+WG1iggdBzjN32Pgo='),(4,'someone',NULL,NULL,NULL,NULL),(6,'weiju',NULL,NULL,NULL,NULL),(7,'user',NULL,NULL,NULL,NULL),(8,'wise-gray-turkey-ak-k_8-prefer_not_to_say-mysession',NULL,NULL,NULL,NULL),(9,'heroic-violet-narwhal-ak-k_8-prefer_not_to_say-mysession',NULL,NULL,NULL,NULL),(10,'strong-red-kookabura-ak-k_8-prefer_not_to_say-mysession',NULL,NULL,NULL,NULL),(11,'wise-indigo-kudu-ak-k_8-prefer_not_to_say-mysession',NULL,NULL,NULL,NULL),(12,'encouraging-blue-finch-ak-k_8-prefer_not_to_say-mysession',NULL,NULL,NULL,NULL),(13,'heroic-orange-dinosaur-ak-k_8-prefer_not_to_say-mysession',NULL,NULL,NULL,NULL);
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

-- Dump completed on 2020-03-24 14:04:11

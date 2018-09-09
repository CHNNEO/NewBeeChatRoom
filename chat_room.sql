-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: localhost    Database: chat_room
-- ------------------------------------------------------
-- Server version	5.7.22-0ubuntu0.16.04.1

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
-- Table structure for table `1_flist`
--

DROP TABLE IF EXISTS `1_flist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `1_flist` (
  `id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(16) CHARACTER SET utf8 NOT NULL,
  `ip` varchar(15) CHARACTER SET utf8 NOT NULL DEFAULT '0',
  `isOnline` enum('在线','离开','忙碌','请勿打扰','隐身','离线') CHARACTER SET utf8 NOT NULL DEFAULT '在线',
  `isDelete` enum('Y','N') CHARACTER SET utf8 DEFAULT 'N',
  `headimg` varchar(12) CHARACTER SET utf8 DEFAULT '1.png'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `1_flist`
--

LOCK TABLES `1_flist` WRITE;
/*!40000 ALTER TABLE `1_flist` DISABLE KEYS */;
INSERT INTO `1_flist` VALUES (0,'1','0','在线','N','30.png');
/*!40000 ALTER TABLE `1_flist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `g_flist`
--

DROP TABLE IF EXISTS `g_flist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `g_flist` (
  `id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(16) CHARACTER SET utf8 NOT NULL,
  `ip` varchar(15) CHARACTER SET utf8 NOT NULL DEFAULT '0',
  `isOnline` enum('在线','离开','忙碌','请勿打扰','隐身','离线') CHARACTER SET utf8 NOT NULL DEFAULT '在线',
  `isDelete` enum('Y','N') CHARACTER SET utf8 DEFAULT 'N',
  `headimg` varchar(12) CHARACTER SET utf8 DEFAULT '1.png'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `g_flist`
--

LOCK TABLES `g_flist` WRITE;
/*!40000 ALTER TABLE `g_flist` DISABLE KEYS */;
INSERT INTO `g_flist` VALUES (0,'g','0','在线','N','30.png');
/*!40000 ALTER TABLE `g_flist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gg_flist`
--

DROP TABLE IF EXISTS `gg_flist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gg_flist` (
  `id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(16) CHARACTER SET utf8 NOT NULL,
  `ip` varchar(15) CHARACTER SET utf8 NOT NULL DEFAULT '0',
  `isOnline` enum('在线','离开','忙碌','请勿打扰','隐身','离线') CHARACTER SET utf8 NOT NULL DEFAULT '在线',
  `isDelete` enum('Y','N') CHARACTER SET utf8 DEFAULT 'N',
  `headimg` varchar(12) CHARACTER SET utf8 DEFAULT '1.png'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gg_flist`
--

LOCK TABLES `gg_flist` WRITE;
/*!40000 ALTER TABLE `gg_flist` DISABLE KEYS */;
INSERT INTO `gg_flist` VALUES (0,'gg','0','在线','N','30.png');
/*!40000 ALTER TABLE `gg_flist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gl_flist`
--

DROP TABLE IF EXISTS `gl_flist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gl_flist` (
  `id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(16) CHARACTER SET utf8 NOT NULL,
  `ip` varchar(15) CHARACTER SET utf8 NOT NULL DEFAULT '0',
  `isOnline` enum('在线','离开','忙碌','请勿打扰','隐身','离线') CHARACTER SET utf8 NOT NULL DEFAULT '在线',
  `isDelete` enum('Y','N') CHARACTER SET utf8 DEFAULT 'N',
  `headimg` varchar(12) CHARACTER SET utf8 DEFAULT '1.png'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gl_flist`
--

LOCK TABLES `gl_flist` WRITE;
/*!40000 ALTER TABLE `gl_flist` DISABLE KEYS */;
INSERT INTO `gl_flist` VALUES (0,'gl','0','在线','N','30.png'),(0,'gg','0','在线','N','2.png');
/*!40000 ALTER TABLE `gl_flist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group_format`
--

DROP TABLE IF EXISTS `group_format`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group_format` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(16) NOT NULL,
  `isOnline` enum('在线','离开','忙碌','请勿打扰','隐身','离线') NOT NULL DEFAULT '在线',
  `isDelete` enum('Y','N') DEFAULT 'N',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group_format`
--

LOCK TABLES `group_format` WRITE;
/*!40000 ALTER TABLE `group_format` DISABLE KEYS */;
/*!40000 ALTER TABLE `group_format` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `groups_info`
--

DROP TABLE IF EXISTS `groups_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `groups_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `g_name` varchar(16) NOT NULL,
  `isDelete` enum('Y','N') DEFAULT 'N',
  PRIMARY KEY (`id`),
  UNIQUE KEY `g_name` (`g_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `groups_info`
--

LOCK TABLES `groups_info` WRITE;
/*!40000 ALTER TABLE `groups_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `groups_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `h_flist`
--

DROP TABLE IF EXISTS `h_flist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `h_flist` (
  `id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(16) CHARACTER SET utf8 NOT NULL,
  `ip` varchar(15) CHARACTER SET utf8 NOT NULL DEFAULT '0',
  `isOnline` enum('在线','离开','忙碌','请勿打扰','隐身','离线') CHARACTER SET utf8 NOT NULL DEFAULT '在线',
  `isDelete` enum('Y','N') CHARACTER SET utf8 DEFAULT 'N',
  `headimg` varchar(12) CHARACTER SET utf8 DEFAULT '1.png'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `h_flist`
--

LOCK TABLES `h_flist` WRITE;
/*!40000 ALTER TABLE `h_flist` DISABLE KEYS */;
INSERT INTO `h_flist` VALUES (0,'h','0','在线','N','30.png');
/*!40000 ALTER TABLE `h_flist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `info_format`
--

DROP TABLE IF EXISTS `info_format`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `info_format` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(16) NOT NULL,
  `ip` varchar(15) NOT NULL DEFAULT '0',
  `isOnline` enum('在线','离开','忙碌','请勿打扰','隐身','离线') NOT NULL DEFAULT '在线',
  `isDelete` enum('Y','N') DEFAULT 'N',
  `headimg` varchar(12) DEFAULT '1.png',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `info_format`
--

LOCK TABLES `info_format` WRITE;
/*!40000 ALTER TABLE `info_format` DISABLE KEYS */;
/*!40000 ALTER TABLE `info_format` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_info`
--

DROP TABLE IF EXISTS `users_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(16) NOT NULL,
  `passwd` varchar(32) NOT NULL,
  `ip` varchar(15) NOT NULL DEFAULT '0',
  `port` varchar(6) NOT NULL DEFAULT '0',
  `isOnline` enum('在线','离开','忙碌','请勿打扰','隐身','离线') NOT NULL DEFAULT '在线',
  `headimg` varchar(12) DEFAULT '1.gif',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_info`
--

LOCK TABLES `users_info` WRITE;
/*!40000 ALTER TABLE `users_info` DISABLE KEYS */;
INSERT INTO `users_info` VALUES (23,'gl','gl','0','0','请勿打扰','30.png'),(24,'gg','gg','0','0','在线','30.png'),(25,'g','g','0','0','在线','30.png'),(26,'h','h','0','0','在线','30.png'),(27,'1','1','0','0','在线','30.png');
/*!40000 ALTER TABLE `users_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-07-16 20:53:10

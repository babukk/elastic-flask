CREATE DATABASE  IF NOT EXISTS `dev-db` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `dev-db`;
-- MySQL dump 10.16  Distrib 10.1.37-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: 10.230.0.177    Database: dev-db
-- ------------------------------------------------------
-- Server version	10.3.13-MariaDB

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
-- Table structure for table `item_company_rel`
--

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (0,'root'),(1,'Administrator'),(2,'Moderator'),(3,'Worker'),(4,'Biller'),(5,'Reporter'),(6,'Sreader');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_company_rel`
--

DROP TABLE IF EXISTS `user_company_rel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_company_rel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(32) DEFAULT NULL,
  `company_id` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `first_idx` (`company_id`),
  KEY `second_idx` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_company_rel`
--

LOCK TABLES `user_company_rel` WRITE;
/*!40000 ALTER TABLE `user_company_rel` DISABLE KEYS */;
INSERT INTO `user_company_rel` VALUES (1,'ODln6GkBZAe3JCUdtbM2','OTlp6GkBZAe3JCUdrLM5');
/*!40000 ALTER TABLE `user_company_rel` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Table structure for table `user_role_rel`
--

DROP TABLE IF EXISTS `user_role_rel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_role_rel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(32) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `first_idx` (`role_id`),
  KEY `second_idx` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_role_rel`
--

LOCK TABLES `user_role_rel` WRITE;
/*!40000 ALTER TABLE `user_role_rel` DISABLE KEYS */;
INSERT INTO `user_role_rel` VALUES (1,'ODln6GkBZAe3JCUdtbM2',0);
/*!40000 ALTER TABLE `user_role_rel` ENABLE KEYS */;
UNLOCK TABLES;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-04 15:57:16

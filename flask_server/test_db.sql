-- MySQL dump 10.13  Distrib 8.0.25, for Win64 (x86_64)
--
-- Host: localhost    Database: test_db
-- ------------------------------------------------------
-- Server version	8.0.25

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
-- Table structure for table `agency`
--

DROP TABLE IF EXISTS `agency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `agency` (
  `agency_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`agency_id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agency`
--

LOCK TABLES `agency` WRITE;
/*!40000 ALTER TABLE `agency` DISABLE KEYS */;
INSERT INTO `agency` VALUES (1,'-'),(3,'House Agency'),(2,'Luxury Living');
/*!40000 ALTER TABLE `agency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat`
--

DROP TABLE IF EXISTS `chat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat` (
  `ChatId` int NOT NULL AUTO_INCREMENT,
  `FirstChatParticipantIdFk` int DEFAULT NULL,
  `SecondChatParticipantIdFk` int DEFAULT NULL,
  PRIMARY KEY (`ChatId`),
  KEY `FirstChatParticipantIdFk` (`FirstChatParticipantIdFk`),
  KEY `SecondChatParticipantIdFk` (`SecondChatParticipantIdFk`),
  CONSTRAINT `chat_ibfk_1` FOREIGN KEY (`FirstChatParticipantIdFk`) REFERENCES `participant` (`ParticipantId`),
  CONSTRAINT `chat_ibfk_2` FOREIGN KEY (`SecondChatParticipantIdFk`) REFERENCES `participant` (`ParticipantId`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat`
--

LOCK TABLES `chat` WRITE;
/*!40000 ALTER TABLE `chat` DISABLE KEYS */;
INSERT INTO `chat` VALUES (1,2,1),(2,1,10),(3,10,2),(4,11,10);
/*!40000 ALTER TABLE `chat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact`
--

DROP TABLE IF EXISTS `contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact` (
  `ContactId` int NOT NULL AUTO_INCREMENT,
  `ParticipantIdFk` int DEFAULT NULL,
  `Username` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`ContactId`),
  UNIQUE KEY `Username` (`Username`),
  KEY `ParticipantIdFk` (`ParticipantIdFk`),
  CONSTRAINT `contact_ibfk_1` FOREIGN KEY (`ParticipantIdFk`) REFERENCES `participant` (`ParticipantId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact`
--

LOCK TABLES `contact` WRITE;
/*!40000 ALTER TABLE `contact` DISABLE KEYS */;
/*!40000 ALTER TABLE `contact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `housematch_hashtag`
--

DROP TABLE IF EXISTS `housematch_hashtag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `housematch_hashtag` (
  `housematch_hashtag_id` int NOT NULL AUTO_INCREMENT,
  `hashtag_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`housematch_hashtag_id`),
  UNIQUE KEY `name_UNIQUE` (`hashtag_name`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `housematch_hashtag`
--

LOCK TABLES `housematch_hashtag` WRITE;
/*!40000 ALTER TABLE `housematch_hashtag` DISABLE KEYS */;
INSERT INTO `housematch_hashtag` VALUES (2,'Big Garden'),(3,'City center'),(1,'Close to a Park'),(4,'Close to a Subway Station'),(5,'Pet friendly'),(6,'Pool'),(7,'Quiet Location'),(8,'Sauna'),(9,'Steam bath');
/*!40000 ALTER TABLE `housematch_hashtag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interests`
--

DROP TABLE IF EXISTS `interests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interests` (
  `idinterests` int NOT NULL AUTO_INCREMENT,
  `ParticipantID` int DEFAULT NULL,
  `property_ID` int DEFAULT NULL,
  PRIMARY KEY (`idinterests`),
  KEY `propID_idx` (`property_ID`),
  CONSTRAINT `propID` FOREIGN KEY (`property_ID`) REFERENCES `properties` (`property_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interests`
--

LOCK TABLES `interests` WRITE;
/*!40000 ALTER TABLE `interests` DISABLE KEYS */;
INSERT INTO `interests` VALUES (1,15,1),(2,15,9),(4,2,2),(5,2,4),(6,14,5),(7,14,8),(8,14,9),(9,2,1),(10,3,1),(11,3,2),(12,3,4),(13,33,52),(14,33,4),(15,33,54),(16,33,53),(17,33,2);
/*!40000 ALTER TABLE `interests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `message` (
  `MessageId` int NOT NULL AUTO_INCREMENT,
  `ChatIdFk` int DEFAULT NULL,
  `ParticipantIdFk` int DEFAULT NULL,
  `Content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `Timestamp` datetime DEFAULT NULL,
  `IsNotification` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`MessageId`),
  KEY `ChatIdFk` (`ChatIdFk`),
  KEY `ParticipantIdFk` (`ParticipantIdFk`),
  CONSTRAINT `message_ibfk_1` FOREIGN KEY (`ChatIdFk`) REFERENCES `chat` (`ChatId`),
  CONSTRAINT `message_ibfk_2` FOREIGN KEY (`ParticipantIdFk`) REFERENCES `participant` (`ParticipantId`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
INSERT INTO `message` VALUES (1,1,2,'hey','2021-06-04 12:24:19',0),(2,1,1,'heyhey','2021-06-04 12:24:38',0),(3,2,1,'hi','2021-06-10 17:49:28',0),(4,2,10,'hi','2021-06-10 17:51:16',0),(5,2,1,'hi','2021-06-10 17:51:27',0),(6,2,1,'hi','2021-06-10 17:56:43',0),(7,2,10,'hi','2021-06-10 19:08:10',0),(8,1,1,'hi','2021-06-10 20:34:05',0),(9,1,1,'hi','2021-06-10 20:36:08',0),(10,3,10,'hi','2021-06-11 11:45:03',0),(12,2,10,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','2021-06-27 16:41:48',0),(13,2,10,'aaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaa','2021-06-27 16:41:59',0),(14,2,10,'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.','2021-06-27 16:42:23',0);
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `participant`
--

DROP TABLE IF EXISTS `participant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `participant` (
  `ParticipantId` int NOT NULL AUTO_INCREMENT,
  `Username` varchar(30) DEFAULT NULL,
  `Password` varchar(200) DEFAULT NULL,
  `Email` varchar(30) DEFAULT NULL,
  `IsActive` tinyint(1) DEFAULT NULL,
  `is_agent` tinyint DEFAULT NULL,
  `is_manager` tinyint DEFAULT NULL,
  `agency_fk` int DEFAULT NULL,
  `firstname` varchar(100) DEFAULT NULL,
  `lastname` varchar(100) DEFAULT NULL,
  `is_legitimate` tinyint DEFAULT '0',
  `is_disabled` tinyint DEFAULT '0',
  `is_chat_bot` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`ParticipantId`),
  UNIQUE KEY `Username` (`Username`),
  UNIQUE KEY `Email` (`Email`),
  KEY `agency_fk_idx` (`agency_fk`),
  CONSTRAINT `agency_fk` FOREIGN KEY (`agency_fk`) REFERENCES `agency` (`agency_id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `participant`
--

LOCK TABLES `participant` WRITE;
/*!40000 ALTER TABLE `participant` DISABLE KEYS */;
INSERT INTO `participant` VALUES (1,'test','gAAAAABg-EZY8LX_LhxRytkYppQQ8BBSo6NRglpZblJtt6xTtrcBGWo2Q16AaId3WTZzAjdJ8ZwfRyvzhd5xVJ2I7NVgRWhn6g==','test@web.de',0,0,0,1,'Peter','Lustig',0,0,0),(2,'test2','gAAAAABg5BsRdVdyzlyFqQJJOYzsk3jgahtt3o1h2T-nWgh0V2Bs-PnwbrQQF5x9kdwsTlgFB7XIwYLDZUzoqEXiCzoWIE4azg==','test2@web.de',0,0,0,1,'David','Witek',0,0,0),(10,'Dave','gAAAAABg3zpXnzmqe3NrZ9K8VXM_wusgKW1OAJ6wBfnPN2yW7fb4CgPHVP5HTWKkq839_2r5sIdzrt2Vi7nPZNncXT2y85VHRg==','dave@web.de',0,0,1,1,'David','Witek',0,0,0),(11,'Dave2','gAAAAABg3zpXnzmqe3NrZ9K8VXM_wusgKW1OAJ6wBfnPN2yW7fb4CgPHVP5HTWKkq839_2r5sIdzrt2Vi7nPZNncXT2y85VHRg==','dave2@web.de',0,1,0,1,'Swag','yeet',0,0,0),(12,'Dave3','gAAAAABg3zpXnzmqe3NrZ9K8VXM_wusgKW1OAJ6wBfnPN2yW7fb4CgPHVP5HTWKkq839_2r5sIdzrt2Vi7nPZNncXT2y85VHRg==','dave3@web.de',0,0,0,1,'Bla','Bla',0,0,0),(13,'test500','gAAAAABg30y-cK9ohc_BfZH6SrppP2ZiRACNyC27QM9DfnD1UZN-6qIGxvNDTRBuF51aLQLrG8sOiZJFWN1Yp6oQp2AsaC_z3A==','test500@web.de',0,0,0,1,'Test','Test2',0,0,0),(14,'elisabeth','gAAAAABg3zpXnzmqe3NrZ9K8VXM_wusgKW1OAJ6wBfnPN2yW7fb4CgPHVP5HTWKkq839_2r5sIdzrt2Vi7nPZNncXT2y85VHRg==','email@web.de',0,0,0,1,'Liz','Lustig',0,0,0),(15,'liz','gAAAAABg3zpXnzmqe3NrZ9K8VXM_wusgKW1OAJ6wBfnPN2yW7fb4CgPHVP5HTWKkq839_2r5sIdzrt2Vi7nPZNncXT2y85VHRg==','liz@m.de',0,0,0,1,'Eli','Müller',1,0,0),(22,'asd','gAAAAABg3zpXnzmqe3NrZ9K8VXM_wusgKW1OAJ6wBfnPN2yW7fb4CgPHVP5HTWKkq839_2r5sIdzrt2Vi7nPZNncXT2y85VHRg==','asd@web.de',0,1,0,3,NULL,NULL,0,0,0),(29,'crypto','gAAAAABg306hkcFBzNnk_3tiPxHXF0BgZV7QmsTOP7kXVeeODd0ijp3xPhJZCut0M8ylfVn0X06UDkKMbhamQK9Sapyj2D8DqA==','crypto@web.de',0,1,0,1,NULL,NULL,0,0,0),(30,'Chat-Bot','gAAAAABg7yQjJM6DjrBXoZXYfMBnc1fC4ohrMw1suhRsx46x288MgkKl8M8kGyRMR8Muuknn50-YctuLakAXBoLn99uvVkj-qA==','',1,0,0,1,NULL,NULL,0,0,1),(33,'Customer','gAAAAABg7yPtrNCS45QBHzhVUR5CerjlGMnsCCsBfZysNUWi7b0--PlCmOLV407WU0JmWyKqWBbNBiUTgSMjCW3amS4dfkpzYQ==','customer@web.de',1,0,0,1,NULL,NULL,0,0,0),(34,'Agent','gAAAAABg7yQjJM6DjrBXoZXYfMBnc1fC4ohrMw1suhRsx46x288MgkKl8M8kGyRMR8Muuknn50-YctuLakAXBoLn99uvVkj-qA==','agent@web.de',0,1,0,1,NULL,NULL,0,0,0),(35,'Manager','gAAAAABg7yRGt7Ec8Gm-iUy-PU5U1bqglWVaWywGuL8gZy_RBBCJOS130gSVvJ98jZ2Z974l7tkb2fhRNZZhxvFD3VxqZYlpCw==','manager@web.de',1,0,1,1,'David','Witek',0,0,0);
/*!40000 ALTER TABLE `participant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `properties`
--

DROP TABLE IF EXISTS `properties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `properties` (
  `property_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `square_meter` float DEFAULT NULL,
  `rooms` int DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL,
  `zipcode` int DEFAULT NULL,
  `street` varchar(45) DEFAULT NULL,
  `street_nr` varchar(45) DEFAULT NULL,
  `photo_path` varchar(250) DEFAULT NULL,
  `approved` tinyint DEFAULT '0',
  `agent_id_fk` int DEFAULT NULL,
  `description` varchar(45) DEFAULT NULL,
  `long_description` varchar(250) DEFAULT NULL,
  `sold` tinyint DEFAULT '0',
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`property_id`),
  KEY `agent_id_idx` (`agent_id_fk`),
  CONSTRAINT `agent_id` FOREIGN KEY (`agent_id_fk`) REFERENCES `participant` (`ParticipantId`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `properties`
--

LOCK TABLES `properties` WRITE;
/*!40000 ALTER TABLE `properties` DISABLE KEYS */;
INSERT INTO `properties` VALUES (1,'Huge Fortress',100000,450,70,'Fulda',36037,'Leipzigerstr.','123','./static/images/properties/castle.jpg',1,34,'','',0,0),(2,'Castle Eisenbach',150000,200,43,'Lauterbach',36341,'Eisenbach','3','./static/images/properties/castle2.jpg',1,34,'','',0,0),(3,'Flat',200000,300,10,'Frankfurt',12345,'Goethestr.','234','./static/images/properties/flat.jpg',1,34,NULL,NULL,1,0),(4,'Villa',250000,250,35,'London',78912,'HeatherParkDr','40','./static/images/properties/villa.jpg',1,34,NULL,NULL,0,0),(5,'Small Castle',300000,150,30,'Frankfurt',60435,'HomburgerLandstraße','10','./static/images/properties/castle.jpg',0,34,NULL,NULL,0,0),(6,'Old Farmhouse',700000,100,25,'Feldberg (Schwarzwald)',79868,'Außenliegend','1','./static/images/properties/haus1.jpeg',1,34,NULL,NULL,1,0),(7,'Clean small house',450000,30,5,'Fulda Künzell',36093,'Turmstraße','4','./static/images/properties/haus2.jpeg',1,34,NULL,NULL,0,0),(8,'Family house',350000,90,10,'Fulda Haimbach',36041,'Merkurstraße','7','./static/images/properties/haus4.jpeg',1,34,NULL,NULL,0,0),(9,'Small House',50000,70,15,'Fulda Haimbach',36041,'Merkurstraße','9','./static/images/properties/haus5.jpeg',1,34,NULL,NULL,1,0),(46,'House in the mountains',150000,75,4,'Frankfurt',60439,'Schillerstraße','12','./static/images/properties/mountains.jpg',0,34,NULL,NULL,0,0),(47,'Lighthouse',899000,350,12,'Fulda',58372,'Davidstraße','99','./static/images/properties/house.jpg',1,34,NULL,NULL,0,0),(48,'Scary House',130000,150,5,'Köln',59573,'Joshuastraße','42','./static/images/properties/villa_2.jpg',0,34,NULL,NULL,0,0),(49,'Lake House',80000,50,2,'Leipzig',84823,'Elisabethstraße','2','./static/images/properties/lake.jpg',1,34,NULL,NULL,0,0),(50,'Tetris House',499000,500,18,'Berlin',49457,'Daryastraße','45','./static/images/properties/residence.jpg',0,34,NULL,NULL,0,0),(51,'Majestic Opera',1000000,500,100,'Hamburg',50953,'Oliverstraße','99','./static/images/properties/sydney.jpg',1,34,NULL,NULL,0,0),(52,'Tiny House',5,0,0,'München',54723,'Goethestraße','56','./static/images/properties/house2.jpg',1,34,NULL,NULL,0,0),(53,'Beach House',699500,400,11,'Kiel',64253,'Peterstraße','3','./static/images/properties/large-home.jpg',1,34,NULL,NULL,0,0),(54,'Beetle Home',100000,100,4,'Frankfurt',57361,'Güntherstraße','89','./static/images/properties/vw-beetle.jpg',1,34,NULL,NULL,0,0),(55,'Pool House',750000,230,7,'Kiel',58371,'Schinkenstraße','8','./static/images/properties/villa3.jpg',0,34,NULL,NULL,0,0),(56,'Vintage House',340000,145,6,'Köln',35938,'Hauptstraße','1','./static/images/properties/vintage.jpg',0,34,NULL,NULL,0,0);
/*!40000 ALTER TABLE `properties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_and_hashtag`
--

DROP TABLE IF EXISTS `property_and_hashtag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `property_and_hashtag` (
  `id` int NOT NULL AUTO_INCREMENT,
  `property_id_fk_2` int DEFAULT NULL,
  `housematch_hashtag_id_fk` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `housematch_hashtag_id_idx` (`housematch_hashtag_id_fk`),
  KEY `property_id_fk_idx` (`property_id_fk_2`),
  CONSTRAINT `housematch_id_fk` FOREIGN KEY (`housematch_hashtag_id_fk`) REFERENCES `housematch_hashtag` (`housematch_hashtag_id`),
  CONSTRAINT `property_id_fk_2` FOREIGN KEY (`property_id_fk_2`) REFERENCES `properties` (`property_id`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_and_hashtag`
--

LOCK TABLES `property_and_hashtag` WRITE;
/*!40000 ALTER TABLE `property_and_hashtag` DISABLE KEYS */;
INSERT INTO `property_and_hashtag` VALUES (5,2,4),(6,5,6),(7,3,4),(11,2,9),(12,3,2),(13,3,1),(28,1,5),(30,46,1),(31,46,2),(32,46,3),(33,47,4),(34,47,5),(35,47,7),(36,48,2),(37,48,5),(38,48,9),(39,49,6),(40,49,8),(41,49,9),(42,50,2),(43,50,4),(44,50,6),(45,50,8),(46,51,1),(47,51,2),(48,51,3),(49,51,4),(50,51,5),(51,51,6),(52,51,7),(53,51,8),(54,51,9),(55,52,2),(56,52,5),(57,52,7),(63,54,2),(64,54,3),(65,54,5),(66,54,6),(67,54,8),(68,54,9),(69,55,4),(70,55,5),(71,55,6),(72,56,8),(73,56,9),(74,7,2),(75,7,4),(76,8,7),(77,8,5),(78,8,1),(79,8,3),(80,6,1),(81,6,7),(82,9,2),(83,9,8),(84,9,7),(85,9,1),(86,4,5),(87,4,6),(88,4,9),(91,53,5),(92,53,6),(93,53,7),(94,53,8),(95,53,9);
/*!40000 ALTER TABLE `property_and_hashtag` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-28 16:42:15

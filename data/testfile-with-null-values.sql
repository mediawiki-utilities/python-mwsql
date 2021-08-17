-- MySQL dump 10.18  Distrib 10.3.27-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: 10.64.32.82    Database: simplewiki
-- ------------------------------------------------------
-- Server version	10.4.19-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `change_tag_def`
--

DROP TABLE IF EXISTS `change_tag_def`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `change_tag_def` (
  `ctd_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ctd_name` varbinary(255) NOT NULL,
  `ctd_user_defined` tinyint(1) NOT NULL,
  `ctd_count` bigint(20) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`ctd_id`),
  UNIQUE KEY `ctd_name` (`ctd_name`),
  KEY `ctd_count` (`ctd_count`),
  KEY `ctd_user_defined` (`ctd_user_defined`)
) ENGINE=InnoDB AUTO_INCREMENT=126 DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `change_tag_def`
--

/*!40000 ALTER TABLE `change_tag_def` DISABLE KEYS */;
INSERT INTO `change_tag_def` VALUES (NULL,'mw-replace?NULL',0,10200),(2,NULL,0,305860),(3,'mw-undo',NULL,58220),(4,'mw-rollback',0,NULL),(5,'mobile edit',0,230487),(6,'mobile web edit',0,223010),(7,'very short new article',0,28586),(8,'visualeditor-wikitext',0,20113),(9,'mw-new-redirect',0,29681),(10,'visualeditor-switched',0,17717),(11,'mw-removed-redirect',0,4426),(12,'repeating characters',0,6721),(13,'blanking',0,19912),(14,'mw-blank',0,42285),(15,'mw-changed-redirect-target',0,4539),(16,'uppercase- or lowercase-only article',0,24377),(17,'emoji',0,2054),(18,'talk page blanking',0,235),(19,'redirect page with extra text',0,675),(20,'article with links to other-language wikis?',0,3556),(21,'possible vandalism',0,4952),(22,'meta spam id',0,219),(23,'copy/paste from another Wikipedia?',0,1229),(24,'contenttranslation',0,1147),(25,'possible spamming',0,420),(26,'mobile app edit',0,6519),(27,'android app edit',0,2033),(28,'massmessage-delivery',0,3698),(36,'ios app edit',0,1023),(37,'possible libel or vandalism',0,1534),(38,'large unwikified new article',0,4066),(39,'New user creating interrogative pages',0,844),(42,'OAuth CID: 99',0,576),(43,'Possible Vandalism',0,9),(44,'Spambot edit?',0,731),(45,'Text after interwiki or categories',0,133),(46,'Text after interwiki/categories',0,283),(47,'abusefilter-condition-limit',0,127),(48,'adding email address',0,37),(50,'article with links to other-language wikis',0,4),(52,'article with uppercase title',0,520),(57,'end of page text',0,165),(58,'gettingstarted edit',0,202),(59,'goji spam test',0,1),(74,'new LGBT rights article',0,173),(75,'new tehsil article',0,83),(76,'ntsamr (global)',0,1),(77,'one-case only article',0,1481),(78,'one-case-only article',0,1779),(83,'repeated xwiki CoI abuse',0,48),(85,'reverting anti-vandal bot',0,664),(86,'short \'X is a city in Y\' article',0,48),(88,'test edit',0,500),(92,'visualeditor-needcheck',0,24),(93,'Possible Vandalism - LTA',1,65),(96,'mw-contentmodelchange',0,6),(97,'contenttranslation-v2',0,583),(98,'OAuth CID: 1188',0,107),(99,'Likely have problems',0,388),(101,'OAuth CID: 1261',0,160),(102,'references removed',0,4277),(103,'Spam Research',0,5),(104,'OAuth CID: 429',0,3),(105,'OAuth CID: 1352',0,5477),(106,'removal of quick deletion templates',0,1789),(107,'advanced mobile edit',0,12013),(108,'OAuth CID: 651',0,5),(109,'OAuth CID: 1805',0,2833),(110,'added links to social media sites',0,679),(111,'discussiontools',0,2832),(112,'discussiontools-reply',0,2444),(113,'discussiontools-visual',0,368),(114,'discussiontools-source',0,2464),(115,'mw-manual-revert',0,44507),(116,'T144167',0,2),(117,'mw-reverted',0,84006),(118,'Ukraine-Russia-related vandalism',0,5),(119,'new user blanking Wikipedia or WP Talk page',0,158),(120,'OAuth CID: 1804',0,99),(121,'discussiontools-newtopic',0,388),(122,'newcomer task',0,410),(123,'mw-add-media',0,23308),(124,'mw-remove-media',0,11135),(125,'discussiontools-source-enhanced',0,341);
/*!40000 ALTER TABLE `change_tag_def` ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-01 11:48:33

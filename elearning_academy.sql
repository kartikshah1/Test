-- MySQL dump 10.13  Distrib 5.5.35, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: elearning_academy
-- ------------------------------------------------------
-- Server version	5.5.35-0ubuntu0.12.04.2

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
-- Table structure for table `assignments_assignment`
--

DROP TABLE IF EXISTS `assignments_assignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assignments_assignment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `serial_number` int(11) NOT NULL,
  `program_language` varchar(32) NOT NULL,
  `deadline` datetime DEFAULT NULL,
  `hard_deadline` datetime DEFAULT NULL,
  `publish_on` datetime NOT NULL,
  `late_submission_allowed` tinyint(1) NOT NULL,
  `document` varchar(100) DEFAULT NULL,
  `helper_code` varchar(100) DEFAULT NULL,
  `model_solution` varchar(100) DEFAULT NULL,
  `student_program_files` varchar(1024) NOT NULL,
  `description` longtext,
  `creater_id` int(11) NOT NULL,
  `createdOn` datetime NOT NULL,
  `last_modified_on` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `course_id` (`course_id`,`name`),
  KEY `creater_id_refs_id_37902041` (`creater_id`),
  CONSTRAINT `course_id_refs_id_b298c92b` FOREIGN KEY (`course_id`) REFERENCES `courseware_course` (`id`),
  CONSTRAINT `creater_id_refs_id_37902041` FOREIGN KEY (`creater_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assignments_assignment`
--

LOCK TABLES `assignments_assignment` WRITE;
/*!40000 ALTER TABLE `assignments_assignment` DISABLE KEYS */;
INSERT INTO `assignments_assignment` VALUES (1,3,'asgn_1',1,'C++','2014-05-31 17:30:00','2014-06-29 19:07:00','2014-01-08 15:36:00',1,'','','','main.cpp','test asgn 1',17,'2014-04-10 19:08:14','2014-04-10 19:08:14'),(2,3,'asgn_2',2,'C++','2014-05-01 17:30:00','2014-06-13 09:07:00','2014-03-04 15:36:00',1,'','','','main.cpp','test asgn 1',17,'2014-04-11 09:08:08','2014-04-11 09:08:08');
/*!40000 ALTER TABLE `assignments_assignment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assignments_assignmenterrors`
--

DROP TABLE IF EXISTS `assignments_assignmenterrors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assignments_assignmenterrors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `assignment_id` int(11) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `object_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `assignment_id_refs_id_8b3b9cee` (`assignment_id`),
  KEY `content_type_id_refs_id_39bc4b59` (`content_type_id`),
  CONSTRAINT `assignment_id_refs_id_8b3b9cee` FOREIGN KEY (`assignment_id`) REFERENCES `assignments_assignment` (`id`),
  CONSTRAINT `content_type_id_refs_id_39bc4b59` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assignments_assignmenterrors`
--

LOCK TABLES `assignments_assignmenterrors` WRITE;
/*!40000 ALTER TABLE `assignments_assignmenterrors` DISABLE KEYS */;
/*!40000 ALTER TABLE `assignments_assignmenterrors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assignments_program`
--

DROP TABLE IF EXISTS `assignments_program`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assignments_program` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `assignment_id` int(11) NOT NULL,
  `name` varchar(128) NOT NULL,
  `program_type` varchar(10) NOT NULL,
  `compiler_command` varchar(1024) NOT NULL,
  `execution_command` varchar(1024) NOT NULL,
  `program_files` varchar(100) DEFAULT NULL,
  `makefile` varchar(100) DEFAULT NULL,
  `description` longtext,
  `is_sane` tinyint(1) NOT NULL,
  `language` varchar(32) NOT NULL,
  `solution_ready` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `assignment_id_refs_id_5751a3b3` (`assignment_id`),
  CONSTRAINT `assignment_id_refs_id_5751a3b3` FOREIGN KEY (`assignment_id`) REFERENCES `assignments_assignment` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assignments_program`
--

LOCK TABLES `assignments_program` WRITE;
/*!40000 ALTER TABLE `assignments_program` DISABLE KEYS */;
INSERT INTO `assignments_program` VALUES (1,1,'asgn_1_prog_1','Evaluate','(lp0\nVg++\np1\naV\np2\naVmain.cpp\np3\na.','','','','test asgn 1...',1,'C++',0);
/*!40000 ALTER TABLE `assignments_program` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assignments_programerrors`
--

DROP TABLE IF EXISTS `assignments_programerrors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assignments_programerrors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `program_id` int(11) NOT NULL,
  `error_message` varchar(4096) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `program_id_refs_id_51db9661` (`program_id`),
  CONSTRAINT `program_id_refs_id_51db9661` FOREIGN KEY (`program_id`) REFERENCES `assignments_program` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assignments_programerrors`
--

LOCK TABLES `assignments_programerrors` WRITE;
/*!40000 ALTER TABLE `assignments_programerrors` DISABLE KEYS */;
/*!40000 ALTER TABLE `assignments_programerrors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assignments_testcase`
--

DROP TABLE IF EXISTS `assignments_testcase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assignments_testcase` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `program_id` int(11) NOT NULL,
  `command_line_args` longtext,
  `time_out` decimal(10,2) NOT NULL,
  `name` varchar(128) NOT NULL,
  `marks` int(11) DEFAULT NULL,
  `input_files` varchar(100) NOT NULL,
  `output_files` varchar(100) NOT NULL,
  `std_in_file_name` varchar(256) NOT NULL,
  `std_out_file_name` varchar(256) NOT NULL,
  `description` longtext,
  PRIMARY KEY (`id`),
  KEY `program_id_refs_id_abea45ea` (`program_id`),
  CONSTRAINT `program_id_refs_id_abea45ea` FOREIGN KEY (`program_id`) REFERENCES `assignments_program` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assignments_testcase`
--

LOCK TABLES `assignments_testcase` WRITE;
/*!40000 ALTER TABLE `assignments_testcase` DISABLE KEYS */;
INSERT INTO `assignments_testcase` VALUES (1,1,'',5.00,'testcase 1',20,'','st/KC-Networks/asgn_1/testcase-files/tmpG18a9l/abc.txt','None','abc.txt','sdbgwb');
/*!40000 ALTER TABLE `assignments_testcase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assignments_testcaseerrors`
--

DROP TABLE IF EXISTS `assignments_testcaseerrors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assignments_testcaseerrors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `testcase_id` int(11) NOT NULL,
  `error_message` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `testcase_id` (`testcase_id`),
  CONSTRAINT `testcase_id_refs_id_b5e59e4a` FOREIGN KEY (`testcase_id`) REFERENCES `assignments_testcase` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assignments_testcaseerrors`
--

LOCK TABLES `assignments_testcaseerrors` WRITE;
/*!40000 ALTER TABLE `assignments_testcaseerrors` DISABLE KEYS */;
/*!40000 ALTER TABLE `assignments_testcaseerrors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_5f412f9a` (`group_id`),
  KEY `auth_group_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=187 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add site',6,'add_site'),(17,'Can change site',6,'change_site'),(18,'Can delete site',6,'delete_site'),(19,'Can add log entry',7,'add_logentry'),(20,'Can change log entry',7,'change_logentry'),(21,'Can delete log entry',7,'delete_logentry'),(22,'Can add votable',8,'add_votable'),(23,'Can change votable',8,'change_votable'),(24,'Can delete votable',8,'delete_votable'),(25,'Can add subscription',9,'add_subscription'),(26,'Can change subscription',9,'change_subscription'),(27,'Can delete subscription',9,'delete_subscription'),(28,'Can add registration',10,'add_registration'),(29,'Can change registration',10,'change_registration'),(30,'Can delete registration',10,'delete_registration'),(31,'Can add email update',11,'add_emailupdate'),(32,'Can change email update',11,'change_emailupdate'),(33,'Can delete email update',11,'delete_emailupdate'),(34,'Can add forgot password',12,'add_forgotpassword'),(35,'Can change forgot password',12,'change_forgotpassword'),(36,'Can delete forgot password',12,'delete_forgotpassword'),(37,'Can add discussion forum',13,'add_discussionforum'),(38,'Can change discussion forum',13,'change_discussionforum'),(39,'Can delete discussion forum',13,'delete_discussionforum'),(40,'Can add tag',14,'add_tag'),(41,'Can change tag',14,'change_tag'),(42,'Can delete tag',14,'delete_tag'),(43,'Can add user setting',15,'add_usersetting'),(44,'Can change user setting',15,'change_usersetting'),(45,'Can delete user setting',15,'delete_usersetting'),(46,'Can add activity',16,'add_activity'),(47,'Can change activity',16,'change_activity'),(48,'Can delete activity',16,'delete_activity'),(49,'Can add content',17,'add_content'),(50,'Can change content',17,'change_content'),(51,'Can delete content',17,'delete_content'),(52,'Can add thread',18,'add_thread'),(53,'Can change thread',18,'change_thread'),(54,'Can delete thread',18,'delete_thread'),(55,'Can add comment',19,'add_comment'),(56,'Can change comment',19,'change_comment'),(57,'Can delete comment',19,'delete_comment'),(58,'Can add reply',20,'add_reply'),(59,'Can change reply',20,'change_reply'),(60,'Can delete reply',20,'delete_reply'),(61,'Can add vote',21,'add_vote'),(62,'Can change vote',21,'change_vote'),(63,'Can delete vote',21,'delete_vote'),(64,'Can add notification',22,'add_notification'),(65,'Can change notification',22,'change_notification'),(66,'Can delete notification',22,'delete_notification'),(67,'Can add major',23,'add_major'),(68,'Can change major',23,'change_major'),(69,'Can delete major',23,'delete_major'),(70,'Can add college',24,'add_college'),(71,'Can change college',24,'change_college'),(72,'Can delete college',24,'delete_college'),(73,'Can add education',25,'add_education'),(74,'Can change education',25,'change_education'),(75,'Can delete education',25,'delete_education'),(76,'Can add company',26,'add_company'),(77,'Can change company',26,'change_company'),(78,'Can delete company',26,'delete_company'),(79,'Can add work',27,'add_work'),(80,'Can change work',27,'change_work'),(81,'Can delete work',27,'delete_work'),(82,'Can add user profile',28,'add_userprofile'),(83,'Can change user profile',28,'change_userprofile'),(84,'Can delete user profile',28,'delete_userprofile'),(85,'Can add custom user',29,'add_customuser'),(86,'Can change custom user',29,'change_customuser'),(87,'Can delete custom user',29,'delete_customuser'),(88,'Can add notification email',30,'add_notificationemail'),(89,'Can change notification email',30,'change_notificationemail'),(90,'Can delete notification email',30,'delete_notificationemail'),(91,'Can add parent category',31,'add_parentcategory'),(92,'Can change parent category',31,'change_parentcategory'),(93,'Can delete parent category',31,'delete_parentcategory'),(94,'Can add category',32,'add_category'),(95,'Can change category',32,'change_category'),(96,'Can delete category',32,'delete_category'),(97,'Can add course info',33,'add_courseinfo'),(98,'Can change course info',33,'change_courseinfo'),(99,'Can delete course info',33,'delete_courseinfo'),(100,'Can add course',34,'add_course'),(101,'Can change course',34,'change_course'),(102,'Can delete course',34,'delete_course'),(103,'Can add offering',35,'add_offering'),(104,'Can change offering',35,'change_offering'),(105,'Can delete offering',35,'delete_offering'),(106,'Can add course history',36,'add_coursehistory'),(107,'Can change course history',36,'change_coursehistory'),(108,'Can delete course history',36,'delete_coursehistory'),(109,'Can add group',37,'add_group'),(110,'Can change group',37,'change_group'),(111,'Can delete group',37,'delete_group'),(112,'Can add group history',38,'add_grouphistory'),(113,'Can change group history',38,'change_grouphistory'),(114,'Can delete group history',38,'delete_grouphistory'),(115,'Can add concept',39,'add_concept'),(116,'Can change concept',39,'change_concept'),(117,'Can delete concept',39,'delete_concept'),(118,'Can add concept history',40,'add_concepthistory'),(119,'Can change concept history',40,'change_concepthistory'),(120,'Can delete concept history',40,'delete_concepthistory'),(121,'Can add quiz',41,'add_quiz'),(122,'Can change quiz',41,'change_quiz'),(123,'Can delete quiz',41,'delete_quiz'),(124,'Can add question module',42,'add_questionmodule'),(125,'Can change question module',42,'change_questionmodule'),(126,'Can delete question module',42,'delete_questionmodule'),(127,'Can add quiz history',43,'add_quizhistory'),(128,'Can change quiz history',43,'change_quizhistory'),(129,'Can delete quiz history',43,'delete_quizhistory'),(130,'Can add question',44,'add_question'),(131,'Can change question',44,'change_question'),(132,'Can delete question',44,'delete_question'),(133,'Can add descriptive question',45,'add_descriptivequestion'),(134,'Can change descriptive question',45,'change_descriptivequestion'),(135,'Can delete descriptive question',45,'delete_descriptivequestion'),(136,'Can add single choice question',46,'add_singlechoicequestion'),(137,'Can change single choice question',46,'change_singlechoicequestion'),(138,'Can delete single choice question',46,'delete_singlechoicequestion'),(139,'Can add multiple choice question',47,'add_multiplechoicequestion'),(140,'Can change multiple choice question',47,'change_multiplechoicequestion'),(141,'Can delete multiple choice question',47,'delete_multiplechoicequestion'),(142,'Can add fixed answer question',48,'add_fixedanswerquestion'),(143,'Can change fixed answer question',48,'change_fixedanswerquestion'),(144,'Can delete fixed answer question',48,'delete_fixedanswerquestion'),(145,'Can add programming question',49,'add_programmingquestion'),(146,'Can change programming question',49,'change_programmingquestion'),(147,'Can delete programming question',49,'delete_programmingquestion'),(148,'Can add testcase',50,'add_testcase'),(149,'Can change testcase',50,'change_testcase'),(150,'Can delete testcase',50,'delete_testcase'),(151,'Can add question history',51,'add_questionhistory'),(152,'Can change question history',51,'change_questionhistory'),(153,'Can delete question history',51,'delete_questionhistory'),(154,'Can add queue',52,'add_queue'),(155,'Can change queue',52,'change_queue'),(156,'Can delete queue',52,'delete_queue'),(157,'Can add submission',53,'add_submission'),(158,'Can change submission',53,'change_submission'),(159,'Can delete submission',53,'delete_submission'),(160,'Can add video',54,'add_video'),(161,'Can change video',54,'change_video'),(162,'Can delete video',54,'delete_video'),(163,'Can add video history',55,'add_videohistory'),(164,'Can change video history',55,'change_videohistory'),(165,'Can delete video history',55,'delete_videohistory'),(166,'Can add marker',56,'add_marker'),(167,'Can change marker',56,'change_marker'),(168,'Can delete marker',56,'delete_marker'),(169,'Can add section marker',57,'add_sectionmarker'),(170,'Can change section marker',57,'change_sectionmarker'),(171,'Can delete section marker',57,'delete_sectionmarker'),(172,'Can add quiz marker',58,'add_quizmarker'),(173,'Can change quiz marker',58,'change_quizmarker'),(174,'Can delete quiz marker',58,'delete_quizmarker'),(175,'Can add concept quiz history',59,'add_conceptquizhistory'),(176,'Can change concept quiz history',59,'change_conceptquizhistory'),(177,'Can delete concept quiz history',59,'delete_conceptquizhistory'),(178,'Can add concept document history',60,'add_conceptdocumenthistory'),(179,'Can change concept document history',60,'change_conceptdocumenthistory'),(180,'Can delete concept document history',60,'delete_conceptdocumenthistory'),(181,'Can add document',61,'add_document'),(182,'Can change document',61,'change_document'),(183,'Can delete document',61,'delete_document'),(184,'Can add section',62,'add_section'),(185,'Can change section',62,'change_section'),(186,'Can delete section',62,'delete_section');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$12000$VevAkUCKq4J4$P7U+yP5E47ChR99ljzp5F6sFehLC0ghbZXbYgr7cVTs=','2014-04-11 09:10:16',1,'elearning','E-Learning','Academy','gagrani.vinayak@gmail.com',1,1,'2014-01-02 03:05:46'),(2,'pbkdf2_sha256$10000$RmDbDuUg3fZd$KyOIbkWvVdKA/0QR2kqBBWZ57f9G+V/PneaoxfhA4HM=','2014-01-02 23:28:44',0,'chebrolu','Kameswari','Chebrolu','kameswari@gmail.com',0,1,'2014-01-02 15:25:18'),(3,'pbkdf2_sha256$12000$PtTfqzJuO0Ca$Zh+8RjOSSZdOv9EFebfOSvi5HFPlLFS/PAavUQPySlA=','2014-01-10 00:31:55',0,'test_user','Test','User','gagrani.vinayak+test_user@gmail.com',0,1,'2014-01-02 15:59:48'),(4,'pbkdf2_sha256$12000$6sFxqMs4fal5$mIdecEDbK3qz8VMqskO6fBKB4YaOkAjY7ywH3ixORK4=','2014-01-08 16:28:21',0,'priyesh','Priyesh','Shetty','priyeshs60@gmail.com',0,0,'2014-01-08 16:28:21'),(5,'pbkdf2_sha256$12000$RDZeI2c0aFds$0hs3WUmilaoBhH66Heo4Bo4vOZev+qjnF3edXApLuj4=','2014-01-08 17:00:30',0,'amanmadaan','Aman','Madaan','madaan.amanmadaan@gmail.com',0,0,'2014-01-08 17:00:30'),(6,'pbkdf2_sha256$12000$Vd2DNNzHsh8z$daI0LOfyeXF5xv1Qob68EP2mNTe/wZj/mXyCSkyBuv4=','2014-01-08 17:44:32',0,'amanmadaan2','Aman','Madaan','amanmadaan@cse.iitb.ac.in',0,0,'2014-01-08 17:44:32'),(7,'pbkdf2_sha256$12000$Jl0EqvFMLpWP$zRX4ecDXvbiGo5yLN717vdgffIfr8vjTvpwPJ+DDH5g=','2014-01-08 20:45:18',0,'ankit8','Ankit','Kumar','ankit_kumar@iitb.ac.in',0,0,'2014-01-08 20:45:18'),(8,'pbkdf2_sha256$12000$YM8rSVPUOkGs$BydQ6UPUt1wWWaFkZRxHnbAK56OKvSEppXk6OtTv43U=','2014-01-08 21:05:42',0,'pulkital','Pulkit','Agrawal','genrelquanta@gmail.com',0,0,'2014-01-08 21:05:42'),(9,'pbkdf2_sha256$12000$PVAAHEs5fDSG$z6wEj2CK/6BJ9fzsrMvJqH/4ojBim1biWSfkEoIF7ws=','2014-01-08 21:08:03',0,'praveshkochar','Pravesh','Kochar','kochar.pravesh@gmail.com',0,0,'2014-01-08 21:08:03'),(10,'pbkdf2_sha256$12000$F5wkSSENhGxs$X+IWecYhNBa09jWXORAEnZEzWtC3G4oMWFNoEf7RDOg=','2014-01-08 22:51:36',0,'ankit_maverick','Ankit','Agrawal','aaaagrawal@iitb.ac.in',0,1,'2014-01-08 22:37:49'),(11,'pbkdf2_sha256$12000$V0qQ5pxk8liw$if5s7IudrVLsfZ3fzn4Dsqa9Sb6QbKiGn4GhUyruHjw=','2014-01-09 02:09:32',0,'AshishBora','Ashish','Bora','ashish.dilip.bora@gmail.com',0,0,'2014-01-09 02:09:32'),(12,'pbkdf2_sha256$12000$3ao6JJMiuTqZ$E/mfBz14vtCAl7FpIrgGOC3T4s7/meOv8cUP2S/Tg94=','2014-01-09 02:33:26',0,'Phoenix','Sudesh','Singhal','sudeshsinghal01@gmail.com',0,0,'2014-01-09 02:33:26'),(13,'pbkdf2_sha256$12000$BwuR2dOWvmll$mXBb6AUwHPy1WJgLiy1BuSrePOE3ZfkddDHH8ljjteY=','2014-01-10 00:46:28',0,'jinx','Ajinkya','Jayawant','ajinkyajayawant@iitb.ac.in',0,0,'2014-01-10 00:46:28'),(14,'pbkdf2_sha256$10000$wBAWDhD5d2uo$7vOI6KnFKx64O0lKogqGHv5lBS0WHxwdLVqS5WudP2M=','2014-01-14 13:05:14',0,'mayank127','Mayank','Meghwanshi','maynkmeghwanshi@gmail.com',0,0,'2014-01-14 13:05:14'),(15,'pbkdf2_sha256$10000$K4Ir9TgY8iqX$x59GnUSQ8DB9zZlr5YjgvoJKSsvyKBu39enjmqtXKCY=','2014-02-13 15:16:48',0,'mayank','','','',0,1,'2014-02-13 14:41:22'),(16,'pbkdf2_sha256$10000$5bepSVeXEqe9$qq+vky3ez63VgoWKpm2WaefHEdvWWg9QRPLwFkY7Kms=','2014-04-11 09:19:55',0,'pj','PJ','PJ','prakharjain09@gmail.com',0,1,'2014-02-28 07:54:39'),(17,'pbkdf2_sha256$10000$yP0NdDbwozNz$lM4kAVQ8hxgDmCwjHtcYLpmwJuWamANryWFMXOB8ZXk=','2014-04-11 09:21:08',0,'st','st','st','sanket.s.totala@gmail.com',0,1,'2014-02-28 08:36:12'),(18,'pbkdf2_sha256$10000$kUwHG2wJGPye$4Xs4hkxKctBFyUxQWC04Ysqm7PcJXsOo9K4wma3w734=','2014-03-01 12:34:04',0,'abc','abc','abc','abc@gmail.com',0,0,'2014-03-01 12:34:04');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_6340c63c` (`user_id`),
  KEY `auth_user_groups_5f412f9a` (`group_id`),
  CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_6340c63c` (`user_id`),
  KEY `auth_user_user_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `concept_conceptdocumenthistory`
--

DROP TABLE IF EXISTS `concept_conceptdocumenthistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `concept_conceptdocumenthistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `document_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `seen_status` tinyint(1) NOT NULL,
  `times_seen` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `concept_conceptdocumenthistory_b7398729` (`document_id`),
  KEY `concept_conceptdocumenthistory_6340c63c` (`user_id`),
  CONSTRAINT `document_id_refs_id_ef356966` FOREIGN KEY (`document_id`) REFERENCES `document_document` (`id`),
  CONSTRAINT `user_id_refs_id_b87ebb6e` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `concept_conceptdocumenthistory`
--

LOCK TABLES `concept_conceptdocumenthistory` WRITE;
/*!40000 ALTER TABLE `concept_conceptdocumenthistory` DISABLE KEYS */;
INSERT INTO `concept_conceptdocumenthistory` VALUES (1,4,1,0,0),(2,8,1,0,0),(3,8,3,0,0),(4,14,1,0,0),(5,15,1,0,0),(6,14,3,0,0),(7,15,3,0,0),(8,8,17,0,0),(9,15,17,0,0),(10,14,17,0,0);
/*!40000 ALTER TABLE `concept_conceptdocumenthistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `concept_conceptquizhistory`
--

DROP TABLE IF EXISTS `concept_conceptquizhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `concept_conceptquizhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `quiz_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `seen_status` tinyint(1) NOT NULL,
  `times_seen` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `concept_conceptquizhistory_eecda460` (`quiz_id`),
  KEY `concept_conceptquizhistory_6340c63c` (`user_id`),
  CONSTRAINT `quiz_id_refs_id_712348f7` FOREIGN KEY (`quiz_id`) REFERENCES `quiz_quiz` (`id`),
  CONSTRAINT `user_id_refs_id_5aeeb193` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `concept_conceptquizhistory`
--

LOCK TABLES `concept_conceptquizhistory` WRITE;
/*!40000 ALTER TABLE `concept_conceptquizhistory` DISABLE KEYS */;
INSERT INTO `concept_conceptquizhistory` VALUES (1,1,1,0,0),(2,2,1,0,0),(3,6,1,0,0),(4,28,1,0,0),(5,28,3,0,0),(6,50,1,0,0),(7,54,1,0,0),(8,54,3,0,0),(9,50,3,0,0),(10,67,3,0,0),(11,67,1,0,0),(12,28,17,0,0),(13,50,17,0,0),(14,54,17,0,0);
/*!40000 ALTER TABLE `concept_conceptquizhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses_course`
--

DROP TABLE IF EXISTS `courses_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courses_course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(20) NOT NULL,
  `name` varchar(150) NOT NULL,
  `creater_id` int(11) NOT NULL,
  `createdOn` datetime NOT NULL,
  `lastModifiedOn` datetime NOT NULL,
  `isActive` tinyint(1) NOT NULL,
  `term` varchar(50) NOT NULL,
  `courseDescription` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`,`creater_id`,`term`),
  KEY `courses_course_3f5e5283` (`creater_id`),
  CONSTRAINT `creater_id_refs_id_05769af7` FOREIGN KEY (`creater_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses_course`
--

LOCK TABLES `courses_course` WRITE;
/*!40000 ALTER TABLE `courses_course` DISABLE KEYS */;
INSERT INTO `courses_course` VALUES (1,'lol 101','lol',1,'2014-03-01 14:54:55','2014-03-01 14:54:55',1,'fall 2014','lol'),(2,'ds','fd',17,'2014-03-04 06:48:52','2014-03-04 06:48:52',1,'winter 2014','Nonefsd');
/*!40000 ALTER TABLE `courses_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses_role`
--

DROP TABLE IF EXISTS `courses_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courses_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `role` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `courses_role_6340c63c` (`user_id`),
  KEY `courses_role_6234103b` (`course_id`),
  CONSTRAINT `course_id_refs_id_f42e546f` FOREIGN KEY (`course_id`) REFERENCES `courses_course` (`id`),
  CONSTRAINT `user_id_refs_id_3e0af09e` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses_role`
--

LOCK TABLES `courses_role` WRITE;
/*!40000 ALTER TABLE `courses_role` DISABLE KEYS */;
INSERT INTO `courses_role` VALUES (1,1,1,'S');
/*!40000 ALTER TABLE `courses_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseware_category`
--

DROP TABLE IF EXISTS `courseware_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courseware_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `courseware_category_410d0aac` (`parent_id`),
  CONSTRAINT `parent_id_refs_id_3d27467b` FOREIGN KEY (`parent_id`) REFERENCES `courseware_parentcategory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseware_category`
--

LOCK TABLES `courseware_category` WRITE;
/*!40000 ALTER TABLE `courseware_category` DISABLE KEYS */;
INSERT INTO `courseware_category` VALUES (1,1,'Systems','');
/*!40000 ALTER TABLE `courseware_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseware_category_content_developers`
--

DROP TABLE IF EXISTS `courseware_category_content_developers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courseware_category_content_developers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `category_id` (`category_id`,`user_id`),
  KEY `courseware_category_content_developers_6f33f001` (`category_id`),
  KEY `courseware_category_content_developers_6340c63c` (`user_id`),
  CONSTRAINT `category_id_refs_id_706db695` FOREIGN KEY (`category_id`) REFERENCES `courseware_category` (`id`),
  CONSTRAINT `user_id_refs_id_94b88707` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseware_category_content_developers`
--

LOCK TABLES `courseware_category_content_developers` WRITE;
/*!40000 ALTER TABLE `courseware_category_content_developers` DISABLE KEYS */;
/*!40000 ALTER TABLE `courseware_category_content_developers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseware_concept`
--

DROP TABLE IF EXISTS `courseware_concept`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courseware_concept` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `title_document_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `max_score` int(11) NOT NULL,
  `playlist` longtext NOT NULL,
  `description` varchar(1023) DEFAULT NULL,
  `is_published` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `courseware_concept_5f412f9a` (`group_id`),
  KEY `courseware_concept_f21325d0` (`title_document_id`),
  CONSTRAINT `group_id_refs_id_58ae00e8` FOREIGN KEY (`group_id`) REFERENCES `courseware_group` (`id`),
  CONSTRAINT `title_document_id_refs_id_4f00bf24` FOREIGN KEY (`title_document_id`) REFERENCES `document_document` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseware_concept`
--

LOCK TABLES `courseware_concept` WRITE;
/*!40000 ALTER TABLE `courseware_concept` DISABLE KEYS */;
INSERT INTO `courseware_concept` VALUES (1,1,1,'Sample Concept','',5,'[[1, 0, 1]]','',0),(2,2,3,'Motivation','',6,'[[6, 0, 0], [10, 1, 0]]','xxx',0),(3,2,6,'Testing Config Upload','',0,'[[8, 0, 0]]','',1),(4,2,7,'KC-Test','',20,'[[28, 0, 1], [8, 0, 2], [36, 0, 0], [46, 1, 0], [57, 2, 0], [58, 3, 0]]','New concept',1),(9,5,13,'Motivation','',8,'[[37, 0, 0], [50, 0, 1], [14, 0, 2]]','Why study computer networks?',1),(10,5,16,'Motivation-v2','',9,'[[38, 0, 0], [54, 0, 1]]','blah blah',1),(11,6,17,'Motivation','',0,'[]','blah blah',0),(12,5,18,'Motivation-v3','',0,'[]','Motivation-v3',1),(13,7,19,'Motivation','',4,'[[59, 0, 0], [67, 0, 1]]','Why study Computer Networks?',1),(14,7,20,'Motivation-unpub','',0,'[[60, 0, 0]]','Motivation unpublished',0);
/*!40000 ALTER TABLE `courseware_concept` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseware_concept_pages`
--

DROP TABLE IF EXISTS `courseware_concept_pages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courseware_concept_pages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `concept_id` int(11) NOT NULL,
  `document_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `concept_id` (`concept_id`,`document_id`),
  KEY `courseware_concept_pages_8a386586` (`concept_id`),
  KEY `courseware_concept_pages_b7398729` (`document_id`),
  CONSTRAINT `concept_id_refs_id_5c6e5733` FOREIGN KEY (`concept_id`) REFERENCES `courseware_concept` (`id`),
  CONSTRAINT `document_id_refs_id_d404d65d` FOREIGN KEY (`document_id`) REFERENCES `document_document` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseware_concept_pages`
--

LOCK TABLES `courseware_concept_pages` WRITE;
/*!40000 ALTER TABLE `courseware_concept_pages` DISABLE KEYS */;
INSERT INTO `courseware_concept_pages` VALUES (1,2,4),(2,4,8),(4,4,15),(3,9,14);
/*!40000 ALTER TABLE `courseware_concept_pages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseware_concept_quizzes`
--

DROP TABLE IF EXISTS `courseware_concept_quizzes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courseware_concept_quizzes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `concept_id` int(11) NOT NULL,
  `quiz_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `concept_id` (`concept_id`,`quiz_id`),
  KEY `courseware_concept_quizzes_8a386586` (`concept_id`),
  KEY `courseware_concept_quizzes_eecda460` (`quiz_id`),
  CONSTRAINT `concept_id_refs_id_07788901` FOREIGN KEY (`concept_id`) REFERENCES `courseware_concept` (`id`),
  CONSTRAINT `quiz_id_refs_id_3aceac70` FOREIGN KEY (`quiz_id`) REFERENCES `quiz_quiz` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseware_concept_quizzes`
--

LOCK TABLES `courseware_concept_quizzes` WRITE;
/*!40000 ALTER TABLE `courseware_concept_quizzes` DISABLE KEYS */;
INSERT INTO `courseware_concept_quizzes` VALUES (1,1,1),(2,1,2),(3,2,6),(4,4,28),(5,9,50),(6,10,54),(7,13,67);
/*!40000 ALTER TABLE `courseware_concept_quizzes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseware_concept_videos`
--

DROP TABLE IF EXISTS `courseware_concept_videos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courseware_concept_videos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `concept_id` int(11) NOT NULL,
  `video_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `concept_id` (`concept_id`,`video_id`),
  KEY `courseware_concept_videos_8a386586` (`concept_id`),
  KEY `courseware_concept_videos_c11471f1` (`video_id`),
  CONSTRAINT `concept_id_refs_id_faf7998e` FOREIGN KEY (`concept_id`) REFERENCES `courseware_concept` (`id`),
  CONSTRAINT `video_id_refs_id_d85781ee` FOREIGN KEY (`video_id`) REFERENCES `video_video` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseware_concept_videos`
--

LOCK TABLES `courseware_concept_videos` WRITE;
/*!40000 ALTER TABLE `courseware_concept_videos` DISABLE KEYS */;
INSERT INTO `courseware_concept_videos` VALUES (6,2,6),(10,2,10),(8,3,8),(18,4,36),(21,4,46),(22,4,57),(23,4,58),(19,9,37),(20,10,38),(24,13,59),(25,14,60);
/*!40000 ALTER TABLE `courseware_concept_videos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseware_concepthistory`
--

DROP TABLE IF EXISTS `courseware_concepthistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courseware_concepthistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `concept_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `score` double NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `concept_id` (`concept_id`,`user_id`),
  KEY `courseware_concepthistory_8a386586` (`concept_id`),
  KEY `courseware_concepthistory_6340c63c` (`user_id`),
  KEY `courseware_concepthistory_796cfe0d` (`user_id`,`concept_id`),
  CONSTRAINT `concept_id_refs_id_21fce143` FOREIGN KEY (`concept_id`) REFERENCES `courseware_concept` (`id`),
  CONSTRAINT `user_id_refs_id_82e30c08` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseware_concepthistory`
--

LOCK TABLES `courseware_concepthistory` WRITE;
/*!40000 ALTER TABLE `courseware_concepthistory` DISABLE KEYS */;
INSERT INTO `courseware_concepthistory` VALUES (1,1,1,5),(2,2,2,0),(3,2,1,0),(4,4,1,16),(5,3,2,0),(6,4,2,0),(7,2,3,0),(8,3,3,0),(9,4,3,4),(10,9,1,0),(11,10,1,5),(12,3,1,0),(13,9,3,0),(14,10,3,0),(15,12,3,0),(16,2,10,0),(17,3,10,0),(18,4,10,0),(19,13,3,2),(20,14,3,0),(21,12,1,0),(22,2,17,0),(23,3,17,0),(24,4,17,0),(25,9,17,0),(26,10,17,0),(27,12,17,0),(28,2,16,0),(29,3,16,0),(30,4,16,0);
/*!40000 ALTER TABLE `courseware_concepthistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseware_course`
--

DROP TABLE IF EXISTS `courseware_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courseware_course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `image` varchar(100) NOT NULL,
  `type` varchar(1) NOT NULL,
  `playlist` longtext NOT NULL,
  `forum_id` int(11) NOT NULL,
  `page_playlist` longtext NOT NULL,
  `max_score` int(11) NOT NULL,
  `course_info_id` int(11) DEFAULT NULL,
  `enrollment_type` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `course_info_id` (`course_info_id`),
  KEY `courseware_course_6f33f001` (`category_id`),
  KEY `courseware_course_f979685d` (`forum_id`),
  CONSTRAINT `category_id_refs_id_fea28ca5` FOREIGN KEY (`category_id`) REFERENCES `courseware_category` (`id`),
  CONSTRAINT `course_info_id_refs_id_4f80be9c` FOREIGN KEY (`course_info_id`) REFERENCES `courseware_courseinfo` (`id`),
  CONSTRAINT `forum_id_refs_id_948ee5aa` FOREIGN KEY (`forum_id`) REFERENCES `discussion_forum_discussionforum` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseware_course`
--

LOCK TABLES `courseware_course` WRITE;
/*!40000 ALTER TABLE `courseware_course` DISABLE KEYS */;
INSERT INTO `courseware_course` VALUES (1,1,'Sample Offering','','O','[[1, 0]]',1,'[[2, 0]]',5,1,'M'),(2,1,'Computer Networks','','T','[[3, 0]]',2,'[]',0,2,'M'),(3,1,'KC-Networks','','O','[[2, 0]]',3,'[[5, 0]]',26,3,'O'),(4,1,'Computer Networks (minor)','','O','[[5, 0]]',4,'[]',17,4,'M'),(5,1,'Final-Test','','O','[[6, 0]]',5,'[]',0,5,'M'),(6,1,'Test-9Jan','','O','[[7, 0]]',6,'[]',4,6,'O'),(7,1,'Dummy','','O','[]',7,'[]',0,7,'O');
/*!40000 ALTER TABLE `courseware_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseware_course_pages`
--

DROP TABLE IF EXISTS `courseware_course_pages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courseware_course_pages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` int(11) NOT NULL,
  `document_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `course_id` (`course_id`,`document_id`),
  KEY `courseware_course_pages_6234103b` (`course_id`),
  KEY `courseware_course_pages_b7398729` (`document_id`),
  CONSTRAINT `course_id_refs_id_b77f7284` FOREIGN KEY (`course_id`) REFERENCES `courseware_course` (`id`),
  CONSTRAINT `document_id_refs_id_76c3590d` FOREIGN KEY (`document_id`) REFERENCES `document_document` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseware_course_pages`
--

LOCK TABLES `courseware_course_pages` WRITE;
/*!40000 ALTER TABLE `courseware_course_pages` DISABLE KEYS */;
INSERT INTO `courseware_course_pages` VALUES (1,1,2),(2,3,5);
/*!40000 ALTER TABLE `courseware_course_pages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseware_coursehistory`
--

DROP TABLE IF EXISTS `courseware_coursehistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courseware_coursehistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `grade` varchar(2) DEFAULT NULL,
  `score` double DEFAULT NULL,
  `active` varchar(1) NOT NULL,
  `is_moderator` tinyint(1) NOT NULL,
  `is_owner` tinyint(1) NOT NULL,
  `show_marks` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `course_id` (`course_id`,`user_id`),
  KEY `courseware_coursehistory_6234103b` (`course_id`),
  KEY `courseware_coursehistory_6340c63c` (`user_id`),
  KEY `courseware_coursehistory_84efe9b6` (`user_id`,`course_id`),
  CONSTRAINT `course_id_refs_id_57eb14a0` FOREIGN KEY (`course_id`) REFERENCES `courseware_course` (`id`),
  CONSTRAINT `user_id_refs_id_30e42065` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseware_coursehistory`
--

LOCK TABLES `courseware_coursehistory` WRITE;
/*!40000 ALTER TABLE `courseware_coursehistory` DISABLE KEYS */;
INSERT INTO `courseware_coursehistory` VALUES (1,1,1,NULL,0,'A',0,1,1),(2,2,1,NULL,0,'A',0,1,1),(3,3,1,NULL,0,'A',0,1,1),(4,3,2,NULL,0,'A',0,0,1),(5,3,3,NULL,0,'A',0,0,1),(6,4,1,NULL,0,'A',0,1,1),(7,5,1,NULL,0,'A',0,1,1),(8,3,10,NULL,0,'P',0,0,1),(9,4,3,NULL,0,'A',0,0,1),(10,6,1,NULL,0,'A',0,1,1),(11,6,3,NULL,2,'A',0,0,1),(12,3,17,NULL,0,'A',0,1,1),(13,7,1,NULL,0,'A',0,1,1),(14,4,17,NULL,0,'A',0,1,1),(15,3,16,NULL,0,'A',0,0,1);
/*!40000 ALTER TABLE `courseware_coursehistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseware_courseinfo`
--

DROP TABLE IF EXISTS `courseware_courseinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courseware_courseinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_time` date DEFAULT NULL,
  `end_time` date DEFAULT NULL,
  `is_published` tinyint(1) NOT NULL,
  `description` varchar(1023) NOT NULL,
  `end_enrollment_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `courseware_courseinfo_66db471f` (`start_time`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseware_courseinfo`
--

LOCK TABLES `courseware_courseinfo` WRITE;
/*!40000 ALTER TABLE `courseware_courseinfo` DISABLE KEYS */;
INSERT INTO `courseware_courseinfo` VALUES (1,NULL,NULL,0,'',NULL),(2,NULL,NULL,1,'',NULL),(3,'2014-03-11','2014-03-31',1,'','2014-03-11'),(4,NULL,NULL,1,'',NULL),(5,NULL,NULL,0,'',NULL),(6,NULL,NULL,1,'',NULL),(7,NULL,NULL,0,'',NULL);
/*!40000 ALTER TABLE `courseware_courseinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseware_group`
--

DROP TABLE IF EXISTS `courseware_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courseware_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `image` varchar(100) NOT NULL,
  `max_score` int(11) NOT NULL,
  `playlist` longtext NOT NULL,
  `description` varchar(1023) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `courseware_group_6234103b` (`course_id`),
  CONSTRAINT `course_id_refs_id_a9fddc0a` FOREIGN KEY (`course_id`) REFERENCES `courseware_course` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseware_group`
--

LOCK TABLES `courseware_group` WRITE;
/*!40000 ALTER TABLE `courseware_group` DISABLE KEYS */;
INSERT INTO `courseware_group` VALUES (1,1,'Sample Group','',5,'[[1, 0]]',''),(2,3,'Introduction','',26,'[[2, 0], [3, 1], [4, 2]]','aaaa'),(3,2,'sdfsdfds','',0,'[]','sdfdsfsdfsf'),(5,4,'Introduction','',17,'[[9, 0], [10, 1], [12, 2]]','Introduction to computer networks'),(6,5,'Introduction','',0,'[[11, 0]]','background material'),(7,6,'Introduction','',4,'[[13, 0], [14, 1]]','An intro to computer networks');
/*!40000 ALTER TABLE `courseware_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseware_group_pages`
--

DROP TABLE IF EXISTS `courseware_group_pages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courseware_group_pages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `document_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`document_id`),
  KEY `courseware_group_pages_5f412f9a` (`group_id`),
  KEY `courseware_group_pages_b7398729` (`document_id`),
  CONSTRAINT `document_id_refs_id_a5143108` FOREIGN KEY (`document_id`) REFERENCES `document_document` (`id`),
  CONSTRAINT `group_id_refs_id_1c0d6309` FOREIGN KEY (`group_id`) REFERENCES `courseware_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseware_group_pages`
--

LOCK TABLES `courseware_group_pages` WRITE;
/*!40000 ALTER TABLE `courseware_group_pages` DISABLE KEYS */;
/*!40000 ALTER TABLE `courseware_group_pages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseware_grouphistory`
--

DROP TABLE IF EXISTS `courseware_grouphistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courseware_grouphistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `score` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`user_id`),
  KEY `courseware_grouphistory_5f412f9a` (`group_id`),
  KEY `courseware_grouphistory_6340c63c` (`user_id`),
  KEY `courseware_grouphistory_dd4f80b0` (`user_id`,`group_id`),
  CONSTRAINT `group_id_refs_id_04e64ea4` FOREIGN KEY (`group_id`) REFERENCES `courseware_group` (`id`),
  CONSTRAINT `user_id_refs_id_bf6768e2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseware_grouphistory`
--

LOCK TABLES `courseware_grouphistory` WRITE;
/*!40000 ALTER TABLE `courseware_grouphistory` DISABLE KEYS */;
INSERT INTO `courseware_grouphistory` VALUES (1,1,1,5),(2,2,2,0),(3,2,1,16),(4,2,3,4),(5,5,1,5),(6,5,3,0),(7,2,10,0),(8,7,3,2),(9,3,1,0),(10,2,17,0),(11,5,17,0),(12,2,16,0);
/*!40000 ALTER TABLE `courseware_grouphistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseware_offering`
--

DROP TABLE IF EXISTS `courseware_offering`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courseware_offering` (
  `course_ptr_id` int(11) NOT NULL,
  PRIMARY KEY (`course_ptr_id`),
  CONSTRAINT `course_ptr_id_refs_id_843df65d` FOREIGN KEY (`course_ptr_id`) REFERENCES `courseware_course` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseware_offering`
--

LOCK TABLES `courseware_offering` WRITE;
/*!40000 ALTER TABLE `courseware_offering` DISABLE KEYS */;
INSERT INTO `courseware_offering` VALUES (1),(3),(4),(5),(6),(7);
/*!40000 ALTER TABLE `courseware_offering` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseware_offering_shortlisted_courses`
--

DROP TABLE IF EXISTS `courseware_offering_shortlisted_courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courseware_offering_shortlisted_courses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `offering_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `offering_id` (`offering_id`,`course_id`),
  KEY `courseware_offering_shortlisted_courses_811bb53c` (`offering_id`),
  KEY `courseware_offering_shortlisted_courses_6234103b` (`course_id`),
  CONSTRAINT `course_id_refs_id_67a3f73b` FOREIGN KEY (`course_id`) REFERENCES `courseware_course` (`id`),
  CONSTRAINT `offering_id_refs_course_ptr_id_40d27a1d` FOREIGN KEY (`offering_id`) REFERENCES `courseware_offering` (`course_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseware_offering_shortlisted_courses`
--

LOCK TABLES `courseware_offering_shortlisted_courses` WRITE;
/*!40000 ALTER TABLE `courseware_offering_shortlisted_courses` DISABLE KEYS */;
/*!40000 ALTER TABLE `courseware_offering_shortlisted_courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseware_parentcategory`
--

DROP TABLE IF EXISTS `courseware_parentcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courseware_parentcategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseware_parentcategory`
--

LOCK TABLES `courseware_parentcategory` WRITE;
/*!40000 ALTER TABLE `courseware_parentcategory` DISABLE KEYS */;
INSERT INTO `courseware_parentcategory` VALUES (1,'Computer Science');
/*!40000 ALTER TABLE `courseware_parentcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cribs_comment`
--

DROP TABLE IF EXISTS `cribs_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cribs_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `crib_id` int(11) NOT NULL,
  `posted_by_id` int(11) NOT NULL,
  `comment` longtext NOT NULL,
  `posted_on` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cribs_comment_8c165527` (`crib_id`),
  KEY `cribs_comment_5862c5f7` (`posted_by_id`),
  CONSTRAINT `crib_id_refs_id_440091a5` FOREIGN KEY (`crib_id`) REFERENCES `cribs_crib` (`id`),
  CONSTRAINT `posted_by_id_refs_id_fd16896a` FOREIGN KEY (`posted_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cribs_comment`
--

LOCK TABLES `cribs_comment` WRITE;
/*!40000 ALTER TABLE `cribs_comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `cribs_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cribs_crib`
--

DROP TABLE IF EXISTS `cribs_crib`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cribs_crib` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `assignment_id` int(11) NOT NULL,
  `created_by_id` int(11) NOT NULL,
  `title` varchar(512) NOT NULL,
  `crib_detail` longtext NOT NULL,
  `is_resolved` tinyint(1) NOT NULL,
  `created_on` datetime NOT NULL,
  `last_modified_on` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cribs_crib_52f7e0e7` (`assignment_id`),
  KEY `cribs_crib_0c98d849` (`created_by_id`),
  CONSTRAINT `assignment_id_refs_id_61b539ee` FOREIGN KEY (`assignment_id`) REFERENCES `assignments_assignment` (`id`),
  CONSTRAINT `created_by_id_refs_id_05c466ea` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cribs_crib`
--

LOCK TABLES `cribs_crib` WRITE;
/*!40000 ALTER TABLE `cribs_crib` DISABLE KEYS */;
/*!40000 ALTER TABLE `cribs_crib` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discussion_forum_activity`
--

DROP TABLE IF EXISTS `discussion_forum_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discussion_forum_activity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `forum_id` int(11) NOT NULL,
  `actor_id` int(11) NOT NULL,
  `happened_at` datetime NOT NULL,
  `operation` varchar(32) NOT NULL,
  `object_type` varchar(32) NOT NULL,
  `object_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `discussion_forum_activity_f979685d` (`forum_id`),
  KEY `discussion_forum_activity_b6bbc2ee` (`actor_id`),
  KEY `discussion_forum_activity_e3d987aa` (`happened_at`),
  CONSTRAINT `actor_id_refs_id_6e87b64b` FOREIGN KEY (`actor_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `forum_id_refs_id_32dce9fe` FOREIGN KEY (`forum_id`) REFERENCES `discussion_forum_discussionforum` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discussion_forum_activity`
--

LOCK TABLES `discussion_forum_activity` WRITE;
/*!40000 ALTER TABLE `discussion_forum_activity` DISABLE KEYS */;
INSERT INTO `discussion_forum_activity` VALUES (1,3,1,'2014-01-03 16:23:28','add','thread',1),(2,3,1,'2014-01-03 16:26:50','add','thread',2);
/*!40000 ALTER TABLE `discussion_forum_activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discussion_forum_comment`
--

DROP TABLE IF EXISTS `discussion_forum_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discussion_forum_comment` (
  `content_ptr_id` int(11) NOT NULL,
  `thread_id` int(11) NOT NULL,
  PRIMARY KEY (`content_ptr_id`),
  KEY `discussion_forum_comment_bd1a2e3a` (`thread_id`),
  CONSTRAINT `content_ptr_id_refs_id_0a4bb8d0` FOREIGN KEY (`content_ptr_id`) REFERENCES `discussion_forum_content` (`id`),
  CONSTRAINT `thread_id_refs_content_ptr_id_c0d6e1b1` FOREIGN KEY (`thread_id`) REFERENCES `discussion_forum_thread` (`content_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discussion_forum_comment`
--

LOCK TABLES `discussion_forum_comment` WRITE;
/*!40000 ALTER TABLE `discussion_forum_comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `discussion_forum_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discussion_forum_content`
--

DROP TABLE IF EXISTS `discussion_forum_content`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discussion_forum_content` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `hit_count` int(11) NOT NULL,
  `forum_id` int(11) NOT NULL,
  `author_id` int(11) NOT NULL,
  `children_count` int(11) NOT NULL,
  `author_badge` varchar(2) NOT NULL,
  `content` longtext NOT NULL,
  `pinned` tinyint(1) NOT NULL,
  `anonymous` tinyint(1) NOT NULL,
  `disabled` tinyint(1) NOT NULL,
  `spam_count` int(11) NOT NULL,
  `upvotes` int(11) NOT NULL,
  `downvotes` int(11) NOT NULL,
  `popularity` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `discussion_forum_content_63b5ea41` (`created`),
  KEY `discussion_forum_content_ec9ad377` (`modified`),
  KEY `discussion_forum_content_f979685d` (`forum_id`),
  KEY `discussion_forum_content_e969df21` (`author_id`),
  KEY `discussion_forum_content_c8a0ade0` (`upvotes`),
  KEY `discussion_forum_content_22fcf4a8` (`downvotes`),
  KEY `discussion_forum_content_f476bdf4` (`popularity`),
  CONSTRAINT `author_id_refs_id_ab8f1fac` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `forum_id_refs_id_cbf5b4c5` FOREIGN KEY (`forum_id`) REFERENCES `discussion_forum_discussionforum` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discussion_forum_content`
--

LOCK TABLES `discussion_forum_content` WRITE;
/*!40000 ALTER TABLE `discussion_forum_content` DISABLE KEYS */;
INSERT INTO `discussion_forum_content` VALUES (1,'2014-01-03 16:23:28','2014-01-08 21:07:10',1,3,1,0,'IN','Reload removed',0,0,0,0,0,0,0),(2,'2014-01-03 16:26:50','2014-01-08 21:07:14',1,3,1,0,'IN','Hiding form after submit',0,0,0,0,0,0,0);
/*!40000 ALTER TABLE `discussion_forum_content` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discussion_forum_discussionforum`
--

DROP TABLE IF EXISTS `discussion_forum_discussionforum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discussion_forum_discussionforum` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `thread_count` int(11) NOT NULL,
  `abuse_threshold` int(11) NOT NULL,
  `review_threshold` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `discussion_forum_discussionforum_63b5ea41` (`created`),
  KEY `discussion_forum_discussionforum_ec9ad377` (`modified`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discussion_forum_discussionforum`
--

LOCK TABLES `discussion_forum_discussionforum` WRITE;
/*!40000 ALTER TABLE `discussion_forum_discussionforum` DISABLE KEYS */;
INSERT INTO `discussion_forum_discussionforum` VALUES (1,'2014-01-02 03:06:33','2014-01-02 03:06:33',0,5,2),(2,'2014-01-02 13:35:56','2014-01-02 13:35:56',0,5,2),(3,'2014-01-02 13:37:05','2014-01-03 16:26:50',2,5,2),(4,'2014-01-05 20:29:37','2014-01-05 20:29:37',0,5,2),(5,'2014-01-08 20:23:57','2014-01-08 20:23:57',0,5,2),(6,'2014-01-09 18:05:03','2014-01-09 18:05:03',0,5,2),(7,'2014-03-04 07:46:04','2014-03-04 07:46:04',0,5,2);
/*!40000 ALTER TABLE `discussion_forum_discussionforum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discussion_forum_notification`
--

DROP TABLE IF EXISTS `discussion_forum_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discussion_forum_notification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `subscription_id` int(11) NOT NULL,
  `notif_type` varchar(32) NOT NULL,
  `info` longtext NOT NULL,
  `is_processed` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `discussion_forum_notification_63b5ea41` (`created`),
  KEY `discussion_forum_notification_ec9ad377` (`modified`),
  KEY `discussion_forum_notification_b75baf19` (`subscription_id`),
  CONSTRAINT `subscription_id_refs_id_76b12b36` FOREIGN KEY (`subscription_id`) REFERENCES `util_subscription` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discussion_forum_notification`
--

LOCK TABLES `discussion_forum_notification` WRITE;
/*!40000 ALTER TABLE `discussion_forum_notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `discussion_forum_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discussion_forum_reply`
--

DROP TABLE IF EXISTS `discussion_forum_reply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discussion_forum_reply` (
  `content_ptr_id` int(11) NOT NULL,
  `thread_id` int(11) NOT NULL,
  `comment_id` int(11) NOT NULL,
  PRIMARY KEY (`content_ptr_id`),
  KEY `discussion_forum_reply_bd1a2e3a` (`thread_id`),
  KEY `discussion_forum_reply_3925f323` (`comment_id`),
  CONSTRAINT `comment_id_refs_content_ptr_id_6c8af965` FOREIGN KEY (`comment_id`) REFERENCES `discussion_forum_comment` (`content_ptr_id`),
  CONSTRAINT `content_ptr_id_refs_id_e06a673b` FOREIGN KEY (`content_ptr_id`) REFERENCES `discussion_forum_content` (`id`),
  CONSTRAINT `thread_id_refs_content_ptr_id_0b685e04` FOREIGN KEY (`thread_id`) REFERENCES `discussion_forum_thread` (`content_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discussion_forum_reply`
--

LOCK TABLES `discussion_forum_reply` WRITE;
/*!40000 ALTER TABLE `discussion_forum_reply` DISABLE KEYS */;
/*!40000 ALTER TABLE `discussion_forum_reply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discussion_forum_tag`
--

DROP TABLE IF EXISTS `discussion_forum_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discussion_forum_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `forum_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `tag_name` varchar(255) NOT NULL,
  `auto_generated` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `forum_id` (`forum_id`,`tag_name`),
  KEY `discussion_forum_tag_f979685d` (`forum_id`),
  CONSTRAINT `forum_id_refs_id_624016b3` FOREIGN KEY (`forum_id`) REFERENCES `discussion_forum_discussionforum` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discussion_forum_tag`
--

LOCK TABLES `discussion_forum_tag` WRITE;
/*!40000 ALTER TABLE `discussion_forum_tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `discussion_forum_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discussion_forum_thread`
--

DROP TABLE IF EXISTS `discussion_forum_thread`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discussion_forum_thread` (
  `content_ptr_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `subscription_id` int(11) NOT NULL,
  PRIMARY KEY (`content_ptr_id`),
  UNIQUE KEY `subscription_id` (`subscription_id`),
  CONSTRAINT `content_ptr_id_refs_id_94b2b300` FOREIGN KEY (`content_ptr_id`) REFERENCES `discussion_forum_content` (`id`),
  CONSTRAINT `subscription_id_refs_id_5a9e57c3` FOREIGN KEY (`subscription_id`) REFERENCES `util_subscription` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discussion_forum_thread`
--

LOCK TABLES `discussion_forum_thread` WRITE;
/*!40000 ALTER TABLE `discussion_forum_thread` DISABLE KEYS */;
INSERT INTO `discussion_forum_thread` VALUES (1,'Testing Reload',1),(2,'Hide Form',2);
/*!40000 ALTER TABLE `discussion_forum_thread` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discussion_forum_thread_tags`
--

DROP TABLE IF EXISTS `discussion_forum_thread_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discussion_forum_thread_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `thread_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `thread_id` (`thread_id`,`tag_id`),
  KEY `discussion_forum_thread_tags_bd1a2e3a` (`thread_id`),
  KEY `discussion_forum_thread_tags_5659cca2` (`tag_id`),
  CONSTRAINT `tag_id_refs_id_290fd80d` FOREIGN KEY (`tag_id`) REFERENCES `discussion_forum_tag` (`id`),
  CONSTRAINT `thread_id_refs_content_ptr_id_1c86627f` FOREIGN KEY (`thread_id`) REFERENCES `discussion_forum_thread` (`content_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discussion_forum_thread_tags`
--

LOCK TABLES `discussion_forum_thread_tags` WRITE;
/*!40000 ALTER TABLE `discussion_forum_thread_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `discussion_forum_thread_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discussion_forum_usersetting`
--

DROP TABLE IF EXISTS `discussion_forum_usersetting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discussion_forum_usersetting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `forum_id` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `email_digest` tinyint(1) NOT NULL,
  `super_user` tinyint(1) NOT NULL,
  `moderator` tinyint(1) NOT NULL,
  `badge` varchar(2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`forum_id`),
  KEY `discussion_forum_usersetting_63b5ea41` (`created`),
  KEY `discussion_forum_usersetting_ec9ad377` (`modified`),
  KEY `discussion_forum_usersetting_6340c63c` (`user_id`),
  KEY `discussion_forum_usersetting_f979685d` (`forum_id`),
  KEY `discussion_forum_usersetting_b478819c` (`user_id`,`forum_id`),
  CONSTRAINT `forum_id_refs_id_76578666` FOREIGN KEY (`forum_id`) REFERENCES `discussion_forum_discussionforum` (`id`),
  CONSTRAINT `user_id_refs_id_27100bc8` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discussion_forum_usersetting`
--

LOCK TABLES `discussion_forum_usersetting` WRITE;
/*!40000 ALTER TABLE `discussion_forum_usersetting` DISABLE KEYS */;
INSERT INTO `discussion_forum_usersetting` VALUES (1,'2014-01-02 03:06:33','2014-01-02 03:06:33',1,1,1,1,1,1,'IN'),(2,'2014-01-02 13:35:56','2014-01-02 13:35:56',1,2,1,1,1,1,'IN'),(3,'2014-01-02 13:37:05','2014-01-02 13:37:05',1,3,1,1,1,1,'IN'),(4,'2014-01-02 15:26:08','2014-01-02 15:26:08',2,3,1,1,0,0,'ST'),(5,'2014-01-02 16:00:37','2014-01-02 16:00:37',3,3,1,1,0,0,'ST'),(6,'2014-01-05 20:29:37','2014-01-05 20:29:37',1,4,1,1,1,1,'IN'),(7,'2014-01-08 20:23:57','2014-01-08 20:23:57',1,5,1,1,1,1,'IN'),(8,'2014-01-08 22:51:49','2014-01-08 22:51:49',10,3,1,1,0,0,'ST'),(9,'2014-01-09 13:31:54','2014-01-09 13:31:54',3,4,1,1,0,0,'ST'),(10,'2014-01-09 18:05:04','2014-01-09 18:05:04',1,6,1,1,1,1,'IN'),(11,'2014-01-09 18:16:14','2014-01-09 18:16:14',3,6,1,1,0,0,'ST'),(12,'2014-03-01 21:35:41','2014-03-01 21:35:41',17,3,1,1,0,0,'ST'),(13,'2014-03-04 07:46:04','2014-03-04 07:46:04',1,7,1,1,1,1,'IN'),(14,'2014-03-11 14:01:38','2014-03-11 14:01:38',17,4,1,1,0,0,'ST'),(15,'2014-03-20 13:39:53','2014-03-20 13:39:53',16,3,1,1,0,0,'ST');
/*!40000 ALTER TABLE `discussion_forum_usersetting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discussion_forum_vote`
--

DROP TABLE IF EXISTS `discussion_forum_vote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discussion_forum_vote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `content_id` int(11) NOT NULL,
  `upvote` tinyint(1) NOT NULL,
  `downvote` tinyint(1) NOT NULL,
  `spam` tinyint(1) NOT NULL,
  `spam_moderated` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`content_id`),
  KEY `discussion_forum_vote_6340c63c` (`user_id`),
  KEY `discussion_forum_vote_49185ad7` (`content_id`),
  KEY `discussion_forum_vote_f5b9478d` (`spam`),
  CONSTRAINT `content_id_refs_id_cb7420aa` FOREIGN KEY (`content_id`) REFERENCES `discussion_forum_content` (`id`),
  CONSTRAINT `user_id_refs_id_c497b406` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discussion_forum_vote`
--

LOCK TABLES `discussion_forum_vote` WRITE;
/*!40000 ALTER TABLE `discussion_forum_vote` DISABLE KEYS */;
/*!40000 ALTER TABLE `discussion_forum_vote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_6340c63c` (`user_id`),
  KEY `django_admin_log_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c0d12874` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'site','sites','site'),(7,'log entry','admin','logentry'),(8,'votable','util','votable'),(9,'subscription','util','subscription'),(10,'registration','registration','registration'),(11,'email update','registration','emailupdate'),(12,'forgot password','registration','forgotpassword'),(13,'discussion forum','discussion_forum','discussionforum'),(14,'tag','discussion_forum','tag'),(15,'user setting','discussion_forum','usersetting'),(16,'activity','discussion_forum','activity'),(17,'content','discussion_forum','content'),(18,'thread','discussion_forum','thread'),(19,'comment','discussion_forum','comment'),(20,'reply','discussion_forum','reply'),(21,'vote','discussion_forum','vote'),(22,'notification','discussion_forum','notification'),(23,'major','user_profile','major'),(24,'college','user_profile','college'),(25,'education','user_profile','education'),(26,'company','user_profile','company'),(27,'work','user_profile','work'),(28,'user profile','user_profile','userprofile'),(29,'custom user','user_profile','customuser'),(30,'notification email','notification','notificationemail'),(31,'parent category','courseware','parentcategory'),(32,'category','courseware','category'),(33,'course info','courseware','courseinfo'),(34,'course','courseware','course'),(35,'offering','courseware','offering'),(36,'course history','courseware','coursehistory'),(37,'group','courseware','group'),(38,'group history','courseware','grouphistory'),(39,'concept','courseware','concept'),(40,'concept history','courseware','concepthistory'),(41,'quiz','quiz','quiz'),(42,'question module','quiz','questionmodule'),(43,'quiz history','quiz','quizhistory'),(44,'question','quiz','question'),(45,'descriptive question','quiz','descriptivequestion'),(46,'single choice question','quiz','singlechoicequestion'),(47,'multiple choice question','quiz','multiplechoicequestion'),(48,'fixed answer question','quiz','fixedanswerquestion'),(49,'programming question','quiz','programmingquestion'),(50,'testcase','quiz','testcase'),(51,'question history','quiz','questionhistory'),(52,'queue','quiz','queue'),(53,'submission','quiz','submission'),(54,'video','video','video'),(55,'video history','video','videohistory'),(56,'marker','video','marker'),(57,'section marker','video','sectionmarker'),(58,'quiz marker','video','quizmarker'),(59,'concept quiz history','concept','conceptquizhistory'),(60,'concept document history','concept','conceptdocumenthistory'),(61,'document','document','document'),(62,'section','document','section'),(63,'program errors','assignments','programerrors'),(64,'testcase errors','assignments','testcaseerrors');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `document_document`
--

DROP TABLE IF EXISTS `document_document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `document_document` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `uid` varchar(32) NOT NULL,
  `is_heading` tinyint(1) NOT NULL,
  `is_link` tinyint(1) NOT NULL,
  `link` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `playlist` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `document_document`
--

LOCK TABLES `document_document` WRITE;
/*!40000 ALTER TABLE `document_document` DISABLE KEYS */;
INSERT INTO `document_document` VALUES (1,'dummy','7c2c7ec7804748b8881b8e69244a9eb9',0,0,'','dummy','[]'),(2,'Sample Page','81c6bb352a45429791f3d432d492808e',1,0,'','','[[1, 0]]'),(3,'dummy','90103ddbd7714f2c8484900374fe2131',0,0,'','dummy','[]'),(4,'xxx','136cc318eb19461d87e417c5043c86fc',0,0,'','See below files','[[2, 0]]'),(5,'Wiki','550ab888021a4e0eb21cbe462abd3b03',1,0,'','specifies schedule','[[4, 0]]'),(6,'dummy','ecfa2f4d8f124183bc3da30fc65e5ebb',0,0,'','dummy','[]'),(7,'dummy','0979c71623114021b7b0f7d3f456dd10',0,0,'','dummy','[]'),(8,'References','1bd837ad9c944226bf0b78fae2b61e16',0,0,'','Look at [IITB site][1]\r\n\r\n\r\n  [1]: http://www.iitb.ac.in','[[5, 0]]'),(9,'dummy','53afcbbb89be4b92b768072086fb625e',0,0,'','dummy','[]'),(10,'dummy','b39ad332ef71471e85deef663a2a32d3',0,0,'','dummy','[]'),(11,'dummy','059728f6f93040339708838aeef8a48e',0,0,'','dummy','[]'),(12,'dummy','86efeca57b354280babfa1ac5898dbf1',0,0,'','dummy','[]'),(13,'dummy','a19219b2522641308350431f205cc620',0,0,'','dummy','[]'),(14,'Dummy reference','956cc769a86a4b9a911e507a53cf51df',0,0,'','[http://www.cse.iitb.ac.in/~br/][1]\r\n\r\n\r\n  [1]: http://www.cse.iitb.ac.in/~br/','[]'),(15,'testing delete','b14ffde103764872bddf24e9518b1d6a',0,0,'','','[]'),(16,'dummy','96f8f01e20004a29a90ca5680e66a6a6',0,0,'','dummy','[]'),(17,'dummy','6ce01232237b4ad097abe25ffdc0e015',0,0,'','dummy','[]'),(18,'dummy','35d550afc8584249a980bf38fabb2a4f',0,0,'','dummy','[]'),(19,'dummy','1479381efdfd4094b55ad668efcd6a84',0,0,'','dummy','[]'),(20,'dummy','b7afdc81161f4e8a9ef686abafc5effe',0,0,'','dummy','[]');
/*!40000 ALTER TABLE `document_document` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `document_section`
--

DROP TABLE IF EXISTS `document_section`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `document_section` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `document_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `file` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `document_section_b7398729` (`document_id`),
  CONSTRAINT `document_id_refs_id_372a1758` FOREIGN KEY (`document_id`) REFERENCES `document_document` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `document_section`
--

LOCK TABLES `document_section` WRITE;
/*!40000 ALTER TABLE `document_section` DISABLE KEYS */;
INSERT INTO `document_section` VALUES (1,2,'Sample Section','Sample\n\n 1. Enter\n 2. Enter\n 3. Enter',''),(2,4,'File-1','   ','uploads/section/problem.jpg'),(4,5,'week-1','- motivation\n - \n\nSample Heading\n---------',''),(5,8,'Paper-1',' ','uploads/section/motivation-slides.pdf');
/*!40000 ALTER TABLE `document_section` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evaluate_assignmentresults`
--

DROP TABLE IF EXISTS `evaluate_assignmentresults`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `evaluate_assignmentresults` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `submission_id` int(11) NOT NULL,
  `submitted_files` longtext,
  `is_stale` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `evaluate_assignmentresults_efe1f810` (`submission_id`),
  CONSTRAINT `submission_id_refs_id_1cb8bfd7` FOREIGN KEY (`submission_id`) REFERENCES `upload_upload` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluate_assignmentresults`
--

LOCK TABLES `evaluate_assignmentresults` WRITE;
/*!40000 ALTER TABLE `evaluate_assignmentresults` DISABLE KEYS */;
INSERT INTO `evaluate_assignmentresults` VALUES (3,3,'main.cpp',0),(5,5,'main.cpp',0),(6,6,'main.cpp',0);
/*!40000 ALTER TABLE `evaluate_assignmentresults` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evaluate_programresults`
--

DROP TABLE IF EXISTS `evaluate_programresults`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `evaluate_programresults` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `program_id` int(11) NOT NULL,
  `assignment_result_id` int(11) NOT NULL,
  `missing_file_names` longtext,
  `compiler_errors` longtext,
  `compiler_output` longtext,
  `compiler_return_code` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `evaluate_programresults_cdb5484e` (`program_id`),
  KEY `evaluate_programresults_2e751ff0` (`assignment_result_id`),
  CONSTRAINT `assignment_result_id_refs_id_dd802516` FOREIGN KEY (`assignment_result_id`) REFERENCES `evaluate_assignmentresults` (`id`),
  CONSTRAINT `program_id_refs_id_73275bab` FOREIGN KEY (`program_id`) REFERENCES `assignments_program` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluate_programresults`
--

LOCK TABLES `evaluate_programresults` WRITE;
/*!40000 ALTER TABLE `evaluate_programresults` DISABLE KEYS */;
INSERT INTO `evaluate_programresults` VALUES (3,2,3,'','','',0),(5,2,5,'','','',0);
/*!40000 ALTER TABLE `evaluate_programresults` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evaluate_testcaseresult`
--

DROP TABLE IF EXISTS `evaluate_testcaseresult`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `evaluate_testcaseresult` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `test_case_id` int(11) NOT NULL,
  `program_result_id` int(11) NOT NULL,
  `error_messages` longtext,
  `return_code` int(11) DEFAULT NULL,
  `test_passed` tinyint(1) NOT NULL,
  `output_files` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `evaluate_testcaseresult_d0522801` (`test_case_id`),
  KEY `evaluate_testcaseresult_fcc1256a` (`program_result_id`),
  CONSTRAINT `program_result_id_refs_id_2fab1973` FOREIGN KEY (`program_result_id`) REFERENCES `evaluate_programresults` (`id`),
  CONSTRAINT `test_case_id_refs_id_c092b133` FOREIGN KEY (`test_case_id`) REFERENCES `assignments_testcase` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluate_testcaseresult`
--

LOCK TABLES `evaluate_testcaseresult` WRITE;
/*!40000 ALTER TABLE `evaluate_testcaseresult` DISABLE KEYS */;
INSERT INTO `evaluate_testcaseresult` VALUES (3,2,3,'/bin/bash: None: No such file or directory\n',1,0,'results/2014/03/21/output_file_2.tar.bz2'),(5,2,5,'/bin/bash: None: No such file or directory\n',1,0,'results/2014/03/21/output_file_2.tar_1.bz2');
/*!40000 ALTER TABLE `evaluate_testcaseresult` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification_notificationemail`
--

DROP TABLE IF EXISTS `notification_notificationemail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notification_notificationemail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `service` varchar(50) NOT NULL,
  `email_subject` varchar(50) NOT NULL,
  `text_email_body` longtext NOT NULL,
  `html_email_body` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `notification_notificationemail_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_17391f39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification_notificationemail`
--

LOCK TABLES `notification_notificationemail` WRITE;
/*!40000 ALTER TABLE `notification_notificationemail` DISABLE KEYS */;
/*!40000 ALTER TABLE `notification_notificationemail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_descriptivequestion`
--

DROP TABLE IF EXISTS `quiz_descriptivequestion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_descriptivequestion` (
  `question_ptr_id` int(11) NOT NULL,
  `answer` longtext NOT NULL,
  PRIMARY KEY (`question_ptr_id`),
  CONSTRAINT `question_ptr_id_refs_id_892e5c94` FOREIGN KEY (`question_ptr_id`) REFERENCES `quiz_question` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_descriptivequestion`
--

LOCK TABLES `quiz_descriptivequestion` WRITE;
/*!40000 ALTER TABLE `quiz_descriptivequestion` DISABLE KEYS */;
/*!40000 ALTER TABLE `quiz_descriptivequestion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_fixedanswerquestion`
--

DROP TABLE IF EXISTS `quiz_fixedanswerquestion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_fixedanswerquestion` (
  `question_ptr_id` int(11) NOT NULL,
  `answer` varchar(128) NOT NULL,
  PRIMARY KEY (`question_ptr_id`),
  CONSTRAINT `question_ptr_id_refs_id_2d23f0b5` FOREIGN KEY (`question_ptr_id`) REFERENCES `quiz_question` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_fixedanswerquestion`
--

LOCK TABLES `quiz_fixedanswerquestion` WRITE;
/*!40000 ALTER TABLE `quiz_fixedanswerquestion` DISABLE KEYS */;
INSERT INTO `quiz_fixedanswerquestion` VALUES (3,'[`4`,`4.0`]'),(4,'[`4`]'),(6,'[`[\\`4\\`]`]'),(7,'[]'),(8,'[]'),(10,'[`[]`]'),(11,'[`8`]'),(41,'[]'),(69,'[`20`,`20.0`]'),(72,'[`[\\`0\\`]`,`0.0`]'),(73,'[`[\\`0\\`]`]'),(83,'[]'),(103,'[`6`]'),(104,'[`12`]'),(126,'[`9`,`9.0`]');
/*!40000 ALTER TABLE `quiz_fixedanswerquestion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_multiplechoicequestion`
--

DROP TABLE IF EXISTS `quiz_multiplechoicequestion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_multiplechoicequestion` (
  `question_ptr_id` int(11) NOT NULL,
  `options` longtext NOT NULL,
  `answer` longtext NOT NULL,
  PRIMARY KEY (`question_ptr_id`),
  CONSTRAINT `question_ptr_id_refs_id_d168d3e7` FOREIGN KEY (`question_ptr_id`) REFERENCES `quiz_question` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_multiplechoicequestion`
--

LOCK TABLES `quiz_multiplechoicequestion` WRITE;
/*!40000 ALTER TABLE `quiz_multiplechoicequestion` DISABLE KEYS */;
INSERT INTO `quiz_multiplechoicequestion` VALUES (12,'[`1`,`2`,`3`,`4`]','[false,true,false,false]'),(46,'[`zero`,`one`,`two`,`three`]','[false,true,true,false]'),(49,'[`zero`,`one`,`two`,`three`]','[false,true,true,false]'),(66,'[`5`,`-7000`,`6`,`800`]','[true,true,false,false]'),(92,'[`wrong`,`correct`,`correct`,`wrong`]','[false,true,true,false]');
/*!40000 ALTER TABLE `quiz_multiplechoicequestion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_programmingquestion`
--

DROP TABLE IF EXISTS `quiz_programmingquestion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_programmingquestion` (
  `question_ptr_id` int(11) NOT NULL,
  `num_testcases` int(11) NOT NULL,
  `command` longtext NOT NULL,
  `acceptable_languages` longtext NOT NULL,
  PRIMARY KEY (`question_ptr_id`),
  CONSTRAINT `question_ptr_id_refs_id_2680ecfa` FOREIGN KEY (`question_ptr_id`) REFERENCES `quiz_question` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_programmingquestion`
--

LOCK TABLES `quiz_programmingquestion` WRITE;
/*!40000 ALTER TABLE `quiz_programmingquestion` DISABLE KEYS */;
/*!40000 ALTER TABLE `quiz_programmingquestion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_question`
--

DROP TABLE IF EXISTS `quiz_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hit_count` int(11) NOT NULL,
  `quiz_id` int(11) NOT NULL,
  `question_module_id` int(11) NOT NULL,
  `description` longtext NOT NULL,
  `hint` longtext,
  `grader_type` varchar(1) NOT NULL,
  `answer_description` longtext NOT NULL,
  `marks` double NOT NULL,
  `gradable` tinyint(1) NOT NULL,
  `granularity` longtext NOT NULL,
  `granularity_hint` longtext,
  `type` varchar(1) NOT NULL,
  `attempts` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `quiz_question_eecda460` (`quiz_id`),
  KEY `quiz_question_e5315577` (`question_module_id`),
  CONSTRAINT `question_module_id_refs_id_e026391f` FOREIGN KEY (`question_module_id`) REFERENCES `quiz_questionmodule` (`id`),
  CONSTRAINT `quiz_id_refs_id_e107ebdf` FOREIGN KEY (`quiz_id`) REFERENCES `quiz_quiz` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=129 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_question`
--

LOCK TABLES `quiz_question` WRITE;
/*!40000 ALTER TABLE `quiz_question` DISABLE KEYS */;
INSERT INTO `quiz_question` VALUES (3,0,1,1,'2+2',NULL,'D','',5,1,'5.0,5.0,0','5.0,5.0,0','F',2),(4,0,5,2,'2+2=?',NULL,'D','4',1,1,'1.0,0','1.0,0','F',1),(6,0,6,3,'2+2=?',NULL,'D','4',1,1,'1.0,0','1.0,0','F',1),(7,0,6,3,'Test','hint','M','Answer description',0,1,'0.0,0','0.0,0','F',1),(8,0,6,3,'test',NULL,'D','test',0,1,'0.0,0','0.0,0','F',1),(10,0,6,4,'3+1=?',NULL,'D','4',4,1,'4.0,4.0,4.0,0','4.0,4.0,4.0,0','F',3),(11,0,6,5,'4+4=?',NULL,'D','8',1,1,'1.0,0','1.0,0','F',1),(12,0,5,8,'What is 1+1? Answer in the space. blahjdkdkvdvvfdbbgnbtntntntntn\ntntntn',NULL,'D','2',2,1,'2.0,0','2.0,0','M',1),(13,0,7,9,'Default Question Text',NULL,'D','',0,1,'0,0','0,0','S',1),(14,0,8,10,'What is the first thing you do when you wake up in the morning?',NULL,'D','',0,1,'0,0','0,0','S',1),(15,0,9,11,'Guess the approximate number of emails that are sent per day.',NULL,'D','',0,1,'0,0','0,0','S',1),(16,0,10,12,'Default Question Text',NULL,'D','',0,1,'0,0','0,0','S',1),(17,0,11,13,'What is the first thing you do when you wake up in the morning?',NULL,'D','',0,1,'0,0','0,0','S',1),(18,0,12,14,'Guess the approximate number of emails that are sent per day.',NULL,'D','',0,1,'0,0','0,0','S',1),(19,0,13,15,'Default Question Text',NULL,'D','',0,1,'0,0','0,0','S',1),(20,0,14,16,'What is the first thing you do when you wake up in the morning?',NULL,'D','',0,1,'0,0','0,0','S',1),(21,0,15,17,'Guess the approximate number of emails that are sent per day.',NULL,'D','',0,1,'0,0','0,0','S',1),(22,0,16,18,'Default Question Text',NULL,'D','',0,1,'0,0','0,0','S',1),(23,0,17,19,'What is the first thing you do when you wake up in the morning?',NULL,'D','',0,1,'0,0','0,0','S',1),(24,0,18,20,'Guess the approximate number of emails that are sent per day.',NULL,'D','',0,1,'0,0','0,0','S',1),(25,0,19,21,'Default Question Text',NULL,'D','',0,1,'0,0','0,0','S',1),(26,0,20,22,'What is the first thing you do when you wake up in the morning?',NULL,'D','',0,1,'0,0','0,0','S',1),(27,0,21,23,'Guess the approximate number of emails that are sent per day.',NULL,'D','',0,1,'0,0','0,0','S',1),(28,0,22,24,'Default Question Text',NULL,'D','',0,1,'0,0','0,0','S',1),(29,0,23,25,'What is the first thing you do when you wake up in the morning?',NULL,'D','',0,1,'0,0','0,0','S',1),(30,0,24,26,'Guess the approximate number of emails that are sent per day.',NULL,'D','',0,1,'0,0','0,0','S',1),(31,0,25,27,'Default Question Text',NULL,'D','',0,1,'0,0','0,0','S',1),(32,0,26,28,'What is the first thing you do when you wake up in the morning?',NULL,'D','',0,1,'0,0','0,0','S',1),(34,0,27,29,'Guess the approximate number of emails that are sent per day.',NULL,'D','',1,1,'0,0','0,0','S',2),(35,0,27,29,'Guess the approximate number of emails that are sent per day.',NULL,'D','',2,1,'0,0','0,0','S',2),(36,0,27,29,'Guess the approximate number of emails that are sent per day.',NULL,'D','',2,1,'0,0','0,0','S',2),(37,0,27,29,'Guess the approximate number of emails that are sent per day.',NULL,'D','',2,1,'0,0','0,0','S',2),(38,0,27,29,'Guess the approximate number of emails that are sent per day.',NULL,'D','',2,1,'0,0','0,0','S',1),(41,0,28,32,'Descriptive',NULL,'D','blah blah',0,1,'0.0,0','0.0,0','F',1),(42,0,28,31,'Blah Blah',NULL,'D','14',4,1,'4.0,4.0,4.0,0','4.0,4.0,4.0,0','S',3),(46,0,28,30,'1,2',NULL,'D','',5,0,'5.0,5.0,5.0,5.0,0','5.0,5.0,5.0,5.0,0','M',4),(48,0,30,35,'1',NULL,'D','',3,0,'3.0,0','3.0,0','S',1),(49,0,30,35,'1,2',NULL,'D','',5,0,'5.0,0','5.0,0','M',1),(50,0,32,36,'Default Question Text',NULL,'D','',0,1,'0,0','0,0','S',1),(51,0,34,37,'Default Question Text',NULL,'D','',0,1,'0,0','0,0','S',1),(52,0,36,38,'Default Question Text',NULL,'D','',0,1,'0,0','0,0','S',1),(53,0,38,39,'Default Question Text',NULL,'D','',0,1,'0,0','0,0','S',1),(54,0,39,40,'What is the first thing you do when you wake up in the morning?',NULL,'D','',0,1,'0,0','0,0','S',1),(55,0,40,41,'Guess the approximate number of emails that are sent per day.',NULL,'D','',0,1,'0,0','0,0','S',1),(56,0,41,42,'Default Question Text',NULL,'D','',0,1,'0,0','0,0','S',1),(57,0,42,43,'What is the first thing you do when you wake up in the morning?',NULL,'D','',0,1,'0,0','0,0','S',1),(58,0,43,44,'Guess the approximate number of emails that are sent per day.',NULL,'D','',0,1,'0,0','0,0','S',1),(62,0,47,48,'What is the first thing you do when you wake up in the morning?',NULL,'D','',0,1,'0,0','0,0','S',1),(65,0,49,50,'Guess the approximate number of emails that are sent per day.',NULL,'D','',0,1,'0,0','0,0','S',1),(66,0,50,51,'What is -6999-1',NULL,'D','This is basic math',4,0,'4.0,4.0,0','4.0,4.0,0','M',2),(69,0,50,51,'What is 10+10?',NULL,'D','20',4,0,'4.0,4.0,0','4.0,4.0,0','F',2),(72,0,28,30,'test',NULL,'D','0',2,0,'2.0,0','2.0,0','F',1),(73,0,28,30,'test',NULL,'D','0',2,0,'2.0,0','2.0,0','F',1),(83,0,48,49,'test with no answer',NULL,'D','test',5,0,'5.0,5.0,0','5.0,5.0,0','F',2),(84,0,28,30,'Tested for normal quiz',NULL,'D','3',2,0,'2.0,1.0,0','1.0,0.5,0','S',2),(92,0,48,49,'test multichoice',NULL,'D','',2,0,'2.0,0','2.0,0','M',1),(93,0,48,49,'1+1 = ?',NULL,'D','',2,0,'2.0,2.0,0','2.0,2.0,0','S',2),(97,0,28,30,'1',NULL,'D','',5,0,'5.0,3.0,0','5.0,3.0,0','S',2),(98,0,51,52,'What is the first thing you do when you wake up in the morning?',NULL,'D','',0,1,'0,0','0,0','S',1),(101,0,53,54,'Guess the approximate number of emails that are sent per day.',NULL,'D','',0,1,'0,0','0,0','S',1),(103,0,54,55,'What is 3+3?',NULL,'D','6',4,0,'4.0,2.0,0','4.0,2.0,0','F',2),(104,0,54,55,'What is 6+6?',NULL,'D','12',5,0,'5.0,4.0,3.0,0','5.0,4.0,3.0,0','F',3),(105,0,52,53,'What is 2+2?',NULL,'D','',4,0,'4.0,2.0,0','4.0,2.0,0','S',2),(107,0,52,53,'What is 2+3?',NULL,'D','simple!',6,0,'4.0,2.0,0','4.0,2.0,0','S',2),(108,0,55,56,'Default Question Text',NULL,'D','',0,1,'0,0','0,0','S',1),(109,0,56,57,'What is the first thing you do when you wake up in the morning?',NULL,'D','',0,1,'0,0','0,0','S',1),(110,0,57,58,'Guess the approximate number of emails that are sent per day.',NULL,'D','',0,1,'0,0','0,0','S',1),(111,0,58,59,'Default Question Text',NULL,'D','',0,1,'0,0','0,0','S',1),(112,0,59,60,'What is the first thing you do when you wake up in the morning?',NULL,'D','',0,1,'0,0','0,0','S',1),(113,0,60,61,'Guess the approximate number of emails that are sent per day.',NULL,'D','',0,1,'0,0','0,0','S',1),(118,0,61,62,'What is the first thing you do when you wake up in the morning?',NULL,'D','Really?',2,0,'2.0,0','2.0,0','S',1),(119,0,62,63,'What is 2+2?',NULL,'D','',4,0,'4.0,2.0,0','4.0,2.0,0','S',2),(120,0,62,63,'What is 2+3?',NULL,'D','',6,0,'6.0,3.0,0','6.0,3.0,0','S',2),(121,0,63,64,'Guess the approximate number of emails that are sent per day.',NULL,'D','',2,0,'2.0,0','2.0,0','S',1),(122,0,64,65,'What is the first thing you do when you wake up in the morning?',NULL,'D','',0,1,'0,0','0,0','S',1),(123,0,65,66,'What is 2+2?',NULL,'D','',0,1,'0,0','0,0','S',1),(124,0,65,66,'What is 2+3?',NULL,'D','',0,1,'0,0','0,0','S',1),(125,0,66,67,'Guess the approximate number of emails that are sent per day.',NULL,'D','',0,1,'0,0','0,0','S',1),(126,0,67,68,'What is 4+5?',NULL,'D','Its simple really!',4,0,'4.0,2.0,0','4.0,2.0,0','F',2),(128,0,46,47,'Guess the approximate number of emails that are sent per day.',NULL,'D','',0,0,'0.0,0','0.0,0','S',1);
/*!40000 ALTER TABLE `quiz_question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_questionhistory`
--

DROP TABLE IF EXISTS `quiz_questionhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_questionhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `attempts` int(11) NOT NULL,
  `marks` double NOT NULL,
  `status` varchar(1) NOT NULL,
  `hint_taken` tinyint(1) NOT NULL,
  `answer_shown` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `question_id` (`question_id`,`student_id`),
  KEY `quiz_questionhistory_25110688` (`question_id`),
  KEY `quiz_questionhistory_94741166` (`student_id`),
  CONSTRAINT `question_id_refs_id_0508d842` FOREIGN KEY (`question_id`) REFERENCES `quiz_question` (`id`),
  CONSTRAINT `student_id_refs_id_55a5edb0` FOREIGN KEY (`student_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_questionhistory`
--

LOCK TABLES `quiz_questionhistory` WRITE;
/*!40000 ALTER TABLE `quiz_questionhistory` DISABLE KEYS */;
INSERT INTO `quiz_questionhistory` VALUES (2,3,1,2,5,'S',0,1),(3,6,1,1,0,'O',0,1),(4,7,1,0,0,'N',0,0),(5,4,1,1,1,'S',0,1),(6,8,1,1,0,'O',0,1),(7,10,1,0,0,'N',0,0),(8,11,1,0,0,'N',0,0),(9,12,1,1,2,'S',0,1),(10,19,1,0,0,'N',0,0),(11,20,1,0,0,'N',0,0),(12,21,1,0,0,'N',0,0),(13,31,1,1,0,'S',0,1),(15,32,1,1,0,'S',0,1),(16,34,1,1,0,'O',0,0),(17,35,1,1,0,'S',0,1),(18,36,1,1,0,'S',0,1),(19,37,1,0,0,'N',0,0),(20,38,1,0,0,'N',0,0),(23,41,1,1,0,'O',0,1),(24,42,1,3,4,'S',0,1),(26,42,3,3,4,'S',0,1),(27,41,3,0,0,'N',0,0),(29,31,3,1,0,'S',0,1),(32,46,1,1,5,'S',0,1),(34,48,1,1,3,'S',0,1),(35,49,1,1,5,'S',0,1),(36,57,1,1,0,'S',0,1),(37,56,1,1,0,'S',0,1),(38,62,1,1,0,'S',0,1),(41,65,1,1,0,'O',0,1),(42,66,1,0,0,'N',0,0),(45,69,1,0,0,'N',0,0),(47,13,1,0,0,'N',0,0),(48,14,1,0,0,'N',0,0),(49,15,1,0,0,'N',0,0),(50,16,1,0,0,'N',0,0),(51,17,1,0,0,'N',0,0),(52,18,1,0,0,'N',0,0),(53,22,1,0,0,'N',0,0),(54,23,1,0,0,'N',0,0),(55,24,1,0,0,'N',0,0),(56,25,1,0,0,'N',0,0),(57,26,1,0,0,'N',0,0),(58,27,1,0,0,'N',0,0),(59,28,1,0,0,'N',0,0),(60,29,1,0,0,'N',0,0),(61,30,1,0,0,'N',0,0),(62,50,1,0,0,'N',0,0),(63,51,1,0,0,'N',0,0),(64,52,1,0,0,'N',0,0),(65,72,1,0,0,'N',0,0),(66,54,1,0,0,'N',0,0),(67,53,1,0,0,'N',0,0),(68,73,1,0,0,'N',0,0),(69,55,1,0,0,'N',0,0),(70,58,1,0,0,'N',0,0),(74,84,1,2,0,'O',0,1),(76,97,1,2,3,'S',0,1),(77,98,1,1,0,'O',0,1),(80,103,1,2,2,'S',0,1),(81,104,1,3,3,'S',0,1),(82,111,1,1,0,'S',0,1),(83,105,1,1,4,'S',0,1),(84,107,1,2,2,'S',0,1),(85,98,3,1,0,'O',0,1),(86,62,3,1,0,'O',0,1),(87,83,3,1,0,'O',0,0),(88,92,3,1,2,'S',0,1),(89,93,3,1,2,'S',0,1),(90,65,3,1,0,'S',0,1),(91,105,3,1,4,'S',0,1),(92,107,3,2,2,'S',0,1),(93,118,3,1,0,'O',0,1),(94,119,3,2,2,'S',0,1),(95,120,3,1,6,'S',0,1),(96,46,3,0,0,'N',0,0),(97,72,3,0,0,'N',0,0),(98,73,3,0,0,'N',0,0),(99,84,3,0,0,'N',0,0),(100,97,3,0,0,'N',0,0),(101,66,3,0,0,'N',0,0),(102,69,3,0,0,'N',0,0),(103,101,3,0,0,'N',0,0),(104,103,3,0,0,'N',0,0),(105,104,3,0,0,'N',0,0),(106,121,3,0,0,'N',0,0),(107,126,3,2,2,'S',0,1),(108,46,17,0,0,'N',0,0),(109,72,17,0,0,'N',0,0),(110,73,17,0,0,'N',0,0),(111,84,17,0,0,'N',0,0),(112,97,17,0,0,'N',0,0);
/*!40000 ALTER TABLE `quiz_questionhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_questionmodule`
--

DROP TABLE IF EXISTS `quiz_questionmodule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_questionmodule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `quiz_id` int(11) NOT NULL,
  `title` longtext NOT NULL,
  `playlist` longtext NOT NULL,
  `questions` int(11) NOT NULL,
  `dummy` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `quiz_questionmodule_eecda460` (`quiz_id`),
  CONSTRAINT `quiz_id_refs_id_7ce7c59c` FOREIGN KEY (`quiz_id`) REFERENCES `quiz_quiz` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_questionmodule`
--

LOCK TABLES `quiz_questionmodule` WRITE;
/*!40000 ALTER TABLE `quiz_questionmodule` DISABLE KEYS */;
INSERT INTO `quiz_questionmodule` VALUES (1,1,'Sample Module','[]',2,0),(2,5,'Easy','[]',1,0),(3,6,'Easy','[]',4,0),(4,6,'2','[]',2,0),(5,6,'3','[]',1,0),(6,6,'xxx','[]',0,0),(7,6,'xx','[]',0,0),(8,5,'quiz-2','[]',1,0),(9,7,'Dummy Title','[]',1,1),(10,8,'Dummy Title','[]',1,1),(11,9,'Dummy Title','[]',1,1),(12,10,'Dummy Title','[]',1,1),(13,11,'Dummy Title','[]',1,1),(14,12,'Dummy Title','[]',1,1),(15,13,'Dummy Title','[]',1,1),(16,14,'Dummy Title','[]',1,1),(17,15,'Dummy Title','[]',1,1),(18,16,'Dummy Title','[]',1,1),(19,17,'Dummy Title','[]',1,1),(20,18,'Dummy Title','[]',1,1),(21,19,'Dummy Title','[]',1,1),(22,20,'Dummy Title','[]',1,1),(23,21,'Dummy Title','[]',1,1),(24,22,'Dummy Title','[]',1,1),(25,23,'Dummy Title','[]',1,1),(26,24,'Dummy Title','[]',1,1),(27,25,'Dummy Title','[]',1,1),(28,26,'Dummy Title','[]',1,1),(29,27,'Dummy Title','[]',5,1),(30,28,'Test-1','[]',12,0),(31,28,'Link-layer','[]',1,0),(32,28,'Descriptive','[]',1,0),(33,29,'test','[]',0,0),(34,25,'New Module','[]',0,0),(35,30,'Testing Module Reload','[]',2,0),(36,32,'Dummy Title','[]',1,1),(37,34,'Dummy Title','[]',1,1),(38,36,'Dummy Title','[]',1,1),(39,38,'Dummy Title','[]',1,1),(40,39,'Dummy Title','[]',1,1),(41,40,'Dummy Title','[]',1,1),(42,41,'Dummy Title','[]',1,1),(43,42,'Dummy Title','[]',1,1),(44,43,'Dummy Title','[]',1,1),(45,44,'Dummy Title','[]',0,1),(46,45,'Dummy Title','[]',0,1),(47,46,'Dummy Title','[]',2,1),(48,47,'Dummy Title','[]',1,1),(49,48,'Dummy Title','[]',16,1),(50,49,'Dummy Title','[]',1,1),(51,50,'Module-1','[]',4,0),(52,51,'Dummy Title','[]',1,1),(53,52,'Dummy Title','[]',6,1),(54,53,'Dummy Title','[]',1,1),(55,54,'This description applies to a bunch of questions','[]',2,0),(56,55,'Dummy Title','[]',1,1),(57,56,'Dummy Title','[]',1,1),(58,57,'Dummy Title','[]',1,1),(59,58,'Dummy Title','[]',1,1),(60,59,'Dummy Title','[]',1,1),(61,60,'Dummy Title','[]',1,1),(62,61,'Dummy Title','[]',1,1),(63,62,'Dummy Title','[]',2,1),(64,63,'Dummy Title','[]',1,1),(65,64,'Dummy Title','[]',1,1),(66,65,'Dummy Title','[]',2,1),(67,66,'Dummy Title','[]',1,1),(68,67,'Test question module','[]',1,0);
/*!40000 ALTER TABLE `quiz_questionmodule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_queue`
--

DROP TABLE IF EXISTS `quiz_queue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_queue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `object_id` longtext NOT NULL,
  `is_processed` tinyint(1) NOT NULL,
  `object_type` varchar(1) NOT NULL,
  `info` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `quiz_queue_63b5ea41` (`created`),
  KEY `quiz_queue_ec9ad377` (`modified`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_queue`
--

LOCK TABLES `quiz_queue` WRITE;
/*!40000 ALTER TABLE `quiz_queue` DISABLE KEYS */;
/*!40000 ALTER TABLE `quiz_queue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_quiz`
--

DROP TABLE IF EXISTS `quiz_quiz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_quiz` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` longtext NOT NULL,
  `question_modules` int(11) NOT NULL,
  `questions` int(11) NOT NULL,
  `marks` double NOT NULL,
  `playlist` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_quiz`
--

LOCK TABLES `quiz_quiz` WRITE;
/*!40000 ALTER TABLE `quiz_quiz` DISABLE KEYS */;
INSERT INTO `quiz_quiz` VALUES (1,'Sample Quiz',1,2,10,'[]'),(2,'Sample',0,0,0,'[]'),(3,'Quiz 1',0,0,0,'[]'),(4,'Quiz 1',0,0,0,'[]'),(5,'Quiz-New',2,2,3,'[]'),(6,'Quiz',5,7,11,'[]'),(7,'Quiz 1',1,1,0,'[]'),(8,'Quiz: First-thing-in-morning',1,1,0,'[]'),(9,'Quiz: Emails-per-day',1,1,0,'[]'),(10,'Quiz 1',1,1,0,'[]'),(11,'Quiz: First-thing-in-morning',1,1,0,'[]'),(12,'Quiz: Emails-per-day',1,1,0,'[]'),(13,'Quiz 1',1,1,0,'[]'),(14,'Quiz: First-thing-in-morning',1,1,0,'[]'),(15,'Quiz: Emails-per-day',1,1,0,'[]'),(16,'Quiz 1',1,1,0,'[]'),(17,'Quiz: First-thing-in-morning',1,1,0,'[]'),(18,'Quiz: Emails-per-day',1,1,0,'[]'),(19,'Quiz 1',1,1,0,'[]'),(20,'Quiz: First-thing-in-morning',1,1,0,'[]'),(21,'Quiz: Emails-per-day',1,1,0,'[]'),(22,'Quiz 1',1,1,0,'[]'),(23,'Quiz: First-thing-in-morning',1,1,0,'[]'),(24,'Quiz: Emails-per-day',1,1,0,'[]'),(25,'Quiz 1',2,1,0,'[]'),(26,'Quiz: First-thing-in-morning',1,1,0,'[]'),(27,'Quiz: Emails-per-day',1,5,8,'[]'),(28,'Quiz',3,14,43,'[]'),(29,'Quiz-test',1,0,0,'[]'),(30,'Testing Quiz',1,2,3,'[]'),(31,'Quiz 1',0,0,0,'[]'),(32,'Quiz 1',1,1,0,'[]'),(33,'Quiz: First-thing-in-morning',0,0,0,'[]'),(34,'Quiz 1',1,1,0,'[]'),(35,'Quiz: First-thing-in-morning',0,0,0,'[]'),(36,'Quiz 1',1,1,0,'[]'),(37,'Quiz: First-thing-in-morning',0,0,0,'[]'),(38,'Quiz 1',1,1,0,'[]'),(39,'Quiz: First-thing-in-morning',1,1,0,'[]'),(40,'Quiz: Emails-per-day',1,1,0,'[]'),(41,'Quiz 1',1,1,0,'[]'),(42,'Quiz: First-thing-in-morning',1,1,0,'[]'),(43,'Quiz: Emails-per-day',1,1,0,'[]'),(44,'Quiz 1',1,0,0,'[]'),(45,'Quiz: First-thing-in-morning',1,0,0,'[]'),(46,'Quiz: Emails-per-day',1,2,1,'[]'),(47,'Quiz: First-thing-in-morning',1,1,0,'[]'),(48,'Test',1,16,35,'[]'),(49,'Quiz: Emails-per-day',1,1,0,'[]'),(50,'Test quiz outside video',1,4,16,'[]'),(51,'Quiz: First-thing-in-morning',1,1,0,'[]'),(52,'Test',1,6,18,'[]'),(53,'Quiz: Emails-per-day',1,1,0,'[]'),(54,'Quiz',1,2,9,'[]'),(55,'Quiz 1',1,1,0,'[]'),(56,'Quiz: First-thing-in-morning',1,1,0,'[]'),(57,'Quiz: Emails-per-day',1,1,0,'[]'),(58,'Quiz 1',1,1,0,'[]'),(59,'Quiz: First-thing-in-morning',1,1,0,'[]'),(60,'Quiz: Emails-per-day',1,1,0,'[]'),(61,'Quiz: First-thing-in-morning',1,1,2,'[]'),(62,'Test',1,2,10,'[]'),(63,'Quiz: Emails-per-day',1,1,2,'[]'),(64,'Quiz: First-thing-in-morning',1,1,0,'[]'),(65,'Test',1,2,0,'[]'),(66,'Quiz: Emails-per-day',1,1,0,'[]'),(67,'Test quiz',1,1,4,'[]');
/*!40000 ALTER TABLE `quiz_quiz` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_quizhistory`
--

DROP TABLE IF EXISTS `quiz_quizhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_quizhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `quiz_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `current_question_module_id` int(11) DEFAULT NULL,
  `marks` double NOT NULL,
  `solved` int(11) NOT NULL,
  `is_graded` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `quiz_quizhistory_eecda460` (`quiz_id`),
  KEY `quiz_quizhistory_6340c63c` (`user_id`),
  KEY `quiz_quizhistory_1a939140` (`current_question_module_id`),
  CONSTRAINT `current_question_module_id_refs_id_1271a922` FOREIGN KEY (`current_question_module_id`) REFERENCES `quiz_questionmodule` (`id`),
  CONSTRAINT `quiz_id_refs_id_d4bd789f` FOREIGN KEY (`quiz_id`) REFERENCES `quiz_quiz` (`id`),
  CONSTRAINT `user_id_refs_id_20f7b839` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_quizhistory`
--

LOCK TABLES `quiz_quizhistory` WRITE;
/*!40000 ALTER TABLE `quiz_quizhistory` DISABLE KEYS */;
INSERT INTO `quiz_quizhistory` VALUES (1,1,1,NULL,5,0,0),(2,5,1,NULL,3,0,0),(3,25,1,NULL,0,0,0),(4,26,1,NULL,0,0,0),(5,27,1,NULL,0,0,0),(6,28,1,NULL,16,0,0),(7,28,3,NULL,4,0,0),(8,25,3,NULL,0,0,0),(9,30,1,NULL,8,0,0),(10,42,1,NULL,0,0,0),(11,41,1,NULL,0,0,0),(12,47,1,NULL,0,0,0),(13,50,1,NULL,0,0,0),(14,48,1,NULL,0,0,0),(15,44,1,NULL,0,0,0),(16,45,1,NULL,0,0,0),(17,52,1,NULL,6,0,0),(18,54,1,NULL,5,0,0),(19,58,1,NULL,0,0,0),(20,48,3,NULL,4,0,0),(21,49,3,NULL,0,0,0),(22,6,2,NULL,0,0,0),(23,28,2,NULL,0,0,0),(24,6,3,NULL,0,0,0),(25,6,10,NULL,0,0,0),(26,28,10,NULL,0,0,0),(27,50,3,NULL,0,0,0),(28,54,3,NULL,0,0,0),(29,52,3,NULL,6,0,0),(30,6,1,NULL,0,0,0),(31,62,3,NULL,8,0,0),(32,67,3,NULL,2,0,0),(33,46,1,NULL,0,0,0),(34,6,17,NULL,0,0,0),(35,28,17,NULL,0,0,0),(36,50,17,NULL,0,0,0),(37,54,17,NULL,0,0,0),(38,6,16,NULL,0,0,0),(39,28,16,NULL,0,0,0);
/*!40000 ALTER TABLE `quiz_quizhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_singlechoicequestion`
--

DROP TABLE IF EXISTS `quiz_singlechoicequestion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_singlechoicequestion` (
  `question_ptr_id` int(11) NOT NULL,
  `options` longtext NOT NULL,
  `answer` int(11) NOT NULL,
  PRIMARY KEY (`question_ptr_id`),
  CONSTRAINT `question_ptr_id_refs_id_e569ee83` FOREIGN KEY (`question_ptr_id`) REFERENCES `quiz_question` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_singlechoicequestion`
--

LOCK TABLES `quiz_singlechoicequestion` WRITE;
/*!40000 ALTER TABLE `quiz_singlechoicequestion` DISABLE KEYS */;
INSERT INTO `quiz_singlechoicequestion` VALUES (13,'[`Default Answer Text`]',0),(14,'[`Check email`, `Check Facebook`, `Brush teeth`, `Play online games`]',0),(15,'[`100 Million`, `1 Billion`, `100 Billion`, `300 Billion`]',3),(16,'[`Default Answer Text`]',0),(17,'[`Check email`, `Check Facebook`, `Brush teeth`, `Play online games`]',0),(18,'[`100 Million`, `1 Billion`, `100 Billion`, `300 Billion`]',3),(19,'[`Default Answer Text`]',0),(20,'[`Check email`, `Check Facebook`, `Brush teeth`, `Play online games`]',0),(21,'[`100 Million`, `1 Billion`, `100 Billion`, `300 Billion`]',3),(22,'[`Default Answer Text`]',0),(23,'[`Check email`, `Check Facebook`, `Brush teeth`, `Play online games`]',0),(24,'[`100 Million`, `1 Billion`, `100 Billion`, `300 Billion`]',3),(25,'[`Default Answer Text`]',0),(26,'[`Check email`, `Check Facebook`, `Brush teeth`, `Play online games`]',0),(27,'[`100 Million`, `1 Billion`, `100 Billion`, `300 Billion`]',3),(28,'[`Default Answer Text`]',0),(29,'[`Check email`, `Check Facebook`, `Brush teeth`, `Play online games`]',0),(30,'[`100 Million`, `1 Billion`, `100 Billion`, `300 Billion`]',3),(31,'[`Default Answer Text`]',0),(32,'[`Check email`, `Check Facebook`, `Brush teeth`, `Play online games`]',0),(34,'[`100 Million`,`1 Billion`,`100 Billion`,`300 Billion`]',3),(35,'[`100 Million`,`1 Billion`,`100 Billion`,`300 Billion`]',3),(36,'[`100 Million`,`1 Billion`,`100 Billion`,`300 Billion`]',3),(37,'[`100 Million`,`1 Billion`,`100 Billion`,`300 Billion`]',3),(38,'[`100 Million`,`1 Billion`,`100 Billion`,`300 Billion`]',3),(42,'[`12`,`13`,`14`]',2),(48,'[`zero`,`one`,`two`]',1),(50,'[`Default Answer Text`]',0),(51,'[`Default Answer Text`]',0),(52,'[`Default Answer Text`]',0),(53,'[`Default Answer Text`]',0),(54,'[`Check email`, `Check Facebook`, `Brush teeth`, `Play online games`]',0),(55,'[`100 Million`, `1 Billion`, `100 Billion`, `300 Billion`]',3),(56,'[`Default Answer Text`]',0),(57,'[`Check email`, `Check Facebook`, `Brush teeth`, `Play online games`]',0),(58,'[`100 Million`, `1 Billion`, `100 Billion`, `300 Billion`]',3),(62,'[`Check email`, `Check Facebook`, `Brush teeth`, `Play online games`]',0),(65,'[`100 Million`, `1 Billion`, `100 Billion`, `300 Billion`]',3),(84,'[`1`,`2`,`3`]',2),(93,'[`1`,`2`]',1),(97,'[`zero`,`one`,`two`,`three`]',1),(98,'[`Check email`, `Check Facebook`, `Brush teeth`, `Play online games`]',0),(101,'[`100 Million`, `1 Billion`, `100 Billion`, `300 Billion`]',3),(105,'[`4`,`1`,`3`,`5`]',0),(107,'[`2`,`3`,`5`,`10`]',2),(108,'[`Default Answer Text`]',0),(109,'[`Check email`, `Check Facebook`, `Brush teeth`, `Play online games`]',0),(110,'[`100 Million`, `1 Billion`, `100 Billion`, `300 Billion`]',3),(111,'[`Default Answer Text`]',0),(112,'[`Check email`, `Check Facebook`, `Brush teeth`, `Play online games`]',0),(113,'[`100 Million`, `1 Billion`, `100 Billion`, `300 Billion`]',3),(118,'[`Check email`,`Check Facebook`,`Brush teeth`,`Play online games`]',0),(119,'[`4`,`1`,`3`,`5`]',0),(120,'[`2`,`3`,`5`,`10`]',2),(121,'[`100 Million`,`1 Billion`,`100 Billion`,`300 Billion`]',3),(122,'[`Check email`, `Check Facebook`, `Brush teeth`, `Play online games`]',0),(123,'[`4`, `1`, `3`, `5`]',0),(124,'[`2`, `3`, `5`, `10`]',2),(125,'[`100 Million`, `1 Billion`, `100 Billion`, `300 Billion`]',3),(128,'[`100 Million`,`1 Billion`,`100 Billion`,`300 Billion`]',3);
/*!40000 ALTER TABLE `quiz_singlechoicequestion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_submission`
--

DROP TABLE IF EXISTS `quiz_submission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_submission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `question_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `grader_type` varchar(1) NOT NULL,
  `answer` longtext NOT NULL,
  `status` varchar(1) NOT NULL,
  `feedback` longtext NOT NULL,
  `result` double NOT NULL,
  `is_correct` tinyint(1) NOT NULL,
  `is_plagiarised` tinyint(1) NOT NULL,
  `has_been_checked` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `quiz_submission_63b5ea41` (`created`),
  KEY `quiz_submission_ec9ad377` (`modified`),
  KEY `quiz_submission_25110688` (`question_id`),
  KEY `quiz_submission_94741166` (`student_id`),
  CONSTRAINT `question_id_refs_id_68f296d3` FOREIGN KEY (`question_id`) REFERENCES `quiz_question` (`id`),
  CONSTRAINT `student_id_refs_id_d621ee56` FOREIGN KEY (`student_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_submission`
--

LOCK TABLES `quiz_submission` WRITE;
/*!40000 ALTER TABLE `quiz_submission` DISABLE KEYS */;
INSERT INTO `quiz_submission` VALUES (1,'2014-01-02 04:12:56','2014-01-02 04:12:56',3,1,'D','3','D','',0,0,0,0),(2,'2014-01-02 04:12:59','2014-01-02 04:12:59',3,1,'D','4','D','',5,1,0,0),(3,'2014-01-02 14:01:43','2014-01-02 14:01:43',6,1,'D','3','D','',0,0,0,0),(4,'2014-01-02 14:02:10','2014-01-02 14:02:10',4,1,'D','4','D','',1,1,0,0),(5,'2014-01-02 14:03:02','2014-01-02 14:03:02',7,1,'M','xxx','A','',0,0,0,0),(6,'2014-01-02 14:04:54','2014-01-02 14:04:54',8,1,'D','xxx','D','',0,0,0,0),(7,'2014-01-02 15:12:11','2014-01-02 15:12:11',12,1,'D','[false,true,false,false]','D','',2,1,0,0),(8,'2014-01-03 00:47:39','2014-01-03 00:47:39',31,1,'D','0','D','',0,1,0,0),(10,'2014-01-03 00:51:33','2014-01-03 00:51:33',32,1,'D','0','D','',0,1,0,0),(11,'2014-01-03 01:15:24','2014-01-03 01:15:24',34,1,'D','2','D','',0,0,0,0),(12,'2014-01-03 01:15:26','2014-01-03 01:15:26',35,1,'D','3','D','',0,1,0,0),(13,'2014-01-03 01:15:34','2014-01-03 01:15:34',36,1,'D','3','D','',0,1,0,0),(16,'2014-01-03 01:54:29','2014-01-03 01:54:29',42,1,'D','0','D','',0,0,0,0),(17,'2014-01-03 01:54:32','2014-01-03 01:54:32',42,1,'D','2','D','',4,1,0,0),(19,'2014-01-03 05:07:50','2014-01-03 05:07:50',42,3,'D','0','D','',0,0,0,0),(20,'2014-01-03 05:07:54','2014-01-03 05:07:54',42,3,'D','1','D','',0,0,0,0),(21,'2014-01-03 05:07:59','2014-01-03 05:07:59',42,3,'D','2','D','',4,1,0,0),(23,'2014-01-03 14:21:46','2014-01-03 14:21:46',31,3,'D','0','D','',0,1,0,0),(25,'2014-01-03 18:40:24','2014-01-03 18:40:24',46,1,'D','[false,true,true,false]','D','',5,1,0,0),(27,'2014-01-03 18:51:53','2014-01-03 18:51:53',48,1,'D','1','D','',3,1,0,0),(28,'2014-01-03 19:01:53','2014-01-03 19:01:53',49,1,'D','[false,true,true,false]','D','',5,1,0,0),(30,'2014-01-04 11:59:25','2014-01-04 11:59:25',41,1,'D','hj','D','',0,0,0,0),(31,'2014-01-04 12:00:11','2014-01-04 12:00:11',57,1,'D','0','D','',0,1,0,0),(32,'2014-01-04 12:00:24','2014-01-04 12:00:24',56,1,'D','0','D','',0,1,0,0),(33,'2014-01-05 23:40:32','2014-01-05 23:40:32',62,1,'D','0','D','',0,1,0,0),(34,'2014-01-05 23:48:09','2014-01-05 23:48:09',65,1,'D','2','D','',0,0,0,0),(43,'2014-01-06 12:32:31','2014-01-06 12:32:31',97,1,'D','0','D','',0,0,0,0),(44,'2014-01-06 12:32:35','2014-01-06 12:32:35',97,1,'D','1','D','',3,1,0,0),(45,'2014-01-06 15:58:24','2014-01-06 15:58:24',84,1,'D','1','D','',0,0,0,0),(46,'2014-01-06 15:58:39','2014-01-06 15:58:39',84,1,'D','0','D','',0,0,0,0),(50,'2014-01-07 00:22:21','2014-01-07 00:22:21',103,1,'D','3','D','',0,0,0,0),(51,'2014-01-07 00:22:27','2014-01-07 00:22:27',103,1,'D','6','D','',2,1,0,0),(52,'2014-01-07 00:22:37','2014-01-07 00:22:37',104,1,'D','5','D','',0,0,0,0),(53,'2014-01-07 00:22:57','2014-01-07 00:22:57',104,1,'D','10','D','',0,0,0,0),(54,'2014-01-07 00:23:04','2014-01-07 00:23:04',104,1,'D','12','D','',3,1,0,0),(55,'2014-01-07 14:06:02','2014-01-07 14:06:02',98,1,'D','3','D','',0,0,0,0),(60,'2014-01-07 11:17:00','2014-01-07 11:17:00',41,1,'D','1','D','',0,0,0,0),(61,'2014-01-07 11:18:55','2014-01-07 11:18:55',41,1,'D','1','D','',0,0,0,0),(62,'2014-01-07 11:20:01','2014-01-07 11:20:01',42,1,'D','0','D','',0,0,0,0),(63,'2014-01-07 11:20:08','2014-01-07 11:20:08',42,1,'D','1','D','',0,0,0,0),(64,'2014-01-07 11:20:13','2014-01-07 11:20:13',42,1,'D','2','D','',4,1,0,0),(65,'2014-01-09 04:52:52','2014-01-09 04:52:52',111,1,'D','0','D','',0,1,0,0),(66,'2014-01-09 13:16:05','2014-01-09 13:16:05',105,1,'D','0','D','',4,1,0,0),(67,'2014-01-09 13:16:15','2014-01-09 13:16:15',107,1,'D','1','D','',0,0,0,0),(68,'2014-01-09 13:16:23','2014-01-09 13:16:23',107,1,'D','2','D','',2,1,0,0),(69,'2014-01-09 13:34:37','2014-01-09 13:34:37',98,3,'D','2','D','',0,0,0,0),(70,'2014-01-09 13:42:29','2014-01-09 13:42:29',83,3,'D','5','D','',0,0,0,0),(71,'2014-01-09 13:42:36','2014-01-09 13:42:36',92,3,'D','[false,true,true,false]','D','',2,1,0,0),(72,'2014-01-09 13:42:44','2014-01-09 13:42:44',93,3,'D','1','D','',2,1,0,0),(73,'2014-01-09 13:56:05','2014-01-09 13:56:05',65,3,'D','3','D','',0,1,0,0),(74,'2014-01-09 17:18:43','2014-01-09 17:18:43',105,3,'D','0','D','',4,1,0,0),(75,'2014-01-09 17:18:48','2014-01-09 17:18:48',107,3,'D','1','D','',0,0,0,0),(76,'2014-01-09 17:18:51','2014-01-09 17:18:51',107,3,'D','2','D','',2,1,0,0),(77,'2014-01-09 18:17:51','2014-01-09 18:17:51',118,3,'D','1','D','',0,0,0,0),(78,'2014-01-09 18:18:39','2014-01-09 18:18:39',119,3,'D','1','D','',0,0,0,0),(79,'2014-01-09 18:18:47','2014-01-09 18:18:47',119,3,'D','0','D','',2,1,0,0),(80,'2014-01-09 18:18:54','2014-01-09 18:18:54',120,3,'D','2','D','',6,1,0,0),(81,'2014-01-09 11:32:58','2014-01-09 11:32:58',62,3,'D','2','D','',0,0,0,0),(82,'2014-01-10 00:32:49','2014-01-10 00:32:49',126,3,'D','7','D','',0,0,0,0),(83,'2014-01-10 00:32:52','2014-01-10 00:32:52',126,3,'D','9','D','',2,1,0,0);
/*!40000 ALTER TABLE `quiz_submission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_testcase`
--

DROP TABLE IF EXISTS `quiz_testcase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quiz_testcase` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) NOT NULL,
  `input_text` longtext NOT NULL,
  `correct_output` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `quiz_testcase_25110688` (`question_id`),
  CONSTRAINT `question_id_refs_question_ptr_id_2d7d0fe3` FOREIGN KEY (`question_id`) REFERENCES `quiz_programmingquestion` (`question_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_testcase`
--

LOCK TABLES `quiz_testcase` WRITE;
/*!40000 ALTER TABLE `quiz_testcase` DISABLE KEYS */;
/*!40000 ALTER TABLE `quiz_testcase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registration_emailupdate`
--

DROP TABLE IF EXISTS `registration_emailupdate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registration_emailupdate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `new_email` varchar(63) NOT NULL,
  `activation_key` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `registration_emailupdate_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_e4c5e2cc` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registration_emailupdate`
--

LOCK TABLES `registration_emailupdate` WRITE;
/*!40000 ALTER TABLE `registration_emailupdate` DISABLE KEYS */;
/*!40000 ALTER TABLE `registration_emailupdate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registration_forgotpassword`
--

DROP TABLE IF EXISTS `registration_forgotpassword`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registration_forgotpassword` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `activation_key` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `registration_forgotpassword_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_8c4c27a2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registration_forgotpassword`
--

LOCK TABLES `registration_forgotpassword` WRITE;
/*!40000 ALTER TABLE `registration_forgotpassword` DISABLE KEYS */;
INSERT INTO `registration_forgotpassword` VALUES (1,11,'ae754190d2e54a3da5dcd6ce96360989');
/*!40000 ALTER TABLE `registration_forgotpassword` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registration_registration`
--

DROP TABLE IF EXISTS `registration_registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registration_registration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `activation_key` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `registration_registration_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_7489dde9` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registration_registration`
--

LOCK TABLES `registration_registration` WRITE;
/*!40000 ALTER TABLE `registration_registration` DISABLE KEYS */;
INSERT INTO `registration_registration` VALUES (1,4,'b931719272154823a5e61e158e3d5441'),(2,5,'80658c92e33f44d3aa20be51c0d023bf'),(3,6,'e8707b80a47f4d6695ba346ce1d860cb'),(4,7,'710a0fae535e4c309289b7aacc270703'),(5,8,'36a516228e8a4deabbc59964d1644d22'),(6,9,'eae4563903ef4043bb7faef423af9ab9'),(8,11,'24caa0c937db44f4a0a272abc5bfb382'),(9,12,'3149aa0722484a04a16a2b9537559fa8'),(10,13,'7927a6ac35134d44aed10ad5e2851c8f'),(11,14,'0c1963533f024fd69278622b5b074748');
/*!40000 ALTER TABLE `registration_registration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `upload_upload`
--

DROP TABLE IF EXISTS `upload_upload`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `upload_upload` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `owner_id` int(11) NOT NULL,
  `assignment_id` int(11) DEFAULT NULL,
  `filePath` varchar(100) NOT NULL,
  `uploaded_on` datetime NOT NULL,
  `is_stale` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `upload_upload_cb902d83` (`owner_id`),
  KEY `upload_upload_52f7e0e7` (`assignment_id`),
  CONSTRAINT `assignment_id_refs_id_818f7594` FOREIGN KEY (`assignment_id`) REFERENCES `assignments_assignment` (`id`),
  CONSTRAINT `owner_id_refs_id_88430a87` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `upload_upload`
--

LOCK TABLES `upload_upload` WRITE;
/*!40000 ALTER TABLE `upload_upload` DISABLE KEYS */;
INSERT INTO `upload_upload` VALUES (3,17,2,'st/2/main.cpp.zip','2014-03-21 08:48:45',0),(5,16,2,'pj/2/main.cpp.zip','2014-03-21 09:12:32',0),(6,16,1,'pj/1/main.cpp','2014-04-10 19:20:47',0);
/*!40000 ALTER TABLE `upload_upload` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_profile_college`
--

DROP TABLE IF EXISTS `user_profile_college`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_profile_college` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `college` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_profile_college`
--

LOCK TABLES `user_profile_college` WRITE;
/*!40000 ALTER TABLE `user_profile_college` DISABLE KEYS */;
INSERT INTO `user_profile_college` VALUES (1,'Indian Institute of Technology, Bombay'),(2,'Indian Institute of Technology, Delhi'),(3,'Indian Institute of Technology, Kanpur'),(4,'Indian Institute of Technology, Roorkee'),(5,'Indian Institute of Technology, Kharagpur'),(6,'Indian Institute of Technology, Madras'),(7,'Indian Institute of Technology, Guwahati');
/*!40000 ALTER TABLE `user_profile_college` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_profile_company`
--

DROP TABLE IF EXISTS `user_profile_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_profile_company` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company` varchar(63) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_profile_company`
--

LOCK TABLES `user_profile_company` WRITE;
/*!40000 ALTER TABLE `user_profile_company` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_profile_company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_profile_customuser`
--

DROP TABLE IF EXISTS `user_profile_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_profile_customuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `is_instructor` tinyint(1) NOT NULL,
  `is_content_developer` tinyint(1) NOT NULL,
  `default_mode` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_db2c19bc` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_profile_customuser`
--

LOCK TABLES `user_profile_customuser` WRITE;
/*!40000 ALTER TABLE `user_profile_customuser` DISABLE KEYS */;
INSERT INTO `user_profile_customuser` VALUES (1,1,1,1,'C'),(2,2,0,0,'S'),(3,3,0,0,'S'),(4,4,0,0,'S'),(5,5,0,0,'S'),(6,6,0,0,'S'),(7,7,0,0,'S'),(8,8,0,0,'S'),(9,9,0,0,'S'),(10,10,0,0,'S'),(11,11,0,0,'S'),(12,12,0,0,'S'),(13,13,0,0,'S'),(14,14,0,0,'S'),(15,15,1,1,'S'),(16,16,0,0,'S'),(17,17,0,0,'S'),(18,18,0,0,'S');
/*!40000 ALTER TABLE `user_profile_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_profile_education`
--

DROP TABLE IF EXISTS `user_profile_education`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_profile_education` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `degree` varchar(63) NOT NULL,
  `college_id` int(11) NOT NULL,
  `major_id` int(11) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_profile_education_6340c63c` (`user_id`),
  KEY `user_profile_education_ac3b121a` (`college_id`),
  KEY `user_profile_education_1b5dac5d` (`major_id`),
  CONSTRAINT `college_id_refs_id_2c319847` FOREIGN KEY (`college_id`) REFERENCES `user_profile_college` (`id`),
  CONSTRAINT `major_id_refs_id_8ea8ed5a` FOREIGN KEY (`major_id`) REFERENCES `user_profile_major` (`id`),
  CONSTRAINT `user_id_refs_id_9d375ee4` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_profile_education`
--

LOCK TABLES `user_profile_education` WRITE;
/*!40000 ALTER TABLE `user_profile_education` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_profile_education` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_profile_major`
--

DROP TABLE IF EXISTS `user_profile_major`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_profile_major` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `major` varchar(63) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_profile_major`
--

LOCK TABLES `user_profile_major` WRITE;
/*!40000 ALTER TABLE `user_profile_major` DISABLE KEYS */;
INSERT INTO `user_profile_major` VALUES (1,'Computer Science'),(2,'Computer Science and Engineering'),(3,'Maths and Computing'),(4,'Electrical Engineering'),(5,'Electronics Engineering'),(6,'Electrical and Electrical Engineering'),(7,'Electronics and Communications'),(8,'Electrical and TeleCommunications'),(9,'Mechanical Engineering');
/*!40000 ALTER TABLE `user_profile_major` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_profile_userprofile`
--

DROP TABLE IF EXISTS `user_profile_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_profile_userprofile` (
  `user_id` int(11) NOT NULL,
  `uid` varchar(32) NOT NULL,
  `dob` date DEFAULT NULL,
  `gender` varchar(1) DEFAULT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `place_city` varchar(63) DEFAULT NULL,
  `place_state` varchar(63) DEFAULT NULL,
  `place_country` varchar(63) DEFAULT NULL,
  `privacy` varchar(2) DEFAULT NULL,
  `about` varchar(255) DEFAULT NULL,
  `interests` varchar(255) DEFAULT NULL,
  `website_twitter` varchar(255) DEFAULT NULL,
  `website_facebook` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `user_id_refs_id_759b3408` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_profile_userprofile`
--

LOCK TABLES `user_profile_userprofile` WRITE;
/*!40000 ALTER TABLE `user_profile_userprofile` DISABLE KEYS */;
INSERT INTO `user_profile_userprofile` VALUES (1,'66287fd8f9c340aa8f6d2015852fdaa9',NULL,NULL,'',NULL,NULL,NULL,NULL,'','',NULL,NULL);
/*!40000 ALTER TABLE `user_profile_userprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_profile_work`
--

DROP TABLE IF EXISTS `user_profile_work`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_profile_work` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `company_id` int(11) NOT NULL,
  `position` varchar(63) NOT NULL,
  `description` varchar(255) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_profile_work_6340c63c` (`user_id`),
  KEY `user_profile_work_0316dde1` (`company_id`),
  CONSTRAINT `company_id_refs_id_c23757cd` FOREIGN KEY (`company_id`) REFERENCES `user_profile_company` (`id`),
  CONSTRAINT `user_id_refs_id_77693161` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_profile_work`
--

LOCK TABLES `user_profile_work` WRITE;
/*!40000 ALTER TABLE `user_profile_work` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_profile_work` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `util_subscription`
--

DROP TABLE IF EXISTS `util_subscription`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `util_subscription` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `util_subscription`
--

LOCK TABLES `util_subscription` WRITE;
/*!40000 ALTER TABLE `util_subscription` DISABLE KEYS */;
INSERT INTO `util_subscription` VALUES (1),(2);
/*!40000 ALTER TABLE `util_subscription` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `util_subscription_users`
--

DROP TABLE IF EXISTS `util_subscription_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `util_subscription_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subscription_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `subscription_id` (`subscription_id`,`user_id`),
  KEY `util_subscription_users_b75baf19` (`subscription_id`),
  KEY `util_subscription_users_6340c63c` (`user_id`),
  CONSTRAINT `subscription_id_refs_id_bb80f71d` FOREIGN KEY (`subscription_id`) REFERENCES `util_subscription` (`id`),
  CONSTRAINT `user_id_refs_id_bcbe1af7` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `util_subscription_users`
--

LOCK TABLES `util_subscription_users` WRITE;
/*!40000 ALTER TABLE `util_subscription_users` DISABLE KEYS */;
INSERT INTO `util_subscription_users` VALUES (1,1,1),(2,2,1);
/*!40000 ALTER TABLE `util_subscription_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `util_votable`
--

DROP TABLE IF EXISTS `util_votable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `util_votable` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `upvotes` int(11) NOT NULL,
  `downvotes` int(11) NOT NULL,
  `popularity` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `util_votable_c8a0ade0` (`upvotes`),
  KEY `util_votable_22fcf4a8` (`downvotes`),
  KEY `util_votable_f476bdf4` (`popularity`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `util_votable`
--

LOCK TABLES `util_votable` WRITE;
/*!40000 ALTER TABLE `util_votable` DISABLE KEYS */;
/*!40000 ALTER TABLE `util_votable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `util_votable_downvoters`
--

DROP TABLE IF EXISTS `util_votable_downvoters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `util_votable_downvoters` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `votable_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `votable_id` (`votable_id`,`user_id`),
  KEY `util_votable_downvoters_09733f67` (`votable_id`),
  KEY `util_votable_downvoters_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_4eae71f1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `votable_id_refs_id_afc1933d` FOREIGN KEY (`votable_id`) REFERENCES `util_votable` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `util_votable_downvoters`
--

LOCK TABLES `util_votable_downvoters` WRITE;
/*!40000 ALTER TABLE `util_votable_downvoters` DISABLE KEYS */;
/*!40000 ALTER TABLE `util_votable_downvoters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `util_votable_upvoters`
--

DROP TABLE IF EXISTS `util_votable_upvoters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `util_votable_upvoters` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `votable_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `votable_id` (`votable_id`,`user_id`),
  KEY `util_votable_upvoters_09733f67` (`votable_id`),
  KEY `util_votable_upvoters_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_c98bec44` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `votable_id_refs_id_0f6fb5b7` FOREIGN KEY (`votable_id`) REFERENCES `util_votable` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `util_votable_upvoters`
--

LOCK TABLES `util_votable_upvoters` WRITE;
/*!40000 ALTER TABLE `util_votable_upvoters` DISABLE KEYS */;
/*!40000 ALTER TABLE `util_votable_upvoters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `video_marker`
--

DROP TABLE IF EXISTS `video_marker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video_marker` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `video_id` int(11) NOT NULL,
  `time` int(11) NOT NULL,
  `type` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `video_id` (`video_id`,`time`,`type`),
  KEY `video_marker_c11471f1` (`video_id`),
  CONSTRAINT `video_id_refs_id_cd298902` FOREIGN KEY (`video_id`) REFERENCES `video_video` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=184 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `video_marker`
--

LOCK TABLES `video_marker` WRITE;
/*!40000 ALTER TABLE `video_marker` DISABLE KEYS */;
INSERT INTO `video_marker` VALUES (11,8,52,'Q'),(12,8,72,'Q'),(13,8,282,'Q'),(17,10,52,'Q'),(18,10,72,'Q'),(19,10,282,'Q'),(110,36,0,'S'),(111,36,6,'S'),(107,36,52,'Q'),(108,36,72,'Q'),(112,36,72,'S'),(113,36,170,'S'),(114,36,233,'S'),(115,36,264,'S'),(109,36,282,'Q'),(116,36,332,'S'),(117,36,346,'S'),(121,37,0,'S'),(122,37,6,'S'),(118,37,72,'Q'),(123,37,72,'S'),(119,37,161,'Q'),(124,37,170,'S'),(125,37,233,'S'),(126,37,264,'S'),(120,37,282,'Q'),(127,37,401,'S'),(128,37,415,'S'),(132,38,0,'S'),(133,38,6,'S'),(129,38,72,'Q'),(134,38,72,'S'),(130,38,161,'Q'),(135,38,170,'S'),(136,38,233,'S'),(137,38,264,'S'),(131,38,282,'Q'),(138,38,401,'S'),(139,38,415,'S'),(143,46,0,'S'),(144,46,7,'S'),(140,46,53,'Q'),(141,46,73,'Q'),(145,46,73,'S'),(146,46,171,'S'),(147,46,234,'S'),(148,46,265,'S'),(142,46,283,'Q'),(149,46,333,'S'),(150,46,347,'S'),(154,58,0,'S'),(155,58,7,'S'),(151,58,53,'Q'),(152,58,73,'Q'),(156,58,73,'S'),(157,58,171,'S'),(158,58,234,'S'),(159,58,265,'S'),(153,58,283,'Q'),(160,58,333,'S'),(161,58,347,'S'),(165,59,0,'S'),(166,59,7,'S'),(162,59,73,'Q'),(167,59,73,'S'),(163,59,162,'Q'),(168,59,171,'S'),(169,59,234,'S'),(170,59,265,'S'),(164,59,283,'Q'),(171,59,402,'S'),(172,59,416,'S'),(176,60,0,'S'),(177,60,7,'S'),(173,60,73,'Q'),(178,60,73,'S'),(174,60,162,'Q'),(179,60,171,'S'),(180,60,234,'S'),(181,60,265,'S'),(175,60,283,'Q'),(182,60,402,'S'),(183,60,416,'S');
/*!40000 ALTER TABLE `video_marker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `video_quizmarker`
--

DROP TABLE IF EXISTS `video_quizmarker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video_quizmarker` (
  `marker_ptr_id` int(11) NOT NULL,
  `quiz_id` int(11) NOT NULL,
  PRIMARY KEY (`marker_ptr_id`),
  KEY `video_quizmarker_eecda460` (`quiz_id`),
  CONSTRAINT `marker_ptr_id_refs_id_5c153c58` FOREIGN KEY (`marker_ptr_id`) REFERENCES `video_marker` (`id`),
  CONSTRAINT `quiz_id_refs_id_b2912192` FOREIGN KEY (`quiz_id`) REFERENCES `quiz_quiz` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `video_quizmarker`
--

LOCK TABLES `video_quizmarker` WRITE;
/*!40000 ALTER TABLE `video_quizmarker` DISABLE KEYS */;
INSERT INTO `video_quizmarker` VALUES (11,13),(12,14),(13,15),(17,19),(18,20),(19,21),(107,44),(108,45),(109,46),(118,47),(119,48),(120,49),(129,51),(130,52),(131,53),(140,55),(141,56),(142,57),(151,58),(152,59),(153,60),(162,61),(163,62),(164,63),(173,64),(174,65),(175,66);
/*!40000 ALTER TABLE `video_quizmarker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `video_sectionmarker`
--

DROP TABLE IF EXISTS `video_sectionmarker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video_sectionmarker` (
  `marker_ptr_id` int(11) NOT NULL,
  `title` varchar(63) NOT NULL,
  PRIMARY KEY (`marker_ptr_id`),
  CONSTRAINT `marker_ptr_id_refs_id_58fb2fce` FOREIGN KEY (`marker_ptr_id`) REFERENCES `video_marker` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `video_sectionmarker`
--

LOCK TABLES `video_sectionmarker` WRITE;
/*!40000 ALTER TABLE `video_sectionmarker` DISABLE KEYS */;
INSERT INTO `video_sectionmarker` VALUES (110,'Computer Networks: Motivation'),(111,'Why Study Computer Networks?'),(112,'Usage: Personal Level '),(113,'Usage: Business Level'),(114,'Out of ordinary/Futuristic Usage'),(115,'Impact'),(116,'Job Opportunities'),(117,'Summary'),(121,'Computer Networks: Motivation'),(122,'Why Study Computer Networks?'),(123,'Usage: Personal Level '),(124,'Usage: Business Level'),(125,'Out of ordinary/Futuristic Usage'),(126,'Impact'),(127,'Job Opportunities'),(128,'Summary'),(132,'Computer Networks: Motivation'),(133,'Why Study Computer Networks?'),(134,'Usage: Personal Level '),(135,'Usage: Business Level'),(136,'Out of ordinary/Futuristic Usage'),(137,'Impact'),(138,'Job Opportunities'),(139,'Summary'),(143,'Computer Networks: Motivation'),(144,'Why Study Computer Networks?'),(145,'Usage: Personal Level '),(146,'Usage: Business Level'),(147,'Out of ordinary/Futuristic Usage'),(148,'Impact'),(149,'Job Opportunities'),(150,'Summary'),(154,'Computer Networks: Motivation'),(155,'Why Study Computer Networks?'),(156,'Usage: Personal Level '),(157,'Usage: Business Level'),(158,'Out of ordinary/Futuristic Usage'),(159,'Impact'),(160,'Job Opportunities'),(161,'Summary'),(165,'Computer Networks: Motivation'),(166,'Why Study Computer Networks?'),(167,'Usage: Personal Level '),(168,'Usage: Business Level'),(169,'Out of ordinary/Futuristic Usage'),(170,'Impact'),(171,'Job Opportunities'),(172,'Summary'),(176,'Computer Networks: Motivation'),(177,'Why Study Computer Networks?'),(178,'Usage: Personal Level '),(179,'Usage: Business Level'),(180,'Out of ordinary/Futuristic Usage'),(181,'Impact'),(182,'Job Opportunities'),(183,'Summary');
/*!40000 ALTER TABLE `video_sectionmarker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `video_video`
--

DROP TABLE IF EXISTS `video_video`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video_video` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `content` longtext NOT NULL,
  `upvotes` int(11) NOT NULL,
  `downvotes` int(11) NOT NULL,
  `video_file` varchar(100) NOT NULL,
  `other_file` varchar(100) DEFAULT NULL,
  `duration` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `video_video`
--

LOCK TABLES `video_video` WRITE;
/*!40000 ALTER TABLE `video_video` DISABLE KEYS */;
INSERT INTO `video_video` VALUES (6,'Testing config File upload','Testing upload',0,0,'static/video/Motivation_2.mp4',NULL,371),(8,'test','',0,0,'static/video/Motivation_4.mp4','uploads/video_other/5_A_Dance_With_Dragons_1.pdf',371),(10,'Slide wala Video','',0,0,'static/video/Motivation_6.mp4','uploads/video_other/5_A_Dance_With_Dragons.pdf',371),(36,'Test Upload','',0,0,'static/video/Motivation_19.mp4','uploads/video_other/feedback-jan2.txt',371),(37,'Motivation','Why study computer networks?',0,0,'static/video/Motivation-v8.mp4','uploads/video_other/motivation-slides_10.pdf',435),(38,'Motivation','blah',0,0,'static/video/Motivation-v8_1.mp4','',435),(39,'Motivation','Motivation video',0,0,'static/video/Motivation-v8_2.mp4','',0),(40,'Motivation','Motivation video description',0,0,'static/video/Motivation-v8_3.mp4','',0),(41,'Motivation-v3','Motivation version 3',0,0,'static/video/Motivation-v8_4.mp4','',0),(42,'Motivation-v3','Motivation version 3',0,0,'static/video/Motivation-v8_5.mp4','',0),(43,'Testing','',0,0,'static/video/Motivation_20.mp4','uploads/video_other/feedback-dec31.txt',0),(44,'Testing','',0,0,'static/video/Motivation_21.mp4','uploads/video_other/feedback-dec31_1.txt',0),(45,'Testing','',0,0,'static/video/Motivation_22.mp4','uploads/video_other/feedback-dec31_2.txt',0),(46,'testing','',0,0,'static/video/Motivation_23.mp4','uploads/video_other/feedback-jan2_1.txt',371),(47,'test','',0,0,'static/video/Motivation_24.mp4','uploads/video_other/br-changes-required.txt',0),(48,'testing','',0,0,'static/video/Motivation_25.mp4','uploads/video_other/feedback-jan2_2.txt',0),(49,'testing','',0,0,'static/video/Motivation_26.mp4','uploads/video_other/feedback-jan2_3.txt',0),(50,'testing','',0,0,'static/video/Motivation_27.mp4','uploads/video_other/feedback-jan2_4.txt',0),(51,'testing','',0,0,'static/video/Motivation_28.mp4','uploads/video_other/feedback-Jan3.txt',0),(52,'testing','',0,0,'static/video/Motivation_29.mp4','uploads/video_other/BlackScholes.pdf',0),(53,'testing','',0,0,'static/video/Motivation_30.mp4','',0),(54,'test','',0,0,'static/video/Motivation_31.mp4','',0),(55,'t','',0,0,'static/video/Motivation_32.mp4','',0),(56,'t','',0,0,'static/video/Motivation_33.mp4','',0),(57,'t','',0,0,'static/video/Motivation_34.mp4','',371),(58,'another video','',0,0,'static/video/Motivation_35.mp4','uploads/video_other/BlackScholes_1.pdf',371),(59,'Motivation','Motivation video',0,0,'static/video/Motivation-v8_6.mp4','uploads/video_other/motivation-slides_11.pdf',435),(60,'Motivation-unpublished','',0,0,'static/video/Motivation-v8_7.mp4','',435);
/*!40000 ALTER TABLE `video_video` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `video_videohistory`
--

DROP TABLE IF EXISTS `video_videohistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video_videohistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `video_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `seen_status` tinyint(1) NOT NULL,
  `times_seen` int(11) NOT NULL,
  `vote` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `video_videohistory_c11471f1` (`video_id`),
  KEY `video_videohistory_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_33a60f18` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `video_id_refs_id_4b319346` FOREIGN KEY (`video_id`) REFERENCES `video_video` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `video_videohistory`
--

LOCK TABLES `video_videohistory` WRITE;
/*!40000 ALTER TABLE `video_videohistory` DISABLE KEYS */;
INSERT INTO `video_videohistory` VALUES (6,6,1,0,0,'N'),(8,8,1,0,0,'N'),(10,10,1,0,0,'N'),(19,36,1,0,0,'N'),(20,37,1,0,0,'N'),(21,38,1,0,0,'N'),(22,46,1,0,0,'N'),(23,57,1,0,0,'N'),(24,58,1,0,0,'N'),(25,38,3,0,0,'N'),(26,37,3,0,0,'N'),(27,59,3,0,0,'N'),(28,36,3,0,0,'N'),(29,46,3,0,0,'N'),(30,57,3,0,0,'N'),(31,58,3,0,0,'N'),(32,59,1,0,0,'N'),(33,36,17,0,0,'N'),(34,46,17,0,0,'N'),(35,57,17,0,0,'N'),(36,58,17,0,0,'N'),(37,8,17,0,0,'N'),(38,37,17,0,0,'N'),(39,38,17,0,0,'N');
/*!40000 ALTER TABLE `video_videohistory` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-04-14 19:38:28


--
-- Table structure for table `studies`
--

DROP TABLE IF EXISTS `studies`;
CREATE TABLE `studies` (
  `study` varchar(50) NOT NULL,
  `title` varchar(200) NOT NULL,
  `legacy_name` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `web_study` varchar(50) NOT NULL,
  `alfresco_node` varchar(255) NOT NULL,
  PRIMARY KEY (`study`),
  KEY `studies_69ba38d1` (`legacy_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `contact_persons`
--

DROP TABLE IF EXISTS `contact_persons`;
CREATE TABLE `contact_persons` (
  `contact_person` varchar(50) NOT NULL,
  `email` varchar(75) NOT NULL,
  `name` varchar(100) NOT NULL,
  `image` varchar(100) NOT NULL DEFAULT '',
  `description` longtext NOT NULL DEFAULT '',
  PRIMARY KEY (`contact_person`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
--
-- Table structure for table `studies_contact_persons`
--

DROP TABLE IF EXISTS `studies_contact_persons`;
CREATE TABLE `studies_contact_persons` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `study_id` varchar(50) NOT NULL,
  `contactperson_id` varchar(50) NOT NULL,
  `contact_type` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `studies_contact_persons_da5fc7d6` (`study_id`),
  KEY `studies_contact_persons_164fb53e` (`contactperson_id`),
  CONSTRAINT `study_id_refs_study_bcb75e31` FOREIGN KEY (`study_id`) REFERENCES `studies` (`study`),
  CONSTRAINT `contactperson_id_refs_contact_person_4427ed1b` FOREIGN KEY (`contactperson_id`) REFERENCES `contact_persons` (`contact_person`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `institutes`
--

DROP TABLE IF EXISTS `institutes`;
CREATE TABLE `institutes` (
  `institute` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`institute`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `affiliations`
--

DROP TABLE IF EXISTS `affiliations`;
CREATE TABLE `affiliations` (
  `affiliation` int(11) NOT NULL AUTO_INCREMENT,
  `institute_id` varchar(100) NOT NULL,
  `contact_person_id` varchar(50) NOT NULL,
  `url` varchar(200) NOT NULL DEFAULT '',
  PRIMARY KEY (`affiliation`),
  UNIQUE KEY `institute_id` (`institute_id`,`contact_person_id`),
  KEY `affiliations_da5f2290` (`institute_id`),
  KEY `affiliations_a2fce082` (`contact_person_id`),
  CONSTRAINT `institute_id_refs_institute_a37a4ce8` FOREIGN KEY (`institute_id`) REFERENCES `institutes` (`institute`),
  CONSTRAINT `contact_person_id_refs_contact_person_5a39adaa` FOREIGN KEY (`contact_person_id`) REFERENCES `contact_persons` (`contact_person`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


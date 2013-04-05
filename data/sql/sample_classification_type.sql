DROP TABLE IF EXISTS `sample_classification_types`;
CREATE TABLE `sample_classification_types` (
  `sample_classification_types` varchar(50) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `description` text,
  `ordr` int(11) DEFAULT NULL,
  PRIMARY KEY (`sample_classification_types`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `sample_classification_types` VALUES ('region','Region','Used for the calculation of genetic marker frequencies on a detailed geographical scale.',2),('subcont','Population','Used for the calculation of SNP allele frequencies.',1);


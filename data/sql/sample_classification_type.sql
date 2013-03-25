DROP TABLE IF EXISTS `sample_classification_type`;
CREATE TABLE `sample_classification_type` (
  `sample_classification_type` varchar(50) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `description` text,
  `ordr` int(11) DEFAULT NULL,
  PRIMARY KEY (`sample_classification_type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `sample_classification_type` VALUES ('region','Region','Used for the calculation of genetic marker frequencies on a detailed geographical scale.',2),('subcont','Population','Used for the calculation of SNP allele frequencies.',1);


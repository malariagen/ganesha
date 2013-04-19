UPDATE sample_contexts sc LEFT JOIN sample_context_description scd ON sc.sample_context = scd.sample_context SET sc.description = scd.description;

INSERT INTO sample_classifications (ordr, sample_classification, sample_classification_type, name, lattit, longit) 
SELECT ordr,sample_classification,sample_classification_type,name,longit,lattit FROM sample_classifications1;

INSERT INTO sample_classifications (sample_classification, sample_classification_type, name, lattit, longit) 
SELECT DISTINCT `Pop`, 'subcont', name, lattit, longit FROM SampleGroups sg LEFT JOIN `Definition-Populations` dp ON dp.ID = sg.`Pop` WHERE `Pop` NOT IN (SELECT sample_classification FROM sample_classifications);

INSERT INTO sample_classifications (sample_classification, sample_classification_type, name, lattit, longit) 
SELECT DISTINCT Country, 'region', name, lattit, longit FROM `metadata-2.2_withsites` md LEFT JOIN `Definition-Regions` dr ON dr.ID = md.Country WHERE Exclude = 'FALSE' AND `Country` NOT IN (SELECT sample_classification FROM sample_classifications);

DROP TABLE IF EXISTS `sample_classifications_samples`;
CREATE TABLE `sample_classifications_samples` (
  `sample_id` varchar(50) DEFAULT NULL,
  `sampleclassification_id` varchar(50) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

delete sample_classifications_samples from sample_classifications_samples LEFT JOIN sample_classifications ON sample_classifications_samples.sampleclassification_id = sample_classifications.sample_classification where sample_classification_type = 'subcont';

insert into sample_classifications_samples (sampleclassification_id, sample_id) SELECT `Pop`, Sample FROM SampleGroups;

delete sample_classifications_samples from sample_classifications_samples LEFT JOIN sample_classifications ON sample_classifications_samples.sampleclassification_id = sample_classifications.sample_classification where sample_classification_type = 'region';

insert into sample_classifications_samples (sampleclassification_id, sample_id) select Country,Sample from `metadata-2.2_withsites` md LEFT JOIN sample_classifications_samples scs ON scs.sample_id = md.Sample  where Exclude='FALSE';

UPDATE contact_persons cp LEFT JOIN images i on i.name = cp.contact_person SET cp.image = i.url;

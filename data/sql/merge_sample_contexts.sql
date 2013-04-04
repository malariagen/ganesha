UPDATE sample_contexts sc LEFT JOIN sample_context_description scd ON sc.sample_context = scd.sample_context SET sc.description = scd.description;

INSERT INTO sample_classifications (sample_classification, sample_classification_type_id) SELECT DISTINCT `Pop`, 'subcont' FROM SampleGroups WHERE `Pop` NOT IN (SELECT sample_classification FROM sample_classifications);


delete from sample_classifications_samples scs LEFT JOIN sample_classifications sc ON scs.sampleclassification_id = sc.sample_classification where sample_classification_type_id = 'subcont';

insert into sample_classifications_samples (sampleclassification_id, sample_id) SELECT `Pop`, Sample FROM SampleGroups;


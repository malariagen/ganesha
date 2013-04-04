UPDATE sample_contexts sc LEFT JOIN sample_context_description scd ON sc.sample_context = scd.sample_context SET sc.description = scd.description;

INSERT INTO sample_classifications (sample_classification, sample_classification_type_id) SELECT DISTINCT `Group`, 'region' FROM SampleGroups WHERE `Group` NOT IN (SELECT sample_classification FROM sample_classifications);

truncate table sample_classifications_samples;
insert into sample_classifications_samples (sampleclassification_id, sample_id) SELECT `Group`, Sample FROM SampleGroups;


UPDATE sample_contexts sc LEFT JOIN sample_context_description scd ON sc.sample_context = scd.sample_context SET sc.description = scd.description;

INSERT INTO sample_classifications (sample_classification, sample_classification_type_id) SELECT DISTINCT `Pop`, 'subcont' FROM SampleGroups WHERE `Pop` NOT IN (SELECT sample_classification FROM sample_classifications);

INSERT INTO sample_classifications (sample_classification, sample_classification_type_id) SELECT DISTINCT Country, 'region' FROM `metadata-2.2_withsites` WHERE Country NOT IN (SELECT sample_classification FROM sample_classifications);

delete sample_classifications_samples from sample_classifications_samples LEFT JOIN sample_classifications ON sample_classifications_samples.sampleclassification_id = sample_classifications.sample_classification where sample_classification_type_id = 'subcont';

insert into sample_classifications_samples (sampleclassification_id, sample_id) SELECT `Pop`, Sample FROM SampleGroups;

delete sample_classifications_samples from sample_classifications_samples LEFT JOIN sample_classifications ON sample_classifications_samples.sampleclassification_id = sample_classifications.sample_classification where sample_classification_type_id = 'region';

insert into sample_classifications_samples (sampleclassification_id, sample_id) select Country,Sample from `metadata-2.2_withsites` md LEFT JOIN sample_classifications_samples scs ON scs.sample_id = md.Sample  where Exclude='FALSE';

DROP VIEW sample_context;
CREATE OR REPLACE VIEW sample_context AS select sample_context_id, title, description, Study as study_id, location_id from sample_with_context where Exclude = 'FALSE' group by sample_context_id;
DROP TABLE IF EXISTS `sample_contexts`;
CREATE TABLE sample_contexts AS SELECT sample_context_id as sample_context, title, description, Study as study_id, location_id FROM sample_context;

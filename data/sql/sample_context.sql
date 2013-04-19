CREATE OR REPLACE VIEW sample_contexts AS select sample_context_id, title, description, Study as study_id, location_id from sample_with_context where Exclude = 'FALSE' group by sample_context_id;

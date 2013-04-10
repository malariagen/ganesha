CREATE OR REPLACE VIEW sample_context AS select sample_context_id, title, description, study_id, location_id from sample_with_context where Exclude = 'FALSE' group by sample_context;

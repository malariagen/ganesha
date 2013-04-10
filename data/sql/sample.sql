CREATE OR REPLACE VIEW sample AS select sample, 0 as is_public, sample_context_id from sample_with_context WHERE Exclude = 'FALSE';

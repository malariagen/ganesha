UPDATE sample_contexts sc LEFT JOIN sample_context_description scd ON sc.sample_context = scd.sample_context SET sc.description = scd.description;

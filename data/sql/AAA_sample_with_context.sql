CREATE OR REPLACE VIEW merged_samples AS SELECT  CASE WHEN LabSample = 'TRUE' THEN 'Lab Sample' WHEN LabSample = 'FALSE' AND Site = '0' THEN 'Unknown' ELSE  SUBSTR(REPLACE(SiteCode,'_',' '),4) END  as title, Site as description, SiteCode as location_id,Num,Sample,md.Study as original_study,Country,LabSample,LowTypability,PcaOutlier,IsDuplicate,ManualExlusion,Exclude,Fws,Typability,UsedInSnpDiscovery,Location,Year,Region,KhCluster,SubCont,Site,SiteCode,SiteInfoSource,Notes,CASE WHEN web_study IS NOT NULL THEN web_study_code ELSE md.Study END AS Study from `metadata-2.2_withsites` md LEFT JOIN studies s ON s.legacy_name = md.Study;

CREATE OR REPLACE VIEW sample_with_context AS SELECT CASE WHEN LabSample = 'TRUE' THEN concat(Study,'_LAB_Lab_Sample') WHEN LabSample = 'FALSE' AND Site = '0' THEN CONCAT(Study,'_XX_Unknown') ELSE CONCAT(Study, '_', SiteCode) END  as sample_context_id , CASE WHEN LabSample = 'TRUE' THEN 'Lab Sample' WHEN LabSample = 'FALSE' AND Site = '0' THEN 'Unknown' ELSE  SUBSTR(REPLACE(SiteCode,'_',' '),4) END  as title, Site as description, SiteCode as location_id,Num,Sample,Study,Country,LabSample,LowTypability,PcaOutlier,IsDuplicate,ManualExlusion,Exclude,Fws,Typability,UsedInSnpDiscovery,Location,Year,Region,KhCluster,SubCont,Site,SiteCode,SiteInfoSource,Notes from `merged_samples`;

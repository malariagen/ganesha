
CREATE OR REPLACE VIEW pf21locusfreqs AS
	SELECT  'region' as `AggregTypeID`,
  Pop as `AggregShortName`,
  Variation as `LocusID`,
  Allele as `VariantID`,
  `Count` FROM `Regions-CompositeGenotypes-Counts`
  UNION
	SELECT  'subcont' as `AggregTypeID`,
  Pop as `AggregShortName`,
  Variation as `LocusID`,
  Allele as `VariantID`,
  `Count` FROM `Population-CompositeGenotypes-Counts`;


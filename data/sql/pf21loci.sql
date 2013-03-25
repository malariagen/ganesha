CREATE OR REPLACE VIEW pf21loci AS SELECT Variation as LocusID,ordr,GenomicRegion,Type as LocusType,GeneName,Name,Comments FROM `Definition-CompositeGenotypes`;

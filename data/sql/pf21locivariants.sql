CREATE OR REPLACE VIEW pf21locivariants AS SELECT Variation as LocusID,Allele as VariantID,ordr,Mutant,Name,Color,Comments FROM `Definition-CompositeGenotypeAlleles`;

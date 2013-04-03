
ALTER TABLE `Populations-AlleleFreq-daf` 
  ADD CONSTRAINT `fk_AlleleFreq-daf_1`
  FOREIGN KEY (`SnpName` )
  REFERENCES `SnpInfo` (`SnpName` )
  ON DELETE NO ACTION
  ON UPDATE NO ACTION
, ADD INDEX `fk_AlleleFreq-daf_1` (`SnpName` ASC) ;

ALTER TABLE `Populations-AlleleFreq-maf` 
  ADD CONSTRAINT `fk_AlleleFreq-maf_1`
  FOREIGN KEY (`SnpName` )
  REFERENCES `SnpInfo` (`SnpName` )
  ON DELETE NO ACTION
  ON UPDATE NO ACTION
, ADD INDEX `fk_AlleleFreq-maf_1` (`SnpName` ASC) ;

ALTER TABLE `Populations-AlleleFreq-nraf` 
  ADD CONSTRAINT `fk_AlleleFreq-nraf_1`
  FOREIGN KEY (`SnpName` )
  REFERENCES `SnpInfo` (`SnpName` )
  ON DELETE NO ACTION
  ON UPDATE NO ACTION
, ADD INDEX `fk_AlleleFreq-nraf_1` (`SnpName` ASC) ;

CREATE OR REPLACE VIEW pfsnprel21 AS SELECT SnpInfo.Num as `num`, CAST(REPLACE(SnpInfo.Chr,'MAL','') AS UNSIGNED) as `chrom`, SnpInfo.Pos as `pos`, SnpInfo.SnpName as `snpid`,
  `ref`, `nonrref`, `outgroup`, `ancestral`, `derived`, `pvtAllele`, `pvtPop`, `GeneId`, `GeneDescription`, `Strand`, `CodonNum`, `Codon`, `NtPos`, `RefAmino`, `Mutation`, `MutCodon`, `MutAmino`, `MutType`, `MutName`, 
	NRAF.WAF as `NRAF_WAF`,NRAF.EAF as `NRAF_EAF`, NRAF.SAS as `NRAF_SAS`, NRAF.SEA as `NRAF_SEA`, NRAF.PNG as `NRAF_PNG`, NRAF.SAM as `NRAF_SAM`,
  MAF.WAF as `MAF_WAF`, MAF.EAF as `MAF_EAF`, MAF.SAS as `MAF_SAS`, MAF.SEA as `MAF_SEA`, MAF.PNG as `MAF_PNG`, MAF.SAM as `MAF_SAM`,
  DAF.WAF as `DAF_WAF`, DAF.EAF as `DAF_EAF`, DAF.SAS as `DAF_SAS`, DAF.SEA as `DAF_SEA`, DAF.PNG as `DAF_PNG`, DAF.SAM as `DAF_SAM`,
  '' as `FST`,
  '' as `aliases` FROM SnpInfo
  LEFT JOIN `Populations-AlleleFreq-nraf` NRAF ON SnpInfo.SnpName = NRAF.SnpName
  LEFT JOIN `Populations-AlleleFreq-maf` MAF ON SnpInfo.SnpName = MAF.SnpName
  LEFT JOIN `Populations-AlleleFreq-daf` DAF ON SnpInfo.SnpName = DAF.SnpName;


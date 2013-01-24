from django.db import models
from django.db.models import CharField, BooleanField, ForeignKey, TextField, URLField, SlugField, ManyToManyField, FloatField, EmailField, IntegerField
from ganesha.util import iso_countries

########### CORE ##########

class Sample(models.Model):
    sample_id = CharField(max_length=20, primary_key=True, help_text='ox_code')
    country_id = ForeignKey('SampleSet', limit_choices_to={'sample_set_type_id__exact':'country'}, related_name='sample_set_id_country')
    population_id = ForeignKey('SampleSet', limit_choices_to={'sample_set_type_id__exact':'population'}, related_name='sample_set_id_population')
    is_public = BooleanField(default=False, help_text='True if this sample has public genotypes')
    study_context_id = ForeignKey('StudyContext')
    class Meta:
        db_table = 'samples'

############ STUDIES ETC ######

class Study(models.Model):
    study_id = SlugField(primary_key=True, help_text='Long form name as in alfresco')
    title = CharField(max_length=200)
    legacy_name = SlugField(max_length=20, help_text='Old short form name e.g. ARC3')
    description = TextField()
    alfresco_node = URLField(help_text='Alfresco workspace:// URL')
    people = TextField(help_text='Comma seperated list of names')
    contact_persons = ManyToManyField('ContactPerson')
    def __unicode__(self):
        return self.study_id
    #FK from sample_contexts
    class Meta:
        db_table = 'studies'
        verbose_name_plural = 'Studies'

class Location(models.Model):
    location_id = SlugField(primary_key=True)
    name = CharField(max_length=100)
    longit = FloatField()
    lattit = FloatField()
    country = SlugField(choices=iso_countries.id_name_tuples)
    #FK from StudyContext
    class Meta:
        db_table = 'locations'

class StudyContext(models.Model):
    study_context_id = SlugField(primary_key=True)
    title = CharField(max_length=100)
    description = TextField()
    study_id = ForeignKey('Study')
    location_id = ForeignKey('Location')
    class Meta:
        db_table = 'study_contexts'

######### COMMUNITY #######

class ContactPerson(models.Model):
    contact_person_email = EmailField(primary_key=True)
    name = CharField(max_length=100)
    description = TextField()
    affiliations = ManyToManyField('Institute', through='Affiliation')
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'contact_persons'


class Affiliation(models.Model):
    institute_name = ForeignKey('Institute')
    contact_person_email = ForeignKey('ContactPerson')
    url = URLField(blank=True, help_text='Individuals profile at this insistution')
    class Meta:
        db_table = 'affiliations'
        unique_together = (('institute_name', 'contact_person_email'),)

class Institute(models.Model):
    institute_name = CharField(max_length=100, primary_key=True)
    #FK from affiliation
    class Meta:
        db_table = 'institutes'

######### SAMPLE SETS #########

class SampleSetType(models.Model):
    sample_set_type_id = SlugField(primary_key=True)
    name = CharField(max_length=100)
    #FK from SampleSet
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'sample_set_types'

class SampleSet(models.Model):
    sample_set_id = SlugField(primary_key=True)
    sample_set_type_id = ForeignKey('SampleSetType')
    name = CharField(max_length=100)
    longit = FloatField(blank=True)
    lattit = FloatField(blank=True)
    geo_json = TextField(blank=True, help_text='GeoJson for drawing region if applicable')
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'sample_sets'

######### RESISTANCE MARKERS ######

class Gene(models.Model):
    gene_id = SlugField(primary_key=True)
    #annotation_id = ForeignKey('Annotation') NOT YET CONFIRMED
    order = IntegerField(help_text='Detemines display ordering')
    name = CharField(max_length=100)
    description = TextField()
    class Meta:
        db_table = 'genes'

class Locus(models.Model):
    locus_id = SlugField(primary_key=True)
    gene_id = ForeignKey('Gene')
    name = CharField(max_length=100)
    description = TextField()
    order = IntegerField(help_text='Detemines display ordering')
    locus_type = SlugField(choices=(('AMINOACID', 'Amino acid'), ('HAPLOTYPE','Haplotype')))
    genomic_region = CharField(max_length=50, help_text='format: Chromosome:Position1-Position2')
    class Meta:
        db_table = 'loci'
        verbose_name_plural = 'Loci'

class LocusVariant(models.Model):
    locus_variant_id = SlugField(primary_key=True)
    locus_id = ForeignKey('Locus')
    name = CharField(max_length=100)
    description = TextField(help_text='Markdown')
    order = IntegerField(help_text='Detemines display ordering')
    is_mutant = BooleanField()
    color = CharField(max_length=6)
    frequencies = ManyToManyField('SampleSet', through='LocusFrequency')
    class Meta:
        db_table = 'loci_variants'
        verbose_name_plural = 'LociVariants'

class LocusFrequency(models.Model):
    sample_set_id = ForeignKey('SampleSet')
    locus_variant_id = ForeignKey('LocusVariant')
    count = IntegerField()
    fraction = FloatField()
    class Meta:
        db_table = 'locus_frequencies'
        unique_together = (('sample_set_id', 'locus_variant_id'),)
        verbose_name_plural = 'LocusFrequencies'

######## SNP INFO #########

class SNP(models.Model):
    snp_id = SlugField(primary_key=True)
    chromosome = SlugField()
    position = IntegerField()
    gene_id = ForeignKey('Gene')
    mutation_name = CharField(max_length=100, help_text="Name of the aminoacid mutation")
    frequencies = ManyToManyField('SampleSet', through='SNPFrequency')
    class Meta:
        db_table = 'snps'

class SNPFrequency(models.Model):
    sample_set_id = ForeignKey('SampleSet')
    snp_id = ForeignKey('SNP')
    count_ref = IntegerField()
    count_non_ref = IntegerField()
    frac_non_ref = FloatField()
    class Meta:
        db_table = "snp_frequencies"
        unique_together = (('sample_set_id', 'snp_id'),)
        verbose_name_plural = 'SNPFrequencies'


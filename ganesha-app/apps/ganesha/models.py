from django.db import models
from django.db.models import CharField, BooleanField, ForeignKey, TextField, URLField, SlugField, ManyToManyField, FloatField, EmailField, IntegerField, AutoField
from ganesha.util import iso_countries, slugify

########### CORE ##########
class Sample(models.Model):
    sample = SlugField(max_length=20, primary_key=True, help_text='ox_code')
    is_public = BooleanField(default=False, help_text='True if this sample has public genotypes')
    sample_context = ForeignKey('SampleContext')
    class Meta:
        db_table = 'samples'

############ STUDIES ETC ######
class Study(models.Model):
    study = SlugField(primary_key=True, help_text='Long form name as in alfresco')
    title = CharField(max_length=200)
    legacy_name = SlugField(max_length=20, help_text='Old short form name e.g. ARC3')
    description = TextField(blank=True)
    alfresco_node = CharField(max_length=255, help_text='Alfresco workspace:// URL')
    people = TextField(help_text='Comma seperated list of names', blank=True)
    contact_persons = ManyToManyField('ContactPerson')
    full_study = BooleanField(default=True,
                              help_text='True if this study has a meaningful independent scientific context')
    def __unicode__(self):
        return self.study
    #FK from sample_contexts
    class Meta:
        db_table = 'studies'
        verbose_name_plural = 'Studies'


class Location(models.Model):
    location = SlugField(primary_key=True)
    name = CharField(max_length=100)
    description = CharField(max_length=255)
    longit = FloatField(null=True)
    lattit = FloatField(null=True)
    country = SlugField(choices=iso_countries.id_name_tuples)
    #FK from StudyContext
    def __unicode__(self):
        return self.country + ', ' + self.name
    class Meta:
        db_table = 'locations'
        ordering = ['country', 'name']


class SampleContext(models.Model):
    sample_context = SlugField(primary_key=True)
    title = CharField(max_length=100)
    description = TextField()
    study = ForeignKey('Study')
    location = ForeignKey('Location')
    #Fk From Sample
    def __unicode__(self):
        return self.sample_context
    class Meta:
        db_table = 'sample_contexts'
        ordering = ['sample_context']

######### COMMUNITY #######

class ContactPerson(models.Model):
    contact_person = SlugField(primary_key=True)
    email = EmailField()
    name = CharField(max_length=100)
    image = CharField(max_length=100)
    description = TextField()
    affiliations = ManyToManyField('Institute', through='Affiliation')
    def save(self, **kwargs):
        if not self.contact_person:
            slugify.unique_slugify(self, self.name, slug_field_name='contact_person')
        super(ContactPerson, self).save()
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'contact_persons'

class StudyContactPerson(models.Model):
    study = ForeignKey('Study')
    contactperson = ForeignKey('ContactPerson')
    class Meta:
        db_table = 'studies_contact_persons'
        managed = False

class Affiliation(models.Model):
    affiliation = AutoField(primary_key=True)
    institute = ForeignKey('Institute')
    contact_person = ForeignKey('ContactPerson')
    url = URLField(blank=True, help_text='Individuals profile at this insistution')
    def __unicode__(self):
        return unicode(self.contact_person) + ' - ' + unicode(self.institute)
    class Meta:
        db_table = 'affiliations'
        unique_together = (('institute', 'contact_person'),)

class Institute(models.Model):
    institute = SlugField(primary_key=True)
    name = CharField(max_length=100)
    def save(self, **kwargs):
        if not self.institute:
            slugify.unique_slugify(self, self.name, slug_field_name='institute')
        super(Institute, self).save()
    #FK from affiliation
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'institutes'

######### SAMPLE SETS #########
class SampleClassificationType(models.Model):
    sample_classification_type = SlugField(primary_key=True)
    name = CharField(max_length=100)
    ordr = IntegerField(help_text='Determines display ordering')
    description = TextField()
    #FK from SampleClassification
    def save(self, **kwargs):
        if not self.sample_classification_type:
            slugify.unique_slugify(self, self.name, slug_field_name='sample_classification_type')
        super(SampleClassificationType, self).save()
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'sample_classification_types'

class SampleClassification(models.Model):
    sample_classification = SlugField(primary_key=True)
    sample_classification_type = ForeignKey('SampleClassificationType')
    ordr = IntegerField(help_text='Determines display ordering')
    name = CharField(max_length=100)
    lattit = FloatField(null=True)
    longit = FloatField(null=True)
    geo_json = TextField(blank=True, help_text='GeoJson for drawing region if applicable')
    samples = ManyToManyField('Sample')
    def __unicode__(self):
        return unicode(self.sample_classification_type) + ' ' + self.name
    class Meta:
        db_table = 'sample_classifications'

class SampleClassificationSample(models.Model):
    sample = ForeignKey('Sample')
    sampleclassification = ForeignKey('SampleClassification')
    class Meta:
        db_table = 'sample_classifications_samples'
        managed = False


######### RESISTANCE MARKERS ######
class Gene(models.Model):
    gene = SlugField(primary_key=True)
    #annotation = ForeignKey('Annotation') NOT YET CONFIRMED
    order = IntegerField(help_text='Detemines display ordering')
    name = CharField(max_length=100)
    description = TextField()
    class Meta:
        db_table = 'genes'

class Locus(models.Model):
    locus = SlugField(primary_key=True)
    gene = ForeignKey('Gene')
    name = CharField(max_length=100)
    description = TextField()
    order = IntegerField(help_text='Detemines display ordering')
    locus_type = SlugField(choices=(('AMINOACID', 'Amino acid'), ('HAPLOTYPE', 'Haplotype')))
    genomic_region = CharField(max_length=50, help_text='format: Chromosome:Position1-Position2')
    class Meta:
        db_table = 'loci'
        verbose_name_plural = 'Loci'

class LocusVariant(models.Model):
    locus_variant = SlugField(primary_key=True)
    locus = ForeignKey('Locus')
    name = CharField(max_length=100)
    description = TextField(help_text='Markdown')
    order = IntegerField(help_text='Detemines display ordering')
    is_mutant = BooleanField()
    color = CharField(max_length=6)
    frequencies = ManyToManyField('SampleClassification', through='LocusFrequency')
    class Meta:
        db_table = 'loci_variants'
        verbose_name_plural = 'LociVariants'

class LocusFrequency(models.Model):
    locus_frequency = AutoField(primary_key=True)
    sample_set = ForeignKey('SampleClassification')
    locus_variant = ForeignKey('LocusVariant')
    count = IntegerField()
    fraction = FloatField()
    class Meta:
        db_table = 'locus_frequencies'
        unique_together = (('sample_set', 'locus_variant'),)
        verbose_name_plural = 'LocusFrequencies'

######## SNP INFO #########
class SNP(models.Model):
    snp = SlugField(primary_key=True)
    chromosome = SlugField()
    position = IntegerField()
    gene = ForeignKey('Gene')
    mutation_name = CharField(max_length=100, help_text="Name of the aminoacid mutation")
    frequencies = ManyToManyField('SampleClassification', through='SNPFrequency')
    class Meta:
        db_table = 'snps'

class SNPFrequency(models.Model):
    snp_freqency = AutoField(primary_key=True)
    sample_set = ForeignKey('SampleClassification')
    snp = ForeignKey('SNP')
    count_ref = IntegerField()
    count_non_ref = IntegerField()
    frac_non_ref = FloatField()
    class Meta:
        db_table = "snp_frequencies"
        unique_together = (('sample_set', 'snp'),)
        verbose_name_plural = 'SNPFrequencies'

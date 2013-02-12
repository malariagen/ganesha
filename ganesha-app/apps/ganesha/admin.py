from django.contrib import admin
from ganesha.models import Sample, Study, Location, SampleContext, ContactPerson, Affiliation, Institute, SampleClassificationType, SampleClassification, Gene, Locus, LocusVariant, LocusFrequency, SNP, SNPFrequency
from tastypie.models import ApiKey

admin.site.register(Study)
admin.site.register(Sample)
admin.site.register(Location)
admin.site.register(SampleContext)
admin.site.register(Affiliation)
admin.site.register(Institute)
admin.site.register(ContactPerson)
admin.site.register(SampleClassificationType)
admin.site.register(SampleClassification)
admin.site.register(Gene)
admin.site.register(Locus)
admin.site.register(LocusVariant)
admin.site.register(LocusFrequency)
admin.site.register(SNP)
admin.site.register(SNPFrequency)

admin.site.register(ApiKey)

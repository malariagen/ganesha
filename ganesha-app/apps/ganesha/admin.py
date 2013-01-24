from django.contrib import admin
from ganesha.models import Sample, Study, Location, StudyContext, ContactPerson, Affiliation, Institute, SampleSetType, SampleSet, Gene, Locus, LocusVariant, LocusFrequency, SNP, SNPFrequency

admin.site.register(Study)
admin.site.register(Sample)
admin.site.register(Location)
admin.site.register(StudyContext)
admin.site.register(Affiliation)
admin.site.register(Institute)
admin.site.register(ContactPerson)
admin.site.register(SampleSetType)
admin.site.register(SampleSet)
admin.site.register(Gene)
admin.site.register(Locus)
admin.site.register(LocusVariant)
admin.site.register(LocusFrequency)
admin.site.register(SNP)
admin.site.register(SNPFrequency)

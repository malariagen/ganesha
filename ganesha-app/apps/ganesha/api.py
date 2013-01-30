from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.api import Api
from tastypie import fields
from types import NoneType
from ganesha.models import Study, Sample, SampleContext, Location, ContactPerson, Affiliation, Institute

######### Inline field defs ########

class ToManyFieldInlineToggle(fields.ToManyField):
    def dehydrate_related(self, bundle, related_resource):
        try:
            isInline = bundle.request.GET.get('inline')
            if isInline not in [ 'true', 'True', True]:
                return related_resource.get_resource_uri(bundle)
        # bundle.request is None
        except NoneType:
            pass

        # Default non-nested behavior
        bundle = related_resource.build_bundle(obj=related_resource.instance, request=bundle.request)
        return related_resource.full_dehydrate(bundle)

class ForeignKeyInlineToggle(fields.ForeignKey):
    def dehydrate_related(self, bundle, related_resource):
        try:
            isInline = bundle.request.GET.get('inline')
            if isInline not in [ 'true', 'True', True]:
                return related_resource.get_resource_uri(bundle)
        # bundle.request is None
        except NoneType:
            pass

        # Default non-nested behavior
        bundle = related_resource.build_bundle(obj=related_resource.instance, request=bundle.request)
        return related_resource.full_dehydrate(bundle)

######### Resource definitions ########

class InstituteResource(ModelResource):
    class Meta:
        queryset = Institute.objects.all()
        authentication = Authentication()
        authorization = Authorization()

class AffiliationResource(ModelResource):
    institute = ForeignKeyInlineToggle(InstituteResource, 'institute')
    class Meta:
        queryset = Affiliation.objects.select_related('institute').all()
        authentication = Authentication()
        authorization = Authorization()

class ContactPersonResource(ModelResource):
    affiliations = ToManyFieldInlineToggle(AffiliationResource, attribute=lambda bundle: bundle.obj.affiliations.through.objects.filter(
contact_person=bundle.obj) or bundle.obj.affiliations)
    #affiliations = fields.ToManyField(AffiliationResource, 'affiliations')
    def save_m2m(self, bundle):
        related_mngr = getattr(bundle.obj, 'affiliations')
        if hasattr(related_mngr, 'clear'):
            # Clear it out, just to be safe.
            related_mngr.clear()
        for related_bundle in bundle.data['affiliations']:
            related_bundle.obj.institute.save()
            related_bundle.obj.institute = related_bundle.obj.institute
            related_bundle.obj.contact_person = bundle.obj
            related_bundle.obj.save()

    class Meta:
        resource_name = 'contact_person'
        queryset = ContactPerson.objects.prefetch_related('affiliations').all()
        authentication = Authentication()
        authorization = Authorization()

class StudyResource(ModelResource):
    contact_persons = ToManyFieldInlineToggle(ContactPersonResource, 'contact_persons')
    class Meta:
        queryset = Study.objects.prefetch_related('contact_persons').all()
        filtering = {
            'study': ALL,
            'legacy_name': ALL,
            'description': ALL,
            'alfreseco_node': ALL,
            'people': ALL,
            'contact_persons': ALL_WITH_RELATIONS
            }
        authentication = Authentication()
        authorization = Authorization()

class LocationResource(ModelResource):
    class Meta:
        queryset = Location.objects.all()
        filtering = {
            'location': ALL,
            'name': ALL,
            'longit': ALL,
            'lattit': ALL,
            'country': ALL,
        }
        authentication = Authentication()
        authorization = Authorization()

class SampleContextResource(ModelResource):
    study = ForeignKeyInlineToggle(StudyResource, 'study',)
    location = ForeignKeyInlineToggle(LocationResource, 'location',)
    samples = fields.ToManyField('ganesha.api.SampleResource', 'sample_set', related_name='sample_context')
    class Meta:
        resource_name = 'sample_context'
        queryset = SampleContext.objects.select_related('study', 'location').all()
        filtering = {
            'sample_context': ALL,
            'title': ALL,
            'description': ALL,
            'study': ALL_WITH_RELATIONS,
            'location': ALL_WITH_RELATIONS,
            }
        authentication = Authentication()
        authorization = Authorization()

class SampleResource(ModelResource):
    sample_context = ForeignKeyInlineToggle(SampleContextResource, 'sample_context')
    #    country = ForeignKeyInlineToggle('SampleSetResource', 'country')
    #    population = ForeignKeyInlineToggle('SampleSetResource', 'population')
    class Meta:
        queryset = Sample.objects.select_related('sample_context', 'country', 'population').all()
        filtering = {
            'sample': ALL,
            'country': ALL_WITH_RELATIONS,
            'population': ALL_WITH_RELATIONS,
            'is_public': ALL,
            'sample_context': ALL_WITH_RELATIONS,
            }
        authentication = Authentication()
        authorization = Authorization()






v1_api = Api(api_name='v1')
v1_api.register(InstituteResource())
v1_api.register(AffiliationResource())
v1_api.register(ContactPersonResource())
v1_api.register(StudyResource())
v1_api.register(SampleContextResource())
v1_api.register(SampleResource())
v1_api.register(LocationResource())

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.api import Api
from tastypie import fields
from ganesha.models import Study, Sample, StudyContext, Location


class StudyResource(ModelResource):
    class Meta:
        queryset = Study.objects.all()

class LocationResource(ModelResource):
    class Meta:
        queryset = Location.objects.all()
        filtering = {
            'country': ALL,
            }

class StudyContextResource(ModelResource):
    location_id = fields.ForeignKey(LocationResource, 'location_id', full=True)
    class Meta:
        resource_name = 'study_context'
        queryset = StudyContext.objects.all()
        filtering = {
            'location_id': ALL_WITH_RELATIONS,
            }


class SampleResource(ModelResource):
    study_context_id = fields.ForeignKey(StudyContextResource, 'study_context_id', full=True)
    class Meta:
        queryset = Sample.objects.all()
        filtering = {
            'study_context_id': ALL_WITH_RELATIONS,
            }



v1_api = Api(api_name='v1')
v1_api.register(StudyResource())
v1_api.register(StudyContextResource())
v1_api.register(SampleResource())
v1_api.register(LocationResource())

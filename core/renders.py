from rest_framework.renderers import JSONRenderer


class VersionedJSONRenderer(JSONRenderer):
    """
    JSON renderer with versioning support
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        request = renderer_context['request']
        version = request.version
        response_data = {'version': version, 'data': data}
        return super().render(response_data, accepted_media_type, renderer_context)




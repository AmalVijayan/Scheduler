from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
import scheduler_api.views


router = DefaultRouter()


# Full CRUD-able APIs
router.register(r'schedule', scheduler_api.views.ScheduleViewSet, basename='schedule')

urlpatterns = [
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),

    # Use the `get_schema_view()` helper to add a `SchemaView` to project URLs.
    #   * `title` and `description` parameters are passed to `SchemaGenerator`.
    #   * Provide view name for use with `reverse()`.
    path('openapi', get_schema_view(
        title="Audio Server",
        description="API for AUDIO SERVER",
        version="0.0.1"
    ), name='openapi-schema'),

    path('', include(router.urls)),
]
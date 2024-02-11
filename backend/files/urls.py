from django.urls import path , include
# from rest_framework import routers
# from .views import LinearRegressionView


# router = routers.DefaultRouter()
# #router.register("files", LinearRegressionView.as_view(),"files")
# router.register(r"files", LinearRegressionView, 'files')
# #router.register('question', cebula_views.QuestionView.as_view({
# #    'get':'list',}), 'userpage-question')

# # router.register("files", LinearRegressionView.as_view({'post': 'create'}),name="files")

# # router.register ("", FileViewSet.upload_csv,basename="upload_csv")

# urlpatterns = [
#     path("",include(router.urls))
# ]

from .views import LinearRegressionView

urlpatterns = [
    path("files/", LinearRegressionView.as_view(), name="linear_regression"),
]

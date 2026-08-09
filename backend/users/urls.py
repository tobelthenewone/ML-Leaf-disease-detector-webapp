from django.urls import path
from .views import CustomUserCreate, BlacklistTokenUpdateView, UserDetail, DeseaseDetail, PredictionDetail, PostDetail, AllDataView, PredictionView,DiseaseDetail,PostList,PredictionList,Post,GetUserView
from . import views


app_name = 'users'

urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist'),
    path('userdetail/', UserDetail.as_view(), name='userdetail'),
    path('predict/', PredictionView.as_view(), name='predict'),
    path('all-data/', AllDataView.as_view(), name='all_data'),
    path('deseaseDetail/', DeseaseDetail.as_view(), name='deseaseDetail'),
    path('predictionDetail/',  PredictionDetail.as_view(), name='predictionDetail'),
    path('diseaseDetail/<int:pk>/', PostDetail.as_view(), name='diseaseDetail'),
    path('all_diseases/' , PostList.as_view(), name='all_diseases'),
    path('predictions/', PredictionList.as_view(), name='prediction'),
    path('prediction/<int:pk>/', Post.as_view(), name='prediction-detail'),
    path('user/', GetUserView.as_view(), name='user'),



]

from django.urls import path
from . import views

app_name = 'videoBlogApp'

urlpatterns = [
    path('search', views.searchBarView, name='search'),
    path('categoryOptions/', views.categoryOptionsView, name='categoryOptionsURL'),
    path('subCategoryOptions/', views.subCategoryOptionsView, name='subCategoryOptionsURL'),
    path('blogVideos/', views.blogVideosView, name='blogVideosURL'),
    path('blogVideosListingDM/', views.blogVideoListingDMView, name='blogVideoListingDMURL'),
    path('blogVideosDetailed/', views.blogVideosDetailedView, name='blogVideosDetailedURL'),
    path('deleteFKdata', views.deleteFKdataView, name='deleteFKdataUrl'),
    path('by-theme/<slug:slug>', views.themeVideoList, name='themeVideoUrl'),
    path('category/<slug:slug>', views.categoryBasedVideosView, name='categoryBasedVideosUrl'),
    path('sub-category/<slug:slug>', views.subCategoryBasedVideosView, name='subCategoryBasedVideosUrl'),
    path('tag/<slug:slug>', views.tagBasedVideosView, name='tagBasedVideosUrl'),
    path('videoBlogGenericData', views.videoBlogGenericDataView, name="videoBlogGenericDataUrl"),
    path('videoPageSectionVisiblity', views.videoPageSectionVisiblityView, name="videoPageSectionVisiblityUrl"),
    path('videoHeading', views.videosHeadingDMView, name="videosHeadingDMUrl"),
    path('delete-this/<slug:slug>/<slug:model>', views.deleteObjectORM, name="deleteUsingORMUrl"),
    path('', views.videoListView, name='videoListURL'),
    path('<slug>', views.videoDetailView, name="videoDetailURL"),
    path('filters/', views.VideoFiltersView.as_view(), name="video_filters"),

    path('videoscreenlistapi/', views.videoListApiView.as_view(), name='videoscreenlistapi'),
    path('videodescriptionpageapi/<int:pk>', views.videoDetailAPIView.as_view(), name='videodescriptionpageapi'),
    path('video-description/<int:pk>/', views.videoDetailAPIView.as_view(), name='video_description_page'),
    path('videoscreencategorylist/', views.VideoScreenCategoryList.as_view(), name='videoscreencategorylist'),
    path('getcategory/<slug:slug>', views.getCategoryBasedVideosView, name='categoryBasedVideosAPI'),
]

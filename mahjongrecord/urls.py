from django.urls import path
from .views import MahjongRecordTop, MahjongRecordCreate, MahjongRecordDelete, MahjongRecordUpdate,\
                scorecalculatefunc, scoresfunc, player_create_func, calculate_uma_oka_benefit_func,\
                confirm_scores_delete_func, scores_delete_func,\
                    signup_func, login_func, logout_func, set_uma_oka_func, caution_func
urlpatterns = [
    path('logout/', logout_func, name='logout'),
    path('top/', MahjongRecordTop.as_view(), name = 'top'),
    path('caution/', caution_func, name = 'caution'),
    path('create/', MahjongRecordCreate.as_view(), name = 'create'),
    path('delete/<int:pk>', MahjongRecordDelete.as_view(), name = 'delete'),
    path('update/<int:pk>', MahjongRecordUpdate.as_view(), name = 'update'),
    path('scorecalculate/<int:pk>', scorecalculatefunc, name = 'scorecalculate'),
    path('scores/', scoresfunc, name = 'scores'),
    path('player_create/', player_create_func, name = 'player_create'),
    path('set/', set_uma_oka_func, name = 'set'),
    path('calculate_uma_oka_benefit/', calculate_uma_oka_benefit_func, name = 'calculate_uma_oka_benefit'),
    path('confirm_scores_delete/', confirm_scores_delete_func, name = 'confirm_scores_delete'),
    path('scores_delete/', scores_delete_func, name = 'scores_delete'),
    path('signup/', signup_func, name = 'signup'),
    path('login/', login_func, name = 'login'), 
]

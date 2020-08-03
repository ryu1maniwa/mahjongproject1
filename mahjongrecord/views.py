from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, TemplateView
from .models import MahjongRecordModel, MahjongPlayerModel, Mahjong_Uma_Oka_Model
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
# Create your views here.

def signup_func(request):
    if request.method == 'POST': #入力するとPOSTとして入ってくる
        signup_username = request.POST['username']
        signup_password = request.POST['password']
        try:
            User.objects.get(username=signup_username)
            return render(request, 'signup.html', {'error':'このユーザは登録されています'})
        except:
            user = User.objects.create_user(signup_username, '', signup_password)
            return redirect('login')
    return render(request, 'signup.html')

def login_func(request):
    if request.method == 'POST':
        login_username = request.POST['username']
        login_password = request.POST['password']

        user = authenticate(request, username=login_username, password=login_password)
        if user is not None:
            login(request, user)
            return redirect('top')
        else:
            return render(request, 'login.html', {'error2':'このユーザは登録されていません'})
    return render(request, 'login.html')

def logout_func(request):
    logout(request)
    return redirect('login')

class MahjongRecordTop(ListView):
    template_name = 'top.html'
    model = MahjongRecordModel

@login_required
def scoresfunc(request):
    players = MahjongPlayerModel.objects.filter(username = request.user.username)
    object_list = MahjongRecordModel.objects.filter(username = request.user.username)
    sum_player1 = MahjongRecordModel.objects.filter(username = request.user.username).aggregate(Sum('calculatedscore1'))
    sum_player2 = MahjongRecordModel.objects.filter(username = request.user.username).aggregate(Sum('calculatedscore2'))
    sum_player3 = MahjongRecordModel.objects.filter(username = request.user.username).aggregate(Sum('calculatedscore3'))
    sum_player4 = MahjongRecordModel.objects.filter(username = request.user.username).aggregate(Sum('calculatedscore4'))
    return render(request, 'scores.html', {'object_list':object_list, 'players':players, \
         'sum_player1':sum_player1, 'sum_player2':sum_player2, 'sum_player3':sum_player3, 'sum_player4':sum_player4})

@login_required
def player_create_func(request):
    if request.method == 'POST': #入力するとPOSTとして入ってくる
        player1 = request.POST['player1']
        player2 = request.POST['player2']
        player3 = request.POST['player3']
        player4 = request.POST['player4']
        MahjongPlayerModel.objects.filter(username = request.user.username).delete()
        players = MahjongPlayerModel(username = request.user.username, player1 = player1, player2 = player2, player3 = player3, player4 = player4)
        players.save()
        return redirect('top')
    return render(request, 'playercreate.html')

@login_required
def set_uma_oka_func(request):
    if request.method == 'POST':
        uma = request.POST['uma']
        oka = request.POST['oka']
        Mahjong_Uma_Oka_Model.objects.filter(username = request.user.username).delete()
        uma_oka = Mahjong_Uma_Oka_Model(username = request.user.username, uma = uma, oka = oka)
        uma_oka.save()
        return redirect('calculate_uma_oka_benefit')
    return render(request, 'set.html')

@login_required
def caution_func(request):
    try:
        get1 = MahjongPlayerModel.objects.get(username = request.user.username)
        get2 = Mahjong_Uma_Oka_Model.objects.get(username = request.user.username)
        return redirect('create')
    except:
        return render(request, 'caution.html')

class MahjongRecordCreate(CreateView):
    template_name = 'create.html'
    def get_context_data(self, *args):
        player_list = MahjongPlayerModel.objects.filter(username = self.request.user.username)
        context = super().get_context_data(*args)
        context['player_list'] = player_list
        return context
    model = MahjongRecordModel
    fields = (
    'username', 'score1', 'score2', 'score3', 'score4',
    'rank1', 'rank2', 'rank3', 'rank4')
    def get_success_url(self):
        return reverse('scorecalculate', kwargs={'pk': self.object.pk})

class MahjongRecordDelete(DeleteView):
    template_name = 'delete.html'
    model = MahjongRecordModel
    success_url = reverse_lazy('scores')

#グローバル変数
class MahjongRecordUpdate(UpdateView):
    template_name = 'update.html'
    model = MahjongRecordModel
    fields = (
    'score1', 'score2', 'score3', 'score4',
    'rank1', 'rank2', 'rank3', 'rank4')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['player_list'] = MahjongPlayerModel.objects.filter(username = self.request.user.username)
        return context
        #templateで{{ player_list }}と打てばMahjongPlayerModel.objects.all()が表示される
    def get_success_url(self):
        return reverse('scorecalculate', kwargs={'pk': self.object.pk})
        
@login_required
def confirm_scores_delete_func(request):
    return render(request, 'confirm_scores_delete.html')

@login_required
def scores_delete_func(request):
    MahjongRecordModel.objects.filter(username = request.user.username).delete()
    return redirect('scores')

@login_required
def calculate_uma_oka_benefit_func(request):
    object_list = Mahjong_Uma_Oka_Model.objects.filter(username = request.user.username).last()
    uma = object_list.uma
    oka = object_list.oka

    if uma == 'なし':
        object_list.uma_oka_benefit_of_2nd_player = - oka
        object_list.uma_oka_benefit_of_3rd_player = - oka
        object_list.uma_oka_benefit_of_4th_player = - oka
        
    elif uma == '5-10':
        object_list.uma_oka_benefit_of_2nd_player = - oka + 5000
        object_list.uma_oka_benefit_of_3rd_player = - oka - 5000
        object_list.uma_oka_benefit_of_4th_player = - oka - 10000

    elif uma == '5-15':
        object_list.uma_oka_benefit_of_2nd_player = - oka + 5000
        object_list.uma_oka_benefit_of_3rd_player = - oka - 5000
        object_list.uma_oka_benefit_of_4th_player = - oka - 15000

    elif uma == '10-20':
        object_list.uma_oka_benefit_of_2nd_player = - oka + 10000
        object_list.uma_oka_benefit_of_3rd_player = - oka - 10000
        object_list.uma_oka_benefit_of_4th_player = - oka - 20000

    elif uma == '10-30':
        object_list.uma_oka_benefit_of_2nd_player = - oka + 10000
        object_list.uma_oka_benefit_of_3rd_player = - oka - 10000
        object_list.uma_oka_benefit_of_4th_player = - oka - 30000

    else: # uma == '20-30'
        object_list.uma_oka_benefit_of_2nd_player = - oka + 20000
        object_list.uma_oka_benefit_of_3rd_player = - oka - 20000
        object_list.uma_oka_benefit_of_4th_player = - oka - 30000
    
    object_list.save()
    return redirect('top')

@login_required
def scorecalculatefunc(request, pk):
    object_list = MahjongRecordModel.objects.filter(username = request.user.username).get(pk=pk)
    score1 = object_list.score1
    score2 = object_list.score2
    score3 = object_list.score3
    score4 = object_list.score4
    rank1 = object_list.rank1
    rank2 = object_list.rank2
    rank3 = object_list.rank3
    rank4 = object_list.rank4
    object_list.calculatedscore1 = round(scorecalculate(request.user.username, rank1, score1)-0.1)
    object_list.calculatedscore2 = round(scorecalculate(request.user.username, rank2, score2)-0.1)
    object_list.calculatedscore3 = round(scorecalculate(request.user.username, rank3, score3)-0.1)
    object_list.calculatedscore4 = round(scorecalculate(request.user.username, rank4, score4)-0.1)
    object_list.save()

    if rank1 == '1st':
        object_list.calculatedscore1 = -(object_list.calculatedscore2 + object_list.calculatedscore3 + object_list.calculatedscore4)
    elif rank2 == '1st':
        object_list.calculatedscore2 = -(object_list.calculatedscore1 + object_list.calculatedscore3 + object_list.calculatedscore4)
    elif rank3 == '1st':
        object_list.calculatedscore3 = -(object_list.calculatedscore2 + object_list.calculatedscore1 + object_list.calculatedscore4)
    else:
        object_list.calculatedscore4 = -(object_list.calculatedscore2 + object_list.calculatedscore3 + object_list.calculatedscore1)
    object_list.save()
    return redirect('scores')

def scorecalculate(request_user, rank, score, **kwargs):
    object_list = Mahjong_Uma_Oka_Model.objects.filter(username = request_user).last()
    uma_oka_benefit_of_2nd_player = object_list.uma_oka_benefit_of_2nd_player
    uma_oka_benefit_of_3rd_player = object_list.uma_oka_benefit_of_3rd_player
    uma_oka_benefit_of_4th_player = object_list.uma_oka_benefit_of_4th_player

    if rank == '2nd':
        result = ((score + uma_oka_benefit_of_2nd_player)/1000)
    elif rank == '3rd':
        result = ((score + uma_oka_benefit_of_3rd_player)/1000)
    elif rank == '4th':
        result = ((score + uma_oka_benefit_of_4th_player)/1000)
    else: #'1st'
        result = 0 #後で計算
    return result
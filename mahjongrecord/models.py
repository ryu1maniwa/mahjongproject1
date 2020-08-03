from django.db import models
# Create your models here.


class MahjongPlayerModel(models.Model): 
    #username = models.CharField(max_length = 10, default = get_user_model().username)
    username = models.CharField(max_length = 100, default = 'taro')
    player1 = models.CharField(max_length = 10, default = 'player1')
    player2 = models.CharField(max_length = 10, default = 'player2')
    player3 = models.CharField(max_length = 10, default = 'player3')
    player4 = models.CharField(max_length = 10, default = 'player4')

class MahjongRecordModel(models.Model):
    username = models.CharField(max_length = 100, default = 'taro')
    RANK = (('1st','1st'), ('2nd','2nd'), ('3rd','3rd'), ('4th','4th'))
    rank1 = models.CharField(
        max_length = 50,
        choices = RANK,
        default = '1st'
    )
    rank2 = models.CharField(
        max_length = 50,
        choices = RANK,
        default = '2nd'
    )
    rank3 = models.CharField(
        max_length = 50,
        choices = RANK,
        default = '3rd'
    )
    rank4 = models.CharField(
        max_length = 50,
        choices = RANK,
        default = '4th'
    )
    score1 = models.IntegerField(default=25000)
    score2 = models.IntegerField(default=25000)
    score3 = models.IntegerField(default=25000)
    score4 = models.IntegerField(default=25000)

    calculatedscore1 = models.IntegerField(null=True, blank=True, default=0)
    calculatedscore2 = models.IntegerField(null=True, blank=True, default=0)
    calculatedscore3 = models.IntegerField(null=True, blank=True, default=0)
    calculatedscore4 = models.IntegerField(null=True, blank=True, default=0)

class Mahjong_Uma_Oka_Model(models.Model):
    username = models.CharField(max_length = 100, default = 'taro')
    uma_choice = (('なし', 'なし'), ('5-10','5-10'), ('5-15','5-15'), ('10-20','10-20'), ('10-30','10-30'), ('20-30','20-30'))
    uma = models.CharField(
        max_length = 50,
        choices = uma_choice,
        default = 'なし'
    )
    oka = models.IntegerField(default=25000)
    uma_oka_benefit_of_2nd_player = models.IntegerField(null=True, blank=True, default=0)
    uma_oka_benefit_of_3rd_player = models.IntegerField(null=True, blank=True, default=0)
    uma_oka_benefit_of_4th_player = models.IntegerField(null=True, blank=True, default=0)
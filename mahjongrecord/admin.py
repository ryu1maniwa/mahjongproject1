from django.contrib import admin
from .models import MahjongRecordModel, MahjongPlayerModel, Mahjong_Uma_Oka_Model
# Register your models here.
admin.site.register(MahjongRecordModel)
admin.site.register(MahjongPlayerModel)
admin.site.register(Mahjong_Uma_Oka_Model)
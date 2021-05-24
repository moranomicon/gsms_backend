from django.urls import path, include
from django.utils import timezone
from rest_framework import routers, serializers, viewsets
from .models import Material, MaterialChangeHistory, PackingListChangeHistory, PackingList, TransferLocation
from django.contrib.auth.models import User


class TransferLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferLocation
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'
        ordering = ['material_no']


# class PalletSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Pallet
#         fields = '__all__'

class PackingListSerializer(serializers.ModelSerializer):
    material_name = MaterialSerializer(data='material_viewset', read_only=True)
    material_name_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = PackingList
        fields = '__all__'
        ordering = ['packing_no']
    

class MaterialChangeHistorySerializer(serializers.ModelSerializer):
    material_name = MaterialSerializer(data='material_viewset')
    class Meta:
        model = MaterialChangeHistory
        fields = '__all__'
        ordering = ['created_at']

class PackingListChangeHistorySerializer(serializers.ModelSerializer):
    packing_list = PackingListSerializer(data='packinglist_viewset')
    class Meta:
        model = PackingListChangeHistory
        fields = '__all__'
        ordering = ['created_at']


class UpdateMaterialSerializer(serializers.Serializer):
    material_in = serializers.IntegerField(required=False, default=0)
    material_out = serializers.IntegerField(required=False, default=0)
    material_change_date = serializers.DateTimeField(default=timezone.now)
    material_quantity = serializers.IntegerField()
    transfer_to = serializers.IntegerField(required=False)


class UpdatePackingListSerializer(serializers.Serializer):
    packing_no = serializers.CharField()
    material_name = serializers.IntegerField()
    packing_change_date = serializers.DateTimeField(default=timezone.now)
    weight = serializers.FloatField()
    weight_out = serializers.IntegerField(required=False, default=0)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        write_only_fields = ('password',)
        read_only_fields = ('id',)

   
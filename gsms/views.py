from datetime import datetime
from django.contrib.auth.models import User
from django.utils import translation
from rest_framework.response import Response
from gsms.serializer import MaterialChangeHistorySerializer, MaterialSerializer, PackingListChangeHistorySerializer, PackingListSerializer, TransferLocationSerializer, UpdateMaterialSerializer, UpdatePackingListSerializer, UserSerializer
from gsms.models import Material, MaterialChangeHistory, PackingList, PackingListChangeHistory, TransferLocation
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.db.models import Sum
from django.db import transaction


# Create your views here.
class TransferLocationViewSet(viewsets.ModelViewSet):
    queryset = TransferLocation.objects.all()
    serializer_class = TransferLocationSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    @action(detail=True,  methods=['put', 'patch', 'post'])
    def update_materials(self, request, pk=None):
        try:
            material = self.get_object()

            serializer = UpdateMaterialSerializer(data=request.data)
            if not serializer.is_valid():
                raise Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            if serializer.data.get('material_in') or serializer.data.get('material_out'):
                MaterialChangeHistory.objects.create(
                    material_name=material, material_old_quantity=material.material_quantity, material_in_qty=serializer.data.get('material_in'), material_out_qty=serializer.data.get('material_out'), material_change_date=serializer.data.get('material_change_date'), transfer_to=TransferLocation(pk=serializer.data.get('transfer_to')))
                material.material_quantity = material.material_quantity + \
                    serializer.data.get('material_in') - \
                    serializer.data.get('material_out')
            else:
                material.material_quantity = serializer.data.get(
                    'material_quantity')
            material.save()

            return Response("Material %s updated!" % material.material_name, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def count_materials(self, request, pk=None):
        total_materials = Material.objects.count()

        return Response(data=total_materials, status=status.HTTP_200_OK)


class PackingListViewSet(viewsets.ModelViewSet):
    queryset = PackingList.objects.all()
    serializer_class = PackingListSerializer

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        #delete all history b4 deleting the packing list
        packing_list = self.get_object()
        PackingListChangeHistory.objects.filter(packing_list=packing_list.pk).delete()

        return super().destroy(request, *args, **kwargs)

    @action(detail=True,  methods=['put', 'patch', 'post'])
    def update_packing_list(self, request, pk=None):
        try:
            packing_list = self.get_object()

            serializer = UpdatePackingListSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            if serializer.data.get('weight_out'):
                PackingListChangeHistory.objects.create(
                    packing_list=packing_list, old_weight=packing_list.weight, weight_out=serializer.data.get('weight_out'), packing_change_date=serializer.data.get('packing_change_date'))
                packing_list.weight = packing_list.weight - \
                    serializer.data.get('weight_out')
            else:
                packing_list.weight = serializer.data.get('weight')
            packing_list.material_name = Material(
                serializer.data.get('material_name'))
            packing_list.packing_no = serializer.data.get('packing_no')
            packing_list.save()

            return Response("Packing List %s updated!" % packing_list.material_name, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)

# class PalletViewSet(viewsets.ModelViewSet):
#     queryset = Pallet.objects.all()
#     serializer_class = PalletSerializer


class MaterialChangeHistoryViewSet(viewsets.ModelViewSet):
    queryset = MaterialChangeHistory.objects.all()
    serializer_class = MaterialChangeHistorySerializer


class PackingListChangeHistoryViewSet(viewsets.ModelViewSet):
    queryset = PackingListChangeHistory.objects.all()
    serializer_class = PackingListChangeHistorySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        auto_generate_email = request.data['first_name'].lower() + request.data['last_name'].lower() + '@greentech.com'
        user = User.objects.create(
            username=request.data['username'],
            email=auto_generate_email,
            first_name=request.data['first_name'],
            last_name=request.data['last_name']
        )

        user.set_password('qwerty123')
        user.save()

        return super().create(request, *args, **kwargs)


class DashboardViewSet(viewsets.ViewSet):

    @action(detail=False,  methods=['get'])
    def total_material(self, request):
        total_material = Material.objects.aggregate(Sum('material_quantity'))['material_quantity__sum']
        return Response(total_material)

    @action(detail=False,  methods=['get'])
    def total_packing_list(self, request):
        total_packing_list = PackingList.objects.exclude(weight=0).count()
        return Response(total_packing_list)

    @action(detail=False,  methods=['get'])
    def total_material_in(self, request):
        today_material_in = MaterialChangeHistory.objects.filter(
            material_change_date__date=datetime.today()).values_list('material_in_qty', flat=True)
        total_material_qty = sum(today_material_in)
        return Response(total_material_qty)

    @action(detail=False,  methods=['get'])
    def total_material_out(self, request):
        today_material_out = MaterialChangeHistory.objects.filter(
            material_change_date__date=datetime.today()).values_list('material_out_qty', flat=True)
        total_material_qty = sum(today_material_out)
        return Response(total_material_qty)

    @action(detail=False,  methods=['get'])
    def total_material_in_yearly(self, request):
        year = datetime.now().year
        months = 1

        material_in_yearly = MaterialChangeHistory.objects.filter(
            material_change_date__year=year).values_list('created_at__month').annotate(Sum('material_in_qty')).order_by('created_at__month')

        total_per_month = []
        while months <= 12:
            qty = 0
            get_month_qty = material_in_yearly.filter(created_at__month=months).first()
            if not get_month_qty:
                total_per_month.append(qty)
            else:
                total_per_month.append(get_month_qty[1])
            months +=1
        return Response(total_per_month)

    @action(detail=False,  methods=['get'])
    def total_material_out_yearly(self, request):
        year = datetime.now().year
        months = 1

        material_out_yearly = MaterialChangeHistory.objects.filter(
            material_change_date__year=year).values_list('created_at__month').annotate(Sum('material_out_qty')).order_by('created_at__month')

        total_per_month = []
        while months <= 12:
            qty = 0
            get_month_qty = material_out_yearly.filter(created_at__month=months).first()
            if not get_month_qty:
                total_per_month.append(qty)
            else:
                total_per_month.append(get_month_qty[1])
            months +=1
        return Response(total_per_month)

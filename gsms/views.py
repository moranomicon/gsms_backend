from rest_framework.response import Response
from gsms.serializer import MaterialChangeHistorySerializer, MaterialSerializer, PackingListChangeHistorySerializer, PackingListSerializer, UpdateMaterialSerializer, UpdatePackingListSerializer
from gsms.models import Material, MaterialChangeHistory, PackingList, PackingListChangeHistory
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action


# Create your views here.
class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    @action(detail=True,  methods=['put', 'patch', 'post'])
    def update_materials(self, request, pk=None):
        try: 
            material = self.get_object()

            serializer = UpdateMaterialSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            if serializer.data.get('material_in') or serializer.data.get('material_out'):
                MaterialChangeHistory.objects.create(
                    material_name=material, material_old_quantity=material.material_quantity, material_in_qty=serializer.data.get('material_in'), material_out_qty=serializer.data.get('material_out'), material_change_date=serializer.data.get('material_change_date'))
                material.material_quantity = material.material_quantity + serializer.data.get('material_in') - serializer.data.get('material_out')
            else:
                material.material_quantity = serializer.data.get('material_quantity')
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
                packing_list.weight = packing_list.weight - serializer.data.get('weight_out') 
            else:
                packing_list.weight = serializer.data.get('weight')
            packing_list.material_name = Material(serializer.data.get('material_name'))
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
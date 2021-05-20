from django.db import models

# Create your models here.


class TransferLocation(models.Model):
    name = models.IntegerField(primary_key=True)
    description = models.TextField()

class Material(models.Model):
    material_name = models.CharField(max_length=50)
    material_quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.material_name

    class Meta:
        ordering = ['material_name']


class PackingList(models.Model):
    packing_no = models.CharField(max_length=50)
    material_name = models.ForeignKey(Material, on_delete=models.DO_NOTHING)
    weight = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.packing_no

    def save(self, *args, **kwargs) -> None:
        self.material_name = Material(self.material_name_id)
        return super().save(*args, **kwargs)
        
    class Meta:
        ordering = ['packing_no']

class MaterialChangeHistory(models.Model):
    material_name = models.ForeignKey(Material, on_delete=models.DO_NOTHING)
    material_old_quantity = models.PositiveIntegerField()
    material_in_qty = models.IntegerField()
    material_out_qty = models.IntegerField()
    material_change_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


class PackingListChangeHistory(models.Model):
    packing_list = models.ForeignKey(PackingList, on_delete=models.DO_NOTHING)
    old_weight = models.PositiveIntegerField()
    weight_out = models.IntegerField()
    transfer_to = models.ForeignKey(TransferLocation, on_delete=models.DO_NOTHING, blank=True, null=True)
    packing_change_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)



# class Pallet(models.Model):
#     packing_list = models.ForeignKey(PackingList, on_delete=models.RESTRICT)
#     pallet_no = models.CharField(max_length=50)
#     weight = models.FloatField()
#     created_at = models.DateTimeField(auto_now_add=True)





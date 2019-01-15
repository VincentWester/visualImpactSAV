from rest_framework import serializers
from visualImpactSAV.models import SAV_file

class SAV_filesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SAV_file
        fields = (
            'creation_date',
            'id',
            'name_customer',
            'society_customer',
            'brand_product',
            'name_product',
            'serial_number_product',
        )
from rest_framework import serializers
from django.contrib.auth.models import User, Group


class UserSerializer(serializers.ModelSerializer):
    group = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'group']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        group_id = validated_data.pop('group', None)
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        
        # Adiciona o usuário ao grupo especificado, se fornecido
        if group_id:
            try:
                if group_id == '1':
                    group = Group.objects.get(name='Vendedor')
                elif group_id == '2':
                    group = Group.objects.get(name='Comprador')
                else:
                    group = None
                
                if group:
                    user.groups.add(group)
            except Group.DoesNotExist:
                pass # Grupo não existe, ignora
        return user
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nome de usuário já está em uso.")
        return value
    
    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value

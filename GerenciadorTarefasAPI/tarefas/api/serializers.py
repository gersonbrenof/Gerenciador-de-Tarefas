from rest_framework import serializers
from django.contrib.auth.models import User
from tarefas.models import Usuario, Tarefa
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
class UsuarioSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=6, error_messages = {"Min_length":"A senha deve possuir mais de 6 caracteres"})
    class Meta:
        model = Usuario
        fields = ('id', 'username','email',  'password')
        extra_kwargs = {'password': {'write_only': True}} 
    def validate_passsword(self,value):
        if " " in value:
            raise serializers.ValidationError("A senha não pode conter espaço em branco")
        
    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
            
            # cria o usuario no modelo do user
        user = User.objects.create_user(username=username, email = email, password=password)
            
        #cria o perfil do usuario no modelo do usuario que no caso vai cria o nome do usuario
            
        usuario = Usuario.objects.create(usuario=user, **validated_data)
            
        return usuario
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        try:
           user = User.objects.get(username=username)
        except User.DoesNotExist:
           raise AuthenticationFailed('Credenciais inválidas')
       
        if not user.check_password(password):
            raise AuthenticationFailed('Credenciais inválidas')
        
        user = authenticate(username=user.username, password=password)
       
        if user is None or not user.is_active:
           raise AuthenticationFailed('Erro Crendencial invlaidados')
        # Gera tokens de acesso
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
        
class TarefaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefa
        fields = ['id', 'titulo_tarefa','descricao', 'data_criacao','status', 'prioridade','categoria', 'etiqueta' , 'is_finalizada']
        read_only_fields = ['usuario'] 
        
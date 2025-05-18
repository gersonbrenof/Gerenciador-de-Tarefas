from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from tarefas.api.serializers import UsuarioSerializer, LoginSerializer, TarefaSerializer, Tarefa
from rest_framework.permissions import  AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from django.db.models import Q
import csv
from django.http import HttpResponse
class RegistrarUsuarioView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UsuarioSerializer
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        
        if serializer.is_valid():
            usuario = serializer.save()
            
            # aqui gera o token de acesso
            
            refresh = RefreshToken.for_user(usuario.usuario)
            access_token = str(refresh.access_token)
            
            return Response({
                'message': 'Usuario Cadastrado com sucesso',
                'access': access_token,
                'refresh': str(refresh)
            }, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    
class LoginView(APIView):
        permission_classes = [AllowAny]
        def post(self, request):
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                return Response(serializer.validated_data, status.HTTP_200_OK)
            return Response(status.HTTP_401_UNAUTHORIZED)

class TarefaViewSet(viewsets.ModelViewSet):
   # queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer 
    permission_classes = [IsAuthenticated] 
    
    
    
    def get_queryset(self):
        
        return Tarefa.objects.filter(usuario = self.request.user.usuario)
    
    def perform_create(self, serializer):
        """Salva a tarefa associando ao usuário logado"""
        
        serializer.save(usuario=self.request.user.usuario)  # Salva a ta
    
    def perform_destroy(self, instance):
        # pega o usuario logado
        usuario_logado = self.request.user.usuario
         # verificar se o usuario esat logado
        if instance.usuario != usuario_logado:
            raise PermissionDenied("Não é possivel deletar essa tarefa por favo deletar uma valida")
        
        instance.delete()
        return Response({'mesage': 'tarefa delatada com sucesso'},status=status.HTTP_204_NO_CONTENT )
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        usuario_logado = request.user.usuario
        
        if instance.usuario != usuario_logado:
            raise PermissionDenied("voce nao tem permissao para editar essa tarefa")
        
        return super().update(request,*args, **kwargs )

class BuscaTarefasApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        termo = request.query_params.get('q', '').strip().lower()
        usuario = request.user.usuario
        
        if not termo:
            return Response({"detail": "É necessário fornecer um termo de busca (?q=)"})
        
        tarefas = Tarefa.objects.filter(usuario=usuario).filter(
            Q(titulo_tarefa__icontains=termo) | Q(etiqueta__icontains=termo)
        )
        serializer = TarefaSerializer(tarefas, many=True)
        return Response(serializer.data)
    
class BuscarPorStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status_param = request.query_params.get('status', None)
        usuario = request.user.usuario

        STATUS_VALIDOS = ['Pendente', 'Em Andamento', 'Concluida']

        # Se status for "Todos" (case insensitive) ou não for passado, retorna todas
        if not status_param or status_param.lower() == 'todos':
            tarefas = Tarefa.objects.filter(usuario=usuario)
        else:
            # Verifica se status é válido
            # Ajusta para ignorar case na verificação
            status_formatado = None
            for s in STATUS_VALIDOS:
                if s.lower() == status_param.lower():
                    status_formatado = s
                    break
            if not status_formatado:
                return Response(
                    {"detail": f"Status inválido. Use um dos seguintes: {STATUS_VALIDOS} ou 'Todos'"},
                    status=400
                )
            tarefas = Tarefa.objects.filter(usuario=usuario, status=status_formatado)

        serializer = TarefaSerializer(tarefas, many=True)
        return Response(serializer.data)
    
class FinalizarTarefaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        usuario = request.user.usuario
        tarefa = get_object_or_404(Tarefa, pk=pk, usuario=usuario)
        
        tarefa.status = 'Concluida'
        tarefa.is_finalizada = True
        tarefa.save()
        
        serializer = TarefaSerializer(tarefa)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ExportarTarefasCSVView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user.usuario  # acessa o modelo Usuario
        tarefas = Tarefa.objects.filter(usuario=usuario)

        # Cria a resposta com tipo CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="tarefas.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Título', 'Descrição', 'Status', 'Data de Criação'])  # Cabeçalho

        for tarefa in tarefas:
            writer.writerow([
                tarefa.id,
                tarefa.titulo_tarefa,
                tarefa.descricao,
                tarefa.status,
                tarefa.data_criacao.strftime('%d/%m/%Y %H:%M')
            ])

        return response
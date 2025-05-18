from django.contrib import admin
from django.urls import path, include
from tarefas.api.views import RegistrarUsuarioView, LoginView, BuscaTarefasApiView, BuscarPorStatusView, FinalizarTarefaView, ExportarTarefasCSVView
urlpatterns = [
   path('api/cadastrar/', RegistrarUsuarioView.as_view(), name='cadastrar'),
   path('api/login/', LoginView
        .as_view(), name='login'),
   path("busca-tarefa/", BuscaTarefasApiView.as_view(), name="busca-tarefas"),
   path('tarefas/filtra-status/', BuscarPorStatusView.as_view(), name='buscar-por-status'),
   path('tarefas/<int:pk>/finalizar/', FinalizarTarefaView.as_view(), name='finalizar-tarefa'),
    path('tarefas/exportar-csv/', ExportarTarefasCSVView.as_view(), name='exportar-tarefas-csv'),
]

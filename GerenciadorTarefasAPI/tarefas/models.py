from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.usuario


class Tarefa(models.Model):
    STATUS_CHOICES = (
        ('Pendente', 'Pendente'),
        ('Em Andamento', 'Em Andamento'),
        ('Concluida', 'Concluida'),
    )
    MEDIA_CHOICES = (
        ('Baixa', 'Baixa'),
        ('Media', 'Media'),
        ('Alta', 'Alta'),
    )
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo_tarefa = models.CharField(max_length=100, blank=False, null=False)
    descricao = models.TextField(blank= False, null=False)
    data_criacao = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendente')
    prioridade = models.CharField(max_length=8, choices=MEDIA_CHOICES, default='Baixa')
    categoria = models.CharField(max_length=300, null=True, blank= True)
    etiqueta = models.CharField(max_length=600, null=True, blank=True)
    is_finalizada = models.BooleanField(default=False)
    def __str__(self):
        return self.titulo_tarefa
    
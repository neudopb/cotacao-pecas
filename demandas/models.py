from django.db import models

class Endereco(models.Model):
    id = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=50)
    cidade = models.CharField(max_length=200)
    endereco = models.CharField(max_length=200)
    numero = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.endereco)

    class Meta:
        db_table = 'endereco'

class Contato(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=200)
    telefone = models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(self.email)

    class Meta:
        db_table = 'contato'

class Demanda(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.TextField(max_length=255)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE)
    anunciante = models.ForeignKey('accounts.CustomUsuario', on_delete=models.CASCADE)
    status = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.id)

    class Meta:
        db_table = 'demanda'
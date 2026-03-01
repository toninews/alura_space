from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.galeria.models import Fotografia


class GaleriaViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='senha-forte-123')
        self.other_user = User.objects.create_user(username='bob', password='senha-forte-456')
        self.fotografia = Fotografia.objects.create(
            nome='Nebulosa de Orion',
            legenda='Registro profundo',
            categoria='NEBULOSA',
            descricao='Descricao da foto',
            publicada=True,
            usuario=self.user,
        )

    def test_index_redireciona_usuario_nao_autenticado(self):
        response = self.client.get(reverse('index'))

        self.assertRedirects(response, f"{reverse('login')}?next={reverse('index')}")

    def test_nova_imagem_associa_usuario_logado(self):
        self.client.login(username='alice', password='senha-forte-123')

        response = self.client.post(reverse('nova_imagem'), data={
            'nome': 'Galaxia de Andromeda',
            'legenda': 'Noite limpa',
            'categoria': 'GALÁXIA',
            'descricao': 'Foto de teste',
            'data_fotografia': '2026-02-28',
        })

        self.assertRedirects(response, reverse('index'))
        fotografia = Fotografia.objects.get(nome='Galaxia de Andromeda')
        self.assertEqual(fotografia.usuario, self.user)

    def test_usuario_nao_pode_editar_foto_de_outra_pessoa(self):
        self.client.login(username='bob', password='senha-forte-456')

        response = self.client.post(
            reverse('editar_imagem', args=[self.fotografia.id]),
            data={
                'nome': 'Nome alterado',
                'legenda': self.fotografia.legenda,
                'categoria': self.fotografia.categoria,
                'descricao': self.fotografia.descricao,
                'data_fotografia': '2026-02-28',
                'usuario': self.user.id,
            },
        )

        self.assertRedirects(response, reverse('index'))
        self.fotografia.refresh_from_db()
        self.assertEqual(self.fotografia.nome, 'Nebulosa de Orion')

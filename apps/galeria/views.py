from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.galeria.forms import FotografiaForms
from apps.galeria.models import Fotografia


@login_required
def index(request):
    fotografias = Fotografia.objects.order_by('-data_fotografia').filter(publicada=True)
    return render(
        request,
        'galeria/index.html',
        {"cards": fotografias, "termo_busca": "", "categoria_ativa": ""},
    )


@login_required
def imagem(request, foto_id):
    fotografia = get_object_or_404(Fotografia, pk=foto_id)
    return render(request, 'galeria/imagem.html', {"fotografia": fotografia})


@login_required
def buscar(request):
    fotografias = Fotografia.objects.order_by('-data_fotografia').filter(publicada=True)
    nome_a_buscar = ''

    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar'].strip()
        if nome_a_buscar:
            fotografias = fotografias.filter(nome__icontains=nome_a_buscar)

    return render(
        request,
        'galeria/index.html',
        {"cards": fotografias, "termo_busca": nome_a_buscar, "categoria_ativa": ""},
    )


@login_required
def nova_imagem(request):
    form = FotografiaForms()
    if request.method == 'POST':
        form = FotografiaForms(request.POST, request.FILES)
        if form.is_valid():
            fotografia = form.save(commit=False)
            fotografia.usuario = request.user
            fotografia.save()
            messages.success(request, 'Nova fotografia cadastrada!')
            return redirect('index')

    return render(request, 'galeria/nova_imagem.html', {'form': form})


@login_required
def editar_imagem(request, foto_id):
    fotografia = get_object_or_404(Fotografia, id=foto_id)

    if fotografia.usuario != request.user and not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para editar esta fotografia.')
        return redirect('index')

    form = FotografiaForms(instance=fotografia)

    if request.method == 'POST':
        form = FotografiaForms(request.POST, request.FILES, instance=fotografia)
        if form.is_valid():
            fotografia = form.save(commit=False)
            fotografia.usuario = fotografia.usuario or request.user
            fotografia.save()
            messages.success(request, 'Fotografia editada com sucesso!')
            return redirect('index')

    return render(request, 'galeria/editar_imagem.html', {'form': form, 'foto_id': foto_id})


@login_required
def deletar_imagem(request, foto_id):
    fotografia = get_object_or_404(Fotografia, id=foto_id)

    if fotografia.usuario != request.user and not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para deletar esta fotografia.')
        return redirect('index')

    fotografia.delete()
    messages.success(request, 'Fotografia deletada com sucesso!')
    return redirect('index')


@login_required
def filtro(request, categoria):
    fotografias = Fotografia.objects.order_by('data_fotografia').filter(publicada=True, categoria=categoria)
    return render(
        request,
        'galeria/index.html',
        {"cards": fotografias, "termo_busca": "", "categoria_ativa": categoria},
    )

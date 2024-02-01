from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import TiposExames, PedidoExame, SolicitacaoExame
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants

@login_required
def solicitar_exames(request): 
    tipos_exames = TiposExames.objects.all()
    if request.method == "GET" :
        return render(request, "solicitar_exames.html", {"tipos_exames": tipos_exames})
    elif request.method == "POST":
        exames_id = request.POST.getlist("exames")
        solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)
        
        preco_total = 0
        for i in solicitacao_exames:
            if i.disponivel:
                preco_total += i.preco

        return render(request, "solicitar_exames.html", {"tipos_exames": tipos_exames,
                                                         "solicitacao_exames": solicitacao_exames,
                                                         "preco_total": preco_total})
        
def fechar_pedido(request):
    
    exames_id = request.POST.getlist('exames')
    solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)
    
    pedido_exames = PedidoExame(
        usuario = request.user,
        data =  datetime.now()
    )
    pedido_exames.save()
    
    for exame in solicitacao_exames:
        solicitacao_exames_temp =  SolicitacaoExame(
            usuario=request.user,
            exame=exame,
            status="E" 
        )
        solicitacao_exames_temp.save()
        pedido_exames.exames.add(solicitacao_exames_temp)
    pedido_exames.save()
    messages.add_message(request, constants.SUCCESS, 'Pedido de exame realizado com sucesso')
    return redirect('/exames/gerenciar_pedidos')   

@login_required
def gerenciar_pedidos(request):
    pedidos_exames = PedidoExame.objects.filter(usuario=request.user)
    return render(request, 'gerenciar_pedidos.html', {'pedidos_exames': pedidos_exames})
 
 
def cancelar_pedido(request, id_pedido):
    pedido = PedidoExame.objects.get(id_pedido)
    if not pedido.usuario == request.user:
        messages.add_message(request, constants.ERROR, 'Pedido não encontrado')
        return redirect('exames/gerenciar_pedidos')
    return HttpResponse(id_pedido)
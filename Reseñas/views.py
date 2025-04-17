from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm
from Trueques.models import IntercambioTrueque
from django.contrib import messages

@login_required
def add_review(request, trade_id):
    trade = get_object_or_404(IntercambioTrueque, trueque_1__id=trade_id, estado__in=['Completado', 'Rechazado'])

    # Verifica si ya existe una reseña realizada para este intercambio

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = Review(
                trade=trade,
                estrellas=form.cleaned_data['estrellas'],
                comentario=form.cleaned_data['comentario'],
                user=request.user,
            )
            cant_estrellas = int(form.cleaned_data['estrellas'])
            if request.user != trade.trueque_1.usuario:  # soy el que ofertó el producto
                # le modifico estrellas al del trueque
                trade.trueque_1.usuario.estrellas_totales += cant_estrellas
                trade.trueque_1.usuario.cant_resenias += 1
                trade.trueque_1.usuario.estrellas = trade.trueque_1.usuario.estrellas_totales / trade.trueque_1.usuario.cant_resenias
                review.user_reseniado = trade.trueque_1.usuario
                trade.trueque_1.usuario.save()
            else:  # soy el truequeante
                # modifico estrellas al del producto
                trade.producto_2.usuario.estrellas_totales += cant_estrellas
                trade.producto_2.usuario.cant_resenias += 1
                trade.producto_2.usuario.estrellas = trade.producto_2.usuario.estrellas_totales / trade.producto_2.usuario.cant_resenias
                review.user_reseniado = trade.producto_2.usuario
                trade.producto_2.usuario.save()

            # Guarda la reseña y marca el intercambio como realizado
            review.save()
            trade.realizado = True
            trade.save()

            return redirect('Usuario:show_trueques_usuario')
    else:
        form = ReviewForm()
    
    return render(request, 'add_review.html', {'form': form, 'trade': trade})

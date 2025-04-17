from django.shortcuts import render
import mercadopago
from django.conf import settings
from django.http import JsonResponse

def donar(request):
    if request.method == 'POST':
        monto = request.POST.get('monto')
        if float(monto) >= 1000:
            sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        
            # Crear preferencia de pago
            preference_data = {
                "items": [
                    {
                        "id": "item-ID-1234",
                        "title": "Donación",
                        "currency_id": "BRL",
                        "picture_url": "https://www.mercadopago.com/org-img/MP3/home/logomp3.gif",
                        "description": "Donación a la organización",
                        "category_id": "donation",
                        "quantity": 1,
                        "unit_price": float(monto)
                    }
                ],
                "payer": {
                    "name": "Juan",
                    "surname": "Pérez",
                    "email": "test_user_653756520@testuser.com",
                    "phone": {
                        "area_code": "11",
                        "number": "4444-4444"
                    },
                    "identification": {
                        "type": "DNI",
                        "number": "12345678"
                    },
                    "address": {
                        "street_name": "Calle",
                        "street_number": 123,
                        "zip_code": "1234"
                    }
                },
                "back_urls": {
                    "success": "http://127.0.0.1:8000/",
                    "failure": "http://127.0.0.1:8000/",
                    "pending": "http://127.0.0.1:8000/"
                },
                "auto_return": "approved",
                "notification_url": "https://www.your-site.com/ipn",
                "statement_descriptor": "MI NEGOCIO",
                "external_reference": "Reference_1234",
                "expires": True,
                "expiration_date_from": "2024-06-01T12:00:00.000-04:00",
                "expiration_date_to": "2025-06-30T12:00:00.000-04:00"
            }

            # Crear la preferencia y obtener la respuesta
            preference_response = sdk.preference().create(preference_data)
            preference = preference_response["response"]

            # Responder con JSON
            return JsonResponse({
                'preference_id': preference['id'],
                'public_key': settings.MERCADOPAGO_PUBLIC_KEY,
            })
        else:
            return JsonResponse({'error_monto': True})
    
    # Renderizar la página inicial
    return render(request, 'donar.html')

from django.shortcuts import render
import json
import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Payment
from shop.models import Order
from django.urls import reverse
from django.shortcuts import redirect

# Create your views here.

api_key = settings.PAYSTACK_TEST_SECRET_KEY
url = settings.PAYSTACK_INITIALIZE_PAYMENT_URL


def payment_process(request):

    payment_id = request.session.get('payment_id')
    payment = get_object_or_404(Payment, id=payment_id)

    amount = payment.get_amount() * 100

    if request.method == "POST":
        success_url = request.build_absolute_uri(reverse("payment:success"))
        cancel_url = request.build_absolute_uri(reverse("payment:canceled"))

        metadata = json.dumps({"payment_id": payment_id,
                               "cancel_action": cancel_url})
        
        session_data = {
            'email': payment.email,
            'amount': amount,
            'callback_url': success_url,
            'metadata': metadata
        }

        headers = {"authorization": f"Bearer {api_key}"}

        #Api request to paystack server
        r = requests.post(url, headers=headers, data=session_data)
        response = r.json()
        print(response)
        if response["status"] == True:
            #redirect to paystack payment form
            try:
                redirect_url = response['data']['authorization_url']
                return redirect(redirect_url, code=303)

            except:
                pass

        else:
            return render(request, 'payment/process.html', locals())
    
    else:
        return render(request, 'payment/process.html', locals())


def payment_success(request):

    payment_id = request.session.get('payment_id', None)
    payment = get_object_or_404(Payment, id=payment_id)
    order = payment.order

    ref = request.GET.get('reference', '')

    url = 'https://api.paystack.co/transaction/verify/{}'.format(ref)

    headers = {"authorization": f"Bearer {api_key}"}
    r = requests.get(url, headers=headers)
    res = r.json()
    res = res["data"]

    if res['status'] == 'success':
        payment.paystack_ref = ref
        payment.paid = True
        payment.save()
        
        order.ordered = True
        order.save()

    return render(request, 'payment/success.html', locals())


def payment_canceled(request):

    return render(request, 'payment/canceled.html')
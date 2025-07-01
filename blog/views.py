from django.shortcuts import render
from django.http import JsonResponse
from .models import Blog, Broker
from .forms import ContactForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BrokerageCalculationInputSerializer

# --- Regular views ---
def home(request):
    return render(request, 'index.html')

def blog_page(request):
    return render(request, 'blog.html')

def broker_comparison_page(request):
    return render(request, 'broker_comparison.html')

def blog_detail(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})

# --- API views ---
def blog_list(request):
    blogs = Blog.objects.all().values('id','title', 'content', 'created_at')
    return JsonResponse(list(blogs), safe=False)

def broker_list(request):
    brokers = Broker.objects.all().values('name', 'brokerage_charge', 'hidden_charges', 'features')
    return JsonResponse(list(brokers), safe=False)

# --- AJAX contact form view ---
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Thank you! We will contact you soon.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

@api_view(['POST'])
def calculate_brokerage(request):
    serializer = BrokerageCalculationInputSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        buy = data['buy_price']
        sell = data['sell_price']
        qty = data['quantity']
        broker = data['broker'].lower()
        segment = data['segment'].lower()

        turnover = (buy + sell) * qty

        # Initialize charges
        brokerage = stt = txn_charges = sebi = gst = stamp_duty = ipft = dp_charges = total_charges = 0

        # Helper to round charges
        def r(x): return round(x, 2)

        if broker in ['zerodha', 'upstox', 'angelone', 'groww']:
            if segment == 'delivery':
                brokerage = 0
                stt = r(turnover * 0.001)
                txn_charges = r(turnover * 0.0000297)
                sebi = r(turnover * 0.000001)
                ipft = r(turnover * 0.000001)
                clearing_charge = 0.85
                gst = r((txn_charges + sebi + clearing_charge) * 0.18)
                stamp_duty = r(buy * qty * 0.00015)

                if broker == 'zerodha':
                    dp_charges = 15.34
                elif broker == 'upstox':
                    dp_charges = 20.0
                elif broker == 'angelone':
                    dp_charges = 20.0 + r(0.18 * 20.0)  # INR 20 + GST
                elif broker == 'groww':
                    dp_charges = 3.50 + 16.5  # default for male user

            elif segment == 'intraday':
                rate = 0.0005 if broker == 'groww' else 0.0003
                brokerage = r(min(20, rate * turnover))
                stt = r(sell * qty * 0.00025)
                txn_charges = r(turnover * 0.0000345)
                sebi = r(turnover * 0.000001)
                ipft = r(turnover * 0.000001)
                gst = r((brokerage + txn_charges) * 0.18)
                stamp_duty = r(buy * qty * 0.00003)

            elif segment in ['futures', 'options']:
                rate = 0.0005 if broker == 'groww' else 0.0003
                brokerage = r(min(20, rate * turnover))
                stt_rate = 0.0001 if segment == 'futures' else 0.0005
                txn_rate = 0.000019 if segment == 'futures' else 0.0005
                stamp_rate = 0.00002 if segment == 'futures' else 0.00003
                stt = r(sell * qty * stt_rate)
                txn_charges = r(turnover * txn_rate)
                sebi = r(turnover * 0.000001)
                ipft = r(turnover * 0.000001)
                gst = r((brokerage + txn_charges) * 0.18)
                stamp_duty = r(buy * qty * stamp_rate)

            total_charges = r(brokerage + stt + txn_charges + sebi + gst + stamp_duty + ipft + dp_charges)
        else:
            return Response({'error': 'Unsupported broker'}, status=400)

        net_pnl = round((sell - buy) * qty - total_charges, 2)

        return Response({
            'broker': broker,
            'segment': segment,
            'order_type': data['order_type'],
            'total_charges': total_charges,
            'net_pnl': net_pnl,
            'breakdown': {
                'brokerage': brokerage,
                'stt': stt,
                'txn_charges': txn_charges,
                'sebi': sebi,
                'gst': gst,
                'stamp_duty': stamp_duty,
                'ipft': ipft,
                'dp_charges': dp_charges
            }
        })

    return Response(serializer.errors, status=400)

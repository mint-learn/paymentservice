# 导入必要的模块和库
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from myapp.models import Account, Order, RefundOrder
import uuid
import sys
from datetime import datetime
from django.contrib.auth import login

max_int = sys.maxsize
def uuid_to_int(uuid):
    return int(uuid.replace('-', ''), 16) % max_int


# 注册接口
@csrf_exempt
def register(request):
    # 判断请求方法是否为POST
    if request.method == 'POST':
        # 从请求中获取必要的参数
        name = request.POST.get('Name')
        email = request.POST.get('Email')
        password = request.POST.get('Password')
        # print("get parameters!\n")
        # 判断参数是否存在
        if name and email and password:
            # 生成一个唯一的用户ID
            # account_id =
            account_id = uuid_to_int(str(uuid.uuid4()))
            account = Account(id=account_id, name=name, email=email, password=password, balance=1000)
            account.save()
            # print("saved\n")

            # 返回成功响应，包含新创建的用户信息
            return JsonResponse({'AccountID': account_id, 'Name': name}, status=200)
        else:
            # 返回参数错误响应
            return HttpResponseBadRequest({'error': 'ID and Password are required。'}, status=422)
    else:
        # 返回请求有误响应
        return HttpResponseBadRequest({'error': 'Request Method must be Post。'}, status=400)

# 登录接口
@csrf_exempt
def loginin(request):
    # 判断请求方法是否为POST
    if request.method == 'POST':
        # 从请求中获取必要的参数
        account_id = request.POST.get('ID')
        password = request.POST.get('Password')
        # 判断参数是否存在
        if account_id and password:
            # 在用户数据库中查找指定的用户对象
            user = Account.objects.filter(id=account_id, password=password).first()
            if user:
                # 如果用户存在，验证密码是否匹配
                if user.password == password:
                    # 返回成功响应
                    request.session['id'] = account_id
                    return JsonResponse({'success': 'Success Login'}, status=200)
                else:
                    # 返回参数错误响应
                    return HttpResponseBadRequest({'error': 'Invalid Password'}, status=422)
            else:
                # 返回参数错误响应
                return HttpResponseBadRequest({'error': 'Account Does Not Exist'}, status=422)
        else:
            # 返回参数错误响应
            return HttpResponseBadRequest({'error': 'ID and Password are required。'}, status=422)
    else:
        # 返回请求有误响应
        return HttpResponseBadRequest({'error': 'Request Method must be Post。'}, status=400)


@csrf_exempt
def Login_Failed(request):
    return JsonResponse({'message': 'Please login to the system'}, status=400)



@csrf_exempt
def balance(request):
    if request.method == 'POST':

        if request.session:
            try:
                id = request.session['id']
                account = Account.objects.get(id=id)

                response_data = {
                    'ID': account.id,
                    'Name': account.name,
                    'Balance': account.balance
                }
                return JsonResponse(response_data, status=200)

            except Account.DoesNotExist:
                return JsonResponse({'error': 'Please login'}, status=422)

    return JsonResponse({'error': 'Invalid Request'}, status=400)

@csrf_exempt
def deposit(request):
    if request.method == 'POST':

        if request.session:
            id = request.session['id']
            try:
                account = Account.objects.get(id=id)
            except Account.DoesNotExist:
                return JsonResponse({'message': 'Account not found'}, status=422)
            price = request.POST.get('Price')
            try:
                price = int(price)
            except ValueError:
                return JsonResponse({'message': 'Invalid price'}, status=422)
            account.balance += price
            account.save()
            response = {'ID': account.id, 'Name': account.name, 'Balance': account.balance}
            return JsonResponse(response, status=200)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


@csrf_exempt

def order_request(request):
    # 获取请求参数
    merchant_order_id = request.POST.get("MerchantOrderId")
    price = request.POST.get("Price")
    if request.session:
        id = request.session['id']
        # 查询账户是否存在
        try:
            account = Account.objects.get(id=id)
        except Account.DoesNotExist:
            return JsonResponse({'message': 'Account not found'}, status=422)

        # 在订单表中生成新数据
        stamp = uuid.uuid4().hex
        payment_id = uuid_to_int(str(uuid.uuid4()))
        order = Order.objects.create(
        from_account=None,
        merchant_order_id=merchant_order_id,
        order_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        payment_id=payment_id,
        payment_time=None,
        price=price,
        stamp=stamp,
        to_account=account.id
        )
        # 返回响应
        return JsonResponse({"PaymentId": order.payment_id, "Stamp": stamp}, status=200)
    else:
        return JsonResponse({'error': 'Please login'}, status=422)


@csrf_exempt

def payment_request(request):
    if request.method == 'POST':
        payment_id = request.POST.get('PaymentId')

        if request.session:
            id = request.session['id']
            # 验证账户和密码是否正确
            try:
                account = Account.objects.get(id=id)
            except Account.DoesNotExist:
                return JsonResponse({'message': 'Account not found'}, status=422)

            # 查找订单并更新支付信息
            try:

                order = Order.objects.get(payment_id=payment_id)
                airline_service = Account.objects.get(id=order.to_account)
                if int(account.balance)-int(order.price) > 0 or int(account.balance)-int(order.price)==0:
                    account.balance -= int(order.price)
                    airline_service.balance += int(order.price)
                    account.save()
                    airline_service.save()
                    order.from_account = account.id
                    order.payment_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    order.save()
                    return JsonResponse({'status': 'success', 'Stamp': order.stamp})
                else:
                    return JsonResponse({'message': 'This account does not have enough money to purchase'}, status=422)


            except Order.DoesNotExist:
                return JsonResponse({'message': 'Order not found'}, status=422)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'Service error'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid Request'}, status=400)



@csrf_exempt

def refund(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    # print(str(request.session)+"\n")
    if request.session:
        id = request.session['id']
        # print(id+"\n")
        airline_service = Account.objects.get(id=id)
        try:
            # print("try get payment_id\n")
            payment_id = request.POST.get('PaymentId')
            price = request.POST.get('Price')

        except (json.JSONDecodeError, KeyError):
            # print("except request data\n")
            return JsonResponse({'message': 'Invalid request data'}, status=422)

    else:
        return JsonResponse({'message': 'Please Login'}, status=422)

    try:
        order = Order.objects.get(payment_id=payment_id)
        total_price = order.price
        loss_price = sum([refund.price for refund in RefundOrder.objects.filter(payment_id=payment_id)])
        user_id = order.from_account
        # print("user_id:" + str(user_id) + "\n")
        user = Account.objects.get(id=user_id)
        if int(total_price) - int(loss_price) - int(price) < 0:
            return JsonResponse({'message': 'Insufficient funds for refund'}, status=400)

        refund_id = uuid_to_int(uuid.uuid4().hex)
        RefundOrder.objects.create(refund_id=refund_id, payment_id=payment_id, price=price, refund_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        airline_service.balance -= int(price)
        user.balance += int(price)
        airline_service.save()
        user.save()
        return JsonResponse({'message': 'Successful Refund'}, status=200)

    except Order.DoesNotExist:
        return JsonResponse({'message': 'Order does not exist'}, status=400)
    except Account.DoesNotExist:
        return JsonResponse({'message': 'Account does not exist'}, status=400)

    except Exception:
        return JsonResponse({'message': 'Server Error'}, status=500)



@csrf_exempt

def search(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    else:
        if request.session:
            id = request.session['id']
            pages = int(request.POST.get('pages'))
            entries_per_page = int(request.POST.get('EntriesPerPage'))

        else:
            return JsonResponse({'message': 'Please Login'}, status=422)


        # Search Order table
        orders = Order.objects.filter(from_account=id, to_account=id)

        # Create list of Show objects for orders
        show_list = []
        for order in orders:
            show = {
                "Type": "Order",
                "PaymentId": order.payment_id,
                "Price": order.price,
                "ToAccount": order.to_account,
                "FromAccount": order.from_account,
                "OrderTime": order.order_time.strftime('%Y-%m-%d %H:%M:%S'),
                "PaymentTime": order.payment_time.strftime('%Y-%m-%d %H:%M:%S')
            }

            # Search RefundOrder table for refunds on this payment_id
            refunds = RefundOrder.objects.filter(payment_id=order.payment_id)
            for refund in refunds:
                refund_show = {
                    "Type": "Refund Order",
                    "PaymentId": order.payment_id,
                    "Price": refund.price,
                    "ToAccount": order.to_account,
                    "FromAccount": order.from_account,
                    "OrderTime": refund.refund_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "PaymentTime": refund.refund_time.strftime('%Y-%m-%d %H:%M:%S')
                }
                show_list.append(refund_show)

            show_list.append(show)

        # Sort show_list by PaymentTime (if not None), then by OrderTime
        show_list.sort(key=lambda x: (
        datetime.strptime(x["PaymentTime"], '%Y-%m-%d %H:%M:%S') if x["PaymentTime"] else datetime.min,
        datetime.strptime(x["OrderTime"], '%Y-%m-%d %H:%M:%S')))

        # Paginate show_list
        start_idx = entries_per_page * (pages - 1)
        end_idx = entries_per_page * pages
        paginated_show_list = show_list[start_idx:end_idx]

        # Return JSON response with paginated_show_list
        return JsonResponse(paginated_show_list, status=200, safe=False)




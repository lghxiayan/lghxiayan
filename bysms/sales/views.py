from django.http import HttpResponse

from common.models import Customer  # 连接数据库中的Customer表


def listorders(request):
    return HttpResponse('静态请求！')


def list_customers(request):  # 从数据库中取值
    html_template = '''
    <style>
        table {
            border-collapse:collapse;
        }
        th,td {
            padding:8px;
            text-align:left;
            border-bottom: 1px solid #ddd;
        }
    </style>
    <table>
        <tr>
            <th>id</th>
            <th>name</th>
            <th>phone</th>
            <th>address</th>
            <th>qq</th>
        </tr>
        %s
    </table>
    '''

    qs = Customer.objects.values()  # 从表中取值
    # print(qs)
    '''
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    # 每条表记录都是是一个dict对象，
    # key 是字段名，value 是 字段值
    
    <QuerySet [{'id': 1, 'name': 'xiayan', 'phone_number': '13409790181', 'address': '龙感湖', 'qq': '43444956'}, 
               {'id': 2, 'name': '夏燕2', 'phone_number': '13409790182', 'address': '龙感湖2', 'qq': None}]>
    '''

    ph = request.GET.get('phone_number', None)  # 检查url是否有参数phone_number
    # print(request.GET)
    '''
    当url为这个地址时：http://127.0.0.1:8000/sales/customers/?phone_number=134,135,136
    会返回这个 <QueryDict: {'phone_number': ['134,135,136']}>
    '''
    if ph:
        qs = qs.filter(phone_number=ph)  # 如果请求参数phone_number的值不为空的话，则执行过滤

    table_content = ''
    for customer in qs:
        table_content += '<tr>'
        for name, value in customer.items():
            table_content += f'<td>{value}</td>'
        table_content += '</tr>'
    return HttpResponse(html_template % table_content)

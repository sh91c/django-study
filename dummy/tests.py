import datetime

from django.db.models import F, Sum, Count, Case, When

from dummy.models import OrderLog, Product

# animal = Product.objects.create(name='동물동요', price=8200)
# pack = Product.objects.create(name='사운드북 패키지', price=38400)
# abc = Product.objects.create(name='ABC Activity', price=9900)
#
# animal = Product.objects.filter(name='동물동요', price=8200).first()
# pack = Product.objects.filter(name='사운드북 패키지', price=38400).first()
# abc = Product.objects.filter(name='ABC Activity', price=9900).first()
#
# may1 = datetime.datetime(2017, 4, 1)
# may2 = datetime.datetime(2018, 4, 2)
# may3 = datetime.datetime(2019, 4, 3)
#
#
# OrderLog.objects.create(created=may1, product=abc)
# OrderLog.objects.create(created=may1, product=animal)
# OrderLog.objects.create(created=may1, product=pack)
# OrderLog.objects.create(created=may1, product=abc)
# OrderLog.objects.create(created=may1, product=animal)
# OrderLog.objects.create(created=may1, product=pack)
# OrderLog.objects.create(created=may2, product=pack)
# OrderLog.objects.create(created=may2, product=abc)
# OrderLog.objects.create(created=may2, product=abc)
# OrderLog.objects.create(created=may2, product=animal)
# OrderLog.objects.create(created=may2, product=abc)
# OrderLog.objects.create(created=may2, product=animal)
# OrderLog.objects.create(created=may3, product=animal)
# OrderLog.objects.create(created=may3, product=pack)
# OrderLog.objects.create(created=may3, product=animal)
# OrderLog.objects.create(created=may3, product=abc)


order_qs = OrderLog.objects.annotate(
    name=F('product__name'),
    price=F('product__price')) \
    .values('created', 'name', 'price')

# 전체 쿼리셋에 대한 값을 계산할 때 aggregate 사용
order_qs.aggregate(total_price=Sum('price'))

# 일별 총 매출 확인 시
# values로 날짜를 묶고(기준을 잡음)
# annotate로 구함
daily_list = order_qs.values('created') \
    .annotate(daily_total=Sum('product__price'))

daily_count = order_qs.filter(
    name='ABC Activity') \
    .values('created', 'name') \
    .annotate(count=Count('name'))

order_list_2 = order_qs.annotate(
    sales_price=Case(When(isCancel=False, then=F('price')), default=0),
    cancel_price=Case(When(isCancel=True, then=F('price')), default=0)
)

result = order_list_2.aggregate(
    total_price=Sum('sales_price')-Sum('cancel_price')
)

print(result)
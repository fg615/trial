# _*_ encoding:utf-8 _*_

from __future__ import unicode_literals
from django.db import models
from datetime import datetime

from DjangoUeditor.models import UEditorField

from django.db import models
import uuid


# Create your models here.


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    material_id = models.CharField(max_length=10, null=False, verbose_name=u"原厂商物料号")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    desc = models.CharField(max_length=300, null=True, blank=True, verbose_name=u"描述")
    # detail = UEditorField(verbose_name=u"图文描述", null=True, width=600, height=300, default='')
    detail = models.CharField(max_length=300, null=True, blank=True, verbose_name=u"详细描述")
    type = models.CharField(verbose_name=u"种类",
                            choices=(("tool", "工具"), ("lug", "端子"), ("dies", "模具"), ("other", "其他")), default="other",
                            max_length=10)

    class Meta:
        verbose_name = u"产品"
        verbose_name_plural = verbose_name
        db_table = "product"

    def __str__(self):
        return self.name


class Price(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price_value = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u"价格")
    currency = models.CharField(max_length=10, choices=(("rmb", "人民币"), ("eur", "欧元"), ("usd", "美元")),
                                verbose_name=u"币种")
    # name = models.CharField(max_length=100, verbose_name=u"名称")
    type = models.CharField(verbose_name=u"价格种类", choices=(("list_price", "面价"), ("deal", "成交价"), ("other", "其他")),
                            max_length=20)

    # product = models.ForeignKey(Product, null=True, on_delete=models.DO_NOTHING, verbose_name=u"产品")
    class Meta:
        verbose_name = u"价格"
        verbose_name_plural = verbose_name
        db_table = "price"

    def __str__(self):
        return u"价格"


class ProductHasPrice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, null=True, on_delete=models.DO_NOTHING, verbose_name=u"产品")
    price = models.ForeignKey(Price, null=True, on_delete=models.DO_NOTHING, verbose_name=u"价格")
    comments = models.TextField(blank=True, verbose_name=u"备注")

    class Meta:
        verbose_name = u"产品定价"
        verbose_name_plural = verbose_name
        db_table = "product_price"


class Partner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name=u"名称", max_length=255)
    partner_type = models.CharField(verbose_name=u"伙伴类型", choices=(("vendor", "供应商"), ("customer", "客户")),
                                    default="customer", max_length=10)
    contact = models.CharField(verbose_name=u"联系人", blank=True, null=True, max_length=255)
    email = models.EmailField(verbose_name=u"邮箱", blank=True, null=True)
    phone = models.CharField(verbose_name=u"电话", null=True, blank=True, max_length=32)

    class Meta:
        verbose_name = u"合作伙伴"
        verbose_name_plural = verbose_name
        db_table = "partner"

    def __str__(self):
        return self.name


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    detail = models.TextField(verbose_name=u"地址", blank=True)
    type = models.CharField(verbose_name=u"地址种类", choices=(("delivery", "交货地址"), ("contact", "联系地址"), ("other", "其他")),
                            max_length=10)
    comment = models.TextField(verbose_name=u"备注", blank=True)
    partner = models.ForeignKey(Partner, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=u"合作伙伴")

    class Meta:
        verbose_name = u"地址"
        verbose_name_plural = verbose_name
        db_table = "address"

    def __str__(self):
        return self.partner.name + self.type


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_status = models.CharField(verbose_name=u"是否开票",
                                      choices=(("partial", "部分开票"), ("fully", "全部开票"), ("na", "还未开票")), default="na",
                                      max_length=10)
    order_type = models.CharField(verbose_name=u"订单类型", choices=(("vendor", "供应商订单"), ("customer", "客户订单")),
                                  default="customer", max_length=10)
    payment_term = models.IntegerField(verbose_name=u"付款周期", blank=True, default=60)
    due_date = models.DateField(verbose_name=u"最迟付款日期", blank=True)
    currency = models.CharField(max_length=10, choices=(("rmb", "人民币"), ("eur", "欧元"), ("usd", "美元")), default="rmb",
                                verbose_name=u"币种")
    exchange_rate = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u"汇率", default=1.0)
    pay_date = models.DateField(verbose_name=u"付款日期", null=True, blank=True);
    partner = models.ForeignKey(Partner, null=True, on_delete=models.DO_NOTHING, verbose_name=u"合作伙伴")

    class Meta:
        verbose_name = u"订单"
        verbose_name_plural = verbose_name
        db_table = "order"

    def __str__(self):
        return self.product.name


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_price = models.ForeignKey(ProductHasPrice, null=True, on_delete=models.DO_NOTHING, verbose_name=u"单位价格")
    quantity = models.IntegerField(verbose_name=u"单位数量", default=1)
    sum = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u"总价")
    currency = models.CharField(max_length=10, choices=(("rmb", "人民币"), ("eur", "欧元"), ("usd", "美元")), default="rmb",
                                verbose_name=u"币种")
    exchange_rate = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u"汇率", default=1.0)
    # pay_date = models.DateField(verbose_name=u"付款日期", null=True, blank=True);
    partner = models.ForeignKey(Order, null=True, on_delete=models.DO_NOTHING, verbose_name=u"订单")

    class Meta:
        verbose_name = u"订单"
        verbose_name_plural = verbose_name
        db_table = "order_item"

    def __str__(self):
        return self.product.name


class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_no = models.CharField(max_length=10, verbose_name=u"发票号码")
    invoice_type = models.CharField(verbose_name=u"发票对象", choices=(("vendor", "供应商账单"), ("customer", "客户账单")),
                                  default="customer", max_length=10)
    is_vat = models.BooleanField(verbose_name=u"是否增票", default=True)
    vat_rate=models.IntegerField(verbose_name=u"增票税率", default=16)
    currency = models.CharField(max_length=10, choices=(("rmb", "人民币"), ("eur", "欧元"), ("usd", "美元")), default="rmb",
                                verbose_name=u"币种")
    exchange_rate = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u"汇率", default=1.0)
    sum_in_rmb =  models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u"人民币金额")

    class Meta:
        verbose_name = u"账单"
        verbose_name_plural = verbose_name
        db_table = "invoice"

    def __str__(self):
        return u"发票"+""+self.invoice_no


class OrderInvoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, verbose_name=u"订单")
    invoice = models.ForeignKey(Invoice, on_delete=models.DO_NOTHING, verbose_name=u"发票")
    is_partial_invoice = models.BooleanField(default=False, verbose_name=u"部分发票");
    currency = models.CharField(max_length=10, choices=(("rmb", "人民币"), ("eur", "欧元"), ("usd", "美元")), default="rmb",
                                verbose_name=u"币种")
    exchange_rate = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u"汇率", default=1.0)
    sum_in_rmb =  models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u"人民币金额")

    class Meta:
        verbose_name = u"订单发票"
        verbose_name_plural = verbose_name
        db_table = "order_invoice"

    def __str__(self):
        return  u"订单" +"的" + self.invoice_no
# class Invoice(models.Model):
#    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
"""
    def get_zj_nums(self):
         # 获取课程章节数
            return self.lesson_set.all().count()

    get_zj_nums.short_description = "章节数"

    def go_to(self):
            from django.utils.safestring import mark_safe
            return mark_safe("<a href='http://www.projectsedu.com'>跳转</>")

    go_to.short_description = "跳转"

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
            # 获取课程所有章节
        return self.lesson_set.all()
"""

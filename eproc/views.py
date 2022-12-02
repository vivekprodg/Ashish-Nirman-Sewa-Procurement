import random
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Sum, Q
from procurement.utils import render_to_pdf
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import *
from django.contrib.auth.decorators import user_passes_test
from account.views import check_staff, check_admin
from account.models import UserDetail, OperationPermission, NotificationPermission
from django.urls import resolve
from .decorators import user_access
from account.views import check_staff
from datetime import date, datetime as dt


def user_site(request):
	current_user = request.user.id
	use = UserDetail.objects.filter(user_id=current_user).first()
	u_site = use.site
	return u_site

def user_role(request):
	current_user = request.user.id
	use = UserDetail.objects.filter(user_id=current_user).first()
	u_status = use.status
	return u_status


@user_passes_test(check_staff, login_url='login_user')
def home(request):
	# sites = Site.objects.all()
	# stk = StockItem.objects.all()
	# u_site = user_site(request)
	# current_user = request.user.username
	# for s in stk:
	# 	url = s.url
	# 	name = s.item
	# 	item_id=s.id
	# 	alias = s.alias
	# 	stock_cat = s.stock_category
	# 	subcat = s.stock_subcategory
	# 	caturl = s.cat_url
	# 	subcaturl = s.subcat_url
	# 	uom = s.uom
	# 	stock_type = s.stock_type
	# 	for s in sites:
	# 		s_site = s.name
	# 		qty = 0
	# 		rate = 0
	# 		amt = 0
	# 		if StockEntry.objects.filter(url=url, stock_site=s_site).exists():
	# 			print('no')
	# 		else:
	# 			query = StockEntry(item=name, item_id=item_id, url=url, stock_site=s_site, alias=alias, stock_category=stock_cat, stock_subcategory=subcat, cat_url=caturl, subcat_url=subcaturl, uom=uom, opening=qty, quantity=qty, rate=rate, amount=amt, stock_type=stock_type, entry_by=current_user, user_site=u_site)
	# 			query.save()
	# sites = Site.objects.all()
	# for s in sites:
	# 	name = s.name

	# stk = StockItem.objects.all()
	# for s in stk:
	# 	sid = s.id
	# 	scat = s.stock_category
	# 	surl = s.cat_url
	# 	sscat = s.stock_subcategory
	# 	if StockSubCategory.objects.filter(cat_name=scat, name=sscat).exists():
	# 		sct = StockSubCategory.objects.filter(cat_name=scat, name=sscat).first()
	# 		ssurl = sct.url
	# 		murl = str(surl)+''+str(sct.url)
	# 		StockItem.objects.filter(id=sid).update(subcat_url=ssurl, main_url=murl)

	# 	su = s.name
	# 	su = su.upper()
	# 	dname = su
	# 	UserDetail.objects.filter(site='ekk bhayalatar 3NO PKG/4no pkr').update(site='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	Supplier.objects.filter(user_site='ekk bhayalatar 3NO PKG/4no pkr').update(user_site='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	CreditPay.objects.filter(user_site='ekk bhayalatar 3NO PKG/4no pkr').update(user_site='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	SupplierCategory.objects.filter(user_site='ekk bhayalatar 3NO PKG/4no pkr').update(user_site='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	StockCategory.objects.filter(user_site='ekk bhayalatar 3NO PKG/4no pkr').update(user_site='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	UOM.objects.filter(user_site='ekk bhayalatar 3NO PKG/4no pkr').update(user_site='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	GoodsEntry.objects.filter(user_site='ekk bhayalatar 3NO PKG/4no pkr').update(user_site='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	PurchaseEntry.objects.filter(user_site='ekk bhayalatar 3NO PKG/4no pkr').update(user_site='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	StockEntry.objects.filter(stock_site='ekk bhayalatar 3NO PKG/4no pkr').update(stock_site='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	StockEntry.objects.filter(user_site='ekk bhayalatar 3NO PKG/4no pkr').update(user_site='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	StockItem.objects.filter(user_site='ekk bhayalatar 3NO PKG/4no pkr').update(user_site='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	MaterialIssueEntry.objects.filter(user_site='ekk bhayalatar 3NO PKG/4no pkr').update(user_site='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	MaterialIssueEntry.objects.filter(issuing_location='ekk bhayalatar 3NO PKG/4no pkr').update(issuing_location='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	MaterialIssueEntry.objects.filter(receiving_location='ekk bhayalatar 3NO PKG/4no pkr').update(receiving_location='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	InternalGrn.objects.filter(user_site='ekk bhayalatar 3NO PKG/4no pkr').update(user_site='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	PurchaseOrder.objects.filter(issuing_site='ekk bhayalatar 3NO PKG/4no pkr').update(issuing_site='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	PurchaseOrder.objects.filter(user_site='ekk bhayalatar 3NO PKG/4no pkr').update(user_site='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	PurchaseItem.objects.filter(purchase_location='ekk bhayalatar 3NO PKG/4no pkr').update(purchase_location='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	MaintainanceBill.objects.filter(user_site='ekk bhayalatar 3NO PKG/4no pkr').update(user_site='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	Fuel.objects.filter(user_site='ekk bhayalatar 3NO PKG/4no pkr').update(user_site='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	Reserviour.objects.filter(user_site='ekk bhayalatar 3NO PKG/4no pkr').update(user_site='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	FuelPurchase.objects.filter(issuing_site='ekk bhayalatar 3NO PKG/4no pkr').update(issuing_site='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	FuelPurchase.objects.filter(purchase_location='ekk bhayalatar 3NO PKG/4no pkr').update(purchase_location='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	FuelPurchase.objects.filter(user_site='ekk bhayalatar 3NO PKG/4no pkr').update(user_site='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	FuelBill.objects.filter(issuing_site='ekk bhayalatar 3NO PKG/4no pkr').update(issuing_site='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	FuelBill.objects.filter(purchase_location='ekk bhayalatar 3NO PKG/4no pkr').update(purchase_location='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	FuelBill.objects.filter(user_site='ekk bhayalatar 3NO PKG/4no pkr').update(user_site='Ekk Bhalayatar 3No PKG/4No PKR')
	# 	DamageEntry.objects.filter(user_site='ekk bhayalatar 3NO PKG/4no pkr').update(user_site='Ekk Bhalayatar 3No PKG/4No PKR')

	# 	UserDetail.objects.filter(site='ashish -yogeshwor -ruchi j/v ').update(site='Ashish -Yogeshwor  J/V')
	# 	Supplier.objects.filter(user_site='ashish -yogeshwor -ruchi j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	CreditPay.objects.filter(user_site='ashish -yogeshwor -ruchi j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	SupplierCategory.objects.filter(user_site='ashish -yogeshwor -ruchi j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	StockCategory.objects.filter(user_site='ashish -yogeshwor -ruchi j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	UOM.objects.filter(user_site='ashish -yogeshwor -ruchi j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	GoodsEntry.objects.filter(user_site='ashish -yogeshwor -ruchi j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	PurchaseEntry.objects.filter(user_site='ashish -yogeshwor -ruchi j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	StockEntry.objects.filter(stock_site='ashish -yogeshwor -ruchi j/v ').update(stock_site='Ashish -Yogeshwor  J/V')
	# 	StockEntry.objects.filter(user_site='ashish -yogeshwor -ruchi j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	StockItem.objects.filter(user_site='ashish -yogeshwor -ruchi j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	MaterialIssueEntry.objects.filter(user_site='ashish -yogeshwor -ruchi j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	MaterialIssueEntry.objects.filter(issuing_location='ashish -yogeshwor -ruchi j/v ').update(issuing_location='Ashish -Yogeshwor  J/V')
	# 	MaterialIssueEntry.objects.filter(receiving_location='ashish -yogeshwor -ruchi j/v ').update(receiving_location='Ashish -Yogeshwor  J/V')
	# 	InternalGrn.objects.filter(user_site='ashish -yogeshwor -ruchi j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	PurchaseOrder.objects.filter(issuing_site='ashish -yogeshwor -ruchi j/v ').update(issuing_site='Ashish -Yogeshwor  J/V')
	# 	PurchaseOrder.objects.filter(user_site='ashish -yogeshwor -ruchi j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	PurchaseItem.objects.filter(purchase_location='ashish -yogeshwor -ruchi j/v ').update(purchase_location='Ashish -Yogeshwor  J/V')
	# 	MaintainanceBill.objects.filter(user_site='ashish -yogeshwor -ruchi j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	Fuel.objects.filter(user_site='ashish -yogeshwor -ruchi j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	Reserviour.objects.filter(user_site='ashish -yogeshwor -ruchi j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	FuelPurchase.objects.filter(issuing_site='ashish -yogeshwor -ruchi j/v ').update(issuing_site='Ashish -Yogeshwor  J/V')
	# 	FuelPurchase.objects.filter(purchase_location='ashish -yogeshwor -ruchi j/v ').update(purchase_location='Ashish -Yogeshwor  J/V')
	# 	FuelPurchase.objects.filter(user_site='ashish -yogeshwor -ruchi j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	FuelBill.objects.filter(issuing_site='ashish -yogeshwor -ruchi j/v ').update(issuing_site='Ashish -Yogeshwor  J/V')
	# 	FuelBill.objects.filter(purchase_location='ashish -yogeshwor -ruchi j/v ').update(purchase_location='Ashish -Yogeshwor  J/V')
	# 	FuelBill.objects.filter(user_site='ashish -yogeshwor -ruchi j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	DamageEntry.objects.filter(user_site='ashish -yogeshwor -ruchi j/v ').update(user_site='Ashish -Yogeshwor  J/V')

	# 	UserDetail.objects.filter(site='ashish -yogeshwor  j/v ').update(site='Ashish -Yogeshwor  J/V')
	# 	Supplier.objects.filter(user_site='ashish -yogeshwor  j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	CreditPay.objects.filter(user_site='ashish -yogeshwor  j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	SupplierCategory.objects.filter(user_site='ashish -yogeshwor  j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	StockCategory.objects.filter(user_site='ashish -yogeshwor  j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	UOM.objects.filter(user_site='ashish -yogeshwor  j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	GoodsEntry.objects.filter(user_site='ashish -yogeshwor  j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	PurchaseEntry.objects.filter(user_site='ashish -yogeshwor  j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	StockEntry.objects.filter(stock_site='ashish -yogeshwor  j/v ').update(stock_site='Ashish -Yogeshwor  J/V')
	# 	StockEntry.objects.filter(user_site='ashish -yogeshwor  j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	StockItem.objects.filter(user_site='ashish -yogeshwor  j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	MaterialIssueEntry.objects.filter(user_site='ashish -yogeshwor  j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	MaterialIssueEntry.objects.filter(issuing_location='ashish -yogeshwor  j/v ').update(issuing_location='Ashish -Yogeshwor  J/V')
	# 	MaterialIssueEntry.objects.filter(receiving_location='ashish -yogeshwor  j/v ').update(receiving_location='Ashish -Yogeshwor  J/V')
	# 	InternalGrn.objects.filter(user_site='ashish -yogeshwor  j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	PurchaseOrder.objects.filter(issuing_site='ashish -yogeshwor  j/v ').update(issuing_site='Ashish -Yogeshwor  J/V')
	# 	PurchaseOrder.objects.filter(user_site='ashish -yogeshwor  j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	PurchaseItem.objects.filter(purchase_location='ashish -yogeshwor  j/v ').update(purchase_location='Ashish -Yogeshwor  J/V')
	# 	MaintainanceBill.objects.filter(user_site='ashish -yogeshwor  j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	Fuel.objects.filter(user_site='ashish -yogeshwor  j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	Reserviour.objects.filter(user_site='ashish -yogeshwor  j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	FuelPurchase.objects.filter(issuing_site='ashish -yogeshwor  j/v ').update(issuing_site='Ashish -Yogeshwor  J/V')
	# 	FuelPurchase.objects.filter(purchase_location='ashish -yogeshwor  j/v ').update(purchase_location='Ashish -Yogeshwor  J/V')
	# 	FuelPurchase.objects.filter(user_site='ashish -yogeshwor  j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	FuelBill.objects.filter(issuing_site='ashish -yogeshwor  j/v ').update(issuing_site='Ashish -Yogeshwor  J/V')
	# 	FuelBill.objects.filter(purchase_location='ashish -yogeshwor  j/v ').update(purchase_location='Ashish -Yogeshwor  J/V')
	# 	FuelBill.objects.filter(user_site='ashish -yogeshwor  j/v ').update(user_site='Ashish -Yogeshwor  J/V')
	# 	DamageEntry.objects.filter(user_site='ashish -yogeshwor  j/v ').update(user_site='Ashish -Yogeshwor  J/V')

	# 	sl = s.name
	# 	sl = sl.lower()
	# 	dname = sl
	# 	UserDetail.objects.filter(site=dname).update(site=name)
	# 	Supplier.objects.filter(user_site=dname).update(user_site=name)
	# 	CreditPay.objects.filter(user_site=dname).update(user_site=name)
	# 	SupplierCategory.objects.filter(user_site=dname).update(user_site=name)
	# 	StockCategory.objects.filter(user_site=dname).update(user_site=name)
	# 	UOM.objects.filter(user_site=dname).update(user_site=name)
	# 	GoodsEntry.objects.filter(user_site=dname).update(user_site=name)
	# 	PurchaseEntry.objects.filter(user_site=dname).update(user_site=name)
	# 	StockEntry.objects.filter(stock_site=dname).update(stock_site=name)
	# 	StockEntry.objects.filter(user_site=dname).update(user_site=name)
	# 	StockItem.objects.filter(user_site=dname).update(user_site=name)
	# 	MaterialIssueEntry.objects.filter(user_site=dname).update(user_site=name)
	# 	MaterialIssueEntry.objects.filter(issuing_location=dname).update(issuing_location=name)
	# 	MaterialIssueEntry.objects.filter(receiving_location=dname).update(receiving_location=name)
	# 	InternalGrn.objects.filter(user_site=dname).update(user_site=name)
	# 	PurchaseOrder.objects.filter(issuing_site=dname).update(issuing_site=name)
	# 	PurchaseOrder.objects.filter(user_site=dname).update(user_site=name)
	# 	PurchaseItem.objects.filter(purchase_location=dname).update(purchase_location=name)
	# 	MaintainanceBill.objects.filter(user_site=dname).update(user_site=name)
	# 	Fuel.objects.filter(user_site=dname).update(user_site=name)
	# 	Reserviour.objects.filter(user_site=dname).update(user_site=name)
	# 	FuelPurchase.objects.filter(issuing_site=dname).update(issuing_site=name)
	# 	FuelPurchase.objects.filter(purchase_location=dname).update(purchase_location=name)
	# 	FuelPurchase.objects.filter(user_site=dname).update(user_site=name)
	# 	FuelBill.objects.filter(issuing_site=dname).update(issuing_site=name)
	# 	FuelBill.objects.filter(purchase_location=dname).update(purchase_location=name)
	# 	FuelBill.objects.filter(user_site=dname).update(user_site=name)
	# 	DamageEntry.objects.filter(user_site=dname).update(user_site=name)

	# 	st = s.name
	# 	st = st.title()
	# 	dname = st
	# 	UserDetail.objects.filter(site=dname).update(site=name)
	# 	Supplier.objects.filter(user_site=dname).update(user_site=name)
	# 	CreditPay.objects.filter(user_site=dname).update(user_site=name)
	# 	SupplierCategory.objects.filter(user_site=dname).update(user_site=name)
	# 	StockCategory.objects.filter(user_site=dname).update(user_site=name)
	# 	UOM.objects.filter(user_site=dname).update(user_site=name)
	# 	GoodsEntry.objects.filter(user_site=dname).update(user_site=name)
	# 	PurchaseEntry.objects.filter(user_site=dname).update(user_site=name)
	# 	StockEntry.objects.filter(stock_site=dname).update(stock_site=name)
	# 	StockEntry.objects.filter(user_site=dname).update(user_site=name)
	# 	StockItem.objects.filter(user_site=dname).update(user_site=name)
	# 	MaterialIssueEntry.objects.filter(user_site=dname).update(user_site=name)
	# 	MaterialIssueEntry.objects.filter(issuing_location=dname).update(issuing_location=name)
	# 	MaterialIssueEntry.objects.filter(receiving_location=dname).update(receiving_location=name)
	# 	InternalGrn.objects.filter(user_site=dname).update(user_site=name)
	# 	PurchaseOrder.objects.filter(issuing_site=dname).update(issuing_site=name)
	# 	PurchaseOrder.objects.filter(user_site=dname).update(user_site=name)
	# 	PurchaseItem.objects.filter(purchase_location=dname).update(purchase_location=name)
	# 	MaintainanceBill.objects.filter(user_site=dname).update(user_site=name)
	# 	Fuel.objects.filter(user_site=dname).update(user_site=name)
	# 	Reserviour.objects.filter(user_site=dname).update(user_site=name)
	# 	FuelPurchase.objects.filter(issuing_site=dname).update(issuing_site=name)
	# 	FuelPurchase.objects.filter(purchase_location=dname).update(purchase_location=name)
	# 	FuelPurchase.objects.filter(user_site=dname).update(user_site=name)
	# 	FuelBill.objects.filter(issuing_site=dname).update(issuing_site=name)
	# 	FuelBill.objects.filter(purchase_location=dname).update(purchase_location=name)
	# 	FuelBill.objects.filter(user_site=dname).update(user_site=name)
	# 	DamageEntry.objects.filter(user_site=dname).update(user_site=name)
	tod = date.today()
	if PurchaseEntry.objects.filter(grn_status='no').exists():
		pe = PurchaseEntry.objects.filter(grn_status='no')
		for p in pe:
			pid = p.id
			pvn = p.voucher_number
			po = p.purchase_order_number
			edate = p.date
			dtt = tod - edate
			dtt = dtt.days
			if dtt > 14:

				notify_topic = 'grn_notify'
				content_id = pid
				content = 'gnoti_add'
				content_val = pvn
				content_val1 = po
				if Notification.objects.filter(content='gnoti_add', content_val=pvn).exists():
					pass
				else:
					q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, content_val=content_val, content_val1=content_val1)
					q.save()
	if PurchaseEntry.objects.filter(transaction_type='credit').exists():
		pe = PurchaseEntry.objects.filter(transaction_type='credit')
		for p in pe:
			pid = p.id
			pvn = p.voucher_number
			po = p.purchase_order_number
			cre = p.day
			edate = p.date
			dtt = tod - edate
			dy = int(cre) - 5
			if dtt.days > dy or dtt.days == dy:

				notify_topic = 'credit_notify'
				content_id = pid
				content = 'crnoti_add'
				content_val = pvn
				content_val1 = po

				if Notification.objects.filter(content='crnoti_add', content_val=pvn).exists():
					pass
				else:
					q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, content_val=content_val, content_val1=content_val1)
					q.save()

	# ve = VehicleList.objects.all()
	# for v in ve:
	# 	vnum = v.vehicle_number
	# 	cnum = v.chasis_number
	# 	enum = v.engine_number
	# 	vehicle_type_name = v.vehicle_type
	# 	vehicle_type = v.vehicle_type_id

	# 	if PurchaseOrder.objects.filter(vehicle_number=vnum).exists():
	# 		PurchaseOrder.objects.filter(vehicle_number=vnum).update(vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)
	# 	if MaintainanceBill.objects.filter(vehicle_number=vnum).exists():
	# 		MaintainanceBill.objects.filter(vehicle_number=vnum).update(vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)
	# 	if Fuel.objects.filter(vehicle_number=vnum).exists():
	# 		Fuel.objects.filter(vehicle_number=vnum).update(vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)
	# 	if VehicleTrack.objects.filter(vehicle_number=vnum).exists():
	# 		VehicleTrack.objects.filter(vehicle_number=vnum).update(vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)

	# 	if PurchaseOrder.objects.filter(vehicle_number=cnum).exists():
	# 		PurchaseOrder.objects.filter(vehicle_number=cnum).update(vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)
	# 	if MaintainanceBill.objects.filter(vehicle_number=cnum).exists():
	# 		MaintainanceBill.objects.filter(vehicle_number=cnum).update(vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)
	# 	if Fuel.objects.filter(vehicle_number=cnum).exists():
	# 		Fuel.objects.filter(vehicle_number=cnum).update(vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)
	# 	if VehicleTrack.objects.filter(vehicle_number=cnum).exists():
	# 		VehicleTrack.objects.filter(vehicle_number=cnum).update(vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)

	# 	if PurchaseOrder.objects.filter(vehicle_number=enum).exists():
	# 		PurchaseOrder.objects.filter(vehicle_number=enum).update(vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)
	# 	if MaintainanceBill.objects.filter(vehicle_number=enum).exists():
	# 		MaintainanceBill.objects.filter(vehicle_number=enum).update(vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)
	# 	if Fuel.objects.filter(vehicle_number=enum).exists():
	# 		Fuel.objects.filter(vehicle_number=enum).update(vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)
	# 	if VehicleTrack.objects.filter(vehicle_number=enum).exists():
	# 		VehicleTrack.objects.filter(vehicle_number=enum).update(vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)


	context = {}    
	return render(request, 'index.html', context)


@user_passes_test(check_staff, login_url='login_user')
def predefined(request):
	scount = Supplier.objects.all().count()
	lcount = Location.objects.all().count()
	vcount = UOM.objects.all().count()
	sitecount = Site.objects.all().count()
	context = {'scount': scount, 'sitecount': sitecount, 'lcount':lcount, 'vcount': vcount}    
	return render(request, 'predefine.html', context)


@user_access
def manage_supplier(request):
	category_dash = SupplierCategory.objects.all()
	scount = Supplier.objects.all().count()
	lcount = Location.objects.all().count()
	vcount = UOM.objects.all().count()
	sitecount = Site.objects.all().count()
	context = {'category_dash': category_dash, 'sitecount': sitecount, 'scount': scount, 'lcount':lcount, 'vcount': vcount}    
	return render(request, 'supplier.html', context)


@user_access
def display_supplier(request):
	supplier_dash = Supplier.objects.all().order_by('-id')
	category_dash = SupplierCategory.objects.all()
	context = {'supplier_dash': supplier_dash, 'category_dash': category_dash}    
	return render(request, 'display/supplier_detail.html', context)


@user_access
def add_supplier(request):
	if request.method=="POST":
		current_user = request.user.username
		name = request.POST.get('name')
		address = request.POST.get('address')
		pan = request.POST.get('pan')
		landline = request.POST.get('landline')
		category = request.POST.get('category')
		person1 = request.POST.get('person1')
		person1email = request.POST.get('person1email')
		person1contact = request.POST.get('person1contact')
		person2 = request.POST.get('person2')
		person2email = request.POST.get('person2email')
		person2contact = request.POST.get('person2contact')
		opening = request.POST.get('opening')
		u_site = user_site(request)

		if Supplier.objects.filter(name=name, address=address, pan_number=pan, landline=landline, suppliers_category=category).exists():
			messages.info(request, 'error')
			return redirect('manage_supplier')
		else:
			query = Supplier(name=name, address=address, pan_number=pan, landline=landline, opening=opening, suppliers_category=category, person_one=person1, person_one_mobile=person1contact, person_one_email=person1email, person_two=person2, person_two_mobile=person2contact, person_two_email=person2email, user_site=u_site, entry_by=current_user)
			query.save()
			messages.info(request, 'done')
			return redirect('manage_supplier')
	else:
		return redirect('manage_supplier')


@user_access
def edit_supplier(request):
	if request.method=="POST":
		sid = request.POST.get('suid')
		name = request.POST.get('name')
		address = request.POST.get('address')
		pan = request.POST.get('pan')
		landline = request.POST.get('landline')
		category = request.POST.get('category')
		person1 = request.POST.get('person1')
		person1email = request.POST.get('person1email')
		person1contact = request.POST.get('person1contact')
		person2 = request.POST.get('person2')
		person2email = request.POST.get('person2email')
		person2contact = request.POST.get('person2contact')
		opening = request.POST.get('opening')

		if Supplier.objects.filter(name=name, address=address, pan_number=pan, landline=landline, suppliers_category=category).exclude(id=sid).exists():
			messages.info(request, 'error')
			return redirect('display_supplier')
		else:
			Supplier.objects.filter(id=sid).update(name=name, address=address, pan_number=pan, landline=landline, opening=opening, suppliers_category=category, person_one=person1, person_one_mobile=person1contact, person_one_email=person1email, person_two=person2, person_two_mobile=person2contact, person_two_email=person2email)
			messages.info(request, 'done')
			return redirect('display_supplier')
	else:
		return redirect('display_supplier')


@user_access
def delete_supplier(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		Supplier.objects.filter(id=sid).delete()
		messages.info(request, 'done')
		return redirect('display_supplier')
	else:
		return redirect('display_supplier')


@user_access
def view_credit(request, sid):
	if Supplier.objects.filter(id=sid).exists():
		record = []
		remain = 0
		rec = 0
		sup = Supplier.objects.filter(id=sid).first()
		opening = sup.opening
		name = sup.name
		total_credit = opening
		remain = opening
		if PurchaseEntry.objects.filter(supplier_id=sid, transaction_type='credit').exists():
			cre = PurchaseEntry.objects.filter(supplier_id=sid, transaction_type='credit').aggregate(Sum('total'))
			credit = cre['total__sum']
			total_credit = float(credit)+float(opening)
			remain = total_credit
			if FuelBill.objects.filter(supplier_id=sid, transaction_type='credit').exists():
				cre = FuelBill.objects.filter(supplier_id=sid, transaction_type='credit').aggregate(Sum('amount'))
				credit = cre['amount__sum']
				total_credit = float(credit)+float(total_credit)
				remain = total_credit
			if CreditPay.objects.filter(supplier_id=sid).exists():
				recc = CreditPay.objects.filter(supplier_id=sid).aggregate(Sum('amount'))
				rec = recc['amount__sum']
				remain = float(total_credit) - float(rec)
				record = CreditPay.objects.filter(supplier_id=sid)
		elif FuelBill.objects.filter(supplier_id=sid, transaction_type='credit').exists():
			cre = FuelBill.objects.filter(supplier_id=sid, transaction_type='credit').aggregate(Sum('amount'))
			credit = cre['amount__sum']
			total_credit = float(credit)+float(opening)
			remain = total_credit
			if CreditPay.objects.filter(supplier_id=sid).exists():
				recc = CreditPay.objects.filter(supplier_id=sid).aggregate(Sum('amount'))
				rec = recc['amount__sum']
				remain = float(total_credit) - float(rec)
				record = CreditPay.objects.filter(supplier_id=sid)
		else:
			if CreditPay.objects.filter(supplier_id=sid).exists():
				recc = CreditPay.objects.filter(supplier_id=sid).aggregate(Sum('amount'))
				rec = recc['amount__sum']
				remain = float(total_credit) - float(rec)
				record = CreditPay.objects.filter(supplier_id=sid)

		context = {'sid': sid, 'rec': rec, 'name': name, 'record': record, 'opening': opening, 'total_credit': total_credit, 'remain': remain}    
		return render(request, 'display/credit_pay.html', context)
	else:
		return redirect('display_supplier')


@user_access
def pay_credit(request):
	if request.method=="POST":
		current_user = request.user.username
		u_site = user_site(request)
		sid = request.POST.get('supid')
		premain = request.POST.get('remain')
		date = request.POST.get('date')
		amount = request.POST.get('amount')
		trans = request.POST.get('trans')
		if trans == 'cheque':
			bank = request.POST.get('bank')
		else:
			bank = ''
		sup = Supplier.objects.filter(id=sid).first()
		sup_name = sup.name
		sup_address = sup.address
		sup_contact = sup.landline
		if float(premain) == 0:
			messages.info(request, 'error')
			return redirect('/credit-detail/'+str(sid)+'/')
		else:
			if float(amount) > float(premain):
				messages.info(request, 'error')
				return redirect('/credit-detail/'+str(sid)+'/')
			else:
				remain = float(premain)-float(amount)
				query = CreditPay(entry_date=date, supplier_id=sid, supplier_name=sup_name, supplier_contact=sup_contact, supplier_address=sup_address, amount=amount, remaining=remain, pay_method=trans, bank=bank, entry_by=current_user, user_site=u_site)
				query.save()
				messages.info(request, 'done')
				return redirect('/credit-detail/'+str(sid)+'/')
	else:
		return redirect('display_supplier')


@user_access
def print_credit(request):
	if request.method=="POST":
		sid = request.POST.get('jid')
		s_good = Supplier.objects.filter(id=sid).first()
		record = []
		remain = 0
		rec = 0
		sup = Supplier.objects.filter(id=sid).first()
		opening = sup.opening
		total_credit = opening
		remain = opening
		if PurchaseEntry.objects.filter(supplier_id=sid, transaction_type='credit').exists():
			cre = PurchaseEntry.objects.filter(supplier_id=sid, transaction_type='credit').aggregate(Sum('total'))
			credit = cre['total__sum']
			total_credit = float(credit)+float(opening)
			remain = total_credit
			if CreditPay.objects.filter(supplier_id=sid).exists():
				recc = CreditPay.objects.filter(supplier_id=sid).aggregate(Sum('amount'))
				rec = recc['amount__sum']
				remain = float(total_credit) - float(rec)
				record = CreditPay.objects.filter(supplier_id=sid)
		else:
			if CreditPay.objects.filter(supplier_id=sid).exists():
				recc = CreditPay.objects.filter(supplier_id=sid).aggregate(Sum('amount'))
				rec = recc['amount__sum']
				remain = float(total_credit) - float(rec)
				record = CreditPay.objects.filter(supplier_id=sid)

		context = {'a': s_good, 'rec': rec, 'record': record, 'opening': opening, 'total_credit': total_credit, 'remain': remain}
		pdf = render_to_pdf('printcredit.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			rnum = random.randint(11111111, 99999999)
			filename = "Reportcredit_%s.pdf" %(rnum)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")
	else:
		return redirect('login_user')


@user_access
def manage_location(request):
	location_dash = Location.objects.all().order_by('-id')
	context = {'location_dash': location_dash}    
	return render(request, 'location.html', context)


@user_access
def add_location(request):
	if request.method=="POST":
		current_user = request.user.username
		name = request.POST.get('name')
		url = request.POST.get('url')
		u_site = user_site(request)

		if Location.objects.filter(location_url=url).exists():
			messages.info(request, 'error')
			return redirect('manage_location')
		else:
			query = Location(location_name=name, location_url=url, user_site=u_site, entry_by=current_user)
			query.save()
			messages.info(request, 'done')
			return redirect('manage_location')
	else:
		return redirect('manage_location')


@user_access
def edit_location(request):
	if request.method=="POST":
		lid = request.POST.get('lid')
		default_name = request.POST.get('default_name')
		name = request.POST.get('name')
		url = request.POST.get('url')

		if Location.objects.filter(location_url=url).exclude(id=lid).exists():
			messages.info(request, 'error')
			return redirect('manage_location')
		else:
			query = Location.objects.filter(id=lid).update(location_name=name, location_url=url)
			messages.info(request, 'done')
			return redirect('manage_location')
	else:
		return redirect('manage_location')


@user_access
def delete_location(request):
	if request.method=="POST":
		lid = request.POST.get('lid')

		Location.objects.filter(id=lid).delete()
		messages.info(request, 'done')
		return redirect('manage_location')
	else:
		return redirect('manage_location')


@user_access
def manage_vehicle(request):
	vehicle_dash = Vehicle.objects.all().order_by('-id')
	context = {'vehicle_dash': vehicle_dash}    
	return render(request, 'vehicle.html', context)


@user_access
def add_vehicle(request):
	if request.method=="POST":
		name = request.POST.get('name')
		current_user = request.user.username

		if Vehicle.objects.filter(vehicle_number=name, entry_by=current_user).exists():
			messages.info(request, 'error')
			return redirect('manage_vehicle')
		else:
			query = Vehicle(vehicle_number=name)
			query.save()
			messages.info(request, 'done')
			return redirect('manage_vehicle')
	else:
		return redirect('manage_vehicle')


@user_access
def edit_vehicle(request):
	if request.method=="POST":
		lid = request.POST.get('lid')
		default_name = request.POST.get('default_name')
		name = request.POST.get('name')

		if Vehicle.objects.filter(vehicle_number=name).exclude(id=lid).exists():
			messages.info(request, 'error')
			return redirect('manage_vehicle')
		else:
			query = Vehicle.objects.filter(id=lid).update(vehicle_number=name)
			messages.info(request, 'done')
			return redirect('manage_vehicle')
	else:
		return redirect('manage_vehicle')


@user_access
def delete_vehicle(request):
	if request.method=="POST":
		lid = request.POST.get('lid')

		Vehicle.objects.filter(id=lid).delete()
		messages.info(request, 'done')
		return redirect('manage_vehicle')
	else:
		return redirect('manage_vehicle')


@user_access
def manage_supplier_category(request):
	category_dash = SupplierCategory.objects.all().order_by('-id')
	context = {'category_dash': category_dash}    
	return render(request, 'supplier_category.html', context)


@user_access
def add_supplier_category(request):
	if request.method=="POST":
		current_user = request.user.username
		name = request.POST.get('name')
		url = request.POST.get('url')
		user_s = user_site(request)

		if SupplierCategory.objects.filter(url=url).exists():
			messages.info(request, 'error')
			return redirect('manage_supplier_category')
		else:
			query = SupplierCategory(name=name, url=url, entry_by=current_user, user_site=user_s)
			query.save()
			messages.info(request, 'done')
			return redirect('manage_supplier_category')
	else:
		return redirect('manage_supplier_category')


@user_access
def edit_supplier_category(request):
	if request.method=="POST":
		lid = request.POST.get('lid')
		default_name = request.POST.get('default_name')
		name = request.POST.get('name')
		url = request.POST.get('url')

		if SupplierCategory.objects.filter(url=url).exclude(id=lid).exists():
			messages.info(request, 'error')
			return redirect('manage_supplier_category')
		else:
			query = SupplierCategory.objects.filter(id=lid).update(name=name, url=url)
			messages.info(request, 'done')
			return redirect('manage_supplier_category')
	else:
		return redirect('manage_supplier_category')


@user_access
def delete_supplier_category(request):
	if request.method=="POST":
		lid = request.POST.get('lid')

		SupplierCategory.objects.filter(id=lid).delete()
		messages.info(request, 'done')
		return redirect('manage_supplier_category')
	else:
		return redirect('manage_supplier_category')


@user_access
def manage_uom(request):
	uom_dash = UOM.objects.all().order_by('-id')
	context = {'uom_dash': uom_dash}    
	return render(request, 'uom.html', context)


@user_access
def add_uom(request):
	if request.method=="POST":
		name = request.POST.get('name')
		current_user = request.user.username
		u_site = user_site(request)

		if UOM.objects.filter(uom=name).exists():
			messages.info(request, 'error')
			return redirect('manage_uom')
		else:
			query = UOM(uom=name, entry_by=current_user, user_site=u_site)
			query.save()
			messages.info(request, 'done')
			return redirect('manage_uom')
	else:
		return redirect('manage_uom')


@user_access
def edit_uom(request):
	if request.method=="POST":
		lid = request.POST.get('lid')
		default_name = request.POST.get('default_name')
		name = request.POST.get('name')

		if UOM.objects.filter(uom=name).exclude(id=lid).exists():
			messages.info(request, 'error')
			return redirect('manage_uom')
		else:
			query = UOM.objects.filter(id=lid).update(uom=name)
			messages.info(request, 'done')
			return redirect('manage_uom')
	else:
		return redirect('manage_uom')


@user_access
def delete_uom(request):
	if request.method=="POST":
		lid = request.POST.get('lid')

		UOM.objects.filter(id=lid).delete()
		messages.info(request, 'done')
		return redirect('manage_uom')
	else:
		return redirect('manage_uom')


@user_passes_test(check_staff, login_url='login_user')
def purchase(request):
	goo = GoodsEntry.objects.all().count()
	invoi = PurchaseEntry.objects.all().count()
	pur = PurchaseOrder.objects.all().count()
	dm = DamageEntry.objects.all().count()
	rm = ReturnEntry.objects.all().count()
	context = {'goo': goo, 'invoi': invoi, 'pur': pur, 'dm': dm, 'rm': rm}    
	return render(request, 'purchase.html', context)


#--ashish begins---------------------------------------

@user_access
def ashish_goods_entry(request):
	supplier_dash = Supplier.objects.all()
	location_dash = Location.objects.all()
	vehicle_dash = Vehicle.objects.all()
	porder = PurchaseOrder.objects.filter(status='approved')
	uom_dash = UOM.objects.all()
	u_site = user_site(request)
	item_dash = StockItem.objects.all()
	grn = 0
	if GoodsEntry.objects.last():
		good = GoodsEntry.objects.last()
		ng = good.grn_count
		grn = int(ng) + 1
	else:
		grn = grn + 1

	gchallan = []
	tran = GoodsEntry.objects.values('challan_number')
	trans = {item['challan_number'] for item in tran}
	for s in trans:
		gchallan.append(s)

	gbill = []
	tran = GoodsEntry.objects.values('bill_number')
	trans = {item['bill_number'] for item in tran}
	for s in trans:
		gbill.append(s)

	igoods = []
	seen = set()
	seen_add = seen.add
	tran = InvoiceItem.objects.values_list('purchaseid', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for s in ent:
		igood = InvoiceItem.objects.filter(purchaseid=s, grn_status='no', issue_use='no').exclude(Q(damage='all') | Q(retur='all'))
		n = len(igood)
		igoods.append([igood, range(1,n)])

	purinvoice = []
	seen = set()
	seen_add = seen.add
	tran = PurchaseEntry.objects.values_list('purchase_order_number', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for s in ent:
		pur = PurchaseEntry.objects.filter(purchase_order_number=s)
		n = len(igood)
		purinvoice.append([pur, range(1,n)])

	context = {'porder':porder, 'purinvoice': purinvoice, 'supplier_dash': supplier_dash, 'igoods': igoods, 'location_dash': location_dash, 'vehicle_dash': vehicle_dash, 'uom_dash': uom_dash, 'item_dash': item_dash, 'grn': grn, 'gchallan': gchallan, 'gbill': gbill}    
	return render(request, 'ashish_goods_entry.html', context)


@user_access
def ashish_goods_display(request):
	u_site = user_site(request)
	u_status = user_role(request)
	s_item = []
	if u_status == 'main_admin' or u_status == 'main_staff':
		s_it = GoodsEntry.objects.all().order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_it, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_item.append([product, range(1, n)])
	else:
		s_it = GoodsEntry.objects.filter(user_site=u_site).order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_it, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_item.append([product, range(1, n)])
	context = {'s_item': s_item}    
	return render(request, 'display/ashish_goods_display.html', context)


@user_access
def ashish_goods_detail(request,gid):
	if GoodsEntry.objects.filter(id=gid).exists():
		item = GoodsEntry.objects.filter(id=gid).first()
		s_goods = Goods.objects.filter(goodsid=gid)
		iextra = GoodsExtra.objects.filter(goodsid=gid)
		context = {'item': item, 's_goods': s_goods, 'iextra': iextra}    
		return render(request, 'display/ashish_goods_detail.html', context)
	else:
		return redirect('ashish_goods_display')


@user_access
def ashish_search_goods(request):
	if request.method == "POST":
		search = request.POST.get('search')
		sea = search.upper()
		se = search.title()
		s = search.lower()
		u_site = user_site(request)
		u_status = user_role(request)
		if u_status == 'main_admin' or u_status == 'main_staff':
			lookup = Q(grn_number=search) | Q(challan_number=search) | Q(bill_number=search) | Q(supplier_name__icontains=search) | Q(vehicle_number__icontains=search) | Q(user_site__icontains=search) | Q(grn_number=sea) | Q(challan_number=sea) | Q(bill_number=sea) | Q(supplier_name=sea) | Q(vehicle_number=sea) | Q(user_site=sea) | Q(grn_number=se) | Q(challan_number=se) | Q(bill_number=se) | Q(supplier_name=se) | Q(vehicle_number=se) | Q(user_site=se) | Q(grn_number=s) | Q(challan_number=s) | Q(bill_number=s) | Q(supplier_name=s) | Q(vehicle_number=s) | Q(user_site=s)
		else:
			lookup = Q(Q(grn_number=search) | Q(challan_number=search) | Q(bill_number=search) | Q(supplier_name__icontains=search) | Q(vehicle_number__icontains=search) | Q(grn_number=sea) | Q(challan_number=sea) | Q(bill_number=sea) | Q(supplier_name=sea) | Q(vehicle_number=sea) | Q(grn_number=se) | Q(challan_number=se) | Q(bill_number=se) | Q(supplier_name=se) | Q(vehicle_number=se) | Q(grn_number=s) | Q(challan_number=s) | Q(bill_number=s) | Q(supplier_name=s) | Q(vehicle_number=s)) & Q(user_site=u_site)
		s_goods = []
		s_goo = GoodsEntry.objects.filter(lookup).order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_goo, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_goods.append([product, range(1, n)])
		context = {'s_goods': s_goods, 'search': search}
		return render(request, 'display/ashish_goods_search.html', context)
	else:
		return redirect('ashish_goods_display')


@user_access
def ashish_print_goods(request):
	if request.method=="POST":
		jid = request.POST.get('jid')
		s_good = GoodsEntry.objects.filter(id=jid).first()
		igoods = Goods.objects.filter(goodsid=jid)
		iextra = GoodsExtra.objects.filter(goodsid=jid)

		context = {'a': s_good, 'igoods': igoods, 'iextra': iextra}
		pdf = render_to_pdf('ashish_printgoods.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			rnum = random.randint(11111111, 99999999)
			filename = "Reportgoods_%s.pdf" %(rnum)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")
	else:
		return redirect('login_user')


@user_access
def ashish_delete_goods(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		ge = GoodsEntry.objects.filter(id=sid).first()
		u_site = ge.user_site
		porder = ge.purchase_order_number
		gq = Goods.objects.filter(goodsid=sid)
		for a in gq:
			itemid = a.item_id
			qty = a.quantity
			pvn = a.pvn
			sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
			qt = float(sq.quantity)
			if qt > float(qty) or qt == float(qty):
				newqty = qt - float(qty)
			if qt < float(qty):
				newqty = float(qty) - qt
			StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)
			PurchaseEntry.objects.filter(voucher_number=pvn).update(grn_id='', grn_status='no')
			InvoiceItem.objects.filter(pvn=pvn).update(grn_id='', grn_status='no')
		# PurchaseOrder.objects.filter(purchase_number=porder).update(grn_id='', grn_status='no')

		GoodsEntry.objects.filter(id=sid).delete()
		Goods.objects.filter(goodsid=sid).delete()
		GoodsExtra.objects.filter(goodsid=sid).delete()
		messages.info(request, 'done')
		return redirect('ashish_goods_display')
	else:
		return redirect('ashish_goods_display')


@user_access
def ashish_goods_edit(request, gid):
	if GoodsEntry.objects.filter(id=gid).exists():
		item = GoodsEntry.objects.filter(id=gid).first()
		cn = item.challan_number
		bn = item.bill_number
		porder = PurchaseOrder.objects.filter(status='approved')
		seen = set()
		seen_add = seen.add
		tran = Goods.objects.values_list('pvn', flat=True).distinct()
		ent = [x for x in tran if not (x in seen or seen_add(x))]
		inv_count = []
		a = 0
		for b in ent:
			que = Goods.objects.filter(pvn=b, goodsid=gid)
			for i in que:
				pvn = i.pvn
				a = a+1
				inv_count.append(pvn)

		supplier_dash = Supplier.objects.all()
		location_dash = Location.objects.all()
		vehicle_dash = Vehicle.objects.all()
		uom_dash = UOM.objects.all()
		u_site = user_site(request)
		item_dash = StockItem.objects.all()

		gchallan = []
		tran = GoodsEntry.objects.values('challan_number')
		trans = {item['challan_number'] for item in tran}
		for s in trans:
			if s != cn:
				gchallan.append(s)

		gbill = []
		tran = GoodsEntry.objects.values('bill_number')
		trans = {item['bill_number'] for item in tran}
		for s in trans:
			if s != bn:
				gbill.append(s) 

		igoods = []
		seen = set()
		seen_add = seen.add
		tran = InvoiceItem.objects.values_list('purchaseid', flat=True).distinct()
		ent = [x for x in tran if not (x in seen or seen_add(x))]
		for s in ent:
			igood = InvoiceItem.objects.filter(purchaseid=s, grn_status='no', issue_use='no')
			n = len(igood)
			igoods.append([igood, range(1,n)])

		invitem = []
		seen = set()
		seen_add = seen.add
		tran = Goods.objects.values_list('pvn', flat=True).distinct()
		ent = [x for x in tran if not (x in seen or seen_add(x))]
		for s in ent:
			inv = Goods.objects.filter(pvn=s, goodsid=gid)
			n = len(inv)
			invitem.append([inv, range(1,n)])

		purinvoice = []
		seen = set()
		seen_add = seen.add
		tran = PurchaseEntry.objects.values_list('purchase_order_number', flat=True).distinct()
		ent = [x for x in tran if not (x in seen or seen_add(x))]
		for s in ent:
			pur = PurchaseEntry.objects.filter(purchase_order_number=s)
			n = len(igood)
			purinvoice.append([pur, range(1,n)])

		purextra = GoodsExtra.objects.filter(goodsid=gid)

		context = {'item': item, 'purextra': purextra, 'purinvoice': purinvoice, 'invitem': invitem, 'igoods': igoods, 'inv_count': inv_count, 'supplier_dash': supplier_dash, 'location_dash': location_dash, 'vehicle_dash': vehicle_dash, 'uom_dash': uom_dash, 'item_dash': item_dash, 'gchallan': gchallan, 'gbill': gbill}    
		return render(request, 'ashish_goods_edit.html', context)
	else:
		return redirect('ashish_goods_display')


@user_access
def ashish_add_goods(request):
	if request.method=="POST":
		current_user = request.user.username
		u_site = user_site(request)
		date = request.POST.get('date')
		grn = request.POST.get('grn')
		grn_count = request.POST.get('grn_count')
		challan = request.POST.get('challan')
		bill = request.POST.get('bill')
		location = request.POST.get('location')
		# supplier = request.POST.get('supplier')
		# vehicle = request.POST.get('vehicle')
		narrat = request.POST.get('narrat')
		porder = request.POST.get('porder')
		porder = porder.upper()
		porder = porder.replace(" ", "")
		itemadd = request.POST.getlist('itemadd')
		# sup = Supplier.objects.filter(id=supplier).first()
		# sup_name = sup.name
		# sup_address = sup.address
		# sup_contact = sup.landline
		for a in itemadd:
			a = str(a)
			pvn = request.POST.get('ipvn'+a)
			itemid = request.POST.get('inameid'+a)
			pvn = pvn.upper()
			if StockEntry.objects.filter(item_id=itemid, stock_site=u_site).exists():
				print('ok')
			else:
				messages.info(request, 'error')
				return redirect('ashish_goods_entry')
			if PurchaseEntry.objects.filter(voucher_number=pvn, grn_status='yes').exists():
				messages.info(request, 'error')
				return redirect('ashish_goods_entry')


		if GoodsEntry.objects.filter(grn_number=grn).exists():
			messages.info(request, 'error')
			return redirect('ashish_goods_entry')
		else:
			query = GoodsEntry(entry_date=date, purchase_order_number=porder, narration=narrat, grn_number=grn, grn_count=grn_count, challan_number=challan, bill_number=bill, location=location, entry_by=current_user, user_site=u_site)
			query.save()

		gid = query.id
		for a in itemadd:
			a = str(a)
			pvn = request.POST.get('ipvn'+a)
			itemid = request.POST.get('inameid'+a)
			item = request.POST.get('iname'+a)
			alias = request.POST.get('ialias'+a)
			uom = request.POST.get('iuom'+a)
			qty = request.POST.get('iqty'+a)
			que = Goods(goodsid=gid, pvn=pvn, grn=grn, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty)
			que.save()
			sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
			qt = float(sq.quantity)
			newqty = qt + float(qty)
			StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)
			if GoodsExtra.objects.filter(goodsid=gid,voucher_number=pvn).exists():
				pass
			else:
				s = PurchaseEntry.objects.filter(voucher_number=pvn).first()
				supp = s.supplier_name
				por = s.purchase_order_number
				pv = pvn.upper()
				query = GoodsExtra(grn_number=grn, goodsid=gid, purchase_order_number=por, voucher_number=pv, supplier=supp)
				query.save()

			PurchaseEntry.objects.filter(voucher_number=pvn).update(grn_id=gid, grn_status='yes')
			InvoiceItem.objects.filter(pvn=pvn).update(grn_id=gid, grn_status='yes')
		# PurchaseOrder.objects.filter(purchase_number=porder).update(grn_id=gid, grn_status='yes')

		pod = porder.upper()
		po = PurchaseOrder.objects.filter(purchase_number=pod).first()

		notify_topic = 'grn'
		content_id = gid
		content = 'grn_add'
		from_site = u_site
		from_user = current_user
		content_val = grn
		content_val2 = po.issuing_site

		q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, from_site=from_site, from_user=from_user, content_val=content_val, content_val2=content_val2)
		q.save()

		messages.info(request, 'done')
		return redirect('ashish_goods_entry')
	else:
		return redirect('ashish_goods_entry')


@user_access
def ashish_edit_goods(request):
	if request.method=="POST":
		gid = request.POST.get('gid')
		date = request.POST.get('date')
		grn = request.POST.get('grn')
		challan = request.POST.get('challan')
		bill = request.POST.get('bill')
		porder = request.POST.get('porder')
		porder = porder.replace(" ", "")
		porder = porder.upper()
		# location = request.POST.get('location')
		# supplier = request.POST.get('supplier')
		# vehicle = request.POST.get('vehicle')
		narrat = request.POST.get('narrat')
		itemadd = request.POST.getlist('itemadd')
		# sup = Supplier.objects.filter(id=supplier).first()
		# sup_name = sup.name
		# sup_address = sup.address
		# sup_contact = sup.landline
		ge = GoodsEntry.objects.filter(id=gid).first()
		u_site = ge.user_site

		gq = Goods.objects.filter(goodsid=gid)
		gpvn = []
		for a in gq:
			pvn = a.pvn
			pvn = pvn.upper()
			gpvn.append(pvn)
		for a in itemadd:
			a = str(a)
			pvn = request.POST.get('ipvn'+a)
			itemid = request.POST.get('inameid'+a)
			pvn = pvn.upper()
			if StockEntry.objects.filter(item_id=itemid, stock_site=u_site).exists():
				print('ok')
			else:
				messages.info(request, 'error')
				return redirect('/ashish-edit-goods/'+str(gid)+'/')
			if PurchaseEntry.objects.filter(voucher_number=pvn, grn_status='yes').exclude(voucher_number__in=gpvn).exists():
				messages.info(request, 'error')
				return redirect('/ashish-edit-goods/'+str(gid)+'/')

		GoodsEntry.objects.filter(id=gid).update(entry_date=date, narration=narrat, challan_number=challan, bill_number=bill)

		gq = Goods.objects.filter(goodsid=gid)
		for a in gq:
			itemid = a.item_id
			qty = a.quantity
			pvn = a.pvn
			sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
			qt = float(sq.quantity)
			if qt > float(qty) or qt == float(qty):
				newqty = qt - float(qty)
			if qt < float(qty):
				newqty = float(qty) - qt
			StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)
			PurchaseEntry.objects.filter(voucher_number=pvn).update(grn_id='', grn_status='no')
			InvoiceItem.objects.filter(pvn=pvn).update(grn_id='', grn_status='no')
		# PurchaseOrder.objects.filter(purchase_number=porder).update(grn_id='', grn_status='no')

		GoodsExtra.objects.filter(goodsid=gid).delete();
		Goods.objects.filter(goodsid=gid).delete();
		for a in itemadd:
			a = str(a)
			pvn = request.POST.get('ipvn'+a)
			itemid = request.POST.get('inameid'+a)
			item = request.POST.get('iname'+a)
			alias = request.POST.get('ialias'+a)
			uom = request.POST.get('iuom'+a)
			qty = request.POST.get('iqty'+a)
			que = Goods(goodsid=gid, pvn=pvn, grn=grn, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty)
			que.save()
			sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
			qt = float(sq.quantity)
			newqty = qt + float(qty)
			StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)
			if GoodsExtra.objects.filter(goodsid=gid,voucher_number=pvn).exists():
				pass
			else:
				s = PurchaseEntry.objects.filter(voucher_number=pvn).first()
				supp = s.supplier_name
				por = s.purchase_order_number
				query = GoodsExtra(grn_number=grn, goodsid=gid, purchase_order_number=por, voucher_number=pvn, supplier=supp)
				query.save()
			PurchaseEntry.objects.filter(voucher_number=pvn).update(grn_id=gid, grn_status='yes')
			InvoiceItem.objects.filter(pvn=pvn).update(grn_id=gid, grn_status='yes')
		# PurchaseOrder.objects.filter(purchase_number=porder).update(grn_id=gid, grn_status='yes')
		messages.info(request, 'done')
		return redirect('/ashish-edit-goods/'+str(gid)+'/')
	else:
		return redirect('ashish_goods_display')


@user_access
def ashish_invoice_entry(request):
	supplier_dash = Supplier.objects.all()
	location_dash = Location.objects.all()
	vehicle_dash = Vehicle.objects.all()
	porder = PurchaseOrder.objects.filter(status='approved')
	uom_dash = UOM.objects.all()
	item_dash = StockItem.objects.all()
	pvn = 0
	if PurchaseEntry.objects.last():
		good = PurchaseEntry.objects.last()
		ng = good.pvn_count
		pvn = int(ng) + 1
	else:
		pvn = pvn + 1

	ichallan = []
	tran = PurchaseEntry.objects.values('challan_number')
	trans = {item['challan_number'] for item in tran}
	for s in trans:
		ichallan.append(s)

	ivoice = []
	tran = PurchaseEntry.objects.values('invoice_number')
	trans = {item['invoice_number'] for item in tran}
	for s in trans:
		ivoice.append(s) 

	pitem = PurchaseItem.objects.all()

	context = {'porder': porder, 'pitem': pitem, 'pvn': pvn, 'item_dash': item_dash, 'ichallan': ichallan, 'ivoice': ivoice, 'supplier_dash': supplier_dash, 'location_dash': location_dash, 'vehicle_dash': vehicle_dash, 'uom_dash': uom_dash}    
	return render(request, 'ashish_purchase_invoice.html', context)


@user_access
def ashish_invoice_display(request):
	u_site = user_site(request)
	u_status = user_role(request)
	s_item = []
	if u_status == 'main_admin' or u_status == 'main_staff':
		s_it = PurchaseEntry.objects.all().order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_it, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_item.append([product, range(1, n)])
	else:
		s_it = PurchaseEntry.objects.filter(user_site=u_site).order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_it, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_item.append([product, range(1, n)])
	context = {'s_item': s_item}    
	return render(request, 'display/ashish_invoice_display.html', context)


@user_access
def ashish_invoice_detail(request,pid):
	if PurchaseEntry.objects.filter(id=pid).exists():
		item = PurchaseEntry.objects.filter(id=pid).first()
		s_goods = InvoiceItem.objects.filter(purchaseid=pid)
		context = {'item': item, 's_goods': s_goods}    
		return render(request, 'display/ashish_invoice_detail.html', context)
	else:
		return redirect('ashish_invoice_display')


@user_access
def ashish_search_invoice(request):
	if request.method == "POST":
		search = request.POST.get('search')
		sea = search.upper()
		se = search.title()
		s = search.lower()
		u_site = user_site(request)
		u_status = user_role(request)
		if u_status == 'main_admin' or u_status == 'main_staff':
			lookup = Q(purchase_order_number=search) | Q(voucher_number=search) | Q(challan_number=search) | Q(invoice_number=search) | Q(invoice_type__icontains=search) | Q(supplier_name__icontains=search) | Q(vehicle_number__icontains=search) | Q(user_site__icontains=search) | Q(narration__icontains=search) | Q(purchase_order_number=sea) | Q(voucher_number=sea) | Q(challan_number=sea) | Q(invoice_number=sea) | Q(invoice_type__icontains=sea) | Q(supplier_name__icontains=sea) | Q(vehicle_number__icontains=sea) | Q(user_site__icontains=sea) | Q(narration__icontains=sea) | Q(purchase_order_number=se) | Q(voucher_number=se) | Q(challan_number=se) | Q(invoice_number=se) | Q(invoice_type__icontains=se) | Q(supplier_name__icontains=se) | Q(vehicle_number__icontains=se) | Q(user_site__icontains=se) | Q(narration__icontains=se) | Q(purchase_order_number=s) | Q(voucher_number=s) | Q(challan_number=s) | Q(invoice_number=s) | Q(invoice_type__icontains=s) | Q(supplier_name__icontains=s) | Q(vehicle_number__icontains=s) | Q(user_site__icontains=s) | Q(narration__icontains=s)
		else:
			lookup = Q(Q(purchase_order_number=search) | Q(voucher_number=search) | Q(challan_number=search) | Q(invoice_number=search) | Q(invoice_type__icontains=search) | Q(supplier_name__icontains=search) | Q(vehicle_number__icontains=search) | Q(narration__icontains=search) | Q(purchase_order_number=sea) | Q(voucher_number=sea) | Q(challan_number=sea) | Q(invoice_number=sea) | Q(invoice_type__icontains=sea) | Q(supplier_name__icontains=sea) | Q(vehicle_number__icontains=sea) | Q(narration__icontains=sea) | Q(purchase_order_number=se) | Q(voucher_number=se) | Q(challan_number=se) | Q(invoice_number=se) | Q(invoice_type__icontains=se) | Q(supplier_name__icontains=se) | Q(vehicle_number__icontains=se) | Q(narration__icontains=se) | Q(purchase_order_number=s) | Q(voucher_number=s) | Q(challan_number=s) | Q(invoice_number=s) | Q(invoice_type__icontains=s) | Q(supplier_name__icontains=s) | Q(vehicle_number__icontains=s) | Q(narration__icontains=s)) & Q(user_site=u_site)
		s_item = []
		s_it = PurchaseEntry.objects.filter(lookup).order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_it, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_item.append([product, range(1, n)])
		context = {'s_item': s_item, 'search': search}
		return render(request, 'display/ashish_search_invoice.html', context)
	else:
		return redirect('ashish_invoice_display')


@user_access
def ashish_print_invoice(request):
	if request.method=="POST":
		jid = request.POST.get('jid')
		s_good = PurchaseEntry.objects.filter(id=jid).first()
		igoods = InvoiceItem.objects.filter(purchaseid=jid)

		context = {'a': s_good, 'igoods': igoods}
		pdf = render_to_pdf('ashish_printinvoice.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			rnum = random.randint(11111111, 99999999)
			filename = "Reportinvoice_%s.pdf" %(rnum)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")
	else:
		return redirect('ashish_invoice_display')


@user_access
def ashish_delete_invoice(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		PurchaseEntry.objects.filter(id=sid).delete()
		InvoiceItem.objects.filter(purchaseid=sid).delete()
		messages.info(request, 'done')
		return redirect('ashish_invoice_display')
	else:
		return redirect('ashish_invoice_display')


@user_access
def ashish_invoice_edit(request, pid):
	if PurchaseEntry.objects.filter(id=pid).exists():
		supplier_dash = Supplier.objects.all()
		location_dash = Location.objects.all()
		vehicle_dash = Vehicle.objects.all()
		uom_dash = UOM.objects.all()
		item_dash = StockItem.objects.all()
		porder = PurchaseOrder.objects.filter(status='approved')
		item = PurchaseEntry.objects.filter(id=pid).first()
		cn = item.challan_number
		ni = item.invoice_number
		invitem = InvoiceItem.objects.filter(purchaseid=pid)

		ichallan = []
		tran = PurchaseEntry.objects.values('challan_number')
		trans = {item['challan_number'] for item in tran}
		for s in trans:
			if s != cn:
				ichallan.append(s)

		ivoice = []
		tran = PurchaseEntry.objects.values('invoice_number')
		trans = {item['invoice_number'] for item in tran}
		for s in trans:
			if s != ni:
				ivoice.append(s)

		inv_count = []
		bill_len = 0
		a = 0
		for b in invitem:
			a = a+1
			inv_count.append(a)

		pitem = PurchaseItem.objects.all()

		context = {'item': item, 'porder': porder, 'pitem': pitem, 'inv_count': inv_count, 'invitem': invitem, 'item_dash': item_dash, 'ichallan': ichallan, 'ivoice': ivoice, 'supplier_dash': supplier_dash, 'location_dash': location_dash, 'vehicle_dash': vehicle_dash, 'uom_dash': uom_dash}    
		return render(request, 'ashish_invoice_edit.html', context)
	else:
		return redirect('ashish_invoice_display')


@user_access
def ashish_add_invoice(request):
	if request.method=="POST":
		current_user = request.user.username
		u_site = user_site(request)
		date = request.POST.get('date')
		invoice_date = request.POST.get('invoice_date')
		voucher_number = request.POST.get('voucher_number')
		pvn_count = request.POST.get('pvn_count')
		challan = request.POST.get('challan')
		invoice = request.POST.get('invoice')
		invoice_type = request.POST.get('invoice_type')
		location = request.POST.get('location')
		supplier = request.POST.get('supplier')
		vehicle = request.POST.get('vehicle')
		trans = request.POST.get('supplier')
		vehicle = request.POST.get('vehicle')
		narrat = request.POST.get('narrat')
		sub_total = request.POST.get('subtotal')
		discount_per = request.POST.get('discount1')
		discount_amt = request.POST.get('discount2')
		porder = request.POST.get('porder')
		porder = porder.replace(" ", "")
		porder = porder.upper()
		vat = request.POST.get('vat')
		total = request.POST.get('total')
		trans = request.POST.get('trans')
		day = request.POST.get('day')
		itemadd = request.POST.getlist('itemadd')
		sup = Supplier.objects.filter(id=supplier).first()
		sup_name = sup.name
		sup_address = sup.address
		sup_contact = sup.landline
		for a in itemadd:
			a = str(a)
			itemid = request.POST.get('inameid'+a)
			po = porder.upper()
			if InvoiceItem.objects.filter(item_id=itemid, po=po).exists():
				messages.info(request, 'error')
				return redirect('ashish_purchase_invoice')


		if PurchaseEntry.objects.filter(voucher_number=voucher_number).exists():
			messages.info(request, 'error')
			return redirect('ashish_purchase_invoice')
		else:
			query = PurchaseEntry(entry_date=date, purchase_order_number=porder, day=day, transaction_type=trans, narration=narrat, invoice_date=invoice_date, invoice_type=invoice_type, voucher_number=voucher_number, pvn_count=pvn_count, challan_number=challan, invoice_number=invoice, location=location, supplier_id=supplier, supplier_name=sup_name, supplier_address=sup_address, supplier_contact=sup_contact, vehicle_number=vehicle, sub_total=sub_total, discount_per=discount_per, discount_amt=discount_amt, vat=vat, total=total, entry_by=current_user, user_site=u_site)
			query.save()
			pid = query.id
			# PurchaseOrder.objects.filter(purchase_number=porder).update(invoice_id=pid, invoice_status="yes")

		pid = query.id
		for a in itemadd:
			a = str(a)
			itemid = request.POST.get('inameid'+a)
			item = request.POST.get('iname'+a)
			alias = request.POST.get('ialias'+a)
			uom = request.POST.get('iuom'+a)
			qty = request.POST.get('iqty'+a)
			rate = request.POST.get('irate'+a)
			amt = request.POST.get('iamt'+a)
			dis_amt = request.POST.get('idisamt'+a)
			dis_per = request.POST.get('idisper'+a)
			po = porder.upper()
			que = InvoiceItem(purchaseid=pid, po=po, pvn=voucher_number, discount_amt=dis_amt, discount_per=dis_per, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty, orig_quantity=qty, useable_quantity=qty, rate=rate, amount=amt)
			que.save()

		pod = porder.upper()
		po = PurchaseOrder.objects.filter(purchase_number=pod).first()

		notify_topic = 'purchase_invoice_entry'
		content_id = pid
		content = 'invoice_add'
		from_site = u_site
		from_user = current_user
		content_val = voucher_number
		content_val2 = po.issuing_site

		q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, from_site=from_site, from_user=from_user, content_val=content_val, content_val2=content_val2)
		q.save()

		notify_topic = 'purchase_invoice_entry'
		content_id = pid
		content = 'invoice_arrival'
		from_site = u_site
		from_user = current_user
		content_val = voucher_number
		content_val1 = pod
		content_val2 = po.issuing_site

		q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, from_site=from_site, from_user=from_user, content_val=content_val, content_val1=content_val1, content_val2=content_val2)
		q.save()

		messages.info(request, 'done')
		return redirect('ashish_purchase_invoice')
	else:
		return redirect('ashish_purchase_invoice')


@user_access
def ashish_edit_invoice(request):
	if request.method=="POST":
		pid = request.POST.get('pid')
		date = request.POST.get('date')
		invoice_date = request.POST.get('invoice_date')
		voucher_number = request.POST.get('voucher_number')
		challan = request.POST.get('challan')
		invoice = request.POST.get('invoice')
		invoice_type = request.POST.get('invoice_type')
		location = request.POST.get('location')
		supplier = request.POST.get('supplier')
		vehicle = request.POST.get('vehicle')
		narrat = request.POST.get('narrat')
		sub_total = request.POST.get('subtotal')
		discount_per = request.POST.get('discount1')
		discount_amt = request.POST.get('discount2')
		vat = request.POST.get('vat')
		total = request.POST.get('total')
		trans = request.POST.get('trans')
		porder = request.POST.get('porder')
		porder = porder.replace(" ", "")
		porder = porder.upper()
		day = request.POST.get('day')
		itemadd = request.POST.getlist('itemadd')
		sup = Supplier.objects.filter(id=supplier).first()
		sup_name = sup.name
		sup_address = sup.address
		sup_contact = sup.landline

		inviid = []
		gm = InvoiceItem.objects.filter(purchaseid=pid)
		for a in gm:
			idd = a.id
			inviid.append(idd)

		for a in itemadd:
			a = str(a)
			itemid = request.POST.get('inameid'+a)
			po = porder.upper()
			if InvoiceItem.objects.filter(item_id=itemid, po=po).exclude(id__in=inviid).exists():
				messages.info(request, 'error')
				return redirect('ashish_purchase_invoice')

		PurchaseEntry.objects.filter(id=pid).update(entry_date=date, narration=narrat, day=day, transaction_type=trans, invoice_date=invoice_date, invoice_type=invoice_type, challan_number=challan, invoice_number=invoice, location=location, supplier_id=supplier, supplier_name=sup_name, supplier_address=sup_address, supplier_contact=sup_contact, vehicle_number=vehicle, sub_total=sub_total, discount_per=discount_per, discount_amt=discount_amt, vat=vat, total=total)

		InvoiceItem.objects.filter(purchaseid=pid).delete();
		for a in itemadd:
			a = str(a)
			# grn = request.POST.get('igrn'+a)
			itemid = request.POST.get('inameid'+a)
			item = request.POST.get('iname'+a)
			alias = request.POST.get('ialias'+a)
			uom = request.POST.get('iuom'+a)
			qty = request.POST.get('iqty'+a)
			rate = request.POST.get('irate'+a)
			amt = request.POST.get('iamt'+a)
			dis_amt = request.POST.get('idisamt'+a)
			dis_per = request.POST.get('idisper'+a)
			po = porder.upper()
			que = InvoiceItem(purchaseid=pid, po=po, pvn=voucher_number, discount_amt=dis_amt, discount_per=dis_per, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty, orig_quantity=qty, useable_quantity=qty, rate=rate, amount=amt)
			que.save()

		messages.info(request, 'done')
		return redirect('/ashish-invoice-edit/'+str(pid)+'/')
	else:
		return redirect('ashish_invoice_display')

# ashish end-------------------------------------


@user_access
def goods_entry(request):
	supplier_dash = Supplier.objects.all()
	location_dash = Location.objects.all()
	vehicle_dash = Vehicle.objects.all()
	porder = PurchaseOrder.objects.filter(status='approved')
	uom_dash = UOM.objects.all()
	u_site = user_site(request)
	item_dash = StockItem.objects.all()
	grn = 0
	if GoodsEntry.objects.last():
		good = GoodsEntry.objects.last()
		ng = good.grn_count
		grn = int(ng) + 1
	else:
		grn = grn + 1

	gchallan = []
	tran = GoodsEntry.objects.values('challan_number')
	trans = {item['challan_number'] for item in tran}
	for s in trans:
		gchallan.append(s)

	gbill = []
	tran = GoodsEntry.objects.values('bill_number')
	trans = {item['bill_number'] for item in tran}
	for s in trans:
		gbill.append(s) 
	context = {'porder': porder, 'supplier_dash': supplier_dash, 'location_dash': location_dash, 'vehicle_dash': vehicle_dash, 'uom_dash': uom_dash, 'item_dash': item_dash, 'grn': grn, 'gchallan': gchallan, 'gbill': gbill}    
	return render(request, 'goods_entry.html', context)


@user_access
def goods_display(request):
	u_site = user_site
	s_item = GoodsEntry.objects.all().order_by('-id')[:30]
	context = {'s_item': s_item}    
	return render(request, 'display/goods_display.html', context)


@user_access
def goods_detail(request,gid):
	if GoodsEntry.objects.filter(id=gid).exists():
		item = GoodsEntry.objects.filter(id=gid).first()
		s_goods = Goods.objects.filter(goodsid=gid)
		context = {'item': item, 's_goods': s_goods}    
		return render(request, 'display/goods_detail.html', context)
	else:
		return redirect('goods_display')


@user_access
def search_goods(request):
	if request.method == "POST":
		search = request.POST.get('search')
		sea = search.upper()
		se = search.title()
		s = search.lower()
		u_site = user_site(request)
		lookup = Q(grn_number=search) | Q(challan_number=search) | Q(bill_number=search) | Q(location=search) | Q(supplier_name=search) | Q(vehicle_number=search) | Q(user_site=search) | Q(grn_number=sea) | Q(challan_number=sea) | Q(bill_number=sea) | Q(location=sea) | Q(supplier_name=sea) | Q(vehicle_number=sea) | Q(user_site=sea) | Q(grn_number=se) | Q(challan_number=se) | Q(bill_number=se) | Q(location=se) | Q(supplier_name=se) | Q(vehicle_number=se) | Q(user_site=se) | Q(grn_number=s) | Q(challan_number=s) | Q(bill_number=s) | Q(location=s) | Q(supplier_name=s) | Q(vehicle_number=s) | Q(user_site=s)
		s_goods = GoodsEntry.objects.filter(lookup).order_by('-id')
		context = {'s_goods': s_goods, 'search': search}
		return render(request, 'display/goods_search.html', context)
	else:
		return redirect('goods_display')


@user_access
def print_goods(request):
	if request.method=="POST":
		jid = request.POST.get('jid')
		s_good = GoodsEntry.objects.filter(id=jid).first()
		igoods = Goods.objects.filter(goodsid=jid)

		context = {'a': s_good, 'igoods': igoods}
		pdf = render_to_pdf('printgoods.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			rnum = random.randint(11111111, 99999999)
			filename = "Reportgoods_%s.pdf" %(rnum)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")
	else:
		return redirect('goods_display')


@user_access
def delete_goods(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		GoodsEntry.objects.filter(id=sid).delete()
		Goods.objects.filter(goodsid=sid).delete()
		messages.info(request, 'done')
		return redirect('goods_display')
	else:
		return redirect('goods_display')


@user_access
def goods_edit(request, gid):
	if GoodsEntry.objects.filter(id=gid).exists():
		item = GoodsEntry.objects.filter(id=gid).first()
		igoods = Goods.objects.filter(goodsid=gid)
		goods_count = []
		a = 0
		for b in igoods:
			a = a+1
			goods_count.append(a)

		supplier_dash = Supplier.objects.all()
		location_dash = Location.objects.all()
		vehicle_dash = Vehicle.objects.all()
		uom_dash = UOM.objects.all()
		u_site = user_site(request)
		item_dash = StockItem.objects.all()

		gchallan = []
		tran = GoodsEntry.objects.values('challan_number')
		trans = {item['challan_number'] for item in tran}
		for s in trans:
			gchallan.append(s)

		gbill = []
		tran = GoodsEntry.objects.values('bill_number')
		trans = {item['bill_number'] for item in tran}
		for s in trans:
			gbill.append(s) 
		context = {'item': item, 'igoods': igoods, 'goods_count': goods_count, 'supplier_dash': supplier_dash, 'location_dash': location_dash, 'vehicle_dash': vehicle_dash, 'uom_dash': uom_dash, 'item_dash': item_dash, 'gchallan': gchallan, 'gbill': gbill}    
		return render(request, 'goods_edit.html', context)
	else:
		return redirect('goods_display')


@user_access
def add_goods(request):
	if request.method=="POST":
		current_user = request.user.username
		u_site = user_site(request)
		date = request.POST.get('date')
		grn = request.POST.get('grn')
		grn_count = request.POST.get('grn_count')
		challan = request.POST.get('challan')
		bill = request.POST.get('bill')
		# location = request.POST.get('location')
		supplier = request.POST.get('supplier')
		vehicle = request.POST.get('vehicle')
		itemadd = request.POST.getlist('itemadd')
		sup = Supplier.objects.filter(id=supplier).first()
		sup_name = sup.name
		sup_address = sup.address
		sup_contact = sup.landline

		if GoodsEntry.objects.filter(grn_number=grn).exists():
			messages.info(request, 'error')
			return redirect('goods_entry')
		else:
			query = GoodsEntry(entry_date=date, grn_number=grn, grn_count=grn_count, challan_number=challan, bill_number=bill, supplier_id=supplier, supplier_name=sup_name, supplier_address=sup_address, supplier_contact=sup_contact, vehicle_number=vehicle, entry_by=current_user, user_site=u_site)
			query.save()

		gid = query.id
		for a in itemadd:
			a = str(a)
			itemid = request.POST.get('inameid'+a)
			item = request.POST.get('iname'+a)
			uom = request.POST.get('iuom'+a)
			qty = request.POST.get('iqty'+a)
			remark = request.POST.get('iremark'+a)
			que = Goods(goodsid=gid, grn=grn, item_id=itemid, item=item, uom=uom, quantity=qty, remark=remark)
			que.save()

		notify_topic = 'grn'
		content_id = gid
		content = 'grn_add'
		from_site = u_site
		from_user = current_user
		content_val = grn

		q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, from_site=from_site, from_user=from_user, content_val=content_val)
		q.save()

		messages.info(request, 'done')
		return redirect('goods_entry')
	else:
		return redirect('goods_entry')


@user_access
def edit_goods(request):
	if request.method=="POST":
		gid = request.POST.get('gid')
		date = request.POST.get('date')
		grn = request.POST.get('grn')
		grn_count = request.POST.get('grn_count')
		challan = request.POST.get('challan')
		bill = request.POST.get('bill')
		# location = request.POST.get('location')
		supplier = request.POST.get('supplier')
		vehicle = request.POST.get('vehicle')
		itemadd = request.POST.getlist('itemadd')
		sup = Supplier.objects.filter(id=supplier).first()
		sup_name = sup.name
		sup_address = sup.address
		sup_contact = sup.landline

		GoodsEntry.objects.filter(id=gid).update(entry_date=date, challan_number=challan, bill_number=bill, supplier_id=supplier, supplier_name=sup_name, supplier_address=sup_address, supplier_contact=sup_contact, vehicle_number=vehicle)

		Goods.objects.filter(goodsid=gid).delete();
		for a in itemadd:
			a = str(a)
			itemid = request.POST.get('inameid'+a)
			item = request.POST.get('iname'+a)
			uom = request.POST.get('iuom'+a)
			qty = request.POST.get('iqty'+a)
			remark = request.POST.get('iremark'+a)
			que = Goods(goodsid=gid, grn=grn, item_id=itemid, item=item, uom=uom, quantity=qty, remark=remark)
			que.save()
		messages.info(request, 'done')
		return redirect('edit-goods/'+str(gid)+'/')
	else:
		return redirect('goods_display')


@user_access
def invoice_entry(request):
	supplier_dash = Supplier.objects.all()
	location_dash = Location.objects.all()
	vehicle_dash = Vehicle.objects.all()
	porder = PurchaseOrder.objects.filter(status='approved', invoice_status='no')
	uom_dash = UOM.objects.all()
	u_site = user_site(request)
	stock_item = StockEntry.objects.all()
	pvn = 0
	if PurchaseEntry.objects.last():
		good = PurchaseEntry.objects.last()
		ng = good.pvn_count
		pvn = int(ng) + 1
	else:
		pvn = pvn + 1

	ichallan = []
	tran = PurchaseEntry.objects.values('challan_number')
	trans = {item['challan_number'] for item in tran}
	for s in trans:
		ichallan.append(s)

	ivoice = []
	tran = PurchaseEntry.objects.values('invoice_number')
	trans = {item['invoice_number'] for item in tran}
	for s in trans:
		ivoice.append(s) 

	igoods = []
	tran = Goods.objects.values('goodsid')
	trans = {item['goodsid'] for item in tran}
	for s in trans:
		igood = Goods.objects.filter(goodsid=s)
		n = len(igood)
		igoods.append([igood, range(1,n)])

	context = {'porder': porder, 'pvn': pvn, 'stock_item': stock_item, 'ichallan': ichallan, 'ivoice': ivoice, 'supplier_dash': supplier_dash, 'igoods': igoods, 'location_dash': location_dash, 'vehicle_dash': vehicle_dash, 'uom_dash': uom_dash}    
	return render(request, 'purchase_invoice.html', context)


@user_access
def invoice_display(request):
	s_item = PurchaseEntry.objects.all().order_by('-id')[:30]
	context = {'s_item': s_item}    
	return render(request, 'display/invoice_display.html', context)


def invoice_detail(request,pid):
	if PurchaseEntry.objects.filter(id=pid).exists():
		item = PurchaseEntry.objects.filter(id=pid).first()
		s_goods = InvoiceItem.objects.filter(purchaseid=pid)
		context = {'item': item, 's_goods': s_goods}    
		return render(request, 'display/invoice_detail.html', context)
	else:
		return redirect('invoice_display')


@user_access
def search_invoice(request):
	if request.method == "POST":
		search = request.POST.get('search')
		sea = search.upper()
		se = search.title()
		s = search.lower()
		lookup = Q(voucher_number=search) | Q(challan_number=search) | Q(invoice_number=search) | Q(invoice_type=search) | Q(location=search) | Q(supplier_name=search) | Q(vehicle_number=search) | Q(user_site=search) | Q(voucher_number=sea) | Q(challan_number=sea) | Q(invoice_number=sea) | Q(invoice_type=sea) | Q(location=sea) | Q(supplier_name=sea) | Q(vehicle_number=sea) | Q(user_site=sea) | Q(voucher_number=se) | Q(challan_number=se) | Q(invoice_number=se) | Q(invoice_type=se) | Q(location=se) | Q(supplier_name=se) | Q(vehicle_number=se) | Q(user_site=se) | Q(voucher_number=s) | Q(challan_number=s) | Q(invoice_number=s) | Q(invoice_type=s) | Q(location=s) | Q(supplier_name=s) | Q(vehicle_number=s) | Q(user_site=s) 
		s_item = PurchaseEntry.objects.filter(lookup).order_by('-id')
		context = {'s_item': s_item, 'search': search}
		return render(request, 'display/search_invoice.html', context)
	else:
		return redirect('invoice_display')


@user_access
def print_invoice(request):
	if request.method=="POST":
		jid = request.POST.get('jid')
		s_good = PurchaseEntry.objects.filter(id=jid).first()
		igoods = InvoiceItem.objects.filter(purchaseid=jid)

		context = {'a': s_good, 'igoods': igoods}
		pdf = render_to_pdf('printinvoice.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			rnum = random.randint(11111111, 99999999)
			filename = "Reportinvoice_%s.pdf" %(rnum)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")
	else:
		return redirect('invoice_display')


@user_access
def delete_invoice(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		PurchaseEntry.objects.filter(id=sid).delete()
		InvoiceItem.objects.filter(purchaseid=sid).delete()
		messages.info(request, 'done')
		return redirect('invoice_display')
	else:
		return redirect('invoice_display')


@user_access
def invoice_edit(request, pid):
	if PurchaseEntry.objects.filter(id=pid).exists():
		supplier_dash = Supplier.objects.all()
		location_dash = Location.objects.all()
		vehicle_dash = Vehicle.objects.all()
		uom_dash = UOM.objects.all()
		u_site = user_site(request)
		stock_item = StockEntry.objects.all()
		item = PurchaseEntry.objects.filter(id=pid).first()
		initem = InvoiceItem.objects.filter(purchaseid=pid)

		ichallan = []
		tran = PurchaseEntry.objects.values('challan_number')
		trans = {item['challan_number'] for item in tran}
		for s in trans:
			ichallan.append(s)

		ivoice = []
		tran = PurchaseEntry.objects.values('invoice_number')
		trans = {item['invoice_number'] for item in tran}
		for s in trans:
			ivoice.append(s) 

		igoods = []
		tran = Goods.objects.values('goodsid')
		trans = {item['goodsid'] for item in tran}
		for s in trans:
			igood = Goods.objects.filter(goodsid=s)
			n = len(igood)
			igoods.append([igood, range(1,n)])

		invitem = []
		tran = InvoiceItem.objects.values('grn')
		trans = {item['grn'] for item in tran}
		for s in trans:
			inv = InvoiceItem.objects.filter(grn=s, purchaseid=pid)
			n = len(inv)
			invitem.append([inv, range(1,n)])

		seen = set()
		seen_add = seen.add
		tran = InvoiceItem.objects.values_list('grn', flat=True).distinct()
		ent = [x for x in tran if not (x in seen or seen_add(x))]
		inv_count = []
		a = 0
		for b in ent:
			que = InvoiceItem.objects.filter(grn=b, purchaseid=pid)
			for i in que:
				grr = i.grn
				a = a+1
				inv_count.append(grr)

		context = {'item': item, 'inv_count': inv_count, 'invitem': invitem, 'initem': initem, 'stock_item': stock_item, 'ichallan': ichallan, 'ivoice': ivoice, 'supplier_dash': supplier_dash, 'igoods': igoods, 'location_dash': location_dash, 'vehicle_dash': vehicle_dash, 'uom_dash': uom_dash}    
		return render(request, 'invoice_edit.html', context)
	else:
		return redirect('invoice_display')


@user_access
def add_invoice(request):
	if request.method=="POST":
		current_user = request.user.username
		u_site = user_site(request)
		date = request.POST.get('date')
		invoice_date = request.POST.get('invoice_date')
		voucher_number = request.POST.get('voucher_number')
		pvn_count = request.POST.get('pvn_count')
		challan = request.POST.get('challan')
		invoice = request.POST.get('invoice')
		invoice_type = request.POST.get('invoice_type')
		location = request.POST.get('location')
		supplier = request.POST.get('supplier')
		vehicle = request.POST.get('vehicle')
		sub_total = request.POST.get('subtotal')
		discount_per = request.POST.get('discount1')
		discount_amt = request.POST.get('discount2')
		vat = request.POST.get('vat')
		total = request.POST.get('total')
		itemadd = request.POST.getlist('itemadd')
		sup = Supplier.objects.filter(id=supplier).first()
		sup_name = sup.name
		sup_address = sup.address
		sup_contact = sup.landline

		if PurchaseEntry.objects.filter(voucher_number=voucher_number).exists():
			messages.info(request, 'error')
			return redirect('purchase_invoice')
		else:
			query = PurchaseEntry(entry_date=date, invoice_date=invoice_date, invoice_type=invoice_type, voucher_number=voucher_number, pvn_count=pvn_count, challan_number=challan, invoice_number=invoice, location=location, supplier_id=supplier, supplier_name=sup_name, supplier_address=sup_address, supplier_contact=sup_contact, vehicle_number=vehicle, sub_total=sub_total, discount_per=discount_per, discount_amt=discount_amt, vat=vat, total=total, entry_by=current_user, user_site=u_site)
			query.save()

		pid = query.id
		for a in itemadd:
			a = str(a)
			grn = request.POST.get('igrn'+a)
			itemid = request.POST.get('inameid'+a)
			item = request.POST.get('iname'+a)
			uom = request.POST.get('iuom'+a)
			qty = request.POST.get('iqty'+a)
			rate = request.POST.get('irate'+a)
			amt = request.POST.get('iamt'+a)
			que = InvoiceItem(purchaseid=pid, pvn=voucher_number, grn=grn, item_id=itemid, item=item, uom=uom, quantity=qty, rate=rate, amount=amt)
			que.save()

			GoodsEntry.objects.filter(grn_number=grn).update(invoice_id=pid, invoice_status="yes")

		notify_topic = 'purchase_invoice_entry'
		content_id = pid
		content = 'invoice_add'
		from_site = u_site
		from_user = current_user
		content_val = voucher_number

		q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, from_site=from_site, from_user=from_user, content_val=content_val)
		q.save()

		messages.info(request, 'done')
		return redirect('purchase_invoice')
	else:
		return redirect('purchase_invoice')


@user_access
def edit_invoice(request):
	if request.method=="POST":
		pid = request.POST.get('pid')
		date = request.POST.get('date')
		invoice_date = request.POST.get('invoice_date')
		voucher_number = request.POST.get('voucher_number')
		challan = request.POST.get('challan')
		invoice = request.POST.get('invoice')
		invoice_type = request.POST.get('invoice_type')
		location = request.POST.get('location')
		supplier = request.POST.get('supplier')
		vehicle = request.POST.get('vehicle')
		sub_total = request.POST.get('subtotal')
		discount_per = request.POST.get('discount1')
		discount_amt = request.POST.get('discount2')
		vat = request.POST.get('vat')
		total = request.POST.get('total')
		itemadd = request.POST.getlist('itemadd')
		sup = Supplier.objects.filter(id=supplier).first()
		sup_name = sup.name
		sup_address = sup.address
		sup_contact = sup.landline

		PurchaseEntry.objects.filter(id=pid).update(entry_date=date, invoice_date=invoice_date, invoice_type=invoice_type, challan_number=challan, invoice_number=invoice, location=location, supplier_id=supplier, supplier_name=sup_name, supplier_address=sup_address, supplier_contact=sup_contact, vehicle_number=vehicle, sub_total=sub_total, discount_per=discount_per, discount_amt=discount_amt, vat=vat, total=total)

		InvoiceItem.objects.filter(purchaseid=pid).delete();
		for a in itemadd:
			a = str(a)
			grn = request.POST.get('igrn'+a)
			itemid = request.POST.get('inameid'+a)
			item = request.POST.get('iname'+a)
			uom = request.POST.get('iuom'+a)
			qty = request.POST.get('iqty'+a)
			rate = request.POST.get('irate'+a)
			amt = request.POST.get('iamt'+a)
			que = InvoiceItem(purchaseid=pid, pvn=voucher_number, grn=grn, item_id=itemid, item=item, uom=uom, quantity=qty, rate=rate, amount=amt)
			que.save()

		messages.info(request, 'done')
		return redirect('/invoice-edit/'+str(pid)+'/')
	else:
		return redirect('invoice_display')


@user_access
def stock(request):
	s_item = StockItem.objects.all().count()
	s_cat = StockCategory.objects.all().count()
	# ss = StockCategory.objects.all()
	# for s in ss:
	# 	sname = s.name
	# 	surl = s.url
	# 	if StockItem.objects.filter(stock_category=sname).exists():
	# 		StockItem.objects.filter(stock_category=sname).update(cat_url=surl)
	# 	if StockEntry.objects.filter(stock_category=sname).exists():
	# 		StockEntry.objects.filter(stock_category=sname).update(cat_url=surl)
	# ss = StockSubCategory.objects.all()
	# for s in ss:
	# 	sname = s.name
	# 	surl = s.url
	# 	if StockItem.objects.filter(stock_subcategory=sname).exists():
	# 		StockItem.objects.filter(stock_subcategory=sname).update(subcat_url=surl)
	# 	if StockEntry.objects.filter(stock_subcategory=sname).exists():
	# 		StockEntry.objects.filter(stock_subcategory=sname).update(subcat_url=surl)
	context = {'s_item': s_item, 's_cat': s_cat}    
	return render(request, 'stock_dash.html', context)


@user_access
def stock_entry(request):
	s_item = StockEntry.objects.all().count()
	s_cat = StockCategory.objects.all().count()
	stock_cat = StockCategory.objects.all()
	uom_dash = UOM.objects.all()
	site_dash = Site.objects.filter(active_status='yes')
	psupa = []
	seen = set()
	seen_add = seen.add
	tran = StockSubCategory.objects.values_list('cat_url', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for r in ent:
		ps = StockSubCategory.objects.filter(cat_url=r)
		n = len(ps)
		psupa.append([ps, range(1,n)])
	context = {'s_item': s_item, 'psupa': psupa, 'site_dash': site_dash, 's_cat': s_cat, 'stock_cat':stock_cat, 'uom_dash': uom_dash}    
	return render(request, 'stock_entry.html', context)


@user_access
def add_stock(request):
	if request.method=="POST":
		current_user = request.user.username
		name = request.POST.get('name')
		url = request.POST.get('url')
		alias = request.POST.get('alias')
		stock_cat = request.POST.get('stock_category')
		caturl = request.POST.get('categoryurl')
		stock_subcat = request.POST.get('subcategory')
		subcaturl = request.POST.get('subcategoryurl')
		mainurl = request.POST.get('mainurl')
		stock_type = request.POST.get('stock_type')
		uom = request.POST.get('uom')
		surl = request.POST.getlist('sites')
		u_site = user_site(request)

		if StockItem.objects.filter(url=url).exists():
			q = StockItem.objects.filter(url=url).first()
			item_id = q.id
		else:
			query = StockItem(item=name, url=url, alias=alias, stock_category=stock_cat, stock_subcategory=stock_subcat, cat_url=caturl, subcat_url=subcaturl, main_url=mainurl, uom=uom, stock_type=stock_type, entry_by=current_user, user_site=u_site)
			query.save()
			item_id = query.id

		if surl:
			for s in surl:
				s_site = request.POST.get('site_name'+str(s))
				qty = request.POST.get('qty'+str(s))
				rate = request.POST.get('rate'+str(s))
				amt = request.POST.get('amt'+str(s))

				if StockEntry.objects.filter(url=url, stock_site=s_site).exists():
					pass
				else:
					query = StockEntry(item=name, item_id=item_id, url=url, stock_site=s_site, alias=alias, stock_category=stock_cat, stock_subcategory=stock_subcat, cat_url=caturl, subcat_url=subcaturl, uom=uom, opening=qty, quantity=qty, rate=rate, amount=amt, stock_type=stock_type, entry_by=current_user, user_site=u_site)
					query.save()

		sites = Site.objects.filter(active_status='yes')
		for s in sites:
			s_site = s.name
			qty = 0
			rate = 0
			amt = 0

			if StockEntry.objects.filter(url=url, stock_site=s_site).exists():
				pass
			else:
				query = StockEntry(item=name, item_id=item_id, url=url, stock_site=s_site, alias=alias, stock_category=stock_cat, stock_subcategory=stock_subcat, cat_url=caturl, subcat_url=subcaturl, uom=uom, opening=qty, quantity=qty, rate=rate, amount=amt, stock_type=stock_type, entry_by=current_user, user_site=u_site)
				query.save()

		messages.info(request, 'done')
		return redirect('stock_entry')
	else:
		return redirect('stock_entry')


@user_access
def stock_display(request):
	u_site = user_site(request)
	u_status = user_role(request)
	if u_status == 'main_admin' or u_status == 'main_staff':
		s_item = StockEntry.objects.all()
	else:
		s_item = StockEntry.objects.filter(stock_site=u_site)
	stock_cat = StockCategory.objects.all()
	uom_dash = UOM.objects.all()
	site_dash = Site.objects.filter(active_status='yes')
	psupa = []
	seen = set()
	seen_add = seen.add
	tran = StockSubCategory.objects.values_list('cat_url', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for r in ent:
		ps = StockSubCategory.objects.filter(cat_url=r)
		n = len(ps)
		psupa.append([ps, range(1,n)])
	context = {'s_item': s_item, 'psupa': psupa, 'site_dash': site_dash, 'stock_cat':stock_cat, 'uom_dash': uom_dash}    
	return render(request, 'display/stock_display.html', context)


@user_access
def stock_item_display(request):
	u_site = user_site(request)
	s_item = StockItem.objects.all()
	stock_cat = StockCategory.objects.all()
	uom_dash = UOM.objects.all()
	site_dash = Site.objects.filter(active_status='yes')
	psupa = []
	seen = set()
	seen_add = seen.add
	tran = StockSubCategory.objects.values_list('cat_url', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for r in ent:
		ps = StockSubCategory.objects.filter(cat_url=r)
		n = len(ps)
		psupa.append([ps, range(1,n)])
	context = {'s_item': s_item, 'psupa': psupa, 'site_dash': site_dash, 'stock_cat':stock_cat, 'uom_dash': uom_dash}    
	return render(request, 'display/stock_item_display.html', context)


@user_access
def search_stock_item(request):
	if request.method == "POST":
		search = request.POST.get('search')
		scat = request.POST.get('searchcat')
		sscat = request.POST.get('searchsubcat')
		ssite = request.POST.get('searchsite')
		# split = search.split('-')
		# if len(search.split('-')) > 1:
		# 	lookup = Q(stock_site__contains=split[1]) & Q(item__contains=split[0])
		# else:
		s_item = StockEntry.objects.all()
		if scat != '' and scat is not None:
			s_item = s_item.filter(stock_category=scat).order_by('-id')
		if sscat != '' and sscat is not None:
			s_item = s_item.filter(stock_subcategory=sscat).order_by('-id')
		if ssite != '' and ssite is not None:
			s_item = s_item.filter(stock_site=ssite).order_by('-id')
		if search != '' and search is not None:
			s_item = s_item.filter(item__icontains=search).order_by('-id')
		stock_cat = StockCategory.objects.all()
		uom_dash = UOM.objects.all()
		site_dash = Site.objects.filter(active_status='yes')
		psupa = []
		seen = set()
		seen_add = seen.add
		tran = StockSubCategory.objects.values_list('cat_url', flat=True).distinct()
		ent = [x for x in tran if not (x in seen or seen_add(x))]
		for r in ent:
			ps = StockSubCategory.objects.filter(cat_url=r)
			n = len(ps)
			psupa.append([ps, range(1,n)])
		context = {'s_item': s_item, 'psupa': psupa, 'site_dash':site_dash, 'search': search, 'scat': scat, 'sscat': sscat, 'ssite': ssite, 'stock_cat':stock_cat, 'uom_dash': uom_dash}
		return render(request, 'display/stock_search.html', context)
	else:
		return redirect('stock_display')


@user_access
def search_item(request):
	if request.method == "POST":
		search = request.POST.get('search')
		scat = request.POST.get('searchcat')
		sscat = request.POST.get('searchsubcat')
		s_item = StockItem.objects.all()
		if scat != '' and scat is not None:
			s_item = s_item.filter(stock_category=scat).order_by('-id')
		if sscat != '' and sscat is not None:
			s_item = s_item.filter(stock_subcategory=sscat).order_by('-id')
		if search != '' and search is not None:
			s_item = s_item.filter(item__icontains=search).order_by('-id')
		stock_cat = StockCategory.objects.all()
		uom_dash = UOM.objects.all()
		site_dash = Site.objects.filter(active_status='yes')
		psupa = []
		seen = set()
		seen_add = seen.add
		tran = StockSubCategory.objects.values_list('cat_url', flat=True).distinct()
		ent = [x for x in tran if not (x in seen or seen_add(x))]
		for r in ent:
			ps = StockSubCategory.objects.filter(cat_url=r)
			n = len(ps)
			psupa.append([ps, range(1,n)])
		context = {'s_item': s_item, 'psupa': psupa, 'site_dash':site_dash, 'scat':scat, 'sscat':sscat, 'search': search, 'stock_cat':stock_cat, 'uom_dash': uom_dash}
		return render(request, 'display/stock_search_item.html', context)
	else:
		return redirect('stock_item_display')


@user_access
def update_stock(request):
	if request.method=="POST":
		sid = request.POST.get('suid')
		name = request.POST.get('name')
		dname = request.POST.get('dname')
		url = request.POST.get('url')
		alias = request.POST.get('alias')
		stock_cat = request.POST.get('category')
		stock_subcat = request.POST.get('subcategory')
		stock_type = request.POST.get('type')
		uom = request.POST.get('uom')
		opening = request.POST.get('opening')
		quantity = request.POST.get('quantity')
		rate = request.POST.get('rate')
		amount = request.POST.get('amount')
		s_site = request.POST.get('site')

		if StockEntry.objects.filter(url=url, stock_site=s_site).exclude(id=sid).exists():
			messages.info(request, 'error')
			return redirect('stock_display')
		else:
			StockEntry.objects.filter(id=sid).update(opening=opening, quantity=quantity, rate=rate, amount=amount)

			messages.info(request, 'done')
			return redirect('stock_display')
	else:
		return redirect('stock_display')


@user_access
def update_stock_item(request):
	if request.method=="POST":
		sid = request.POST.get('suid')
		name = request.POST.get('name')
		dname = request.POST.get('dname')
		dalias = request.POST.get('dalias')
		duom = request.POST.get('duom')
		url = request.POST.get('url')
		alias = request.POST.get('alias')
		stock_cat = request.POST.get('category')
		stock_subcat = request.POST.get('subcategory')
		stock_type = request.POST.get('type')
		uom = request.POST.get('uom')
		sc = StockCategory.objects.filter(name=stock_cat).first()
		scurl = sc.url
		scc = StockSubCategory.objects.filter(cat_name=stock_cat, name=stock_subcat).first()
		sscurl = scc.url
		murl = str(scurl)+''+str(sscurl)

		if StockItem.objects.filter(url=url).exclude(id=sid).exists():
			messages.info(request, 'error')
			return redirect('stock_display')
		else:
			StockItem.objects.filter(id=sid).update(item=name, url=url, alias=alias, stock_category=stock_cat, stock_subcategory=stock_subcat, cat_url=scurl, subcat_url=sscurl, main_url=murl, uom=uom, stock_type=stock_type)
			StockEntry.objects.filter(item_id=sid).update(item=name, url=url, alias=alias, stock_category=stock_cat, stock_subcategory=stock_subcat, cat_url=scurl, subcat_url=sscurl, uom=uom, stock_type=stock_type)
			if name != dname:
				Goods.objects.filter(item_id=sid).update(item=name)
				InvoiceItem.objects.filter(item_id=sid).update(item=name)
				MaterialItem.objects.filter(item_id=sid).update(item=name)
				TransferItem.objects.filter(item_id=sid).update(item=name)
				InternalGrnItems.objects.filter(item_id=sid).update(item=name)
				MaintainanceItem.objects.filter(item_id=sid).update(item_name=name)
			if alias != dalias:
				Goods.objects.filter(item_id=sid).update(alias=alias)
				InvoiceItem.objects.filter(item_id=sid).update(alias=alias)
				MaterialItem.objects.filter(item_id=sid).update(alias=alias)
				TransferItem.objects.filter(item_id=sid).update(alias=alias)
				InternalGrnItems.objects.filter(item_id=sid).update(alias=alias)
				MaintainanceItem.objects.filter(item_id=sid).update(alias=alias)
			if uom != duom:
				Goods.objects.filter(item_id=sid).update(uom=uom)
				InvoiceItem.objects.filter(item_id=sid).update(uom=uom)
				MaterialItem.objects.filter(item_id=sid).update(uom=uom)
				TransferItem.objects.filter(item_id=sid).update(uom=uom)
				InternalGrnItems.objects.filter(item_id=sid).update(uom=uom)
				MaintainanceItem.objects.filter(item_id=sid).update(uom=uom)

			messages.info(request, 'done')
			return redirect('stock_item_display')
	else:
		return redirect('stock_item_display')


@user_access
def delete_stock(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		StockEntry.objects.filter(id=sid).delete()
		messages.info(request, 'done')
		return redirect('stock_display')
	else:
		return redirect('stock_display')


@user_access
def delete_stock_item(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		StockItem.objects.filter(id=sid).delete()
		StockEntry.objects.filter(item_id=sid).delete()
		messages.info(request, 'done')
		return redirect('stock_item_display')
	else:
		return redirect('stock_item_display')


@user_access
def stock_category(request):
	category_dash = StockCategory.objects.all()
	subcategory_dash = StockSubCategory.objects.all()
	psupa = []
	# seen = set()
	# seen_add = seen.add
	# tran = StockSubCategory.objects.values_list('cat_url', flat=True).distinct()
	# ent = [x for x in tran if not (x in seen or seen_add(x))]
	# for r in ent:
	# 	ps = StockSubCategory.objects.filter(cat_url=r)
	# 	n = len(ps)
	# 	psupa.append([ps, range(1,n)])
	context = {'category_dash': category_dash, 'psupa': psupa, 'subcategory_dash': subcategory_dash}    
	return render(request, 'stock_category.html', context)


@user_access
def add_stock_category(request):
	if request.method=="POST":
		name = request.POST.get('name')
		url = request.POST.get('url')
		current_user = request.user.username
		u_site = user_site(request)

		if StockCategory.objects.filter(url=url).exists():
			messages.info(request, 'error')
			return redirect('manage_stock_category')
		else:
			query = StockCategory(name=name, url=url, entry_by=current_user, user_site=u_site)
			query.save()
			messages.info(request, 'done')
			return redirect('manage_stock_category')
	else:
		return redirect('manage_stock_category')


@user_access
def edit_stock_category(request):
	if request.method=="POST":
		lid = request.POST.get('lid')
		default = request.POST.get('default')
		name = request.POST.get('name')
		url = request.POST.get('url')

		if StockCategory.objects.filter(url=url).exclude(id=lid).exists():
			messages.info(request, 'error')
			return redirect('manage_stock_category')
		else:
			StockCategory.objects.filter(id=lid).update(name=name, url=url)
			if StockItem.objects.filter(stock_category=default).exists():
				StockItem.objects.filter(stock_category=default).update(stock_category=name, cat_url=url)
			if StockEntry.objects.filter(stock_category=default).exists():
				StockEntry.objects.filter(stock_category=default).update(stock_category=name, cat_url=url)
			if StockSubCategory.objects.filter(cat_name=default).exists():
				StockSubCategory.objects.filter(cat_name=default).update(cat_name=name, cat_url=url)
			messages.info(request, 'done')
			return redirect('manage_stock_category')
	else:
		return redirect('manage_stock_category')


@user_access
def delete_stock_category(request):
	if request.method=="POST":
		lid = request.POST.get('lid')
		stk = StockCategory.objects.filter(id=lid).first()
		urll = stk.url

		StockCategory.objects.filter(id=lid).delete()
		if StockSubCategory.objects.filter(cat_url=urll).exists():
			StockSubCategory.objects.filter(cat_url=urll).delete()
		messages.info(request, 'done')
		return redirect('manage_stock_category')
	else:
		return redirect('manage_stock_category')


@user_access
def add_stock_subcategory(request):
	if request.method=="POST":
		name = request.POST.get('name')
		cat = request.POST.get('stock_category')
		url = request.POST.get('url')
		caturl = request.POST.get('caturl')
		current_user = request.user.username
		u_site = user_site(request)

		if StockSubCategory.objects.filter(cat_url=caturl, url=url).exists():
			messages.info(request, 'error')
			return redirect('manage_stock_category')
		else:
			query = StockSubCategory(name=name, url=url, cat_name=cat, cat_url=caturl, entry_by=current_user, user_site=u_site)
			query.save()
			messages.info(request, 'done')
			return redirect('manage_stock_category')
	else:
		return redirect('manage_stock_category')


@user_access
def edit_stock_subcategory(request):
	if request.method=="POST":
		lid = request.POST.get('lid')
		name = request.POST.get('name')
		cat = request.POST.get('stock_category')
		url = request.POST.get('url')
		caturl = request.POST.get('caturl')
		default = request.POST.get('default')

		if StockSubCategory.objects.filter(cat_url=caturl, url=url).exclude(id=lid).exists():
			messages.info(request, 'error')
			return redirect('manage_stock_category')
		else:
			StockSubCategory.objects.filter(id=lid).update(cat_name=cat, cat_url=caturl, name=name, url=url)
			if StockItem.objects.filter(stock_subcategory=default).exists():
				StockItem.objects.filter(stock_subcategory=default).update(stock_subcategory=name, subcat_url=url)
			if StockEntry.objects.filter(stock_subcategory=default).exists():
				StockEntry.objects.filter(stock_subcategory=default).update(stock_subcategory=name, subcat_url=url)
			messages.info(request, 'done')
			return redirect('manage_stock_category')
	else:
		return redirect('manage_stock_category')


@user_access
def delete_stock_subcategory(request):
	if request.method=="POST":
		lid = request.POST.get('lid')

		StockSubCategory.objects.filter(id=lid).delete()
		messages.info(request, 'done')
		return redirect('manage_stock_category')
	else:
		return redirect('manage_stock_category')


@user_access
def material_issue(request):
	vehicle_dash = Vehicle.objects.all()
	u_site = user_site(request)
	porder = PurchaseOrder.objects.all().exclude(po_vehi='yes')
	item_real = StockItem.objects.all()
	item_dash = StockEntry.objects.filter(stock_site=u_site)
	mat = MaterialIssueEntry.objects.all().count()
	site_dash = Site.objects.filter(active_status='yes').exclude(name=u_site)
	mie = 0
	if MaterialIssueEntry.objects.last():
		good = MaterialIssueEntry.objects.last()
		ng = good.mie_count
		mie = int(ng) + 1
	else:
		mie = mie + 1

	psupa = []
	seen = set()
	seen_add = seen.add
	tran = PurchaseEntry.objects.values_list('purchase_order_number', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for r in ent:
		ps = PurchaseEntry.objects.filter(purchase_order_number=r)
		n = len(ps)
		psupa.append([ps, range(1,n)])

	igoods = []
	tran = InvoiceItem.objects.values_list('purchaseid', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for s in ent:
		igood = InvoiceItem.objects.filter(purchaseid=s, grn_status='yes', issue_use="no").exclude(Q(damage='all') | Q(retur='all'))
		n = len(igood)
		igoods.append([igood, range(1,n)])

	itemsel = []
	seen =set()
	seen_add = seen.add
	ent = StockItem.objects.values_list('main_url', flat=True)
	ent = [x for x in ent if not (x in seen or seen_add(x))]
	for e in ent:
		isel = StockItem.objects.filter(main_url=e)
		n = len(isel)
		itemsel.append([isel, range(1,n)])

	stock_cat = StockCategory.objects.all()
	psupa = []
	seen = set()
	seen_add = seen.add
	tran = StockSubCategory.objects.values_list('cat_url', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for r in ent:
		ps = StockSubCategory.objects.filter(cat_url=r)
		n = len(ps)
		psupa.append([ps, range(1,n)])

	context = {'psupa': psupa, 'itemsel': itemsel, 'stock_cat': stock_cat, 'psupa': psupa, 'igoods': igoods, 'porder': porder, 'item_real': item_real, 'mie': mie, 'site_dash':site_dash, 'u_site': u_site, 'mat': mat, 'vehicle_dash': vehicle_dash, 'item_dash': item_dash}    
	return render(request, 'material_issue.html', context)


@user_access
def material_display(request):
	u_site = user_site(request)
	u_status = user_role(request)
	s_item = []
	if u_status == 'main_admin' or u_status == 'main_staff':
		s_it = MaterialIssueEntry.objects.all().order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_it, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_item.append([product, range(1, n)])
	else:
		s_it = MaterialIssueEntry.objects.filter(user_site=u_site).order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_it, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_item.append([product, range(1, n)])
	context = {'s_item': s_item}    
	return render(request, 'display/material_display.html', context)


@user_access
def material_detail(request,mid):
	if MaterialIssueEntry.objects.filter(id=mid).exists():
		item = MaterialIssueEntry.objects.filter(id=mid).first()
		s_goods = MaterialItem.objects.filter(materialid=mid)
		context = {'item': item, 's_goods': s_goods}    
		return render(request, 'display/material_detail.html', context)
	else:
		return redirect('material_display')


@user_access
def search_material(request):
	if request.method == "POST":
		search = request.POST.get('search')
		sea = search.upper()
		se = search.title()
		s = search.lower()
		u_site = user_site(request)
		u_status = user_role(request)
		if u_status == 'main_admin' or u_status == 'main_staff':
			lookup = Q(issuing_location__icontains=search) | Q(mie_number=search) | Q(vehicle_number__icontains=search) | Q(user_site__icontains=search) | Q(issuing_location=sea) | Q(mie_number=sea) | Q(vehicle_number=sea) | Q(user_site=sea) | Q(issuing_location=se) | Q(mie_number=se) | Q(vehicle_number=se) | Q(user_site=se) | Q(issuing_location=s) | Q(mie_number=s) | Q(vehicle_number=s) | Q(user_site=s)
		else:
			lookup = Q(Q(mie_number=search) | Q(vehicle_number__icontains=search) | Q(mie_number=sea) | Q(vehicle_number=sea) | Q(mie_number=se) | Q(vehicle_number=se) | Q(mie_number=s) | Q(vehicle_number=s)) & Q(user_site=u_site)
		s_goods = []
		s_goo = MaterialIssueEntry.objects.filter(lookup).order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_goo, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_goods.append([product, range(1, n)])
		context = {'s_goods': s_goods, 'search': search}
		return render(request, 'display/material_search.html', context)
	else:
		return redirect('material_display')


@user_access
def print_material(request):
	if request.method=="POST":
		jid = request.POST.get('jid')
		s_good = MaterialIssueEntry.objects.filter(id=jid).first()
		igoods = MaterialItem.objects.filter(materialid=jid)

		context = {'a': s_good, 'igoods': igoods}
		pdf = render_to_pdf('printmaterial.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			rnum = random.randint(11111111, 99999999)
			filename = "Reportmaterial_%s.pdf" %(rnum)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")
	else:
		return redirect('material_display')


@user_access
def delete_material(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		ge = MaterialIssueEntry.objects.filter(id=sid).first()
		u_site = ge.user_site
		gq = MaterialItem.objects.filter(materialid=sid)
		for a in gq:
			itemid = a.item_id
			qty = a.quantity
			if a.pvn:
				pvn = a.pvn
				sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
				qt = float(sq.quantity)
				newqty = qt + float(qty)
				StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)
				InvoiceItem.objects.filter(pvn=pvn).update(issue_use='no')
			else:
				sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
				qt = float(sq.quantity)
				newqty = qt + float(qty)
				StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)

		MaterialIssueEntry.objects.filter(id=sid).delete()
		MaterialItem.objects.filter(materialid=sid).delete()
		messages.info(request, 'done')
		return redirect('material_display')
	else:
		return redirect('material_display')


@user_access
def material_edit(request, mid):
	if MaterialIssueEntry.objects.filter(id=mid).exists():
		item = MaterialIssueEntry.objects.filter(id=mid).first()
		porder = PurchaseOrder.objects.all().exclude(po_vehi='yes')
		bills = []
		bill = MaterialItem.objects.filter(materialid=mid)
		bill_len = len(bill)
		goods_count = []
		a = 0
		for b in bill:
			a = a+1
			goods_count.append(a)
		bills.append([bill, range(1, bill_len)])
		location_dash = Location.objects.all()
		vehicle_dash = Vehicle.objects.all()
		u_site = user_site(request)
		item_dash = StockEntry.objects.filter(stock_site=u_site)
		item_real = StockItem.objects.all()
		site_dash = Site.objects.filter(active_status='yes').exclude(name=u_site)

		psupa = []
		seen = set()
		seen_add = seen.add
		tran = PurchaseEntry.objects.values_list('purchase_order_number', flat=True).distinct()
		ent = [x for x in tran if not (x in seen or seen_add(x))]
		for r in ent:
			ps = PurchaseEntry.objects.filter(purchase_order_number=r)
			n = len(ps)
			psupa.append([ps, range(1,n)])


		igoods = []
		tran = InvoiceItem.objects.values_list('purchaseid', flat=True).distinct()
		ent = [x for x in tran if not (x in seen or seen_add(x))]
		for s in ent:
			igood = InvoiceItem.objects.filter(purchaseid=s, grn_status='yes', issue_use="no").exclude(Q(damage='all') | Q(retur='all'))
			n = len(igood)
			igoods.append([igood, range(1,n)])

		mitm = MaterialItem.objects.filter(materialid=mid).exclude(pvn='')

		itemsel = []
		seen =set()
		seen_add = seen.add
		ent = StockItem.objects.values_list('main_url', flat=True)
		ent = [x for x in ent if not (x in seen or seen_add(x))]
		for e in ent:
			isel = StockItem.objects.filter(main_url=e)
			n = len(isel)
			itemsel.append([isel, range(1,n)])

		stock_cat = StockCategory.objects.all()
		psupa = []
		seen = set()
		seen_add = seen.add
		tran = StockSubCategory.objects.values_list('cat_url', flat=True).distinct()
		ent = [x for x in tran if not (x in seen or seen_add(x))]
		for r in ent:
			ps = StockSubCategory.objects.filter(cat_url=r)
			n = len(ps)
			psupa.append([ps, range(1,n)])

		context = {'psupa': psupa, 'itemsel': itemsel, 'stock_cat': stock_cat, 'psupa': psupa, 'porder': porder, 'bills': bills, 'bill':bill, 'igoods': igoods, 'mitm': mitm, 'item': item, 'item_real': item_real, 'site_dash': site_dash, 'u_site': u_site, 'igoods': igoods, 'goods_count': goods_count, 'location_dash': location_dash, 'vehicle_dash': vehicle_dash, 'item_dash': item_dash}    
		return render(request, 'material_edit.html', context)
	else:
		return redirect('material_display')


@user_access
def add_material(request):
	if request.method=="POST":
		date = request.POST.get('date')
		issue_locate = request.POST.get('issue_locate')
		mie_number = request.POST.get('mie')
		mie_count = request.POST.get('mie_count')
		# receive_locate = request.POST.get('receive_locate')
		issue_for = request.POST.get('issue_for')
		narrat = request.POST.get('narrat')
		porder = request.POST.get('jobnumber')
		porder = porder.replace(" ", "")
		itemadd = request.POST.getlist('itemadd')
		exitemadd = request.POST.getlist('exitemadd')
		current_user = request.user.username
		u_site = user_site(request)

		for a in itemadd:
			a = str(a)
			if request.POST.get('inameid'+a):
				itemid = request.POST.get('inameid'+a)
				item = request.POST.get('iname'+a)
				qty = request.POST.get('iqty'+a)
				if StockEntry.objects.filter(item_id=itemid, stock_site=u_site).exists():
					sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
					qt = float(sq.quantity)
					if qt < float(qty):
						messages.info(request, 'error')
						return redirect('material_issue')
				else:
					messages.info(request, 'error')
					return redirect('material_issue')
		if len(exitemadd) > 0:
			for a in itemadd:
				a = str(a)
				if request.POST.get('iid'+a):
					itemid = request.POST.get('iid'+a)
					qty = request.POST.get('iqty'+a)
					if StockEntry.objects.filter(item_id=itemid, stock_site=u_site).exists():
						sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
						qt = float(sq.quantity)
						if qt < float(qty):
							messages.info(request, 'error')
							return redirect('material_issue')
					else:
						messages.info(request, 'error')
						return redirect('material_issue')

		query = MaterialIssueEntry(issue_date=date, mie_number=mie_number, purchase_order_number=porder, mie_count=mie_count, narration=narrat, issuing_location=issue_locate, issue_for=issue_for, entry_by=current_user, user_site=u_site)
		query.save()

		mid = query.id
		for a in itemadd:
			a = str(a)
			if request.POST.get('ipvn'+a):
				pvn = request.POST.get('ipvn'+a)
				itemid = request.POST.get('inameid'+a)
				item = request.POST.get('iname'+a)
				alias = request.POST.get('ialias'+a)
				uom = request.POST.get('iuom'+a)
				qty = request.POST.get('iqty'+a)
				que = MaterialItem(materialid=mid, po=porder, pvn=pvn, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty)
				que.save()
				InvoiceItem.objects.filter(pvn=pvn).update(issue_use='yes')
				sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
				qt = float(sq.quantity)
				newqty = qt - float(qty)
				StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)
		if len(exitemadd) > 0:
			for a in itemadd:
				a = str(a)
				if request.POST.get('iid'+a):
					itemid = request.POST.get('iid'+a)
					item = request.POST.get('iname'+a)
					alias = request.POST.get('ialias'+a)
					uom = request.POST.get('iuom'+a)
					qty = request.POST.get('iqty'+a)
					que = MaterialItem(materialid=mid, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty)
					que.save()
					sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
					qt = float(sq.quantity)
					newqty = qt - float(qty)
					StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)

		pod = porder.upper()
		po = PurchaseOrder.objects.filter(purchase_number=pod).first()

		notify_topic = 'material_issue'
		content_id = mid
		content = 'material_add'
		from_site = u_site
		from_user = current_user
		content_val = issue_locate
		content_val2 = po.issuing_site

		q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, from_site=from_site, from_user=from_user, content_val=content_val, content_val2=content_val2)
		q.save()

		messages.info(request, 'done')
		return redirect('material_issue')
	else:
		return redirect('material_issue')


@user_access
def edit_material(request):
	if request.method=="POST":
		mid = request.POST.get('mid')
		date = request.POST.get('date')
		issue_locate = request.POST.get('issue_locate')
		mie_number = request.POST.get('mie')
		mie_count = request.POST.get('mie_count')
		# receive_locate = request.POST.get('receive_locate')
		issue_for = request.POST.get('issue_for')
		porder = request.POST.get('jobnumber')
		porder = porder.replace(" ", "")
		narrat = request.POST.get('narrat')
		exitemadd = request.POST.getlist('exitemadd')
		# receive_locate = request.POST.get('receive_locate')
		itemadd = request.POST.getlist('itemadd')

		ge = MaterialIssueEntry.objects.filter(id=mid).first()
		u_site = ge.user_site

		for a in itemadd:
			a = str(a)
			if request.POST.get('inameid'+a):
				itemid = request.POST.get('inameid'+a)
				qty = request.POST.get('iqty'+a)
				if StockEntry.objects.filter(item_id=itemid, stock_site=u_site).exists():
					sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
					qt = float(sq.quantity)
					if qt < float(qty):
						messages.info(request, 'error')
						return redirect('/material-issue-edit/'+str(mid)+'/')
				else:
					messages.info(request, 'error')
					return redirect('/material-issue-edit/'+str(mid)+'/')
		if len(exitemadd) > 0:
			for a in itemadd:
				a = str(a)
				if request.POST.get('iid'+a):
					itemid = request.POST.get('iid'+a)
					qty = request.POST.get('iqty'+a)
					if StockEntry.objects.filter(item_id=itemid, stock_site=u_site).exists():
						sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
						qt = float(sq.quantity)
						if qt < float(qty):
							messages.info(request, 'error')
							return redirect('/material-issue-edit/'+str(mid)+'/')
					else:
						messages.info(request, 'error')
						return redirect('/material-issue-edit/'+str(mid)+'/')

		MaterialIssueEntry.objects.filter(id=mid).update(issue_date=date, issuing_location=issue_locate, purchase_order_number=porder, issue_for=issue_for, narration=narrat)

		gq = MaterialItem.objects.filter(materialid=mid)
		for a in gq:
			itemid = a.item_id
			qty = a.quantity
			if a.pvn:
				pvn = a.pvn
				sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
				qt = float(sq.quantity)
				newqty = qt + float(qty)
				StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)
				InvoiceItem.objects.filter(pvn=pvn).update(issue_use='no')
			else:
				sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
				qt = float(sq.quantity)
				newqty = qt + float(qty)
				StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)

		MaterialItem.objects.filter(materialid=mid).delete();
		for a in itemadd:
			a = str(a)
			if request.POST.get('ipvn'+a):
				pvn = request.POST.get('ipvn'+a)
				itemid = request.POST.get('inameid'+a)
				item = request.POST.get('iname'+a)
				alias = request.POST.get('ialias'+a)
				uom = request.POST.get('iuom'+a)
				qty = request.POST.get('iqty'+a)
				que = MaterialItem(materialid=mid, po=porder, pvn=pvn, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty)
				que.save()
				InvoiceItem.objects.filter(pvn=pvn).update(issue_use='yes')
				sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
				qt = float(sq.quantity)
				newqty = qt - float(qty)
				StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)
		if len(exitemadd) > 0:
			for a in itemadd:
				a = str(a)
				if request.POST.get('iid'+a):
					itemid = request.POST.get('iid'+a)
					item = request.POST.get('iname'+a)
					alias = request.POST.get('ialias'+a)
					uom = request.POST.get('iuom'+a)
					qty = request.POST.get('iqty'+a)
					que = MaterialItem(materialid=mid, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty)
					que.save()
					sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
					qt = float(sq.quantity)
					newqty = qt - float(qty)
					StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)

		messages.info(request, 'done')
		return redirect('/material-issue-edit/'+str(mid)+'/')
	else:
		return redirect('material_display')


@user_access
def internal_dash(request):
	s_item = InternalTransfer.objects.all().count()
	s_cat = InternalGrn.objects.all().count()
	d_cat = InternalDamageEntry.objects.all().count()
	context = {'s_item': s_item, 's_cat': s_cat, 'd_cat': d_cat}    
	return render(request, 'internal_dash.html', context)


@user_access
def internal_transfer(request):
	location_dash = Location.objects.all()
	vehicle_dash = Vehicle.objects.all()
	u_site = user_site(request)
	item_dash = StockEntry.objects.filter(stock_site=u_site)
	item_real = StockItem.objects.all()
	mat = InternalTransfer.objects.all().count()
	site_dash = Site.objects.filter(active_status='yes').exclude(name=u_site)
	itn = 0
	if InternalTransfer.objects.last():
		good = InternalTransfer.objects.last()
		ng = good.itn_count
		itn = int(ng) + 1
	else:
		itn = itn + 1

	itemsel = []
	seen =set()
	seen_add = seen.add
	ent = StockItem.objects.values_list('main_url', flat=True)
	ent = [x for x in ent if not (x in seen or seen_add(x))]
	for e in ent:
		isel = StockItem.objects.filter(main_url=e)
		n = len(isel)
		itemsel.append([isel, range(1,n)])

	stock_cat = StockCategory.objects.all()
	psupa = []
	seen = set()
	seen_add = seen.add
	tran = StockSubCategory.objects.values_list('cat_url', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for r in ent:
		ps = StockSubCategory.objects.filter(cat_url=r)
		n = len(ps)
		psupa.append([ps, range(1,n)])

	context = {'location_dash': location_dash, 'itemsel': itemsel, 'stock_cat': stock_cat, 'psupa': psupa, 'item_real': item_real, 'itn':itn, 'site_dash': site_dash, 'u_site': u_site, 'mat': mat, 'vehicle_dash': vehicle_dash, 'item_dash': item_dash}    
	return render(request, 'internal_transfer.html', context)


@user_access
def internal_display(request):
	u_site = user_site(request)
	u_status = user_role(request)
	s_item = []
	if u_status == 'main_admin' or u_status == 'main_staff':
		s_it = InternalTransfer.objects.all().order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_it, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_item.append([product, range(1, n)])
	else:
		s_it = InternalTransfer.objects.filter(user_site=u_site).order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_it, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_item.append([product, range(1, n)])
	context = {'s_item': s_item}    
	return render(request, 'display/internal_display.html', context)


@user_access
def internal_detail(request,mid):
	if InternalTransfer.objects.filter(id=mid).exists():
		item = InternalTransfer.objects.filter(id=mid).first()
		s_goods = TransferItem.objects.filter(transferid=mid)
		context = {'item': item, 's_goods': s_goods}    
		return render(request, 'display/internal_detail.html', context)
	else:
		return redirect('internal_display')


@user_access
def search_internal(request):
	if request.method == "POST":
		search = request.POST.get('search')
		sea = search.upper()
		se = search.title()
		s = search.lower()
		u_site = user_site(request)
		u_status = user_role(request)
		if u_status == 'main_admin' or u_status == 'main_staff':
			lookup = Q(issuing_location__icontains=search) | Q(itn_number=search) | Q(receiving_location__icontains=search) | Q(user_site__icontains=search) | Q(issuing_location=sea) | Q(itn_number=sea) | Q(receiving_location=sea) | Q(user_site=sea) | Q(issuing_location=se) | Q(itn_number=se) | Q(receiving_location=se) | Q(user_site=se) | Q(issuing_location=s) | Q(itn_number=se) | Q(receiving_location=s) | Q(user_site=s)
		else:
			lookup = Q(Q(itn_number=search) | Q(receiving_location__icontains=search) | Q(itn_number=sea) | Q(receiving_location=sea) | Q(itn_number=se) | Q(receiving_location=se) | Q(itn_number=se) | Q(receiving_location=s)) & Q(user_site=u_site)
		s_goods = []
		s_goo = InternalTransfer.objects.filter(lookup).order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_goo, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_goods.append([product, range(1, n)])
		context = {'s_goods': s_goods, 'search': search}
		return render(request, 'display/internal_search.html', context)
	else:
		return redirect('internal_display')


@user_access
def print_internal(request):
	if request.method=="POST":
		jid = request.POST.get('jid')
		s_good = InternalTransfer.objects.filter(id=jid).first()
		igoods = TransferItem.objects.filter(transferid=jid)

		context = {'a': s_good, 'igoods': igoods}
		pdf = render_to_pdf('printinternal.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			rnum = random.randint(11111111, 99999999)
			filename = "Reportinternal_%s.pdf" %(rnum)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")
	else:
		return redirect('internal_display')


@user_access
def delete_internal(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		InternalTransfer.objects.filter(id=sid).delete()
		TransferItem.objects.filter(transferid=sid).delete()
		messages.info(request, 'done')
		return redirect('internal_display')
	else:
		return redirect('internal_display')


@user_access
def internal_edit(request, mid):
	if InternalTransfer.objects.filter(id=mid).exists():
		item = InternalTransfer.objects.filter(id=mid).first()
		igoods = TransferItem.objects.filter(transferid=mid)
		goods_count = []
		a = 0
		for b in igoods:
			a = a+1
			goods_count.append(a)

		location_dash = Location.objects.all()
		vehicle_dash = Vehicle.objects.all()
		u_site = user_site(request)
		item_dash = StockEntry.objects.filter(stock_site=u_site)
		item_real = StockItem.objects.all()
		site_dash = Site.objects.filter(active_status='yes').exclude(name=u_site)

		itemsel = []
		seen =set()
		seen_add = seen.add
		ent = StockItem.objects.values_list('main_url', flat=True)
		ent = [x for x in ent if not (x in seen or seen_add(x))]
		for e in ent:
			isel = StockItem.objects.filter(main_url=e)
			n = len(isel)
			itemsel.append([isel, range(1,n)])

		stock_cat = StockCategory.objects.all()
		psupa = []
		seen = set()
		seen_add = seen.add
		tran = StockSubCategory.objects.values_list('cat_url', flat=True).distinct()
		ent = [x for x in tran if not (x in seen or seen_add(x))]
		for r in ent:
			ps = StockSubCategory.objects.filter(cat_url=r)
			n = len(ps)
			psupa.append([ps, range(1,n)])

		context = {'item': item, 'itemsel': itemsel, 'stock_cat': stock_cat, 'psupa': psupa, 'item_real': item_real, 'site_dash': site_dash, 'u_site': u_site, 'igoods': igoods, 'goods_count': goods_count, 'location_dash': location_dash, 'vehicle_dash': vehicle_dash, 'item_dash': item_dash}    
		return render(request, 'internal_edit.html', context)
	else:
		return redirect('material_display')


@user_access
def add_internal(request):
	if request.method=="POST":
		current_user = request.user.username
		date = request.POST.get('date')
		issue_locate = request.POST.get('issue_locate')
		receive_locate = request.POST.get('receive_locate')
		itn_number = request.POST.get('itn')
		itn_count = request.POST.get('itn_count')
		narrat = request.POST.get('narrat')
		itemadd = request.POST.getlist('itemadd')
		u_site = user_site(request)

		for a in itemadd:
			a = str(a)
			itemid = request.POST.get('inameid'+a)
			qty = request.POST.get('iqty'+a)
			if StockEntry.objects.filter(item_id=itemid, stock_site=u_site).exists():
				sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
				qt = float(sq.quantity)
				if qt < float(qty):
					messages.info(request, 'error')
					return redirect('internal_transfer')
			else:
				messages.info(request, 'error')
				return redirect('internal_transfer')

		query = InternalTransfer(issue_date=date, narration=narrat, itn_number=itn_number, itn_count=itn_count, issuing_location=issue_locate, receiving_location=receive_locate, entry_by=current_user, user_site=u_site)
		query.save()

		mid = query.id
		for a in itemadd:
			a = str(a)
			itemid = request.POST.get('inameid'+a)
			item = request.POST.get('iname'+a)
			alias = request.POST.get('ialias'+a)
			uom = request.POST.get('iuom'+a)
			qty = request.POST.get('iqty'+a)
			que = TransferItem(transferid=mid, pvn=itn_number, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty)
			que.save()

		notify_topic = 'internal_transfer'
		content_id = mid
		content = 'transfer_add'
		from_site = u_site
		from_user = current_user
		content_val = issue_locate
		content_val1 = receive_locate
		content_val2 = receive_locate

		q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, from_site=from_site, from_user=from_user, content_val=content_val, content_val1=content_val1, content_val2=content_val2)
		q.save()

		messages.info(request, 'done')
		return redirect('internal_transfer')
	else:
		return redirect('internal_transfer')


@user_access
def edit_internal(request):
	if request.method=="POST":
		mid = request.POST.get('mid')
		date = request.POST.get('date')
		itn_number = request.POST.get('itn')
		issue_locate = request.POST.get('issue_locate')
		receive_locate = request.POST.get('receive_locate')
		narrat = request.POST.get('narrat')
		itemadd = request.POST.getlist('itemadd')

		ge = InternalTransfer.objects.filter(id=mid).first()
		u_site = ge.user_site
		for a in itemadd:
			a = str(a)
			itemid = request.POST.get('inameid'+a)
			qty = request.POST.get('iqty'+a)
			if StockEntry.objects.filter(item_id=itemid, stock_site=u_site).exists():
				sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
				qt = float(sq.quantity)
				if qt < float(qty):
					messages.info(request, 'error')
					return redirect('/internal-transfer-edit/'+str(mid)+'/')
			else:
				messages.info(request, 'error')
				return redirect('/internal-transfer-edit/'+str(mid)+'/')

		InternalTransfer.objects.filter(id=mid).update(issue_date=date, narration=narrat, issuing_location=issue_locate, receiving_location=receive_locate)

		TransferItem.objects.filter(transferid=mid).delete();
		for a in itemadd:
			a = str(a)
			itemid = request.POST.get('inameid'+a)
			item = request.POST.get('iname'+a)
			alias = request.POST.get('ialias'+a)
			uom = request.POST.get('iuom'+a)
			qty = request.POST.get('iqty'+a)
			que = TransferItem(transferid=mid, pvn=itn_number, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty)
			que.save()
		messages.info(request, 'done')
		return redirect('/internal-transfer-edit/'+str(mid)+'/')
	else:
		return redirect('internal_display')


@user_access
def transfer_goods_entry(request):
	supplier_dash = Supplier.objects.all()
	location_dash = Location.objects.all()
	vehicle_dash = Vehicle.objects.all()
	uom_dash = UOM.objects.all()
	u_site = user_site(request)
	item_dash = StockItem.objects.all()
	grn = 0
	if InternalGrn.objects.last():
		good = InternalGrn.objects.last()
		ng = good.grn_count
		grn = int(ng) + 1
	else:
		grn = grn + 1

	ingg = []
	intg = InternalTransfer.objects.filter(receiving_location=u_site)
	for i in intg:
		ingg.append(i.itn_number)

	igoods = []
	tran = TransferItem.objects.values('transferid')
	trans = {item['transferid'] for item in tran}
	for s in trans:
		igood = TransferItem.objects.filter(transferid=s, pvn__in=ingg, grn_status='no')
		n = len(igood)
		igoods.append([igood, range(1,n)])
	context = {'supplier_dash': supplier_dash, 'igoods': igoods, 'location_dash': location_dash, 'vehicle_dash': vehicle_dash, 'uom_dash': uom_dash, 'item_dash': item_dash, 'grn': grn}    
	return render(request, 'transfer_grn.html', context)


@user_access
def transfer_goods_display(request):
	u_site = user_site(request)
	u_status = user_role(request)
	s_item = []
	if u_status == 'main_admin' or u_status == 'main_staff':
		s_it = InternalGrn.objects.all().order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_it, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_item.append([product, range(1, n)])
	else:
		s_it = InternalGrn.objects.filter(user_site=u_site).order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_it, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_item.append([product, range(1, n)])
	context = {'s_item': s_item}    
	return render(request, 'display/transfer_grn_display.html', context)


@user_access
def transfer_goods_detail(request,gid):
	if InternalGrn.objects.filter(id=gid).exists():
		item = InternalGrn.objects.filter(id=gid).first()
		s_goods = InternalGrnItems.objects.filter(goodsid=gid)
		context = {'item': item, 's_goods': s_goods}    
		return render(request, 'display/transfer_gen_detail.html', context)
	else:
		return redirect('transfer_goods_display')


@user_access
def transfer_search_goods(request):
	if request.method == "POST":
		search = request.POST.get('search')
		sea = search.upper()
		se = search.title()
		s = search.lower()
		u_site = user_site(request)
		u_status = user_role(request)
		if u_status == 'main_admin' or u_status == 'main_staff':
			lookup = Q(grn_number=search) | Q(user_site__icontains=search) | Q(grn_number=sea) | Q(user_site=sea) | Q(grn_number=se) | Q(user_site=se) | Q(grn_number=s) | Q(user_site=s)
		else:
			lookup = Q(Q(grn_number=search) | Q(grn_number=sea) | Q(grn_number=se) | Q(grn_number=s)) & Q(user_site=u_site)
		s_goods = []
		s_goo = InternalGrn.objects.filter(lookup).order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_goo, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_goods.append([product, range(1, n)])
		context = {'s_goods': s_goods, 'search': search}
		return render(request, 'display/transfer_grn_search.html', context)
	else:
		return redirect('transfer_goods_display')


@user_access
def transfer_print_goods(request):
	if request.method=="POST":
		jid = request.POST.get('jid')
		s_good = InternalGrn.objects.filter(id=jid).first()
		igoods = InternalGrnItems.objects.filter(goodsid=jid)

		context = {'a': s_good, 'igoods': igoods}
		pdf = render_to_pdf('print_transfer_grn.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			rnum = random.randint(11111111, 99999999)
			filename = "Report_transfer_grn_%s.pdf" %(rnum)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")
	else:
		return redirect('login_user')


@user_access
def transfer_delete_goods(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		it = InternalGrnItems.objects.filter(goodsid=sid)
		for i in it:
			itemid = i.item_id
			qty = i.quantity
			pvn = i.pvn
			itn = InternalTransfer.objects.filter(itn_number=pvn).first()
			source = itn.issuing_location
			dest = itn.receiving_location
			sq = StockEntry.objects.filter(item_id=itemid, stock_site=source).first()
			qt = float(sq.quantity)
			newqty = qt + float(qty)
			StockEntry.objects.filter(item_id=itemid, stock_site=source).update(quantity=newqty)
			sq = StockEntry.objects.filter(item_id=itemid, stock_site=dest).first()
			qt = float(sq.quantity)
			newqty = qt - float(qty)
			StockEntry.objects.filter(item_id=itemid, stock_site=dest).update(quantity=newqty)
			InternalTransfer.objects.filter(itn_number=pvn).update(grn_id='', grn_status='no')
			TransferItem.objects.filter(pvn=pvn).update(grn_id='', grn_status='no')

		InternalGrn.objects.filter(id=sid).delete()
		InternalGrnItems.objects.filter(goodsid=sid).delete()
		messages.info(request, 'done')
		return redirect('transfer_goods_display')
	else:
		return redirect('transfer_goods_display')


@user_access
def transfer_goods_edit(request, gid):
	if InternalGrn.objects.filter(id=gid).exists():
		item = InternalGrn.objects.filter(id=gid).first()
		u_site = item.user_site
		seen = set()
		seen_add = seen.add
		tran = InternalGrnItems.objects.values_list('pvn', flat=True).distinct()
		ent = [x for x in tran if not (x in seen or seen_add(x))]
		inv_count = []
		a = 0
		for b in ent:
			que = InternalGrnItems.objects.filter(pvn=b, goodsid=gid)
			for i in que:
				pvn = i.pvn
				a = a+1
				inv_count.append(pvn)

		supplier_dash = Supplier.objects.all()
		location_dash = Location.objects.all()
		vehicle_dash = Vehicle.objects.all()
		uom_dash = UOM.objects.all()
		item_dash = StockItem.objects.all()

		ingg = []
		intg = InternalTransfer.objects.filter(receiving_location=u_site)
		for i in intg:
			ingg.append(i.itn_number)

		igoods = []
		tran = TransferItem.objects.values('transferid')
		trans = {item['transferid'] for item in tran}
		for s in trans:
			igood = TransferItem.objects.filter(transferid=s, pvn__in=ingg, grn_status='no')
			n = len(igood)
			igoods.append([igood, range(1,n)])

		mitm = InternalGrnItems.objects.filter(goodsid=gid)

		invitem = []
		tran = InternalGrnItems.objects.values('pvn')
		trans = {item['pvn'] for item in tran}
		for s in trans:
			inv = InternalGrnItems.objects.filter(pvn=s, goodsid=gid)
			n = len(inv)
			invitem.append([inv, range(1,n)])
		context = {'item': item, 'invitem': invitem, 'igoods': igoods, 'mitm': mitm, 'inv_count': inv_count, 'supplier_dash': supplier_dash, 'location_dash': location_dash, 'vehicle_dash': vehicle_dash, 'uom_dash': uom_dash, 'item_dash': item_dash}    
		return render(request, 'edit_transfer_grn.html', context)
	else:
		return redirect('transfer_goods_display')


@user_access
def transfer_add_goods(request):
	if request.method=="POST":
		current_user = request.user.username
		u_site = user_site(request)
		date = request.POST.get('date')
		grn = request.POST.get('grn')
		grn_count = request.POST.get('grn_count')
		# vehicle = request.POST.get('vehicle')
		narrat = request.POST.get('narrat')
		itemadd = request.POST.getlist('itemadd')
		for a in itemadd:
			a = str(a)
			pvn = request.POST.get('ipvn'+a)
			itemid = request.POST.get('inameid'+a)
			if StockEntry.objects.filter(item_id=itemid, stock_site=u_site).exists():
				print('ok')
			else:
				messages.info(request, 'error')
				return redirect('transfer_goods_entry')
			if InternalGrnItems.objects.filter(pvn=pvn, item_id=itemid).exists():
				messages.info(request, 'error')
				return redirect('transfer_goods_entry')

		if InternalGrn.objects.filter(grn_number=grn).exists():
			messages.info(request, 'error')
			return redirect('transfer_goods_entry')
		else:
			query = InternalGrn(entry_date=date, narration=narrat, grn_number=grn, grn_count=grn_count, entry_by=current_user, user_site=u_site)
			query.save()

		gid = query.id
		sdis = []
		for a in itemadd:
			a = str(a)
			pvn = request.POST.get('ipvn'+a)
			itemid = request.POST.get('inameid'+a)
			item = request.POST.get('iname'+a)
			alias = request.POST.get('ialias'+a)
			uom = request.POST.get('iuom'+a)
			qty = request.POST.get('iqty'+a)
			que = InternalGrnItems(goodsid=gid, pvn=pvn, grn=grn, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty, orig_quantity=qty)
			que.save()
			itn = InternalTransfer.objects.filter(itn_number=pvn).first()
			source = itn.issuing_location
			dest = itn.receiving_location
			sdis.append([source,dest])
			sq = StockEntry.objects.filter(item_id=itemid, stock_site=source).first()
			qt = float(sq.quantity)
			newqty = qt - float(qty)
			StockEntry.objects.filter(item_id=itemid, stock_site=source).update(quantity=newqty)
			sq = StockEntry.objects.filter(item_id=itemid, stock_site=dest).first()
			qt = float(sq.quantity)
			newqty = qt + float(qty)
			StockEntry.objects.filter(item_id=itemid, stock_site=dest).update(quantity=newqty)
			InternalTransfer.objects.filter(itn_number=pvn).update(grn_id=grn, grn_status='yes')
			TransferItem.objects.filter(pvn=pvn).update(grn_id=grn, grn_status='yes')

			# PurchaseEntry.objects.filter(voucher_number=pvn).update(grn_id=gid, grn_status='yes')
		dd = {}
		for s, d in sdis:
			dd[s] = d
		nsdis = {}
		for key,value in dd.items():
			if key not in nsdis.keys() or value not in nsdis.values():
				nsdis[key] = value

		for s, d in nsdis.items():
			notify_topic = 'internal_transfer'
			content_id = gid
			content = 'transfer_grn'
			from_site = u_site
			from_user = current_user
			content_val = grn
			content_val2 = s
			content_val3 = d

			q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, from_site=from_site, from_user=from_user, content_val=content_val, content_val2=content_val2, content_val3=content_val3)
			q.save()

		messages.info(request, 'done')
		return redirect('transfer_goods_entry')
	else:
		return redirect('transfer_goods_entry')


@user_access
def transfer_edit_goods(request):
	if request.method=="POST":
		gid = request.POST.get('gid')
		date = request.POST.get('date')
		grn = request.POST.get('grn')
		# vehicle = request.POST.get('vehicle')
		narrat = request.POST.get('narrat')
		itemadd = request.POST.getlist('itemadd')

		ge = InternalGrn.objects.filter(id=gid).first()
		u_site = ge.user_site

		itiid = []
		it = InternalGrnItems.objects.filter(goodsid=gid)
		for i in it:
			idd = i.id
			itiid.append(idd)
		for a in itemadd:
			a = str(a)
			pvn = request.POST.get('ipvn'+a)
			itemid = request.POST.get('inameid'+a)
			if StockEntry.objects.filter(item_id=itemid, stock_site=u_site).exists():
				print('ok')
			else:
				messages.info(request, 'error')
				return redirect('/transfer-edit-goods/'+str(gid)+'/')
			if InternalGrnItems.objects.filter(pvn=pvn, item_id=itemid).exclude(id__in=itiid).exists():
				messages.info(request, 'error')
				return redirect('/transfer-edit-goods/'+str(gid)+'/')

		InternalGrn.objects.filter(id=gid).update(entry_date=date, narration=narrat)

		for i in it:
			itemid = i.item_id
			qty = i.quantity
			pvn = i.pvn
			itn = InternalTransfer.objects.filter(itn_number=pvn).first()
			source = itn.issuing_location
			dest = itn.receiving_location
			sq = StockEntry.objects.filter(item_id=itemid, stock_site=source).first()
			qt = float(sq.quantity)
			newqty = qt + float(qty)
			StockEntry.objects.filter(item_id=itemid, stock_site=source).update(quantity=newqty)
			sq = StockEntry.objects.filter(item_id=itemid, stock_site=dest).first()
			qt = float(sq.quantity)
			newqty = qt - float(qty)
			StockEntry.objects.filter(item_id=itemid, stock_site=dest).update(quantity=newqty)
			InternalTransfer.objects.filter(itn_number=pvn).update(grn_id='', grn_status='no')
			TransferItem.objects.filter(pvn=pvn).update(grn_id='', grn_status='no')

		InternalGrnItems.objects.filter(goodsid=gid).delete();
		for a in itemadd:
			a = str(a)
			pvn = request.POST.get('ipvn'+a)
			itemid = request.POST.get('inameid'+a)
			item = request.POST.get('iname'+a)
			alias = request.POST.get('ialias'+a)
			uom = request.POST.get('iuom'+a)
			qty = request.POST.get('iqty'+a)
			que = InternalGrnItems(goodsid=gid, pvn=pvn, grn=grn, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty, orig_quantity=qty)
			que.save()
			itn = InternalTransfer.objects.filter(itn_number=pvn).first()
			source = itn.issuing_location
			dest = itn.receiving_location
			sq = StockEntry.objects.filter(item_id=itemid, stock_site=source).first()
			qt = float(sq.quantity)
			newqty = qt - float(qty)
			StockEntry.objects.filter(item_id=itemid, stock_site=source).update(quantity=newqty)
			sq = StockEntry.objects.filter(item_id=itemid, stock_site=dest).first()
			qt = float(sq.quantity)
			newqty = qt + float(qty)
			StockEntry.objects.filter(item_id=itemid, stock_site=dest).update(quantity=newqty)
			InternalTransfer.objects.filter(itn_number=pvn).update(grn_id=grn, grn_status='yes')
			TransferItem.objects.filter(pvn=pvn).update(grn_id=grn, grn_status='yes')

		messages.info(request, 'done')
		return redirect('/transfer-edit-goods/'+str(gid)+'/')
	else:
		return redirect('transfer_goods_display')


@user_passes_test(check_staff, login_url='login_user')
def sale_dash(request):
	s_item = OutSaleEntry.objects.all().count()
	s_cat = StockCategory.objects.all().count()
	context = {'s_item': s_item, 's_cat': s_cat}    
	return render(request, 'saledash.html', context)


@user_access
def out_sales(request):
	location_dash = Location.objects.all()
	vehicle_dash = Vehicle.objects.all()
	u_site = user_site(request)
	item_dash = StockItem.objects.all()
	sid = 0
	if OutSaleEntry.objects.last():
		good = OutSaleEntry.objects.last()
		ng = good.sid_count
		sid = int(ng) + 1
	else:
		sid = sid + 1

	context = {'sid': sid, 'u_site': u_site, 'item_dash': item_dash, 'location_dash': location_dash, 'vehicle_dash': vehicle_dash}    
	return render(request, 'sales.html', context)


@user_access
def sale_display(request):
	s_item = OutSaleEntry.objects.all().order_by('-id')[:30]
	context = {'s_item': s_item}    
	return render(request, 'display/sale_display.html', context)


@user_access
def sale_detail(request,sid):
	if OutSaleEntry.objects.filter(id=sid).exists():
		item = OutSaleEntry.objects.filter(id=sid).first()
		s_goods = SalesItem.objects.filter(saleid=sid)
		context = {'item': item, 's_goods': s_goods}    
		return render(request, 'display/sale_detail.html', context)
	else:
		return redirect('sale_display')


@user_access
def search_sales(request):
	if request.method == "POST":
		search = request.POST.get('search')
		sea = search.upper()
		se = search.title()
		s = search.lower()
		lookup = Q(issuing_location=search) | Q(sales_id=search) | Q(buyer=search) | Q(invoice_type=search) | Q(user_site=search) | Q(issuing_location=sea) | Q(sales_id=sea) | Q(buyer=sea) | Q(invoice_type=sea) | Q(user_site=sea) | Q(issuing_location=se) | Q(sales_id=se) | Q(buyer=se) | Q(invoice_type=se) | Q(user_site=se)| Q(issuing_location=s) | Q(sales_id=s) | Q(buyer=s) | Q(invoice_type=s) | Q(user_site=s)
		s_item = OutSaleEntry.objects.filter(lookup).order_by('-id')
		context = {'s_item': s_item, 'search': search}
		return render(request, 'display/search_sale.html', context)
	else:
		return redirect('sale_display')


@user_access
def print_sale(request):
	if request.method=="POST":
		jid = request.POST.get('jid')
		s_good = OutSaleEntry.objects.filter(id=jid).first()
		igoods = SalesItem.objects.filter(saleid=jid)

		context = {'a': s_good, 'igoods': igoods}
		pdf = render_to_pdf('printsale.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			rnum = random.randint(11111111, 99999999)
			filename = "Reportsale_%s.pdf" %(rnum)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")
	else:
		return redirect('sale_display')


@user_access
def delete_sale(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		OutSaleEntry.objects.filter(id=sid).delete()
		SalesItem.objects.filter(purchaseid=sid).delete()
		messages.info(request, 'done')
		return redirect('sale_display')
	else:
		return redirect('sale_display')


@user_access
def sale_edit(request, sid):
	if OutSaleEntry.objects.filter(id=sid).exists():
		location_dash = Location.objects.all()
		vehicle_dash = Vehicle.objects.all()
		u_site = user_site(request)
		item_dash = StockItem.objects.all()
		item = OutSaleEntry.objects.filter(id=sid).first()
		invitem = SalesItem.objects.filter(saleid=sid)

		inv_count = []
		a = 0
		for b in invitem:
			a = a+1
			inv_count.append(a)

		context = {'item': item, 'inv_count': inv_count, 'invitem': invitem, 'item_dash': item_dash, 'location_dash': location_dash, 'vehicle_dash': vehicle_dash}    
		return render(request, 'sale_edit.html', context)
	else:
		return redirect('sale_display')


@user_access
def add_sale(request):
	if request.method=="POST":
		current_user = request.user.username
		date = request.POST.get('date')
		saleid = request.POST.get('saleid')
		sid_count = request.POST.get('sid_count')
		issuing = request.POST.get('issue_locate')
		invoice_type = request.POST.get('invoice_type')
		buyer = request.POST.get('buyer')
		sub_total = request.POST.get('subtotal')
		discount_per = request.POST.get('discount1')
		discount_amt = request.POST.get('discount2')
		vat = request.POST.get('vat')
		total = request.POST.get('total')
		itemadd = request.POST.getlist('itemadd')
		u_site = user_site(request)

		if OutSaleEntry.objects.filter(sales_id=saleid).exists():
			messages.info(request, 'error')
			return redirect('out_sales')
		else:
			query = OutSaleEntry(sales_date=date, sales_id=saleid, invoice_type=invoice_type, sid_count=sid_count, issuing_location=issuing, buyer=buyer, sub_total=sub_total, discount_amt=discount_amt, discount_per=discount_per, vat=vat, total=total, entry_by=current_user, user_site=u_site)
			query.save()

		pid = query.id
		for a in itemadd:
			a = str(a)
			itemid = request.POST.get('inameid'+a)
			item = request.POST.get('iname'+a)
			uom = request.POST.get('iuom'+a)
			qty = request.POST.get('iqty'+a)
			rate = request.POST.get('irate'+a)
			amt = request.POST.get('iamt'+a)
			que = SalesItem(saleid=pid, item_id=itemid, item=item, uom=uom, quantity=qty, rate=rate, amount=amt)
			que.save()

		notify_topic = 'out_sales_entry'
		content_id = pid
		content = 'sales_add'
		from_site = u_site
		from_user = current_user
		content_val = issue_locate
		content_val1 = buyer

		q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, from_site=from_site, from_user=from_user, content_val=content_val, content_val1=content_val1)
		q.save()

		messages.info(request, 'done')
		return redirect('out_sales')
	else:
		return redirect('out_sales')


@user_access
def edit_sale(request):
	if request.method=="POST":
		sid = request.POST.get('sid')
		date = request.POST.get('date')
		saleid = request.POST.get('saleid')
		sid_count = request.POST.get('sid_count')
		issuing = request.POST.get('issue_locate')
		invoice_type = request.POST.get('invoice_type')
		buyer = request.POST.get('buyer')
		sub_total = request.POST.get('subtotal')
		discount_per = request.POST.get('discount1')
		discount_amt = request.POST.get('discount2')
		vat = request.POST.get('vat')
		total = request.POST.get('total')
		itemadd = request.POST.getlist('itemadd')

		OutSaleEntry.objects.filter(id=sid).update(sales_date=date, invoice_type=invoice_type, issuing_location=issuing, buyer=buyer, sub_total=sub_total, discount_amt=discount_amt, discount_per=discount_per, vat=vat, total=total, entry_by='amish')
		
		SalesItem.objects.filter(saleid=sid).delete()
		for a in itemadd:
			a = str(a)
			itemid = request.POST.get('inameid'+a)
			item = request.POST.get('iname'+a)
			uom = request.POST.get('iuom'+a)
			qty = request.POST.get('iqty'+a)
			rate = request.POST.get('irate'+a)
			amt = request.POST.get('iamt'+a)
			que = SalesItem(saleid=sid, item_id=itemid, item=item, uom=uom, quantity=qty, rate=rate, amount=amt)
			que.save()

		messages.info(request, 'done')
		return redirect('/sales-edit/'+str(sid)+'/')
	else:
		return redirect('sale_display')


@user_access
def manage_site(request):
	scount = Supplier.objects.all().count()
	lcount = Location.objects.all().count()
	vcount = UOM.objects.all().count()
	sitecount = Site.objects.all().count()
	context = {'scount': scount, 'sitecount': sitecount, 'lcount':lcount, 'vcount': vcount}    
	return render(request, 'site.html', context)


@user_access
def site_display(request):
	site_dash = Site.objects.all().order_by('-id')
	context = {'site_dash': site_dash}    
	return render(request, 'display/site_display.html', context)


@user_access
def add_site(request):
	if request.method=="POST":
		current_user = request.user.username
		name = request.POST.get('name')
		url = request.POST.get('url')
		address = request.POST.get('address')
		pan = request.POST.get('pan')
		contact = request.POST.get('contact')
		role = request.POST.get('admin_sta')
		u_site = user_site(request)

		if Site.objects.filter(url=url).exists():
			messages.info(request, 'error')
			return redirect('manage_site')
		else:
			query = Site(name=name, url=url, address=address, pan_number=pan, contact=contact, role=role, entry_by=current_user, user_site=u_site)
			query.save()
			s_site = query.name
			stoc = StockItem.objects.all()
			for s in stoc:
				itemid = s.id
				name = s.item
				alias = s.alias
				url = s.url
				cat = s.stock_category
				subcat = s.stock_subcategory
				caturl = s.cat_url
				subcaturl = s.subcat_url
				uom = s.uom
				stock_type = s.stock_type 
				qty = 0
				rate = 0
				amt = 0

				if StockEntry.objects.filter(url=url, stock_site=s_site).exists():
					pass
				else:
					query = StockEntry(item=name, item_id=itemid, url=url, stock_site=s_site, alias=alias, stock_category=cat, stock_subcategory=subcat, cat_url=caturl, subcat_url=subcaturl, uom=uom, opening=qty, quantity=qty, rate=rate, amount=amt, stock_type=stock_type, entry_by=current_user, user_site=s_site)
					query.save()
			messages.info(request, 'done')
			return redirect('manage_site')
	else:
		return redirect('manage_site')


@user_access
def edit_site(request):
	if request.method=="POST":
		sid = request.POST.get('suid')
		name = request.POST.get('name')
		dname = request.POST.get('dname')
		url = request.POST.get('url')
		address = request.POST.get('address')
		pan = request.POST.get('pan')
		contact = request.POST.get('contact')
		role = request.POST.get('admin_sta')

		if Site.objects.filter(url=url).exclude(id=sid).exists():
			messages.info(request, 'error')
			return redirect('site_display')
		else:
			Site.objects.filter(id=sid).update(name=name, url=url, address=address, pan_number=pan, contact=contact, role=role)
			UserDetail.objects.filter(site=dname).update(site=name)
			Supplier.objects.filter(user_site=dname).update(user_site=name)
			CreditPay.objects.filter(user_site=dname).update(user_site=name)
			SupplierCategory.objects.filter(user_site=dname).update(user_site=name)
			StockCategory.objects.filter(user_site=dname).update(user_site=name)
			UOM.objects.filter(user_site=dname).update(user_site=name)
			GoodsEntry.objects.filter(user_site=dname).update(user_site=name)
			PurchaseEntry.objects.filter(user_site=dname).update(user_site=name)
			StockEntry.objects.filter(stock_site=dname).update(stock_site=name)
			StockEntry.objects.filter(user_site=dname).update(user_site=name)
			StockItem.objects.filter(user_site=dname).update(user_site=name)
			MaterialIssueEntry.objects.filter(user_site=dname).update(user_site=name)
			MaterialIssueEntry.objects.filter(issuing_location=dname).update(issuing_location=name)
			MaterialIssueEntry.objects.filter(receiving_location=dname).update(receiving_location=name)
			InternalTransfer.objects.filter(user_site=dname).update(user_site=name)
			InternalTransfer.objects.filter(issuing_location=dname).update(issuing_location=name)
			InternalTransfer.objects.filter(receiving_location=dname).update(receiving_location=name)
			InternalGrn.objects.filter(user_site=dname).update(user_site=name)
			PurchaseOrder.objects.filter(issuing_site=dname).update(issuing_site=name)
			PurchaseOrder.objects.filter(user_site=dname).update(user_site=name)
			PurchaseItem.objects.filter(purchase_location=dname).update(purchase_location=name)
			MaintainanceBill.objects.filter(user_site=dname).update(user_site=name)
			Fuel.objects.filter(user_site=dname).update(user_site=name)
			Reserviour.objects.filter(user_site=dname).update(user_site=name)
			FuelPurchase.objects.filter(issuing_site=dname).update(issuing_site=name)
			FuelPurchase.objects.filter(purchase_location=dname).update(purchase_location=name)
			FuelPurchase.objects.filter(user_site=dname).update(user_site=name)
			FuelBill.objects.filter(issuing_site=dname).update(issuing_site=name)
			FuelBill.objects.filter(purchase_location=dname).update(purchase_location=name)
			FuelBill.objects.filter(user_site=dname).update(user_site=name)
			DamageEntry.objects.filter(user_site=dname).update(user_site=name)
			ReturnEntry.objects.filter(user_site=dname).update(user_site=name)
			InternalDamageEntry.objects.filter(user_site=dname).update(user_site=name)
			VehicleList.objects.filter(current=dname).update(current=name)
			FuelLeakage.objects.filter(user_site=dname).update(user_site=name)
			messages.info(request, 'done')
			return redirect('site_display')
	else:
		return redirect('site_display')


@user_access
def delete_site(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		Site.objects.filter(id=sid).delete()
		messages.info(request, 'done')
		return redirect('site_display')
	else:
		return redirect('site_display')


@user_access
def deactivate_site(request):
	if request.method=="POST":
		sid = request.POST.get('sid')
		ss = Site.objects.get(id=sid)
		sname = ss.name

		if UserDetail.objects.filter(site=sname).exists():
			uu = UserDetail.objects.filter(site=sname)
			for u in uu:
				uuid = u.id
				uid = u.user_id
				u = User.objects.get(id=uid)
				u.is_staff = False
				u.is_superuser = False
				u.is_active = False
				u.save()
				UserDetail.objects.filter(id=uuid).update(active_status='no')
		Site.objects.filter(id=sid).update(active_status='no')
		messages.info(request, 'done')
		return redirect('site_display')
	else:
		return redirect('site_display')


@user_access
def purchase_order(request):
	supplier_dash = Supplier.objects.all()
	location_dash = Location.objects.all()
	v_type = VehicleType.objects.all()
	uom_dash = UOM.objects.all()
	u_site = user_site(request)
	item_dash = StockItem.objects.all()
	pon = 0
	if PurchaseOrder.objects.last():
		good = PurchaseOrder.objects.last()
		ng = good.pon_count
		pon = int(ng) + 1
	else:
		pon = pon + 1

	vehis = []
	seen =set()
	seen_add = seen.add
	ent = VehicleList.objects.values_list('vehicle_type_id', flat=True)
	ent = [x for x in ent if not (x in seen or seen_add(x))]
	for e in ent:
		vehi = VehicleList.objects.filter(vehicle_type_id=e, active_status='yes')
		n = len(vehi)
		vehis.append([vehi, range(1,n)])

	itemsel = []
	seen =set()
	seen_add = seen.add
	ent = StockItem.objects.values_list('main_url', flat=True)
	ent = [x for x in ent if not (x in seen or seen_add(x))]
	for e in ent:
		isel = StockItem.objects.filter(main_url=e)
		n = len(isel)
		itemsel.append([isel, range(1,n)])

	stock_cat = StockCategory.objects.all()
	psupa = []
	seen = set()
	seen_add = seen.add
	tran = StockSubCategory.objects.values_list('cat_url', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for r in ent:
		ps = StockSubCategory.objects.filter(cat_url=r)
		n = len(ps)
		psupa.append([ps, range(1,n)])

	context = {'vehis': vehis, 'stock_cat': stock_cat, 'psupa': psupa, 'itemsel': itemsel, 'v_type': v_type, 'supplier_dash': supplier_dash, 'location_dash': location_dash, 'uom_dash': uom_dash, 'item_dash': item_dash, 'pon': pon, 'u_site': u_site}    
	return render(request, 'purchase_order.html', context)


@user_access
def purchase_order_display(request):
	u_site = user_site(request)
	u_status = user_role(request)
	s_item = []
	if u_status == 'main_admin' or u_status == 'main_staff':
		s_it = PurchaseOrder.objects.all().order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_it, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_item.append([product, range(1, n)])
	else:
		s_it = PurchaseOrder.objects.filter(user_site=u_site).order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_it, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_item.append([product, range(1, n)])
	context = {'s_item': s_item}    
	return render(request, 'display/purchase_order_display.html', context)


@user_access
def purchase_order_detail(request,gid):
	if PurchaseOrder.objects.filter(id=gid).exists():
		site_dash = Site.objects.filter(active_status='yes')
		item = PurchaseOrder.objects.filter(id=gid).first()
		s_goods = PurchaseItem.objects.filter(purchase_order_id=gid)
		context = {'item': item, 's_goods': s_goods, 'site_dash': site_dash}    
		return render(request, 'display/purchase_order_detail.html', context)
	else:
		return redirect('purchase_order_display')


@user_access
def search_purchase_order(request):
	if request.method == "POST":
		search = request.POST.get('search')
		sea = search.upper()
		se = search.title()
		s = search.lower()
		u_site = user_site(request)
		u_status = user_role(request)
		if u_status == 'main_admin' or u_status == 'main_staff':
			lookup = Q(purchase_number=search) | Q(issuing_site__icontains=search) | Q(narration__icontains=search) | Q(purchase_number=sea) | Q(issuing_site=sea) | Q(purchase_number=se) | Q(issuing_site=se) | Q(purchase_number=s) | Q(issuing_site=s)
		else:
			lookup = Q(Q(purchase_number=search) | Q(purchase_number=sea) | Q(purchase_number=se) | Q(purchase_number=s) | Q(narration__icontains=search)) & Q(user_site=u_site)
		s_goods = []
		s_goo = PurchaseOrder.objects.filter(lookup).order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_goo, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_goods.append([product, range(1, n)])
		context = {'s_goods': s_goods, 'search': search}
		return render(request, 'display/purchase_order_search.html', context)
	else:
		return redirect('purchase_order_display')


@user_access
def print_purchase_order(request):
	if request.method=="POST":
		jid = request.POST.get('jid')
		s_good = PurchaseOrder.objects.filter(id=jid).first()
		igoods = PurchaseItem.objects.filter(purchase_order_id=jid)

		context = {'a': s_good, 'igoods': igoods}
		pdf = render_to_pdf('print_purchase_order.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			rnum = random.randint(11111111, 99999999)
			filename = "Reportgoods_%s.pdf" %(rnum)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")
	else:
		return redirect('purchase_order_display')


@user_access
def delete_purchase_order(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		PurchaseOrder.objects.filter(id=sid).delete()
		PurchaseItem.objects.filter(purchase_order_id=sid).delete()
		messages.info(request, 'done')
		return redirect('purchase_order_display')
	else:
		return redirect('purchase_order_display')


@user_access
def cancel_purchase_order(request, pid):
	if PurchaseOrder.objects.filter(id=pid).exists():
		current_user = request.user.username
		u_site = user_site(request)

		p = PurchaseOrder.objects.filter(id=pid).first()
		pon = p.purchase_number
		if GoodsEntry.objects.filter(purchase_order_number=pon).exists():
			messages.info(request, 'error')
			return redirect('/purchase-order-detail/'+str(pid)+'/')
		if PurchaseEntry.objects.filter(purchase_order_number=pon).exists():
			messages.info(request, 'error')
			return redirect('/purchase-order-detail/'+str(pid)+'/')
		us_site = p.user_site
		PurchaseOrder.objects.filter(id=pid).update(cancelled_by=current_user, status="cancelled")

		notify_topic = 'purchase_order'
		content_id = pid
		content = 'purchase_order_cancel'
		from_site = u_site
		from_user = current_user
		content_val = pon
		content_val3 = us_site

		q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, from_site=from_site, from_user=from_user, content_val=content_val, content_val3=content_val3)
		q.save()

		messages.info(request, 'done')
		return redirect('/purchase-order-detail/'+str(pid)+'/')
	else:
		return redirect('purchase_order_display')


@user_access
def approve_purchase_order(request):
	if request.method=="POST":
		pid = request.POST.get('pid')
		current_user = request.user.username
		u_site = user_site(request)

		p = PurchaseOrder.objects.filter(id=pid).first()
		pon = p.purchase_number
		us_site = p.user_site
		items = PurchaseItem.objects.filter(purchase_order_id=pid)
		for i in items:
			iid = i.id
			iname = i.item
			plocate = request.POST.get('plocate'+str(iid))
			PurchaseItem.objects.filter(id=iid).update(purchase_location=plocate)

			notify_topic = 'purchase_order'
			content_id = pid
			content = 'purchase_order_approve_location'
			from_site = u_site
			from_user = current_user
			content_val = pon
			content_val1 = iname
			content_val2 = plocate

			q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, from_site=from_site, from_user=from_user, content_val=content_val, content_val1=content_val1, content_val2=content_val2)
			q.save()
		PurchaseOrder.objects.filter(id=pid).update(approved_by=current_user, status="approved")

		notify_topic = 'purchase_order'
		content_id = pid
		content = 'purchase_order_approve'
		from_site = u_site
		from_user = current_user
		content_val = pon
		content_val3 = us_site

		q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, from_site=from_site, from_user=from_user, content_val=content_val, content_val3=content_val3)
		q.save()

		messages.info(request, 'done')
		return redirect('/purchase-order-detail/'+str(pid)+'/')
	else:
		return redirect('purchase_order_display')


@user_access
def purchase_order_edit(request, gid):
	if PurchaseOrder.objects.filter(id=gid).exists():
		item = PurchaseOrder.objects.filter(id=gid).first()
		igoods = PurchaseItem.objects.filter(purchase_order_id=gid)
		goods_count = []
		a = 0
		for b in igoods:
			a = a+1
			goods_count.append(a)

		supplier_dash = Supplier.objects.all()
		location_dash = Location.objects.all()
		vehicle_dash = Vehicle.objects.all()
		uom_dash = UOM.objects.all()
		u_site = user_site(request)
		item_dash = StockItem.objects.all()
		v_type = VehicleType.objects.all()
		vehis = []
		seen =set()
		seen_add = seen.add
		ent = VehicleList.objects.values_list('vehicle_type_id', flat=True)
		ent = [x for x in ent if not (x in seen or seen_add(x))]
		for e in ent:
			vehi = VehicleList.objects.filter(vehicle_type_id=e, active_status='yes')
			n = len(vehi)
			vehis.append([vehi, range(1,n)])

		itemsel = []
		seen =set()
		seen_add = seen.add
		ent = StockItem.objects.values_list('main_url', flat=True)
		ent = [x for x in ent if not (x in seen or seen_add(x))]
		for e in ent:
			isel = StockItem.objects.filter(main_url=e)
			n = len(isel)
			itemsel.append([isel, range(1,n)])

		stock_cat = StockCategory.objects.all()
		psupa = []
		seen = set()
		seen_add = seen.add
		tran = StockSubCategory.objects.values_list('cat_url', flat=True).distinct()
		ent = [x for x in tran if not (x in seen or seen_add(x))]
		for r in ent:
			ps = StockSubCategory.objects.filter(cat_url=r)
			n = len(ps)
			psupa.append([ps, range(1,n)])

		context = {'item': item, 'stock_cat': stock_cat, 'psupa': psupa, 'itemsel': itemsel, 'igoods': igoods, 'v_type': v_type, 'vehis': vehis, 'goods_count': goods_count, 'supplier_dash': supplier_dash, 'location_dash': location_dash, 'vehicle_dash': vehicle_dash, 'uom_dash': uom_dash, 'item_dash': item_dash}    
		return render(request, 'edit_purchase_order.html', context)
	else:
		return redirect('purchase_order_display')


@user_access
def add_purchase_order(request):
	if request.method=="POST":
		current_user = request.user.username
		date = request.POST.get('date')
		pon = request.POST.get('pon')
		pon_count = request.POST.get('pon_count')
		issue_site = request.POST.get('issue_site')
		po = request.POST.get('po')
		narrat = request.POST.get('narrat')
		itemadd = request.POST.getlist('itemadd')
		u_site = user_site(request)
		vehi_type = ''
		vehi_type_id = ''
		vehi_num = ''
		num_type = ''

		for a in itemadd:
			a = str(a)
			itemid = request.POST.get('inameid'+a)
			if StockEntry.objects.filter(item_id=itemid, stock_site=u_site).exists():
				print('ok')
			else:
				messages.info(request, 'error')
				return redirect('purchase_order')

		if po == 'yes':
			vehi_type = request.POST.get('vehicle_type')
			vehi_type_id = request.POST.get('vehicle_type_id')
			vehi_num = request.POST.get('vehicle')
			num_type = request.POST.get('num_type')

		if PurchaseOrder.objects.filter(purchase_number=pon).exists():
			messages.info(request, 'error')
			return redirect('purchase_order')
		else:
			query = PurchaseOrder(entry_date=date, purchase_number=pon, po_vehi=po, vehicle_type=vehi_type, vehicle_type_id=vehi_type_id, vehicle_number=vehi_num, number_type=num_type, narration=narrat, pon_count=pon_count, issuing_site=issue_site, entry_by=current_user, user_site=u_site)
			query.save()

		gid = query.id
		for a in itemadd:
			a = str(a)
			itemid = request.POST.get('inameid'+a)
			item = request.POST.get('iname'+a)
			alias = request.POST.get('ialias'+a)
			uom = request.POST.get('iuom'+a)
			qty = request.POST.get('iqty'+a)
			desc = request.POST.get('idesc'+a)
			que = PurchaseItem(purchase_order_id=gid, pon=pon, description=desc, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty)
			que.save()

		pr = Site.objects.filter(role='admin', active_status='yes').first()

		notify_topic = 'purchase_order'
		content_id = gid
		content = 'purchase_order_add'
		from_site = u_site
		from_user = current_user
		content_val = pon
		content_val2 = pr.name
		q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, from_site=from_site, from_user=from_user, content_val=content_val, content_val2=content_val2)
		q.save()
		messages.info(request, 'done')
		return redirect('purchase_order')
	else:
		return redirect('purchase_order')


@user_access
def edit_purchase_order(request):
	if request.method=="POST":
		gid = request.POST.get('gid')
		date = request.POST.get('date')
		pon = request.POST.get('pon')
		pon_count = request.POST.get('pon_count')
		po = request.POST.get('po')
		narrat = request.POST.get('narrat')
		issue_site = request.POST.get('issue_site')
		itemadd = request.POST.getlist('itemadd')
		vehi_type = ''
		vehi_type_id = ''
		vehi_num = ''
		num_type = ''

		ge = PurchaseOrder.objects.filter(id=gid).first()
		u_site = ge.issuing_site

		for a in itemadd:
			a = str(a)
			itemid = request.POST.get('inameid'+a)
			if StockEntry.objects.filter(item_id=itemid, stock_site=u_site).exists():
				print('ok')
			else:
				messages.info(request, 'error')
				return redirect('/purchase-order-edit/'+str(gid)+'/')

		if po == 'yes':
			vehi_type = request.POST.get('vehicle_type')
			vehi_type_id = request.POST.get('vehicle_type_id')
			vehi_num = request.POST.get('vehicle')
			num_type = request.POST.get('num_type')
		
		PurchaseOrder.objects.filter(id=gid).update(entry_date=date, narration=narrat, po_vehi=po, vehicle_type=vehi_type, vehicle_type_id=vehi_type_id, vehicle_number=vehi_num, number_type=num_type, issuing_site=issue_site)

		PurchaseItem.objects.filter(purchase_order_id=gid).delete()
		for a in itemadd:
			a = str(a)
			itemid = request.POST.get('inameid'+a)
			item = request.POST.get('iname'+a)
			uom = request.POST.get('iuom'+a)
			alias = request.POST.get('ialias'+a)
			qty = request.POST.get('iqty'+a)
			desc = request.POST.get('idesc'+a)
			que = PurchaseItem(purchase_order_id=gid, description=desc, pon=pon, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty)
			que.save()
		messages.info(request, 'done')
		return redirect('/purchase-order-edit/'+str(gid)+'/')
	else:
		return redirect('purchase_order_display')


@user_access
def quotation_entry(request):
	supplier_dash = Supplier.objects.all()
	uom_dash = UOM.objects.all()
	item_dash = StockItem.objects.all()

	qsupplier = []
	tran = QuotationEntry.objects.values('supplier')
	trans = {item['supplier'] for item in tran}
	for s in trans:
		qsupplier.append(s)

	context = {'supplier_dash': supplier_dash, 'uom_dash': uom_dash, 'item_dash': item_dash, 'qsupplier': qsupplier}    
	return render(request, 'quotation_entry.html', context)


@user_access
def quotation_display(request):
	s_item = QuotationEntry.objects.all().order_by('-id')[:30]
	context = {'s_item': s_item}    
	return render(request, 'display/quotation_display.html', context)


@user_access
def quotation_detail(request,gid):
	if QuotationEntry.objects.filter(id=gid).exists():
		item = QuotationEntry.objects.filter(id=gid).first()
		s_goods = QuotationItem.objects.filter(quotationid=gid)
		context = {'item': item, 's_goods': s_goods}    
		return render(request, 'display/quotation_detail.html', context)
	else:
		return redirect('quotation_display')


@user_access
def search_quotation(request):
	if request.method == "POST":
		search = request.POST.get('search')
		sea = search.upper()
		se = search.title()
		s = search.lower()
		lookup = Q(supplier_name=search) | Q(supplier_name=sea) | Q(supplier_name=se) | Q(supplier_name=s)
		s_goods = QuotationEntry.objects.filter(lookup).order_by('-id')
		context = {'s_goods': s_goods, 'search': search}
		return render(request, 'display/quotation_search.html', context)
	else:
		return redirect('quotation_display')


@user_access
def print_quotation(request):
	if request.method=="POST":
		jid = request.POST.get('jid')
		s_good = QuotationEntry.objects.filter(id=jid).first()
		igoods = QuotationItem.objects.filter(quotationid=jid)

		context = {'a': s_good, 'igoods': igoods}
		pdf = render_to_pdf('printquotation.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			rnum = random.randint(11111111, 99999999)
			filename = "Reportquotation_%s.pdf" %(rnum)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")
	else:
		return redirect('quotation_display')


@user_access
def delete_quotation(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		QuotationEntry.objects.filter(id=sid).delete()
		QuotationItem.objects.filter(quotationid=sid).delete()
		messages.info(request, 'done')
		return redirect('quotation_display')
	else:
		return redirect('quotation_display')


@user_access
def quotation_edit(request, gid):
	if QuotationEntry.objects.filter(id=gid).exists():
		item = QuotationEntry.objects.filter(id=gid).first()
		igoods = QuotationItem.objects.filter(quotationid=gid)
		goods_count = []
		a = 0
		for b in igoods:
			a = a+1
			goods_count.append(a)

		supplier_dash = Supplier.objects.all()
		uom_dash = UOM.objects.all()
		item_dash = StockItem.objects.all()

		qsupplier = []
		tran = QuotationEntry.objects.values('supplier')
		trans = {item['supplier'] for item in tran}
		for s in trans:
			qsupplier.append(s) 

		context = {'item': item, 'igoods': igoods, 'goods_count': goods_count, 'supplier_dash': supplier_dash, 'uom_dash': uom_dash, 'item_dash': item_dash, 'qsupplier': qsupplier}    
		return render(request, 'quotation_edit.html', context)
	else:
		return redirect('quotation_display')


@user_access
def add_quotation(request):
	if request.method=="POST":
		current_user = request.user.username
		u_site = user_site(request)
		date = request.POST.get('date')
		valid_date = request.POST.get('valid_date')
		supplier = request.POST.get('supplier')
		itemadd = request.POST.getlist('itemadd')
		sup = Supplier.objects.filter(id=supplier).first()
		sup_name = sup.name
		sup_address = sup.address
		sup_contact = sup.landline

		if QuotationEntry.objects.filter(supplier=supplier).exists():
			messages.info(request, 'error')
			return redirect('quotation_entry')
		else:
			query = QuotationEntry(entry_date=date, valid_date=valid_date, supplier=supplier, supplier_name=sup_name, supplier_address=sup_address, supplier_contact=sup_contact, entry_by=current_user, user_site=u_site)
			query.save()

		gid = query.id
		for a in itemadd:
			a = str(a)
			itemid = request.POST.get('inameid'+a)
			item = request.POST.get('iname'+a)
			uom = request.POST.get('iuom'+a)
			rate = request.POST.get('irate'+a)
			que = QuotationItem(quotationid=gid, item_id=itemid, item=item, uom=uom, rate=rate)
			que.save()
		messages.info(request, 'done')
		return redirect('quotation_entry')
	else:
		return redirect('quotation_entry')


@user_access
def edit_quotation(request):
	if request.method=="POST":
		gid = request.POST.get('gid')
		date = request.POST.get('date')
		valid_date = request.POST.get('valid_date')
		supplier = request.POST.get('supplier')
		itemadd = request.POST.getlist('itemadd')
		sup = Supplier.objects.filter(id=supplier).first()
		sup_name = sup.name
		sup_address = sup.address
		sup_contact = sup.landline

		QuotationEntry,objects.filter(id=gid).update(entry_date=date, valid_date=valid_date, supplier_id=supplier, supplier_name=sup_name, supplier_address=sup_address, supplier_contact=sup_contact, entry_by='amish')

		QuotationItem.objects.filter(quotationid=gid).delete()
		for a in itemadd:
			a = str(a)
			itemid = request.POST.get('inameid'+a)
			item = request.POST.get('iname'+a)
			uom = request.POST.get('iuom'+a)
			rate = request.POST.get('irate'+a)
			que = QuotationItem(quotationid=gid, item_id=itemid, item=item, uom=uom, rate=rate)
			que.save()
		messages.info(request, 'done')
		return redirect('/quotation-edit/'+str(gid)+'/')
	else:
		return redirect('quotation_display')


def notify(request):
	notify  = []
	checked = []
	len1 = 0
	len2 = 0
	noti_c = 0
	current_user = request.user.username
	udet = UserDetail.objects.filter(user_name=current_user).first()
	status = udet.status
	if status == 'main_admin':
		npp = []
		np = NotificationPermission.objects.filter(main_admin='yes')
		for i in np:
			ii = i.url
			npp.append(ii)
		notify = Notification.objects.filter(notify_topic__in=npp, status='pending').order_by('-id')
		checked = Notification.objects.filter(notify_topic__in=npp, status='checked').order_by('-id')
		noti_c = Notification.objects.filter(notify_topic__in=npp, status='pending').count()
		# lookup1 = Q(Q(notify_topic='purchase_order') | Q(notify_topic='grn') | Q(notify_topic='purchase_invoice_entry') | Q(notify_topic='material_issue') | Q(notify_topic='internal_transfer') | Q(notify_topic='out_sales_entry')) & Q(status='pending') & Q(main_admin='yes')
		# lookup2 = Q(Q(notify_topic='purchase_order') | Q(notify_topic='grn') | Q(notify_topic='purchase_invoice_entry') | Q(notify_topic='material_issue') | Q(notify_topic='internal_transfer') | Q(notify_topic='out_sales_entry')) & Q(status='checked') & Q(main_admin='yes')
	if status == 'main_staff':
		npp = []
		np = NotificationPermission.objects.filter(main_staff='yes')
		for i in np:
			ii = i.url
			npp.append(ii)
		notify = Notification.objects.filter(notify_topic__in=npp, status='pending').order_by('-id')
		checked = Notification.objects.filter(notify_topic__in=npp, status='checked').order_by('-id')
		noti_c = Notification.objects.filter(notify_topic__in=npp, status='pending').count()
	if status == 'site_admin':
		npp = []
		np = NotificationPermission.objects.filter(site_admin='yes')
		for i in np:
			ii = i.url
			npp.append(ii)
		notify = Notification.objects.filter(notify_topic__in=npp, status='pending').order_by('-id')
		checked = Notification.objects.filter(notify_topic__in=npp, status='checked').order_by('-id')
		noti_c = Notification.objects.filter(notify_topic__in=npp, status='pending').count()
	if status == 'site_staff':
		npp = []
		np = NotificationPermission.objects.filter(site_staff='yes')
		for i in np:
			ii = i.url
			npp.append(ii)
		notify = Notification.objects.filter(notify_topic__in=npp, status='pending').order_by('-id')
		checked = Notification.objects.filter(notify_topic__in=npp, status='checked').order_by('-id')
		noti_c = Notification.objects.filter(notify_topic__in=npp, status='pending').count()
	len1 = len(notify)
	len2 = len(checked)
	context = {'noti_c': noti_c, 'notify': notify, 'checked': checked, 'len1': len1, 'len2': len2}    
	return render(request, 'display/notify.html', context)


def noti_count(request):
	noti_c = 0
	current_user = request.user.username
	udet = UserDetail.objects.filter(user_name=current_user).first()
	status = udet.status
	site = udet.site
	if status == 'main_admin':
		npp = []
		np = NotificationPermission.objects.filter(main_admin='yes')
		for i in np:
			ii = i.url
			npp.append(ii)
		noti_c = Notification.objects.filter(notify_topic__in=npp, status='pending').count()
	if status == 'main_staff':
		npp = []
		np = NotificationPermission.objects.filter(main_staff='yes')
		for i in np:
			ii = i.url
			npp.append(ii)
		noti_c = Notification.objects.filter(notify_topic__in=npp, status='pending').count()
	if status == 'site_admin':
		npp = []
		np = NotificationPermission.objects.filter(site_admin='yes')
		for i in np:
			ii = i.url
			npp.append(ii)
		noti_c = Notification.objects.filter(Q(Q(notify_topic__in=npp) & Q(status='pending')) & Q(Q(from_site=site) | Q(content_val2=site) | Q(content_val3=site))).count()
	if status == 'site_staff':
		npp = []
		np = NotificationPermission.objects.filter(site_staff='yes')
		for i in np:
			ii = i.url
			npp.append(ii)
		noti_c = Notification.objects.filter(Q(Q(notify_topic__in=npp) & Q(status='pending')) & Q(Q(from_site=site) | Q(content_val2=site) | Q(content_val3=site))).count()

	context = {'noti_c': noti_c}    
	return render(request, 'display/noti_count.html', context)


def noti(request):
	notify  = []
	checked = []
	len1 = 0
	len2 = 0
	noti_c = 0
	current_user = request.user.username
	udet = UserDetail.objects.filter(user_name=current_user).first()
	status = udet.status
	site = udet.site
	todate = date.today()
	if status == 'main_admin':
		npp = []
		np = NotificationPermission.objects.filter(main_admin='yes')
		for i in np:
			ii = i.url
			npp.append(ii)
		notify = Notification.objects.filter(notify_topic__in=npp, status='pending').order_by('-id')
		checked = Notification.objects.filter(notify_topic__in=npp, status='checked', date_on=todate).order_by('-id')
		noti_c = Notification.objects.filter(notify_topic__in=npp, status='pending').count()
		# lookup1 = Q(Q(notify_topic='purchase_order') | Q(notify_topic='grn') | Q(notify_topic='purchase_invoice_entry') | Q(notify_topic='material_issue') | Q(notify_topic='internal_transfer') | Q(notify_topic='out_sales_entry')) & Q(status='pending') & Q(main_admin='yes')
		# lookup2 = Q(Q(notify_topic='purchase_order') | Q(notify_topic='grn') | Q(notify_topic='purchase_invoice_entry') | Q(notify_topic='material_issue') | Q(notify_topic='internal_transfer') | Q(notify_topic='out_sales_entry')) & Q(status='checked') & Q(main_admin='yes')
	if status == 'main_staff':
		npp = []
		np = NotificationPermission.objects.filter(main_staff='yes')
		for i in np:
			ii = i.url
			npp.append(ii)
		notify = Notification.objects.filter(notify_topic__in=npp, status='pending').order_by('-id')
		checked = Notification.objects.filter(notify_topic__in=npp, status='checked', date_on=todate).order_by('-id')
		noti_c = Notification.objects.filter(notify_topic__in=npp, status='pending').count()
	if status == 'site_admin':
		npp = []
		np = NotificationPermission.objects.filter(site_admin='yes')
		for i in np:
			ii = i.url
			npp.append(ii)
		notify = Notification.objects.filter(Q(Q(notify_topic__in=npp) & Q(status='pending')) & Q(Q(from_site=site) | Q(content_val2=site) | Q(content_val3=site))).order_by('-id')
		checked = Notification.objects.filter(Q(Q(notify_topic__in=npp) & Q(status='checked') & Q(date_on=todate)) & Q(Q(from_site=site) | Q(content_val2=site) | Q(content_val3=site))).order_by('-id')
		noti_c = Notification.objects.filter(Q(Q(notify_topic__in=npp) & Q(status='pending')) & Q(Q(from_site=site) | Q(content_val2=site) | Q(content_val3=site))).count()
	if status == 'site_staff':
		npp = []
		np = NotificationPermission.objects.filter(site_staff='yes')
		for i in np:
			ii = i.url
			npp.append(ii)
		notify = Notification.objects.filter(Q(Q(notify_topic__in=npp) & Q(status='pending')) & Q(Q(from_site=site) | Q(content_val2=site) | Q(content_val3=site))).order_by('-id')
		checked = Notification.objects.filter(Q(Q(notify_topic__in=npp) & Q(status='checked') & Q(date_on=todate)) & Q(Q(from_site=site) | Q(content_val2=site) | Q(content_val3=site))).order_by('-id')
		noti_c = Notification.objects.filter(Q(Q(notify_topic__in=npp) & Q(status='pending')) & Q(Q(from_site=site) | Q(content_val2=site) | Q(content_val3=site))).count()
	len1 = len(notify)
	len2 = len(checked)

	context = {'notify': notify, 'checked': checked, 'len1': len1, 'len2': len2}    
	return render(request, 'display/noti.html', context)


def notify_check(request,nid,nt,cid):
	if Notification.objects.filter(id=nid).exists():
		Notification.objects.filter(id=nid).update(status='checked')
		if nt == 'purchase_order':
			return redirect('/purchase-order-detail/'+str(cid)+'/')
		if nt == 'grn':
			return redirect('/ashish-goods-detail/'+str(cid)+'/')
		if nt == 'purchase_invoice_entry':
			return redirect('/ashish-invoice-detail/'+str(cid)+'/')
		if nt == 'material_issue':
			return redirect('/material-issue-detail/'+str(cid)+'/')
		if nt == 'internal_transfer':
			return redirect('/internal-transfer-detail/'+str(cid)+'/')
		if nt == 'transfer_grn':
			return redirect('/transfer-goods-detail/'+str(cid)+'/')
		if nt == 'out_sales_entry':
			return redirect('/sales-detail/'+str(cid)+'/')
		if nt == 'fuel_purchase_order':
			return redirect('/fuel-purchase-order-detail/'+str(cid)+'/')
		if nt == 'damage_entry':
			return redirect('/damage-detail/'+str(cid)+'/')
		if nt == 'return_entry':
			return redirect('/return-detail/'+str(cid)+'/')
		if nt == 'movement':
			return redirect('/movement-detail/'+str(cid)+'/')
		if nt == 'grn_notify':
			return redirect('/ashish-invoice-detail/'+str(cid)+'/')
		if nt == 'credit_notify':
			return redirect('/ashish-invoice-detail/'+str(cid)+'/')
		if nt == 'internal_damage_entry':
			return redirect('/internal-damage-detail/'+str(cid)+'/')
	else:
		return redirect('home')


@user_access
def reports(request):
	item_dash = StockItem.objects.all()
	site_dash = Site.objects.all()
	f_type = FuelType.objects.all()
	v_type = VehicleType.objects.all()
	reserve = Reserviour.objects.all()
	supplier_dash = Supplier.objects.all()
	vehis = []
	seen =set()
	seen_add = seen.add
	ent = VehicleList.objects.values_list('vehicle_type_id', flat=True)
	ent = [x for x in ent if not (x in seen or seen_add(x))]
	for e in ent:
		vehi = VehicleList.objects.filter(vehicle_type_id=e)
		n = len(vehi)
		vehis.append([vehi, range(1,n)])
	context = {'item_dash': item_dash, 'site_dash': site_dash, 'f_type': f_type, 'vehis': vehis, 'v_type': v_type, 'reserve': reserve, 'supplier_dash': supplier_dash}    
	return render(request, 'report.html', context)


@user_access
def generate_report(request):
	if request.method == "POST":
		report = []
		item_val = ''
		site_val = ''
		vehicle_val = ''
		fsite = ''
		tsite = ''
		vehicle_type_val = ''
		num_type = ''
		fromdate = ''
		todate = ''
		total_opening = ''
		total_qty = ''
		total_amt = ''
		credit = ''
		cash = ''
		vh = ''
		eng = ''
		ch = ''
		report_val = request.POST.get('report_val')
		if report_val == 'stock_report':
			report_head = 'Stock Report'
			if request.POST.get('item'):
				if request.POST.get('site'):
					item_val = request.POST.get('item')
					site_val = request.POST.get('site')
					report = StockEntry.objects.filter(item=item_val, stock_site=site_val)
					total_opening = StockEntry.objects.filter(item=item_val, stock_site=site_val).aggregate(Sum('opening'))
					total_qty = StockEntry.objects.filter(item=item_val, stock_site=site_val).aggregate(Sum('quantity'))
				else:
					item_val = request.POST.get('item')
					report = StockEntry.objects.filter(item=item_val)
					total_opening = StockEntry.objects.filter(item=item_val).aggregate(Sum('opening'))
					total_qty = StockEntry.objects.filter(item=item_val).aggregate(Sum('quantity'))
			else:
				if request.POST.get('site'):
					site_val = request.POST.get('site')
					report = StockEntry.objects.filter(stock_site=site_val)

		if report_val == 'grn_report':
			report_head = 'GRN Report'
			if request.POST.get('fromdate') and request.POST.get('todate'):
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				if request.POST.get('item'):
					if request.POST.get('site'):
						item_val = request.POST.get('item')
						site_val = request.POST.get('site')
						grrn = GoodsEntry.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val)
						for r in grrn:
							grnn = r.id
							grrnn = GoodsEntry.objects.filter(id=grnn).first()
							goo = Goods.objects.filter(goodsid=grnn, item=item_val)
							gex = GoodsExtra.objects.filter(goodsid=grnn)
							report.append([grrnn,gex,goo])
					else:
						item_val = request.POST.get('item')
						grrn = GoodsEntry.objects.filter(entry_date__range=[fromdate, todate])
						for r in grrn:
							grnn = r.id
							gex = GoodsExtra.objects.filter(goodsid=grnn)
							goo = Goods.objects.filter(goodsid=grnn, item=item_val)
							for g in goo:
								ggid = g.id
								gid = g.goodsid
								grrnn = GoodsEntry.objects.filter(id=gid).first()
								report.append([grrnn,gex,goo])
				else:
					if request.POST.get('site'):
						site_val = request.POST.get('site')
						grrn = GoodsEntry.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val)
						for r in grrn:
							grnn = r.id
							grrnn = GoodsEntry.objects.filter(id=grnn).first()
							goo = Goods.objects.filter(goodsid=grnn)
							gex = GoodsExtra.objects.filter(goodsid=grnn)
							report.append([grrnn,gex,goo])

		if report_val == 'invoice_report':
			report_head = 'Invoice Report'
			if request.POST.get('fromdate') and request.POST.get('todate'):
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				if request.POST.get('item'):
					if request.POST.get('site'):
						item_val = request.POST.get('item')
						site_val = request.POST.get('site')
						grrn = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val)
						total_amt = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val).aggregate(Sum('total'))
						credit = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val, transaction_type='credit').aggregate(Sum('total'))
						cash = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val, transaction_type='cash').aggregate(Sum('total'))
						for r in grrn:
							grnn = r.id
							grrnn = PurchaseEntry.objects.filter(id=grnn).first()
							goo = InvoiceItem.objects.filter(purchaseid=grnn, item=item_val)
							report.append([grrnn,goo])
					else:
						item_val = request.POST.get('item')
						ppid = []
						grrn = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate])
						for r in grrn:
							grnn = r.id
							goo = InvoiceItem.objects.filter(purchaseid=grnn, item=item_val)
							for g in goo:
								ggid = g.id
								gid = g.goodsid
								ppid.append(gid)
								grrnn = PurchaseEntry.objects.filter(id=gid).first()
								report.append([grrnn,goo])
						total_amt = PurchaseEntry.objects.filter(id__in=ppid).aggregate(Sum('total'))
						credit = MaintainanceBill.objects.filter(id__in=ppid, transaction_type='credit').aggregate(Sum('total'))
						cash = MaintainanceBill.objects.filter(id__in=ppid, transaction_type='cash').aggregate(Sum('total'))
				else:
					if request.POST.get('site'):
						site_val = request.POST.get('site')
						grrn = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val)
						total_amt = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val).aggregate(Sum('total'))
						credit = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val, transaction_type='credit').aggregate(Sum('total'))
						cash = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val, transaction_type='cash').aggregate(Sum('total'))
						for r in grrn:
							grnn = r.id
							grrnn = PurchaseEntry.objects.filter(id=grnn).first()
							goo = InvoiceItem.objects.filter(purchaseid=grnn)
							report.append([grrnn,goo])

		if report_val == 'material_report':
			report_head = 'Material Issue Report'
			if request.POST.get('fromdate') and request.POST.get('todate'):
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				if request.POST.get('item'):
					if request.POST.get('site'):
						item_val = request.POST.get('item')
						site_val = request.POST.get('site')
						grrn = MaterialIssueEntry.objects.filter(issue_date__range=[fromdate, todate], user_site=site_val)
						for r in grrn:
							grnn = r.id
							grrnn = MaterialIssueEntry.objects.filter(id=grnn).first()
							goo = MaterialItem.objects.filter(materialid=grnn, item=item_val)
							report.append([grrnn,goo])
					else:
						item_val = request.POST.get('item')
						grrn = MaterialIssueEntry.objects.filter(issue_date__range=[fromdate, todate])
						for r in grrn:
							grnn = r.id
							goo = MaterialItem.objects.filter(materialid=grnn, item=item_val)
							for g in goo:
								ggid = g.id
								gid = g.goodsid
								grrnn = MaterialIssueEntry.objects.filter(id=gid).first()
								report.append([grrnn,goo])
				else:
					if request.POST.get('site'):
						site_val = request.POST.get('site')
						grrn = MaterialIssueEntry.objects.filter(issue_date__range=[fromdate, todate], user_site=site_val)
						for r in grrn:
							grnn = r.id
							grrnn = MaterialIssueEntry.objects.filter(id=grnn).first()
							goo = MaterialItem.objects.filter(materialid=grnn)
							report.append([grrnn,goo])

		if report_val == 'internal_report':
			report_head = 'Internal Transfer Report'
			if request.POST.get('fromdate') and request.POST.get('todate'):
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				if request.POST.get('item'):
					if request.POST.get('site'):
						item_val = request.POST.get('item')
						site_val = request.POST.get('site')
						grrn = InternalTransfer.objects.filter(issue_date__range=[fromdate, todate], user_site=site_val)
						for r in grrn:
							grnn = r.id
							grrnn = InternalTransfer.objects.filter(id=grnn).first()
							goo = TransferItem.objects.filter(transferid=grnn, item=item_val)
							report.append([grrnn,goo])
					else:
						item_val = request.POST.get('item')
						grrn = InternalTransfer.objects.filter(issue_date__range=[fromdate, todate])
						for r in grrn:
							grnn = r.id
							goo = TransferItem.objects.filter(transferid=grnn, item=item_val)
							for g in goo:
								ggid = g.id
								gid = g.goodsid
								grrnn = InternalTransfer.objects.filter(id=gid).first()
								report.append([grrnn,goo])
				else:
					if request.POST.get('site'):
						site_val = request.POST.get('site')
						grrn = InternalTransfer.objects.filter(issue_date__range=[fromdate, todate], user_site=site_val)
						for r in grrn:
							grnn = r.id
							grrnn = InternalTransfer.objects.filter(id=grnn).first()
							goo = TransferItem.objects.filter(transferid=grnn)
							report.append([grrnn,goo])

		if report_val == 'transfer_grn':
			report_head = 'Internal Transfer GRN Report'
			if request.POST.get('fromdate') and request.POST.get('todate'):
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				if request.POST.get('item'):
					if request.POST.get('site'):
						item_val = request.POST.get('item')
						site_val = request.POST.get('site')
						grrn = InternalGrn.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val)
						for r in grrn:
							grnn = r.id
							grrnn = InternalGrn.objects.filter(id=grnn).first()
							goo = InternalGrnItems.objects.filter(goodsid=grnn, item=item_val)
							report.append([grrnn,goo])
					else:
						item_val = request.POST.get('item')
						grrn = InternalGrn.objects.filter(entry_date__range=[fromdate, todate])
						for r in grrn:
							grnn = r.id
							goo = InternalGrnItems.objects.filter(goodsid=grnn, item=item_val)
							for g in goo:
								ggid = g.id
								gid = g.goodsid
								grrnn = InternalGrn.objects.filter(id=gid).first()
								report.append([grrnn,goo])
				else:
					if request.POST.get('site'):
						site_val = request.POST.get('site')
						grrn = InternalGrn.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val)
						for r in grrn:
							grnn = r.id
							grrnn = InternalGrn.objects.filter(id=grnn).first()
							goo = InternalGrnItems.objects.filter(goodsid=grnn)
							report.append([grrnn,goo])

		if report_val == 'fuel_purchase':
			report_head = 'Reserviour-wise Fuel Purchase Report'
			if request.POST.get('fromdate') and request.POST.get('todate'):
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				if request.POST.get('item'):
					if request.POST.get('site'):
						item_val = request.POST.get('item')
						site_val = request.POST.get('site')
						report = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val, fuel_type=item_val).order_by('entry_date')
						total_qty = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val, fuel_type=item_val).aggregate(Sum('quantity'))
						total_amt = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val, fuel_type=item_val).aggregate(Sum('amount'))
					else:
						item_val = request.POST.get('item')
						report = FuelBill.objects.filter(entry_date__range=[fromdate, todate], fuel_type=item_val).order_by('entry_date')
						total_qty = FuelBill.objects.filter(entry_date__range=[fromdate, todate], fuel_type=item_val).aggregate(Sum('quantity'))
						total_amt = FuelBill.objects.filter(entry_date__range=[fromdate, todate], fuel_type=item_val).aggregate(Sum('amount'))
				else:
					if request.POST.get('site'):
						site_val = request.POST.get('site')
						report = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val).order_by('entry_date')
						total_qty = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val).aggregate(Sum('quantity'))
						total_amt = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val).aggregate(Sum('amount'))

		if report_val == 'vehicle_fuel':
			report_head = 'Vehicle-wise Fuel Consumption Report'
			if request.POST.get('fromdate') and request.POST.get('todate'):
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				if request.POST.get('vehicle_type_name'):
					if request.POST.get('vehicle'):
						if request.POST.get('site'):
							if request.POST.get('item'):
								item_val = request.POST.get('item')
								site_val = request.POST.get('site')
								vehicle_val = request.POST.get('vehicle')
								vehicle_type_val = request.POST.get('vehicle_type_name')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(reserviour=site_val) & Q(fuel_type=item_val) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))) .order_by('date')
								total_qty = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(reserviour=site_val) & Q(fuel_type=item_val) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('quantity'))
							else:
								site_val = request.POST.get('site')
								vehicle_val = request.POST.get('vehicle')
								vehicle_type_val = request.POST.get('vehicle_type_name')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(reserviour=site_val) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('date')
								total_qty = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(reserviour=site_val) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('quantity'))
						else:
							if request.POST.get('item'):
								item_val = request.POST.get('item')
								vehicle_val = request.POST.get('vehicle')
								vehicle_type_val = request.POST.get('vehicle_type_name')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(fuel_type=item_val) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('date')
								total_qty = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(fuel_type=item_val) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('quantity'))
							else:
								vehicle_val = request.POST.get('vehicle')
								vehicle_type_val = request.POST.get('vehicle_type_name')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('date')
								total_qty = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('quantity'))
					else:
						if request.POST.get('site'):
							if request.POST.get('item'):
								item_val = request.POST.get('item')
								site_val = request.POST.get('site')
								vehicle_type_val = request.POST.get('vehicle_type_name')
								report = Fuel.objects.filter(date__range=[fromdate, todate], reserviour=site_val, fuel_type=item_val, vehicle_type=vehicle_type_val).order_by('date')
								total_qty = Fuel.objects.filter(date__range=[fromdate, todate], reserviour=site_val, fuel_type=item_val, vehicle_type=vehicle_type_val).aggregate(Sum('quantity'))
							else:
								site_val = request.POST.get('site')
								vehicle_type_val = request.POST.get('vehicle_type_name')
								report = Fuel.objects.filter(date__range=[fromdate, todate], reserviour=site_val, vehicle_type=vehicle_type_val).order_by('date')
								total_qty = Fuel.objects.filter(date__range=[fromdate, todate], reserviour=site_val, vehicle_type=vehicle_type_val).aggregate(Sum('quantity'))
						else:
							if request.POST.get('item'):
								item_val = request.POST.get('item')
								vehicle_type_val = request.POST.get('vehicle_type_name')
								report = Fuel.objects.filter(date__range=[fromdate, todate], fuel_type=item_val, vehicle_type=vehicle_type_val).order_by('date')
								total_qty = Fuel.objects.filter(date__range=[fromdate, todate], fuel_type=item_val, vehicle_type=vehicle_type_val).aggregate(Sum('quantity'))
							else:
								vehicle_type_val = request.POST.get('vehicle_type_name')
								report = Fuel.objects.filter(date__range=[fromdate, todate], vehicle_type=vehicle_type_val).order_by('date')
								total_qty = Fuel.objects.filter(date__range=[fromdate, todate], vehicle_type=vehicle_type_val).aggregate(Sum('quantity'))
				else:
					if request.POST.get('vehicle'):
						if request.POST.get('site'):
							if request.POST.get('item'):
								item_val = request.POST.get('item')
								site_val = request.POST.get('site')
								vehicle_val = request.POST.get('vehicle')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(reserviour=site_val) & Q(fuel_type=item_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('date')
								total_qty = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(reserviour=site_val) & Q(fuel_type=item_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('quantity'))
							else:
								site_val = request.POST.get('site')
								vehicle_val = request.POST.get('vehicle')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(reserviour=site_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('date')
								total_qty = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(reserviour=site_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('quantity'))
						else:
							if request.POST.get('item'):
								item_val = request.POST.get('item')
								vehicle_val = request.POST.get('vehicle')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(fuel_type=item_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('date')
								total_qty = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(fuel_type=item_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('quantity'))
							else:
								vehicle_val = request.POST.get('vehicle')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('date')
								total_qty = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('quantity'))
					else:
						if request.POST.get('site'):
							if request.POST.get('item'):
								item_val = request.POST.get('item')
								site_val = request.POST.get('site')
								report = Fuel.objects.filter(date__range=[fromdate, todate], reserviour=site_val, fuel_type=item_val).order_by('date')
								total_qty = Fuel.objects.filter(date__range=[fromdate, todate], reserviour=site_val, fuel_type=item_val).aggregate(Sum('quantity'))
							else:
								site_val = request.POST.get('site')
								report = Fuel.objects.filter(date__range=[fromdate, todate], reserviour=site_val).order_by('date')
								total_qty = Fuel.objects.filter(date__range=[fromdate, todate], reserviour=site_val).aggregate(Sum('quantity'))
						else:
							if request.POST.get('item'):
								item_val = request.POST.get('item')
								report = Fuel.objects.filter(date__range=[fromdate, todate], fuel_type=item_val).order_by('date')
								total_qty = Fuel.objects.filter(date__range=[fromdate, todate], fuel_type=item_val).aggregate(Sum('quantity'))
							else:
								vehicle_type_val = request.POST.get('vehicle_type_name')
								report = Fuel.objects.filter(date__range=[fromdate, todate]).order_by('date')
								total_qty = Fuel.objects.filter(date__range=[fromdate, todate]).aggregate(Sum('quantity'))

		if report_val == 'maintain_log':
			report_head = 'All Maintainance Log'
			if request.POST.get('fromdate') and request.POST.get('todate'):
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				if request.POST.get('site'):
					site_val = request.POST.get('site')
					report = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val).order_by('entry_date')
					total_amt = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val).aggregate(Sum('total'))
				else:
					report = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate]).order_by('entry_date')
					total_amt = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate]).aggregate(Sum('total'))

		if report_val == 'vehicle_maintain':
			report_head = 'Vehicle-wise Maintainance Log'
			if request.POST.get('fromdate') and request.POST.get('todate'):
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				if request.POST.get('vehicle_type_name') or request.POST.get('vehicle'):
					if request.POST.get('vehicle_type_name'):
						if request.POST.get('vehicle'):
							if request.POST.get('site'):
								site_val = request.POST.get('site')
								vehicle_val = request.POST.get('vehicle')
								vehicle_type_val = request.POST.get('vehicle_type_name')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = MaintainanceBill.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(user_site=site_val) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')
								total_amt = MaintainanceBill.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(user_site=site_val) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('total'))
							else:
								vehicle_val = request.POST.get('vehicle')
								vehicle_type_val = request.POST.get('vehicle_type_name')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = MaintainanceBill.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')
								total_amt = MaintainanceBill.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('total'))
						else:
							if request.POST.get('site'):
								site_val = request.POST.get('site')
								vehicle_type_val = request.POST.get('vehicle_type_name')
								report = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val, vehicle_type=vehicle_type_val).order_by('entry_date')
								total_amt = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val, vehicle_type=vehicle_type_val).aggregate(Sum('total'))
							else:
								vehicle_type_val = request.POST.get('vehicle_type_name')
								report = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], vehicle_type=vehicle_type_val).order_by('entry_date')
								total_amt = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], vehicle_type=vehicle_type_val).aggregate(Sum('total'))
					else:
						if request.POST.get('vehicle'):
							if request.POST.get('site'):
								site_val = request.POST.get('site')
								vehicle_val = request.POST.get('vehicle')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = MaintainanceBill.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(user_site=site_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')
								total_amt = MaintainanceBill.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(user_site=site_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('total'))
							else:
								vehicle_val = request.POST.get('vehicle')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = MaintainanceBill.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')
								total_amt = MaintainanceBill.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('total'))

		if report_val == 'vendor_maintain':
			report_head = 'Vendor-wise Transaction Log'
			if request.POST.get('fromdate') and request.POST.get('todate'):
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				if request.POST.get('sup'):
					site_val = request.POST.get('sup')
					item_val = request.POST.get('supname')
					report = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate], supplier_id=site_val).order_by('entry_date')
					total_amt = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate], supplier_id=site_val).aggregate(Sum('total'))
					credit = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate], supplier_id=site_val, transaction_type='credit').aggregate(Sum('total'))
					cash = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate], supplier_id=site_val, transaction_type='cash').aggregate(Sum('total'))

		if report_val == 'vehicle_move':
			report_head = 'Vehicle Movement Report'
			if request.POST.get('fromdate') and request.POST.get('todate'):
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				if request.POST.get('vehicle_type_name') or request.POST.get('vehicle'):
					if request.POST.get('vehicle_type_name'):
						if request.POST.get('vehicle'):
							if request.POST.get('fromsite'):
								if request.POST.get('tosite'):
									fsite = request.POST.get('fromsite')
									tsite = request.POST.get('tosite')
									num_type = request.POST.get('num_type')
									vehicle_val = request.POST.get('vehicle')
									vehicle_type_val = request.POST.get('vehicle_type_name')
									if num_type == 'vehicle':
										vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'engine':
										vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'chasis':
										vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
										eng = vd.engine_number
										vh = vd.vehicle_number
										ch = vd.chasis_number
									report = VehicleTrack.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(from_site=fsite) & Q(to_site=tsite) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')
								else:
									fsite = request.POST.get('fsite')
									vehicle_val = request.POST.get('vehicle')
									num_type = request.POST.get('num_type')
									vehicle_type_val = request.POST.get('vehicle_type_name')
									if num_type == 'vehicle':
										vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'engine':
										vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'chasis':
										vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
										eng = vd.engine_number
										vh = vd.vehicle_number
										ch = vd.chasis_number
									report = VehicleTrack.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(from_site=fsite) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')
							else:
								if request.POST.get('tosite'):
									tsite = request.POST.get('tosite')
									vehicle_val = request.POST.get('vehicle')
									num_type = request.POST.get('num_type')
									vehicle_type_val = request.POST.get('vehicle_type_name')
									if num_type == 'vehicle':
										vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'engine':
										vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'chasis':
										vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
										eng = vd.engine_number
										vh = vd.vehicle_number
										ch = vd.chasis_number
									report = VehicleTrack.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(to_site=tsite) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')
								else:
									vehicle_val = request.POST.get('vehicle')
									num_type = request.POST.get('num_type')
									vehicle_type_val = request.POST.get('vehicle_type_name')
									if num_type == 'vehicle':
										vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'engine':
										vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'chasis':
										vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
										eng = vd.engine_number
										vh = vd.vehicle_number
										ch = vd.chasis_number
									report = VehicleTrack.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')

						else:
							if request.POST.get('fromsite'):
								if request.POST.get('tosite'):
									fsite = request.POST.get('fromsite')
									tsite = request.POST.get('tosite')
									vehicle_type_val = request.POST.get('vehicle_type_name')
									report = VehicleTrack.objects.filter(entry_date__range=[fromdate, todate], from_site=fsite, to_site=tsite, vehicle_type=vehicle_type_val).order_by('entry_date')
								else:
									fsite = request.POST.get('fromsite')
									vehicle_type_val = request.POST.get('vehicle_type_name')
									report = VehicleTrack.objects.filter(entry_date__range=[fromdate, todate], from_site=fsite, vehicle_type=vehicle_type_val).order_by('entry_date')
							else:
								if request.POST.get('tosite'):
									tsite = request.POST.get('tosite')
									vehicle_type_val = request.POST.get('vehicle_type_name')
									report = VehicleTrack.objects.filter(entry_date__range=[fromdate, todate], to_site=tsite, vehicle_type=vehicle_type_val).order_by('entry_date')
								else:
									vehicle_type_val = request.POST.get('vehicle_type_name')
									report = VehicleTrack.objects.filter(entry_date__range=[fromdate, todate], vehicle_type=vehicle_type_val).order_by('entry_date')
					else:
						if request.POST.get('vehicle'):
							if request.POST.get('fromsite'):
								if request.POST.get('tosite'):
									fsite = request.POST.get('fromsite')
									tsite = request.POST.get('tosite')
									vehicle_val = request.POST.get('vehicle')
									num_type = request.POST.get('num_type')
									if num_type == 'vehicle':
										vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'engine':
										vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'chasis':
										vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
										eng = vd.engine_number
										vh = vd.vehicle_number
										ch = vd.chasis_number
									report = VehicleTrack.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(from_site=fsite) & Q(to_site=tsite) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')
								else:
									fsite = request.POST.get('fromsite')
									vehicle_val = request.POST.get('vehicle')
									num_type = request.POST.get('num_type')
									if num_type == 'vehicle':
										vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'engine':
										vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'chasis':
										vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
										eng = vd.engine_number
										vh = vd.vehicle_number
										ch = vd.chasis_number
									report = VehicleTrack.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(from_site=fsite) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')
							else:
								if request.POST.get('tosite'):
									tsite = request.POST.get('tosite')
									vehicle_val = request.POST.get('vehicle')
									num_type = request.POST.get('num_type')
									if num_type == 'vehicle':
										vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'engine':
										vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'chasis':
										vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
										eng = vd.engine_number
										vh = vd.vehicle_number
										ch = vd.chasis_number
									report = VehicleTrack.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(to_site=tsite) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')
								else:
									vehicle_val = request.POST.get('vehicle')
									num_type = request.POST.get('num_type')
									if num_type == 'vehicle':
										vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'engine':
										vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'chasis':
										vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
										eng = vd.engine_number
										vh = vd.vehicle_number
										ch = vd.chasis_number
									report = VehicleTrack.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')

		context = {'report': report, 'report_val': report_val, 'report_head': report_head, 'item_val': item_val, 'site_val': site_val, 'fromdate': fromdate, 'todate': todate, 'total_opening': total_opening, 'total_qty': total_qty, 'total_amt': total_amt, 'vehicle_val': vehicle_val, 'vehicle_type_val': vehicle_type_val, 'credit': credit, 'cash': cash, 'fsite': fsite, 'tsite': tsite, 'num_type': num_type}    
		return render(request, 'report_generation.html', context)
	else:
		return redirect('reports')


@user_access
def generate_report_pdf(request):
	if request.method == "POST":
		report = []
		item_val = ''
		site_val = ''
		vehicle_val = ''
		fsite = ''
		tsite = ''
		vehicle_type_val = ''
		num_type = ''
		fromdate = ''
		todate = ''
		total_opening = ''
		total_qty = ''
		total_amt = ''
		credit = ''
		cash = ''
		vh = ''
		eng = ''
		ch = ''
		report_val = request.POST.get('report_val')
		if report_val == 'stock_report':
			report_head = 'Stock Report'
			if request.POST.get('item'):
				if request.POST.get('site'):
					item_val = request.POST.get('item')
					site_val = request.POST.get('site')
					report = StockEntry.objects.filter(item=item_val, stock_site=site_val)
					total_opening = StockEntry.objects.filter(item=item_val, stock_site=site_val).aggregate(Sum('opening'))
					total_qty = StockEntry.objects.filter(item=item_val, stock_site=site_val).aggregate(Sum('quantity'))
				else:
					item_val = request.POST.get('item')
					report = StockEntry.objects.filter(item=item_val)
					total_opening = StockEntry.objects.filter(item=item_val).aggregate(Sum('opening'))
					total_qty = StockEntry.objects.filter(item=item_val).aggregate(Sum('quantity'))
			else:
				if request.POST.get('site'):
					site_val = request.POST.get('site')
					report = StockEntry.objects.filter(stock_site=site_val)

		if report_val == 'grn_report':
			report_head = 'GRN Report'
			if request.POST.get('fromdate') and request.POST.get('todate'):
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				if request.POST.get('item'):
					if request.POST.get('site'):
						item_val = request.POST.get('item')
						site_val = request.POST.get('site')
						grrn = GoodsEntry.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val)
						for r in grrn:
							grnn = r.id
							grrnn = GoodsEntry.objects.filter(id=grnn).first()
							goo = Goods.objects.filter(goodsid=grnn, item=item_val)
							gex = GoodsExtra.objects.filter(goodsid=grnn)
							report.append([grrnn,gex,goo])
					else:
						item_val = request.POST.get('item')
						grrn = GoodsEntry.objects.filter(entry_date__range=[fromdate, todate])
						for r in grrn:
							grnn = r.id
							gex = GoodsExtra.objects.filter(goodsid=grnn)
							goo = Goods.objects.filter(goodsid=grnn, item=item_val)
							for g in goo:
								ggid = g.id
								gid = g.goodsid
								grrnn = GoodsEntry.objects.filter(id=gid).first()
								report.append([grrnn,gex,goo])
				else:
					if request.POST.get('site'):
						site_val = request.POST.get('site')
						grrn = GoodsEntry.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val)
						for r in grrn:
							grnn = r.id
							grrnn = GoodsEntry.objects.filter(id=grnn).first()
							goo = Goods.objects.filter(goodsid=grnn)
							gex = GoodsExtra.objects.filter(goodsid=grnn)
							report.append([grrnn,gex,goo])

		if report_val == 'invoice_report':
			report_head = 'Invoice Report'
			if request.POST.get('fromdate') and request.POST.get('todate'):
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				if request.POST.get('item'):
					if request.POST.get('site'):
						item_val = request.POST.get('item')
						site_val = request.POST.get('site')
						grrn = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val)
						total_amt = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val).aggregate(Sum('total'))
						credit = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val, transaction_type='credit').aggregate(Sum('total'))
						cash = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val, transaction_type='cash').aggregate(Sum('total'))
						for r in grrn:
							grnn = r.id
							grrnn = PurchaseEntry.objects.filter(id=grnn).first()
							goo = InvoiceItem.objects.filter(purchaseid=grnn, item=item_val)
							report.append([grrnn,goo])
					else:
						item_val = request.POST.get('item')
						ppid = []
						grrn = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate])
						for r in grrn:
							grnn = r.id
							goo = InvoiceItem.objects.filter(purchaseid=grnn, item=item_val)
							for g in goo:
								ggid = g.id
								gid = g.goodsid
								ppid.append(gid)
								grrnn = PurchaseEntry.objects.filter(id=gid).first()
								report.append([grrnn,goo])
						total_amt = PurchaseEntry.objects.filter(id__in=ppid).aggregate(Sum('total'))
						credit = MaintainanceBill.objects.filter(id__in=ppid, transaction_type='credit').aggregate(Sum('total'))
						cash = MaintainanceBill.objects.filter(id__in=ppid, transaction_type='cash').aggregate(Sum('total'))
				else:
					if request.POST.get('site'):
						site_val = request.POST.get('site')
						grrn = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val)
						total_amt = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val).aggregate(Sum('total'))
						credit = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val, transaction_type='credit').aggregate(Sum('total'))
						cash = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val, transaction_type='cash').aggregate(Sum('total'))
						for r in grrn:
							grnn = r.id
							grrnn = PurchaseEntry.objects.filter(id=grnn).first()
							goo = InvoiceItem.objects.filter(purchaseid=grnn)
							report.append([grrnn,goo])

		if report_val == 'material_report':
			report_head = 'Material Issue Report'
			if request.POST.get('fromdate') and request.POST.get('todate'):
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				if request.POST.get('item'):
					if request.POST.get('site'):
						item_val = request.POST.get('item')
						site_val = request.POST.get('site')
						grrn = MaterialIssueEntry.objects.filter(issue_date__range=[fromdate, todate], user_site=site_val)
						for r in grrn:
							grnn = r.id
							grrnn = MaterialIssueEntry.objects.filter(id=grnn).first()
							goo = MaterialItem.objects.filter(materialid=grnn, item=item_val)
							report.append([grrnn,goo])
					else:
						item_val = request.POST.get('item')
						grrn = MaterialIssueEntry.objects.filter(issue_date__range=[fromdate, todate])
						for r in grrn:
							grnn = r.id
							goo = MaterialItem.objects.filter(materialid=grnn, item=item_val)
							for g in goo:
								ggid = g.id
								gid = g.goodsid
								grrnn = MaterialIssueEntry.objects.filter(id=gid).first()
								report.append([grrnn,goo])
				else:
					if request.POST.get('site'):
						site_val = request.POST.get('site')
						grrn = MaterialIssueEntry.objects.filter(issue_date__range=[fromdate, todate], user_site=site_val)
						for r in grrn:
							grnn = r.id
							grrnn = MaterialIssueEntry.objects.filter(id=grnn).first()
							goo = MaterialItem.objects.filter(materialid=grnn)
							report.append([grrnn,goo])

		if report_val == 'internal_report':
			report_head = 'Internal Transfer Report'
			if request.POST.get('fromdate') and request.POST.get('todate'):
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				if request.POST.get('item'):
					if request.POST.get('site'):
						item_val = request.POST.get('item')
						site_val = request.POST.get('site')
						grrn = InternalTransfer.objects.filter(issue_date__range=[fromdate, todate], user_site=site_val)
						for r in grrn:
							grnn = r.id
							grrnn = InternalTransfer.objects.filter(id=grnn).first()
							goo = TransferItem.objects.filter(transferid=grnn, item=item_val)
							report.append([grrnn,goo])
					else:
						item_val = request.POST.get('item')
						grrn = InternalTransfer.objects.filter(issue_date__range=[fromdate, todate])
						for r in grrn:
							grnn = r.id
							goo = TransferItem.objects.filter(transferid=grnn, item=item_val)
							for g in goo:
								ggid = g.id
								gid = g.goodsid
								grrnn = InternalTransfer.objects.filter(id=gid).first()
								report.append([grrnn,goo])
				else:
					if request.POST.get('site'):
						site_val = request.POST.get('site')
						grrn = InternalTransfer.objects.filter(issue_date__range=[fromdate, todate], user_site=site_val)
						for r in grrn:
							grnn = r.id
							grrnn = InternalTransfer.objects.filter(id=grnn).first()
							goo = TransferItem.objects.filter(transferid=grnn)
							report.append([grrnn,goo])

		if report_val == 'transfer_grn':
			report_head = 'Internal Transfer GRN Report'
			if request.POST.get('fromdate') and request.POST.get('todate'):
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				if request.POST.get('item'):
					if request.POST.get('site'):
						item_val = request.POST.get('item')
						site_val = request.POST.get('site')
						grrn = InternalGrn.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val)
						for r in grrn:
							grnn = r.id
							grrnn = InternalGrn.objects.filter(id=grnn).first()
							goo = InternalGrnItems.objects.filter(goodsid=grnn, item=item_val)
							report.append([grrnn,goo])
					else:
						item_val = request.POST.get('item')
						grrn = InternalGrn.objects.filter(entry_date__range=[fromdate, todate])
						for r in grrn:
							grnn = r.id
							goo = InternalGrnItems.objects.filter(goodsid=grnn, item=item_val)
							for g in goo:
								ggid = g.id
								gid = g.goodsid
								grrnn = InternalGrn.objects.filter(id=gid).first()
								report.append([grrnn,goo])
				else:
					if request.POST.get('site'):
						site_val = request.POST.get('site')
						grrn = InternalGrn.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val)
						for r in grrn:
							grnn = r.id
							grrnn = InternalGrn.objects.filter(id=grnn).first()
							goo = InternalGrnItems.objects.filter(goodsid=grnn)
							report.append([grrnn,goo])

		if report_val == 'fuel_purchase':
			report_head = 'Reserviour-wise Fuel Purchase Report'
			if request.POST.get('fromdate') and request.POST.get('todate'):
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				if request.POST.get('item'):
					if request.POST.get('site'):
						item_val = request.POST.get('item')
						site_val = request.POST.get('site')
						report = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val, fuel_type=item_val).order_by('entry_date')
						total_qty = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val, fuel_type=item_val).aggregate(Sum('quantity'))
						total_amt = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val, fuel_type=item_val).aggregate(Sum('amount'))
					else:
						item_val = request.POST.get('item')
						report = FuelBill.objects.filter(entry_date__range=[fromdate, todate], fuel_type=item_val).order_by('entry_date')
						total_qty = FuelBill.objects.filter(entry_date__range=[fromdate, todate], fuel_type=item_val).aggregate(Sum('quantity'))
						total_amt = FuelBill.objects.filter(entry_date__range=[fromdate, todate], fuel_type=item_val).aggregate(Sum('amount'))
				else:
					if request.POST.get('site'):
						site_val = request.POST.get('site')
						report = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val).order_by('entry_date')
						total_qty = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val).aggregate(Sum('quantity'))
						total_amt = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val).aggregate(Sum('amount'))

		if report_val == 'vehicle_fuel':
			report_head = 'Vehicle-wise Fuel Consumption Report'
			if request.POST.get('fromdate') and request.POST.get('todate'):
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				if request.POST.get('vehicle_type_name'):
					if request.POST.get('vehicle'):
						if request.POST.get('site'):
							if request.POST.get('item'):
								item_val = request.POST.get('item')
								site_val = request.POST.get('site')
								vehicle_val = request.POST.get('vehicle')
								vehicle_type_val = request.POST.get('vehicle_type_name')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(reserviour=site_val) & Q(fuel_type=item_val) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))) .order_by('date')
								total_qty = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(reserviour=site_val) & Q(fuel_type=item_val) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('quantity'))
							else:
								site_val = request.POST.get('site')
								vehicle_val = request.POST.get('vehicle')
								vehicle_type_val = request.POST.get('vehicle_type_name')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(reserviour=site_val) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('date')
								total_qty = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(reserviour=site_val) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('quantity'))
						else:
							if request.POST.get('item'):
								item_val = request.POST.get('item')
								vehicle_val = request.POST.get('vehicle')
								vehicle_type_val = request.POST.get('vehicle_type_name')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(fuel_type=item_val) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('date')
								total_qty = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(fuel_type=item_val) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('quantity'))
							else:
								vehicle_val = request.POST.get('vehicle')
								vehicle_type_val = request.POST.get('vehicle_type_name')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('date')
								total_qty = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('quantity'))
					else:
						if request.POST.get('site'):
							if request.POST.get('item'):
								item_val = request.POST.get('item')
								site_val = request.POST.get('site')
								vehicle_type_val = request.POST.get('vehicle_type_name')
								report = Fuel.objects.filter(date__range=[fromdate, todate], reserviour=site_val, fuel_type=item_val, vehicle_type=vehicle_type_val).order_by('date')
								total_qty = Fuel.objects.filter(date__range=[fromdate, todate], reserviour=site_val, fuel_type=item_val, vehicle_type=vehicle_type_val).aggregate(Sum('quantity'))
							else:
								site_val = request.POST.get('site')
								vehicle_type_val = request.POST.get('vehicle_type_name')
								report = Fuel.objects.filter(date__range=[fromdate, todate], reserviour=site_val, vehicle_type=vehicle_type_val).order_by('date')
								total_qty = Fuel.objects.filter(date__range=[fromdate, todate], reserviour=site_val, vehicle_type=vehicle_type_val).aggregate(Sum('quantity'))
						else:
							if request.POST.get('item'):
								item_val = request.POST.get('item')
								vehicle_type_val = request.POST.get('vehicle_type_name')
								report = Fuel.objects.filter(date__range=[fromdate, todate], fuel_type=item_val, vehicle_type=vehicle_type_val).order_by('date')
								total_qty = Fuel.objects.filter(date__range=[fromdate, todate], fuel_type=item_val, vehicle_type=vehicle_type_val).aggregate(Sum('quantity'))
							else:
								vehicle_type_val = request.POST.get('vehicle_type_name')
								report = Fuel.objects.filter(date__range=[fromdate, todate], vehicle_type=vehicle_type_val).order_by('date')
								total_qty = Fuel.objects.filter(date__range=[fromdate, todate], vehicle_type=vehicle_type_val).aggregate(Sum('quantity'))
				else:
					if request.POST.get('vehicle'):
						if request.POST.get('site'):
							if request.POST.get('item'):
								item_val = request.POST.get('item')
								site_val = request.POST.get('site')
								vehicle_val = request.POST.get('vehicle')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(reserviour=site_val) & Q(fuel_type=item_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('date')
								total_qty = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(reserviour=site_val) & Q(fuel_type=item_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('quantity'))
							else:
								site_val = request.POST.get('site')
								vehicle_val = request.POST.get('vehicle')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(reserviour=site_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('date')
								total_qty = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(reserviour=site_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('quantity'))
						else:
							if request.POST.get('item'):
								item_val = request.POST.get('item')
								vehicle_val = request.POST.get('vehicle')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(fuel_type=item_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('date')
								total_qty = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(fuel_type=item_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('quantity'))
							else:
								vehicle_val = request.POST.get('vehicle')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('date')
								total_qty = Fuel.objects.filter(Q(date__range=[fromdate, todate]) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('quantity'))
					else:
						if request.POST.get('site'):
							if request.POST.get('item'):
								item_val = request.POST.get('item')
								site_val = request.POST.get('site')
								report = Fuel.objects.filter(date__range=[fromdate, todate], reserviour=site_val, fuel_type=item_val).order_by('date')
								total_qty = Fuel.objects.filter(date__range=[fromdate, todate], reserviour=site_val, fuel_type=item_val).aggregate(Sum('quantity'))
							else:
								site_val = request.POST.get('site')
								report = Fuel.objects.filter(date__range=[fromdate, todate], reserviour=site_val).order_by('date')
								total_qty = Fuel.objects.filter(date__range=[fromdate, todate], reserviour=site_val).aggregate(Sum('quantity'))
						else:
							if request.POST.get('item'):
								item_val = request.POST.get('item')
								report = Fuel.objects.filter(date__range=[fromdate, todate], fuel_type=item_val).order_by('date')
								total_qty = Fuel.objects.filter(date__range=[fromdate, todate], fuel_type=item_val).aggregate(Sum('quantity'))
							else:
								vehicle_type_val = request.POST.get('vehicle_type_name')
								report = Fuel.objects.filter(date__range=[fromdate, todate]).order_by('date')
								total_qty = Fuel.objects.filter(date__range=[fromdate, todate]).aggregate(Sum('quantity'))

		if report_val == 'maintain_log':
			report_head = 'All Maintainance Log'
			if request.POST.get('fromdate') and request.POST.get('todate'):
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				if request.POST.get('site'):
					site_val = request.POST.get('site')
					report = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val).order_by('entry_date')
					total_amt = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val).aggregate(Sum('total'))
				else:
					report = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate]).order_by('entry_date')
					total_amt = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate]).aggregate(Sum('total'))

		if report_val == 'vehicle_maintain':
			report_head = 'Vehicle-wise Maintainance Log'
			if request.POST.get('fromdate') and request.POST.get('todate'):
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				if request.POST.get('vehicle_type_name') or request.POST.get('vehicle'):
					if request.POST.get('vehicle_type_name'):
						if request.POST.get('vehicle'):
							if request.POST.get('site'):
								site_val = request.POST.get('site')
								vehicle_val = request.POST.get('vehicle')
								vehicle_type_val = request.POST.get('vehicle_type_name')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = MaintainanceBill.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(user_site=site_val) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')
								total_amt = MaintainanceBill.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(user_site=site_val) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('total'))
							else:
								vehicle_val = request.POST.get('vehicle')
								vehicle_type_val = request.POST.get('vehicle_type_name')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = MaintainanceBill.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')
								total_amt = MaintainanceBill.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('total'))
						else:
							if request.POST.get('site'):
								site_val = request.POST.get('site')
								vehicle_type_val = request.POST.get('vehicle_type_name')
								report = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val, vehicle_type=vehicle_type_val).order_by('entry_date')
								total_amt = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val, vehicle_type=vehicle_type_val).aggregate(Sum('total'))
							else:
								vehicle_type_val = request.POST.get('vehicle_type_name')
								report = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], vehicle_type=vehicle_type_val).order_by('entry_date')
								total_amt = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], vehicle_type=vehicle_type_val).aggregate(Sum('total'))
					else:
						if request.POST.get('vehicle'):
							if request.POST.get('site'):
								site_val = request.POST.get('site')
								vehicle_val = request.POST.get('vehicle')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = MaintainanceBill.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(user_site=site_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')
								total_amt = MaintainanceBill.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(user_site=site_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('total'))
							else:
								vehicle_val = request.POST.get('vehicle')
								num_type = request.POST.get('num_type')
								if num_type == 'vehicle':
									vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'engine':
									vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
									vh = vd.vehicle_number
									eng = vd.engine_number
									ch = vd.chasis_number
								if num_type == 'chasis':
									vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
									eng = vd.engine_number
									vh = vd.vehicle_number
									ch = vd.chasis_number
								report = MaintainanceBill.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')
								total_amt = MaintainanceBill.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).aggregate(Sum('total'))

		if report_val == 'vendor_maintain':
			report_head = 'Vendor-wise Transaction Log'
			if request.POST.get('fromdate') and request.POST.get('todate'):
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				if request.POST.get('sup'):
					site_val = request.POST.get('sup')
					item_val = request.POST.get('supname')
					report = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate], supplier_id=site_val).order_by('entry_date')
					total_amt = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate], supplier_id=site_val).aggregate(Sum('total'))
					credit = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate], supplier_id=site_val, transaction_type='credit').aggregate(Sum('total'))
					cash = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate], supplier_id=site_val, transaction_type='cash').aggregate(Sum('total'))

		if report_val == 'vehicle_move':
			report_head = 'Vehicle Movement Report'
			if request.POST.get('fromdate') and request.POST.get('todate'):
				fromdate = request.POST.get('fromdate')
				todate = request.POST.get('todate')
				if request.POST.get('vehicle_type_name') or request.POST.get('vehicle'):
					if request.POST.get('vehicle_type_name'):
						if request.POST.get('vehicle'):
							if request.POST.get('fromsite'):
								if request.POST.get('tosite'):
									fsite = request.POST.get('fromsite')
									tsite = request.POST.get('tosite')
									num_type = request.POST.get('num_type')
									vehicle_val = request.POST.get('vehicle')
									vehicle_type_val = request.POST.get('vehicle_type_name')
									if num_type == 'vehicle':
										vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'engine':
										vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'chasis':
										vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
										eng = vd.engine_number
										vh = vd.vehicle_number
										ch = vd.chasis_number
									report = VehicleTrack.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(from_site=fsite) & Q(to_site=tsite) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')
								else:
									fsite = request.POST.get('fsite')
									vehicle_val = request.POST.get('vehicle')
									num_type = request.POST.get('num_type')
									vehicle_type_val = request.POST.get('vehicle_type_name')
									if num_type == 'vehicle':
										vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'engine':
										vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'chasis':
										vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
										eng = vd.engine_number
										vh = vd.vehicle_number
										ch = vd.chasis_number
									report = VehicleTrack.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(from_site=fsite) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')
							else:
								if request.POST.get('tosite'):
									tsite = request.POST.get('tosite')
									vehicle_val = request.POST.get('vehicle')
									num_type = request.POST.get('num_type')
									vehicle_type_val = request.POST.get('vehicle_type_name')
									if num_type == 'vehicle':
										vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'engine':
										vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'chasis':
										vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
										eng = vd.engine_number
										vh = vd.vehicle_number
										ch = vd.chasis_number
									report = VehicleTrack.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(to_site=tsite) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')
								else:
									vehicle_val = request.POST.get('vehicle')
									num_type = request.POST.get('num_type')
									vehicle_type_val = request.POST.get('vehicle_type_name')
									if num_type == 'vehicle':
										vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'engine':
										vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'chasis':
										vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
										eng = vd.engine_number
										vh = vd.vehicle_number
										ch = vd.chasis_number
									report = VehicleTrack.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(vehicle_type=vehicle_type_val) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')

						else:
							if request.POST.get('fromsite'):
								if request.POST.get('tosite'):
									fsite = request.POST.get('fromsite')
									tsite = request.POST.get('tosite')
									vehicle_type_val = request.POST.get('vehicle_type_name')
									report = VehicleTrack.objects.filter(entry_date__range=[fromdate, todate], from_site=fsite, to_site=tsite, vehicle_type=vehicle_type_val).order_by('entry_date')
								else:
									fsite = request.POST.get('fromsite')
									vehicle_type_val = request.POST.get('vehicle_type_name')
									report = VehicleTrack.objects.filter(entry_date__range=[fromdate, todate], from_site=fsite, vehicle_type=vehicle_type_val).order_by('entry_date')
							else:
								if request.POST.get('tosite'):
									tsite = request.POST.get('tosite')
									vehicle_type_val = request.POST.get('vehicle_type_name')
									report = VehicleTrack.objects.filter(entry_date__range=[fromdate, todate], to_site=tsite, vehicle_type=vehicle_type_val).order_by('entry_date')
								else:
									vehicle_type_val = request.POST.get('vehicle_type_name')
									report = VehicleTrack.objects.filter(entry_date__range=[fromdate, todate], vehicle_type=vehicle_type_val).order_by('entry_date')
					else:
						if request.POST.get('vehicle'):
							if request.POST.get('fromsite'):
								if request.POST.get('tosite'):
									fsite = request.POST.get('fromsite')
									tsite = request.POST.get('tosite')
									vehicle_val = request.POST.get('vehicle')
									num_type = request.POST.get('num_type')
									if num_type == 'vehicle':
										vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'engine':
										vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'chasis':
										vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
										eng = vd.engine_number
										vh = vd.vehicle_number
										ch = vd.chasis_number
									report = VehicleTrack.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(from_site=fsite) & Q(to_site=tsite) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')
								else:
									fsite = request.POST.get('fromsite')
									vehicle_val = request.POST.get('vehicle')
									num_type = request.POST.get('num_type')
									if num_type == 'vehicle':
										vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'engine':
										vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'chasis':
										vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
										eng = vd.engine_number
										vh = vd.vehicle_number
										ch = vd.chasis_number
									report = VehicleTrack.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(from_site=fsite) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')
							else:
								if request.POST.get('tosite'):
									tsite = request.POST.get('tosite')
									vehicle_val = request.POST.get('vehicle')
									num_type = request.POST.get('num_type')
									if num_type == 'vehicle':
										vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'engine':
										vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'chasis':
										vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
										eng = vd.engine_number
										vh = vd.vehicle_number
										ch = vd.chasis_number
									report = VehicleTrack.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(to_site=tsite) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')
								else:
									vehicle_val = request.POST.get('vehicle')
									num_type = request.POST.get('num_type')
									if num_type == 'vehicle':
										vd = VehicleList.objects.filter(vehicle_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'engine':
										vd = VehicleList.objects.filter(engine_number=vehicle_val).first()
										vh = vd.vehicle_number
										eng = vd.engine_number
										ch = vd.chasis_number
									if num_type == 'chasis':
										vd = VehicleList.objects.filter(chasis_number=vehicle_val).first()
										eng = vd.engine_number
										vh = vd.vehicle_number
										ch = vd.chasis_number
									report = VehicleTrack.objects.filter(Q(entry_date__range=[fromdate, todate]) & Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))).order_by('entry_date')

		context = {'report': report, 'report_val': report_val, 'report_head': report_head, 'item_val': item_val, 'site_val': site_val, 'fromdate': fromdate, 'todate': todate, 'total_opening': total_opening, 'total_qty': total_qty, 'total_amt': total_amt, 'vehicle_val': vehicle_val, 'vehicle_type_val': vehicle_type_val, 'credit': credit, 'cash': cash, 'fsite': fsite, 'tsite': tsite, 'num_type': num_type}    
		pdf = render_to_pdf('report_pdf.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			rnum = random.randint(11111111, 99999999)
			filename = "Report_%s.pdf" %(rnum)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")
	else:
		return redirect('reports')


def report_redirects(request,rst,rval):
	if rst == 'invoice':
		rval = rval.upper()
		if PurchaseEntry.objects.filter(voucher_number=rval).exists():
			pe = PurchaseEntry.objects.get(voucher_number=rval)
			pid = pe.id
			return redirect('/ashish-invoice-detail/'+str(pid)+'/')
	return HttpResponse("Not Found")


#Reserviour and Maintainance part ====================================

def manage_reserviour(request):
	count1 = Reserviour.objects.all().count()
	count2 = FuelPurchase.objects.all().count()
	count3 = FuelBill.objects.all().count()
	count4 = FuelInternalTransfer.objects.all().count()
	count5 = FuelLeakage.objects.all().count()
	context = {'count1': count1, 'count2': count2, 'count3': count3, 'count4': count4, 'count5': count5}
	return render(request, 'fuelmaintain/reserviour_dash.html', context)


@user_access
def reserviour_add(request):
	site_dash = Site.objects.filter(active_status='yes')
	context = {'site_dash': site_dash}
	return render(request, 'fuelmaintain/reserviour.html', context)


@user_access
def add_reserviour(request):
	if request.method=="POST":
		current_user = request.user.username
		u_site = user_site(request)
		name = request.POST.get('name')
		url = request.POST.get('url')
		site = request.POST.get('site')
		location = request.POST.get('location')
		capacity = request.POST.get('capacity')
		opening = request.POST.get('opening')

		if Reserviour.objects.filter(url=url, site=site).exists():
			messages.info(request, 'error')
			return redirect('manage_reserviour')
		else:
			query = Reserviour(name=name, url=url, site=site, location=location, capacity=capacity, opening=opening, stock=opening, entry_by=current_user, user_site=u_site)
			query.save()
			messages.info(request, 'done')
			return redirect('manage_reserviour')
	else:
		return redirect('manage_reserviour')


@user_access
def reserviour_display(request):
	reserve = Reserviour.objects.all()
	site_dash = Site.objects.filter(active_status='yes')
	context = {'reserve': reserve, 'site_dash': site_dash}
	return render(request, 'fuelmaintain/display/reserviour_display.html', context)


@user_access
def update_reserviour(request):
	if request.method=="POST":
		rid = request.POST.get('suid')
		name = request.POST.get('name')
		url = request.POST.get('url')
		site = request.POST.get('site')
		location = request.POST.get('location')
		capacity = request.POST.get('capacity')
		opening = request.POST.get('opening')
		dopening = request.POST.get('dopening')
		dstock = request.POST.get('dstock')
		dname = request.POST.get('dname')

		opencalc = float(dopening)-float(opening)
		if opencalc > 0:
			dstock = float(dstock) - opencalc
		if opencalc < 0:
			opencalc = abs(opencalc)
			dstock = float(dstock) + opencalc

		if Reserviour.objects.filter(url=url, site=site).exclude(id=rid).exists():
			messages.info(request, 'error')
			return redirect('reserviour_display')
		else:
			Reserviour.objects.filter(id=rid).update(name=name, url=url, site=site, location=location, capacity=capacity, opening=opening, stock=dstock)
			if Fuel.objects.filter(reserviour=dname).exists():
				Fuel.objects.filter(reserviour=dname).update(reserviour=name)
			if FuelPurchase.objects.filter(reserviour=dname).exists():
				FuelPurchase.objects.filter(reserviour=dname).update(reserviour=name)
			if FuelBill.objects.filter(reserviour=dname).exists():
				FuelBill.objects.filter(reserviour=dname).update(reserviour=name)
			if FuelInternalTransfer.objects.filter(from_reserviour=dname).exists():
				FuelInternalTransfer.objects.filter(from_reserviour=dname).update(from_reserviour=name)
			if FuelInternalTransfer.objects.filter(to_reserviour=dname).exists():
				FuelInternalTransfer.objects.filter(to_reserviour=dname).update(to_reserviour=name)
			if FuelLeakage.objects.filter(reserviour=dname).exists():
				FuelLeakage.objects.filter(reserviour=dname).update(reserviour=name)
			messages.info(request, 'done')
			return redirect('reserviour_display')

	else:
		return redirect('log_dashboard')


@user_access
def delete_reserviour(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		Reserviour.objects.filter(id=sid).delete()
		messages.info(request, 'done')
		return redirect('reserviour_display')
	else:
		return redirect('reserviour_display')


@user_access
def fuel_manage(request):
	fueldash = []
	seen =set()
	seen_add = seen.add
	ent = Fuel.objects.values_list('coupon_number', flat=True)
	ent = [x for x in ent if not (x in seen or seen_add(x))]
	for s in ent:
		fueldash.append(s)
	v_type = VehicleType.objects.all()
	reserve = Reserviour.objects.all()
	f_type = FuelType.objects.all()
	vehis = []
	seen =set()
	seen_add = seen.add
	ent = VehicleList.objects.values_list('vehicle_type_id', flat=True)
	ent = [x for x in ent if not (x in seen or seen_add(x))]
	for e in ent:
		vehi = VehicleList.objects.filter(vehicle_type_id=e, active_status='yes')
		n = len(vehi)
		vehis.append([vehi, range(1,n)])
	if Fuel.objects.last():
		jd = Fuel.objects.last()
		jn = jd.fcn
		newpei = jn+1
	else:
		newpei = 1
	context = {'couponlist': fueldash, 'newpei': newpei, 'vehis': vehis, 'f_type': f_type, 'v_type': v_type, 'reserve':reserve}
	return render(request, 'fuelmaintain/fuel_manage.html', context)


@user_access
def add_consumption(request):
	if request.method=="POST":
		current_user = request.user.username
		u_site = user_site(request)
		date = request.POST.get('date')
		coupon = request.POST.get('coupon')
		consump_number = request.POST.get('consump_number')
		fcn = request.POST.get('pvn_count')
		kilometer = request.POST.get('kilometer')
		quantity = request.POST.get('quantity')
		reserve_val = request.POST.get('reserviour_name')
		reserve_id = request.POST.get('reserviour')
		vehicle = request.POST.get('vehicle')
		vehicle_type = request.POST.get('vehicle_type_name')
		vehicle_type_id = request.POST.get('vehicle_type')
		num_type = request.POST.get('num_type')
		fuel_type = request.POST.get('fuel_type')
		datetim = datetime.datetime.now()
		datetim = datetim.replace(tzinfo=None)
		datetim = datetim.replace(second=0, microsecond=0)
		dateon = datetime.date.today()

		upreserve = Reserviour.objects.filter(id=reserve_id).first()
		stock = upreserve.stock
		newstock = float(stock) - float(quantity)
		if newstock > 0 or newstock == 0:
			query = Fuel(date=date, consump_number=consump_number, fcn=fcn, fuel_type=fuel_type, coupon_number=coupon, number_type=num_type, vehicle_type=vehicle_type, vehicle_type_id=vehicle_type_id, vehicle_number=vehicle, user_site=u_site, reserviour=reserve_val, reserviour_id=reserve_id, kilometer=kilometer, quantity=quantity, entry_datetime_on=datetim, entry_date_on=dateon, entry_by=current_user)
			query.save()
			Reserviour.objects.filter(id=reserve_id).update(stock=newstock)
			messages.info(request, 'done')
			return redirect('fuel_manage')
		else:
			messages.info(request, 'error')
			return redirect('fuel_manage')

		return HttpResponse()
	else:
		return redirect('fuel_manage')


@user_access
def fuel_display(request):
	u_site = user_site(request)
	u_status = user_role(request)
	if u_status == 'main_admin' or u_status == 'main_staff':
		s_item = Fuel.objects.all().order_by('-id')[:30]
	else:
		s_item = Fuel.objects.filter(user_site=u_site).order_by('-id')[:30]
	context = {'s_item': s_item}
	return render(request, 'fuelmaintain/display/fuel_display.html', context)


@user_access
def consumption_detail(request, fid):
	current_user = request.user.username
	u_site = user_site(request)
	item = Fuel.objects.filter(id=fid).first()
	context = {'item': item}
	return render(request, 'fuelmaintain/display/consumption_detail.html', context)


@user_access
def edit_fuel(request, fid):
	item = Fuel.objects.filter(id=fid).first()
	cp = item.coupon_number
	fueldash = []
	seen =set()
	seen_add = seen.add
	ent = Fuel.objects.values_list('coupon_number', flat=True)
	ent = [x for x in ent if not (x in seen or seen_add(x))]
	for s in ent:
		if s != cp:
			fueldash.append(s)
	v_type = VehicleType.objects.all()
	reserve = Reserviour.objects.all()
	f_type = FuelType.objects.all()
	vehis = []
	seen =set()
	seen_add = seen.add
	ent = VehicleList.objects.values_list('vehicle_type_id', flat=True)
	ent = [x for x in ent if not (x in seen or seen_add(x))]
	for e in ent:
		vehi = VehicleList.objects.filter(vehicle_type_id=e, active_status='yes')
		n = len(vehi)
		vehis.append([vehi, range(1,n)])
	context = {'couponlist': fueldash, 'item': item, 'vehis': vehis, 'f_type': f_type, 'v_type': v_type, 'reserve':reserve}
	return render(request, 'fuelmaintain/edit_cunsumption.html', context)


@user_access
def update_fuel(request):
	if request.method=="POST":
		fid = request.POST.get('fid')
		date = request.POST.get('date')
		coupon = request.POST.get('coupon')
		kilometer = request.POST.get('kilometer')
		quantity = request.POST.get('quantity')
		default_quantity = request.POST.get('default_quantity')
		reserve_id = request.POST.get('reserviour')
		reserve_val = request.POST.get('reserviour_name')
		default_reserve_id = request.POST.get('default_reserve')
		vehicle_type = request.POST.get('vehicle_type_name')
		vehicle_type_id = request.POST.get('vehicle_type')
		vehicle = request.POST.get('vehicle')
		num_type = request.POST.get('num_type')
		fuel_type = request.POST.get('fuel_type')

		upreserve1 = Reserviour.objects.filter(id=default_reserve_id).first()
		stock1 = upreserve1.stock
		newstock1 = float(stock1) + float(default_quantity)
		Reserviour.objects.filter(id=default_reserve_id).update(stock=newstock1)
		upreserve2 = Reserviour.objects.filter(id=reserve_id).first()
		stock2 = upreserve2.stock
		newstock2 = float(stock2) - float(quantity)
		if newstock2 > 0 or newstock2 == 0:
			Reserviour.objects.filter(id=reserve_id).update(stock=newstock2)
			Fuel.objects.filter(id=fid).update(coupon_number=coupon, fuel_type=fuel_type, number_type=num_type, vehicle_type=vehicle_type, vehicle_type_id=vehicle_type_id, vehicle_number=vehicle, date=date, kilometer=kilometer, quantity=quantity, reserviour=reserve_val, reserviour_id=reserve_id)
			messages.info(request, 'done')
			return redirect('/edit-fuel/'+str(fid)+'/')
		else:
			messages.info(request, 'error')
			return redirect('/edit-fuel/'+str(fid)+'/')
	else:
		return redirect('fuel_display')


@user_access
def search_fuel_consumption(request):
	if request.method == "POST":
		search = request.POST.get('search')
		sea = search.upper()
		se = search.title()
		s = search.lower()
		u_site = user_site(request)
		u_status = user_role(request)
		if u_status == 'main_admin' or u_status == 'main_staff':
			lookup = Q(consump_number=search) | Q(coupon_number=search) | Q(vehicle_number__icontains=search) | Q(vehicle_type__icontains=search) | Q(user_site__icontains=search) | Q(reserviour__icontains=search) | Q(fuel_type__icontains=search) | Q(consump_number=sea) | Q(coupon_number=sea) | Q(vehicle_number=sea) | Q(vehicle_type=sea) | Q(user_site=sea) | Q(reserviour=sea) | Q(fuel_type=sea) | Q(consump_number=se) | Q(coupon_number=se) | Q(vehicle_number=se) | Q(vehicle_type=se) | Q(user_site=se) | Q(reserviour=se) | Q(fuel_type=se) | Q(consump_number=s) | Q(coupon_number=s) | Q(vehicle_number=s) | Q(vehicle_type=s) | Q(user_site=s) | Q(reserviour=s) | Q(fuel_type=s)
		else:
			lookup = Q(Q(consump_number=search) | Q(coupon_number=search) | Q(vehicle_number__icontains=search) | Q(vehicle_type__icontains=search) | Q(reserviour__icontains=search) | Q(fuel_type__icontains=search) | Q(consump_number=sea) | Q(coupon_number=sea) | Q(vehicle_number=sea) | Q(vehicle_type=sea) | Q(reserviour=sea) | Q(fuel_type=sea) | Q(consump_number=se) | Q(coupon_number=se) | Q(vehicle_number=se) | Q(vehicle_type=se) | Q(reserviour=se) | Q(fuel_type=se) | Q(consump_number=s) | Q(coupon_number=s) | Q(vehicle_number=s) | Q(vehicle_type=s) | Q(reserviour=s) | Q(fuel_type=s)) & Q(user_site=u_site)
		s_item = Fuel.objects.filter(lookup).order_by('-id')
		context = {'s_item': s_item, 'search': search}
		return render(request, 'fuelmaintain/display/fuel_consumption_search.html', context)
	else:
		return redirect('fuel_display')


@user_access
def delete_fuel_consumption(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		Fuel.objects.filter(id=sid).delete()
		messages.info(request, 'done')
		return redirect('fuel_display')
	else:
		return redirect('fuel_display')


@user_access
def print_fuelconsump(request):
	if request.method=="POST":
		jid = request.POST.get('jid')
		job = Fuel.objects.filter(id=jid).first()

		context = {'a': job}
		pdf = render_to_pdf('fuelmaintain/printfuel_consump.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			rnum = random.randint(11111111, 99999999)
			filename = "Reportfuelconsump_%s.pdf" %(rnum)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")
	else:
		return redirect('fuel_display')


@user_access
def fuel_purchase_order(request):
	reserve = Reserviour.objects.all()
	f_type = FuelType.objects.all()
	site_dash = Site.objects.filter(active_status='yes')
	u_site = user_site(request)
	if FuelPurchase.objects.last():
		jd = FuelPurchase.objects.last()
		jn = jd.pon
		newpon = jn+1
	else:
		newpon = 1

	context = {'newpon': newpon, 'f_type': f_type, 'site_dash': site_dash, 'reserve': reserve, 'u_site': u_site}
	return render(request, 'fuelmaintain/fuel_purchase_order.html', context)


@user_access
def add_fuelpurchase(request):
	if request.method=="POST":
		current_user = request.user.username
		u_site = user_site(request)
		reserve = request.POST.get('reserviour')
		quantity = request.POST.get('quantity')
		rate = request.POST.get('rate')
		amount = request.POST.get('amount')
		date = request.POST.get('date')
		purchase_number = request.POST.get('purchase_number')
		pon = request.POST.get('pon')
		location = request.POST.get('location')
		fuel_type = request.POST.get('fuel_type')
		narrat = request.POST.get('narrat')
		if quantity=='' or quantity=='None':
			quantity = 0
			rate = 0
			amount = 0
		if rate=='' or rate=='None':
			rate = 0
			quantity = 0
			amount = 0

		if FuelPurchase.objects.filter(purchase_number=purchase_number).exists():
			messages.info(request, 'error')
			return redirect('fuel_purchase_order')
		else:
			query = FuelPurchase(location=location, fuel_type=fuel_type, purchase_number=purchase_number, pon=pon, issuing_site=u_site, user_site=u_site, entry_date=date, reserviour=reserve, quantity=quantity, rate=rate, amount=amount, narration=narrat, entry_by=current_user)
			query.save()
		
		notify_topic = 'fuel_purchase_order'
		content_id = query.id
		content = 'fuel_purchase_order_add'
		from_site = u_site
		from_user = current_user
		content_val = purchase_number

		q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, from_site=from_site, from_user=from_user, content_val=content_val)
		q.save()


		messages.info(request, 'done')
		return redirect('fuel_purchase_order')
	else:
		return redirect('fuel_purchase_order')


@user_access
def fuel_purchase_display(request):
	u_site = user_site(request)
	u_status = user_role(request)
	s_item = []
	if u_status == 'main_admin' or u_status == 'main_staff':
		s_it = FuelPurchase.objects.all().order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_it, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_item.append([product, range(1, n)])
	else:
		s_it = FuelPurchase.objects.filter(issuing_site=u_site).order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_it, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_item.append([product, range(1, n)])
	context = {'s_item': s_item}
	return render(request, 'fuelmaintain/display/fuel_purchase_display.html', context)


@user_access
def fuel_purchase_detail(request, fid):
	current_user = request.user.username
	u_site = user_site(request)
	site_dash = Site.objects.filter(active_status='yes')
	item = FuelPurchase.objects.filter(id=fid).first()
	context = {'item': item, 'site_dash':site_dash}
	return render(request, 'fuelmaintain/display/fuel_purchase_detail.html', context)


@user_access
def fuel_purchase_edit(request, fid):
	u_site = user_site(request)
	item = FuelPurchase.objects.filter(id=fid).first()
	reserve = Reserviour.objects.all()
	f_type = FuelType.objects.all()
	context = {'item': item, 'f_type': f_type, 'reserve': reserve}
	return render(request, 'fuelmaintain/edit_fuel_purchase.html', context)


@user_access
def update_fuel_purchase_order(request):
	if request.method=="POST":
		pid = request.POST.get('fid')
		reserve = request.POST.get('reserviour')
		quantity = request.POST.get('quantity')
		rate = request.POST.get('rate')
		amount = request.POST.get('amount')
		date = request.POST.get('date')
		purchase_number = request.POST.get('purchase_number')
		location = request.POST.get('location')
		fuel_type = request.POST.get('fuel_type')
		narrat = request.POST.get('narrat')
		if quantity=='' or quantity=='None':
			quantity = 0
			rate = 0
			amount = 0
		if rate=='' or rate=='None':
			rate = 0
			quantity = 0
			amount = 0

		FuelPurchase.objects.filter(id=pid).update(location=location, fuel_type=fuel_type, entry_date=date, reserviour=reserve, quantity=quantity, rate=rate, amount=amount, narration=narrat)

		messages.info(request, 'done')
		return redirect('/fuel-purchase-order-edit/'+str(pid)+'/')
	else:
		return redirect('fuel_purchase_display')


@user_access
def approve_fuel_purchase(request):
	if request.method == "POST":
		current_user = request.user.username
		u_site = user_site(request)
		fid = request.POST.get('pid')
		locate = request.POST.get('site')
		datetim = datetime.datetime.now()
		datetim = datetim.replace(tzinfo=None)
		datetim = datetim.replace(second=0, microsecond=0)
		date = datetime.date.today()

		FuelPurchase.objects.filter(id=fid).update(status='approved', purchase_location=locate, approved_by=current_user, approved_datetime_on=datetim, approved_date_on=date)
		f = FuelPurchase.objects.filter(id=fid).first()
		ffid = f.purchase_number
		sitee = f.issuing_site

		notify_topic = 'fuel_purchase_order'
		content_id = fid
		content = 'fuel_purchase_order_approved'
		from_site = u_site
		from_user = current_user
		content_val = ffid

		q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, from_site=from_site, from_user=from_user, content_val=content_val)
		q.save()

		notify_topic = 'fuel_purchase_order'
		content_id = fid
		content = 'fuel_purchase_order_approve_location'
		from_site = u_site
		from_user = current_user
		content_val = ffid
		content_val2 = locate

		q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, from_site=from_site, from_user=from_user, content_val=content_val, content_val2=content_val2)
		q.save()

		return redirect('/fuel-purchase-order-detail/'+str(fid)+'/')
	else:
		return redirect('fuel_purchase_display')


@user_access
def cancel_fuel_purchase(request):
	if request.method == "POST":
		current_user = request.user.username
		fid = request.POST.get('sid')
		u_site = user_site(request)
		fl = FuelPurchase.objects.filter(id=fid).first()
		f = FuelPurchase.objects.filter(id=fid).first()
		ffid = f.purchase_number
		sitee = f.issuing_site

		FuelPurchase.objects.filter(id=fid).update(status='cancelled', cancelled_by=current_user)

		notify_topic = 'fuel_purchase_order'
		content_id = fid
		content = 'fuel_purchase_order_cancel'
		from_site = u_site
		from_user = current_user
		content_val = ffid
		content_val2 = sitee

		q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, from_site=from_site, from_user=from_user, content_val=content_val, content_val2=content_val2)
		q.save()

		return redirect('/fuel-purchase-order-detail/'+str(fid)+'/')
	else:
		return redirect('fuel_purchase_display')


@user_access
def delete_fuel_purchase(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		FuelPurchase.objects.filter(id=sid).delete()
		messages.info(request, 'done')
		return redirect('fuel_purchase_display')
	else:
		return redirect('fuel_purchase_display')


@user_access
def search_fuel_purchase(request):
	if request.method == "POST":
		search = request.POST.get('search')
		sea = search.upper()
		se = search.title()
		s = search.lower()
		u_site = user_site(request)
		u_status = user_role(request)
		if u_status == 'main_admin' or u_status == 'main_staff':
			lookup = Q(purchase_number=search) | Q(issuing_site=search) | Q(reserviour=search) | Q(fuel_type=search) | Q(location=search) | Q(purchase_number=sea) | Q(issuing_site=sea) | Q(reserviour=sea) | Q(fuel_type=sea) | Q(location=sea) | Q(purchase_number=se) | Q(issuing_site=se) | Q(reserviour=se) | Q(fuel_type=se) | Q(location=se) | Q(purchase_number=s) | Q(issuing_site=s) | Q(reserviour=s) | Q(fuel_type=s) | Q(location=s)
		else:
			lookup = Q(Q(purchase_number=search) | Q(reserviour=search) | Q(fuel_type=search) | Q(location=search) | Q(purchase_number=sea) | Q(reserviour=sea) | Q(fuel_type=sea) | Q(location=sea) | Q(purchase_number=se) | Q(reserviour=se) | Q(fuel_type=se) | Q(location=se) | Q(purchase_number=s) | Q(reserviour=s) | Q(fuel_type=s) | Q(location=s)) & Q(issuing_site=u_site)
		s_item = []
		if u_status == 'main_admin' or u_status == 'main_staff':
			s_it = FuelPurchase.objects.filter(lookup).order_by('-id')
			page = request.GET.get('page', 1)
			paginator = Paginator(s_it, 30)
			try:
				product = paginator.page(page)
			except PageNotAnInteger:
				product = paginator.page(1)
			except EmptyPage:
				product = paginator.page(paginator.num_pages)
			n = len(product)
			s_item.append([product, range(1, n)])
		context = {'s_item': s_item, 'search': search}
		return render(request, 'fuelmaintain/display/fuel_purchase_search.html', context)
	else:
		return redirect('fuel_purchase_display')


@user_access
def print_fuelpurchase(request):
	if request.method=="POST":
		jid = request.POST.get('jid')
		job = FuelPurchase.objects.filter(id=jid).first()

		context = {'a': job}
		pdf = render_to_pdf('fuelmaintain/printfuel_purchase.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			rnum = random.randint(11111111, 99999999)
			filename = "Reportfuelpurchase_%s.pdf" %(rnum)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")
	else:
		return redirect('fuel_purchase_display')


@user_access
def fuel_purchase_bill(request):
	party = FuelPurchase.objects.all()
	supplier_dash = Supplier.objects.all()
	if FuelBill.objects.last():
		jd = FuelBill.objects.last()
		jn = jd.pbn
		newpon = jn+1
	else:
		newpon = 1

	context = {'newpon': newpon, 'party': party, 'supplier_dash': supplier_dash}
	return render(request, 'fuelmaintain/fuel_purchase_bill.html', context)


@user_access
def add_purchase_bill(request):
	if request.method=="POST":
		current_user = request.user.username
		u_site = user_site(request)
		entry_date = request.POST.get('date')
		purchase_bill_number = request.POST.get('purchase_bill_number')
		pbn = request.POST.get('pbn')
		invoice = request.POST.get('invoice')
		supplier = request.POST.get('supplier')
		day = request.POST.get('day')
		trans = request.POST.get('trans')
		quantity = request.POST.get('quantity')
		rate = request.POST.get('rate')
		amount = request.POST.get('amount')
		vatval = request.POST.get('vatval')
		narrat = request.POST.get('narrat')
		sup = Supplier.objects.filter(id=supplier).first()
		sup_name = sup.name
		sup_address = sup.address
		sup_contact = sup.landline
		if vatval == 'yes':
			vat = request.POST.get('vat')
		else:
			vat = ''

		purchase_number = request.POST.get('purchase_number')
		purchase_number = purchase_number.upper()
		if FuelBill.objects.filter(purchase_order_number=purchase_number).exists():
			messages.info(request, 'error')
			return redirect('fuel_purchase_bill')
		jobn = str(purchase_number)
		site = request.POST.get('site'+jobn)
		purchase_order_number = request.POST.get('pn'+jobn)
		reserviour = request.POST.get('reserve'+jobn)
		po_entry_date = request.POST.get('poentry'+jobn)
		po_status = request.POST.get('postatus'+jobn)
		po_approve = request.POST.get('poapprove'+jobn)
		fuel_type = request.POST.get('pofuel'+jobn)
		location = request.POST.get('polocation'+jobn)
		purchase_loc = request.POST.get('popurchase'+jobn)

		reserve = Reserviour.objects.filter(name=reserviour).first()
		stock = reserve.stock
		stock = float(stock)
		grand_stock = stock + float(quantity)
		datetim = datetime.datetime.now()
		datetim = datetim.replace(tzinfo=None)
		datetim = datetim.replace(second=0, microsecond=0)
		date = datetime.date.today()

		query = FuelBill(entry_by=current_user, issuing_site=site, purchase_bill_number=purchase_bill_number, pbn=pbn, purchase_order_number=purchase_order_number, invoice_number=invoice, supplier_id=supplier, supplier_name=sup_name, supplier_address=sup_address, supplier_contact=sup_contact, transaction_type=trans, day=day, reserviour=reserviour, quantity=quantity, rate=rate, vat=vat, amount=amount, po_entry_date=po_entry_date, po_status=po_status, po_approved_by=po_approve, grand_stock=grand_stock, fuel_type=fuel_type, location=location, purchase_location=purchase_loc, approved_datetime_on=datetim, approved_date_on=date, entry_date=entry_date, narration=narrat, user_site=u_site)
		query.save()

		Reserviour.objects.filter(name=reserviour).update(stock=grand_stock)

		messages.info(request, 'done')
		return redirect('fuel_purchase_bill')
	else:
		return redirect('fuel_purchase_bill')


@user_access
def fuel_bill_display(request):
	u_site = user_site(request)
	u_status = user_role(request)
	s_item = []
	if u_status == 'main_admin' or u_status == 'main_staff':
		s_it = FuelBill.objects.all().order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_it, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_item.append([product, range(1, n)])
	else:
		s_it = FuelBill.objects.filter(issuing_site=u_site).order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_it, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_item.append([product, range(1, n)])
	context = {'s_item': s_item}
	return render(request, 'fuelmaintain/display/fuel_bill_display.html', context)


@user_access
def fuel_bill_detail(request, fid):
	item = FuelBill.objects.filter(id=fid).first()
	context = {'item': item}
	return render(request, 'fuelmaintain/display/fuel_bill_detail.html', context)


@user_access
def fuel_bill_edit(request, fid):
	item = FuelBill.objects.filter(id=fid).first()
	reserve = FuelPurchase.objects.all()
	supplier_dash = Supplier.objects.all()
	context = {'item': item, 'party': reserve, 'supplier_dash': supplier_dash}
	return render(request, 'fuelmaintain/edit_fuel_bill.html', context)


@user_access
def edit_purchase_bill(request):
	if request.method=="POST":
		current_user = request.user.username
		fid = request.POST.get('pid')
		print(fid)
		entry_date = request.POST.get('date')
		invoice = request.POST.get('invoice')
		quantity = request.POST.get('quantity')
		supplier = request.POST.get('supplier')
		trans = request.POST.get('trans')
		day = request.POST.get('day')
		dqty = request.POST.get('defaultqty')
		rate = request.POST.get('rate')
		amount = request.POST.get('amount')
		vatval = request.POST.get('vatval')
		narrat = request.POST.get('narrat')
		sup = Supplier.objects.filter(id=supplier).first()
		sup_name = sup.name
		sup_address = sup.address
		sup_contact = sup.landline
		if vatval == 'yes':
			vat = request.POST.get('vat')
		else:
			vat = ''

		purchase_number = request.POST.get('purchase_number')
		purchase_number = purchase_number.upper()
		if FuelBill.objects.filter(purchase_order_number=purchase_number).exclude(id=fid).exists():
			messages.info(request, 'error')
			return redirect('/fuel-purchase-bill-edit/'+str(fid)+'/')
		jobn = str(purchase_number)
		site = request.POST.get('site'+jobn)
		purchase_order_number = request.POST.get('pn'+jobn)
		reserviour = request.POST.get('reserve'+jobn)
		po_entry_date = request.POST.get('poentry'+jobn)
		po_status = request.POST.get('postatus'+jobn)
		po_approve = request.POST.get('poapprove'+jobn)
		fuel_type = request.POST.get('pofuel'+jobn)
		location = request.POST.get('polocation'+jobn)
		purchase_loc = request.POST.get('popurchase'+jobn)

		reserve = Reserviour.objects.filter(name=reserviour).first()
		stock = reserve.stock
		stock = float(stock)
		minus = stock - float(dqty)
		if minus < 0:
			minus = float(dqty) - stock
		grand_stock = minus + float(quantity)

		FuelBill.objects.filter(id=fid).update(issuing_site=site, purchase_order_number=purchase_order_number, invoice_number=invoice, supplier_id=supplier, supplier_name=sup_name, supplier_address=sup_address, supplier_contact=sup_contact, transaction_type=trans, day=day, reserviour=reserviour, quantity=quantity, rate=rate, vat=vat, amount=amount, po_entry_date=po_entry_date, po_status=po_status, po_approved_by=po_approve, grand_stock=grand_stock, fuel_type=fuel_type, location=location, purchase_location=purchase_loc, narration=narrat, entry_date=entry_date)

		Reserviour.objects.filter(name=reserviour).update(stock=grand_stock)

		messages.info(request, 'done')
		return redirect('/fuel-purchase-bill-edit/'+str(fid)+'/')
	else:
		return redirect('fuel_bill_display')


@user_access
def search_fuel_bill(request):
	if request.method == "POST":
		search = request.POST.get('search')
		sea = search.upper()
		se = search.title()
		s = search.lower()
		u_site = user_site(request)
		u_status = user_role(request)
		if u_status == 'main_admin' or u_status == 'main_staff':
			lookup = Q(purchase_bill_number=search) | Q(purchase_order_number=search) | Q(invoice_number=search) | Q(issuing_site=search) | Q(reserviour=search) | Q(fuel_type=search) | Q(purchase_bill_number=sea) | Q(purchase_order_number=sea) | Q(invoice_number=sea) | Q(issuing_site=sea) | Q(reserviour=sea) | Q(fuel_type=sea) | Q(purchase_bill_number=se) | Q(purchase_order_number=se) | Q(invoice_number=se) | Q(issuing_site=se) | Q(reserviour=se) | Q(fuel_type=se) | Q(purchase_bill_number=s) | Q(purchase_order_number=s) | Q(invoice_number=s) | Q(issuing_site=s) | Q(reserviour=s) | Q(fuel_type=s)
		else:
			lookup = Q(Q(purchase_bill_number=search) | Q(purchase_order_number=search) | Q(invoice_number=search) | Q(reserviour=search) | Q(fuel_type=search) | Q(purchase_bill_number=sea) | Q(purchase_order_number=sea) | Q(invoice_number=sea) | Q(reserviour=sea) | Q(fuel_type=sea) | Q(purchase_bill_number=se) | Q(purchase_order_number=se) | Q(invoice_number=se) | Q(reserviour=se) | Q(fuel_type=se) | Q(purchase_bill_number=s) | Q(purchase_order_number=s) | Q(invoice_number=s) | Q(reserviour=s) | Q(fuel_type=s)) & Q(issuing_site=u_site)
		s_item = []
		if u_status == 'main_admin' or u_status == 'main_staff':
			s_it = FuelBill.objects.filter(lookup).order_by('-id')
			page = request.GET.get('page', 1)
			paginator = Paginator(s_it, 30)
			try:
				product = paginator.page(page)
			except PageNotAnInteger:
				product = paginator.page(1)
			except EmptyPage:
				product = paginator.page(paginator.num_pages)
			n = len(product)
			s_item.append([product, range(1, n)])
		context = {'s_item': s_item, 'search': search}
		return render(request, 'fuelmaintain/display/fuel_bill_search.html', context)
	else:
		return redirect('fuel_bill_display')


@user_access
def print_fuelbill(request):
	if request.method=="POST":
		jid = request.POST.get('jid')
		job = FuelBill.objects.filter(id=jid).first()

		context = {'a': job}
		pdf = render_to_pdf('fuelmaintain/printfuel_bill.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			rnum = random.randint(11111111, 99999999)
			filename = "Reportfuelbill_%s.pdf" %(rnum)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")
	else:
		return redirect('fuel_bill_display')


@user_access
def delete_fuel_bill(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		FuelBill.objects.filter(id=sid).delete()
		messages.info(request, 'done')
		return redirect('fuel_bill_display')
	else:
		return redirect('fuel_bill_display')


@user_access
def vehicle_type(request):
	v_type = VehicleType.objects.all().order_by('-id')
	context = {'v_type': v_type}
	return render(request, 'fuelmaintain/vehicle_type.html', context)


@user_access
def add_vehicle_type(request):
	if request.method=="POST":
		name = request.POST.get('vehi_type')
		url = request.POST.get('url')
		if VehicleType.objects.filter(url=url).exists():
			messages.info(request, 'error')
			return redirect('vehicle_type')
		else:
			query = VehicleType(type_name=name, url=url)
			query.save()

			messages.info(request, 'done')
			return redirect('vehicle_type')
	else:
		return redirect('vehicle_type')


@user_access
def vehicle_type_display(request):
	v_item = VehicleType.objects.all()
	context = {'party': fuel}
	return render(request, 'fuelmaintain/display/vehicle_type_display.html', context)


@user_access
def update_vehicle_type(request):
	if request.method=="POST":
		fid = request.POST.get('lid')
		defaulturl = request.POST.get('default')
		name = request.POST.get('name')
		url = request.POST.get('url')

		if VehicleType.objects.filter(url=url).exclude(id=fid).exists():
			messages.info(request, 'error')
			return redirect('vehicle_type')
		else:
			VehicleType.objects.filter(id=fid).update(type_name=name, url=url)
			

		return redirect('vehicle_type')
	else:
		return redirect('vehicle_type')


@user_access
def delete_vehicle_type(request):
	if request.method=="POST":
		sid = request.POST.get('lid')

		VehicleType.objects.filter(id=sid).delete()
		messages.info(request, 'done')
		return redirect('vehicle_type')
	else:
		return redirect('vehicle_type')


@user_access
def reserviour_report(request):
	reserve = Reserviour.objects.all()
	reserve_name = 'none'
	stocke = 0
	session = 0
	grand = 0
	consumption = 0
	total_fuel = 0
	total_price = 0
	opening = 0
	total_con = 0
	filter_purchase = []
	fuel_consump = []
	purchasee = []
	consump_total = []
	total_transfer = 0
	total_receive = 0
	rrid = []
	rid = 0
	if 'reserviour_id' in request.session:
		rid = request.session['reserviour_id']
		reser = Reserviour.objects.filter(id=rid).first()
		reserve_name = reser.name
		if FuelBill.objects.filter(reserviour=reserve_name).last():
			session = 1
			stocke = reser.stock
			opening = reser.opening
			purchasee = FuelBill.objects.filter(reserviour=reserve_name).last()
			approve_dt = purchasee.approved_datetime_on
			approve_d = purchasee.approved_date_on
			pid = purchasee.id
			grand = purchasee.grand_stock
			consumption = float(grand)-float(stocke)
			fuel_consum = Fuel.objects.filter(reserviour_id=rid).order_by('id')
			for f in fuel_consum:
				fid = f.id
				entry_dt = f.entry_datetime_on
				if entry_dt > approve_dt or entry_dt == approve_dt:
					rrid.append(fid)
			fuel_consump = Fuel.objects.filter(id__in=rrid).order_by('date')
			consump_total = Fuel.objects.filter(id__in=rrid).aggregate(Sum('quantity'))
			total_fuel = FuelBill.objects.filter(reserviour=reserve_name).aggregate(Sum('quantity'))
			total_price = FuelBill.objects.filter(reserviour=reserve_name).aggregate(Sum('amount'))
			total_con = Fuel.objects.filter(reserviour_id=rid).aggregate(Sum('quantity'))
		else:
			session = 1
			stocke = reser.stock
			grand = reser.opening
			opening = reser.opening
			purchasee = []
			consumption = float(grand)-float(stocke)
			filter_purchase = []
			fuel_consump = Fuel.objects.filter(reserviour_id=rid).order_by('date')
			consump_total = Fuel.objects.filter(reserviour_id=rid).aggregate(Sum('quantity'))
			total_fuel = FuelBill.objects.filter(reserviour=reserve_name).aggregate(Sum('quantity'))
			total_price = FuelBill.objects.filter(reserviour=reserve_name).aggregate(Sum('amount'))
			total_con = Fuel.objects.filter(reserviour_id=rid).aggregate(Sum('quantity'))

		if FuelInternalTransfer.objects.filter(from_reserviour=reserve_name).exists():
			total_transfer = FuelInternalTransfer.objects.filter(from_reserviour=reserve_name).aggregate(Sum('quantity'))
		if FuelInternalTransfer.objects.filter(to_reserviour=reserve_name).exists():
			total_receive = FuelInternalTransfer.objects.filter(to_reserviour=reserve_name).aggregate(Sum('quantity'))

	context = {'reserviour': reserve, 'session':session, 'rid': rid, 'total_fuel': total_fuel, 'total_price': total_price, 'total_con': total_con, 'opening': opening, 'purchasee': purchasee, 'reserve_name': reserve_name, 'stocke': stocke, 'grand':grand, 'consumption': consumption, 'filter_purchase': filter_purchase, 'fuel_consump': fuel_consump, 'consump_total': consump_total, 'total_transfer': total_transfer, 'total_receive': total_receive}
	return render(request, 'fuelmaintain/reserviour_report.html', context)


@user_access
def reserviour_report_pdf(request):
	if request.method=="POST":
		reserve_name = 'none'
		fuel_consump = []
		consump_total = []
		rrid = []
		rid = 0
		pbn = ''
		try:
			rid = request.POST.get('rid')
			reser = Reserviour.objects.filter(id=rid).first()
			reserve_name = reser.name
			purchase = FuelBill.objects.filter(reserviour=reserve_name).last()
			approve_dt = purchase.approved_datetime_on
			approve_d = purchase.approved_date_on
			pbn = purchase.purchase_bill_number
			fuel_consum = Fuel.objects.filter(reserviour_id=rid).order_by('id')
			for f in fuel_consum:
				fid = f.id
				entry_dt = f.entry_datetime_on
				if entry_dt > approve_dt or entry_dt == approve_dt:
					rrid.append(fid)
			fuel_consump = Fuel.objects.filter(id__in=rrid).order_by('date')
			consump_total = Fuel.objects.filter(id__in=rrid).aggregate(Sum('quantity'))
		except:
			rid = request.POST.get('rid')
			reser = Reserviour.objects.filter(id=rid).first()
			reserve_name = reser.name
			fuel_consump = Fuel.objects.filter(reserviour_id=rid).order_by('date')
			consump_total = Fuel.objects.filter(reserviour_id=rid).aggregate(Sum('quantity'))

		context = {'fuel_consump': fuel_consump, 'consump_total': consump_total, 'reserviour': reserve_name, 'pbn': pbn}
		pdf = render_to_pdf('fuelmaintain/print_reserviour.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			rnum = random.randint(11111111, 99999999)
			filename = "Report_reserviour_%s.pdf" %(rnum)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")


@user_access
def reserviour_session(request,rid):
	# del request.session['reserviour_filter_id']
	# del request.session['reserviour_purchase_id']
	# request.session.modified = True
	request.session['reserviour_id'] = rid
	return  redirect('reserviour_report')


def maintainance_dashboard(request):
	count1 = Fuel.objects.all().count()
	count2 = MaintainanceBill.objects.all().count()
	count3 = VehicleList.objects.all().count()
	count4 = VehicleTrack.objects.all().count()
	context = {'count1': count1, 'count2': count2, 'count3': count3, 'count4': count4}
	return render(request, 'fuelmaintain/maintainance_dashboard.html', context)


@user_access
def fuel_type_dash(request):
	v_type = FuelType.objects.all().order_by('-id')
	context = {'v_type': v_type}
	return render(request, 'fuelmaintain/fuel_type.html', context)


@user_access
def add_fuel_type(request):
	if request.method=="POST":
		name = request.POST.get('vehi_type')
		url = request.POST.get('url')
		if FuelType.objects.filter(url=url).exists():
			messages.info(request, 'error')
			return redirect('fuel_type')
		else:
			query = FuelType(name=name, url=url)
			query.save()

			messages.info(request, 'done')
			return redirect('fuel_type')
	else:
		return redirect('fuel_type')


@user_access
def fuel_type_display(request):
	fuel = FuelType.objects.all()
	context = {'party': fuel}
	return render(request, 'fuelmaintain/display/fuel_type_display.html', context)


@user_access
def update_fuel_type(request):
	if request.method=="POST":
		fid = request.POST.get('lid')
		defaulturl = request.POST.get('default')
		name = request.POST.get('name')
		url = request.POST.get('url')

		if FuelType.objects.filter(url=url).exclude(id=fid).exists():
			messages.info(request, 'error')
			return redirect('fuel_type')
		else:
			FuelType.objects.filter(id=fid).update(name=name, url=url)
			
			messages.info(request, 'done')
			return redirect('fuel_type')
	else:
		return redirect('fuel_type')


@user_access
def delete_fuel_type(request):
	if request.method=="POST":
		sid = request.POST.get('lid')

		FuelType.objects.filter(id=sid).delete()
		messages.info(request, 'done')
		return redirect('fuel_type')
	else:
		return redirect('fuel_type')


@user_access
def problem_category(request):
	problem_dash = ProblemCategory.objects.all().order_by('-id')
	context = {'problem_dash': problem_dash}
	return render(request, 'fuelmaintain/problem_category.html', context)


@user_access
def add_problem(request):
	if request.method=="POST":
		name = request.POST.get('problem')
		url = request.POST.get('url')

		if ProblemCategory.objects.filter(problem_url=url).exists():
			messages.info(request, 'error')
			return redirect('problem_category')
		else:
			query = ProblemCategory(name=name, problem_url=url)
			query.save()
			messages.info(request, 'done')
			return redirect('problem_category')
	else:
		return redirect('problem_category')


@user_access
def problem_display(request):
	fuel = ProblemCategory.objects.all()
	context = {'party': fuel}
	return render(request, 'fuelmaintain/display/problem_display.html', context)


@user_access
def update_problem(request):
	if request.method=="POST":
		fid = request.POST.get('lid')
		defaulturl = request.POST.get('default')
		name = request.POST.get('name')
		url = request.POST.get('url')

		if ProblemCategory.objects.filter(problem_url=url).exclude(id=fid).exists():
			messages.info(request, 'error')
			return redirect('problem_category')
		else:
			ProblemCategory.objects.filter(id=fid).update(name=name, problem_url=url)
			
			messages.info(request, 'done')
			return redirect('problem_category')
	else:
		return redirect('problem_category')


@user_access
def delete_problem(request):
	if request.method=="POST":
		sid = request.POST.get('lid')

		ProblemCategory.objects.filter(id=sid).delete()
		messages.info(request, 'done')
		return redirect('problem_category')
	else:
		return redirect('problem_category')


@user_access
def problem_subcategory(request):
	all_cats = []
	length = 0
	seen =set()
	seen_add = seen.add
	ent = ProblemSubCategory.objects.values_list('problem_url', flat=True)
	ent = [x for x in ent if not (x in seen or seen_add(x))]
	for c in ent:
		subcategory = ProblemSubCategory.objects.filter(problem_url=c)

		n = len(subcategory)
		if n > 0:
			length = 1
		all_cats.append([subcategory, range(1, n)])
	problem_dash = ProblemCategory.objects.all()
	context = {'all_cats': all_cats, 'problem_dash': problem_dash}
	return render(request, 'fuelmaintain/problem_subcategory.html', context)



@user_access
def add_subproblem(request):
	if request.method=="POST":
		name = request.POST.get('subproblem')
		url = request.POST.get('url')
		problem_url = request.POST.get('problemval')
		problem_name = request.POST.get('problem_name')
		if ProblemSubCategory.objects.filter(problem_url=problem_url, problem_suburl=url).exists():
			messages.info(request, 'error')
			return redirect('problem_subcategory')
		else:
			query = ProblemSubCategory(name=name, problem_suburl=url, problem_url=problem_url, problem_name=problem_name)
			query.save()

			messages.info(request, 'done')
			return redirect('problem_subcategory')
	else:
		return redirect('problem_subcategory')


@user_access
def update_subproblem(request):
	if request.method=="POST":
		fid = request.POST.get('lid')
		defaulturl = request.POST.get('default')
		name = request.POST.get('name')
		url = request.POST.get('url')
		problem_url = request.POST.get('purl')
		if ProblemSubCategory.objects.filter(problem_url=problem_url, problem_suburl=url).exclude(id=fid).exists():
			messages.info(request, 'error')
			return redirect('problem_subcategory')
		else:
			ProblemSubCategory.objects.filter(id=fid).update(name=name, problem_suburl=url)
			
			messages.info(request, 'done')
			return redirect('problem_subcategory')

		return HttpResponse()
	else:
		return redirect('problem_subcategory')


@user_access
def delete_subproblem(request):
	if request.method=="POST":
		sid = request.POST.get('lid')

		ProblemSubCategory.objects.filter(id=sid).delete()
		messages.info(request, 'done')
		return redirect('problem_subcategory')
	else:
		return redirect('problem_subcategory')


@user_access
def manage_maintainance(request):
	problem = ProblemCategory.objects.all()
	supplier_dash = Supplier.objects.all()
	v_type = VehicleType.objects.all()
	item_real = StockItem.objects.all()
	u_site = user_site(request)
	porder = PurchaseOrder.objects.filter(status='approved', issuing_site=u_site, po_vehi="yes")
	sub_material = []
	seen =set()
	seen_add = seen.add
	ent = ProblemSubCategory.objects.values_list('problem_url', flat=True)
	ent = [x for x in ent if not (x in seen or seen_add(x))]
	for s in ent:
		submat = ProblemSubCategory.objects.filter(problem_url=s)
		n = len(submat)
		sub_material.append([submat, range(1,n)])
	ivoice = []
	seen =set()
	seen_add = seen.add
	ent = MaintainanceBill.objects.values_list('bill_number', flat=True)
	ent = [x for x in ent if not (x in seen or seen_add(x))]
	for s in ent:
		ivoice.append(s)

	if MaintainanceBill.objects.last():
		jd = MaintainanceBill.objects.last()
		jn = jd.pei
		newpei = jn+1
	else:
		newpei = 1

	vehis = []
	seen =set()
	seen_add = seen.add
	ent = VehicleList.objects.values_list('vehicle_type_id', flat=True)
	ent = [x for x in ent if not (x in seen or seen_add(x))]
	for e in ent:
		vehi = VehicleList.objects.filter(vehicle_type_id=e, active_status='yes')
		n = len(vehi)
		vehis.append([vehi, range(1,n)])

	pitem = PurchaseItem.objects.all()
	psupa = []
	seen = set()
	seen_add = seen.add
	tran = PurchaseEntry.objects.values_list('purchase_order_number', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for r in ent:
		ps = PurchaseEntry.objects.filter(purchase_order_number=r)
		n = len(ps)
		psupa.append([ps, range(1,n)])

	igoods = []
	tran = InvoiceItem.objects.values_list('purchaseid', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for s in ent:
		igood = InvoiceItem.objects.filter(purchaseid=s, issue_use="no", grn_status='yes').exclude(Q(damage='all') | Q(retur='all'))
		n = len(igood)
		igoods.append([igood, range(1,n)])

	ingg = []
	intg = InternalGrn.objects.filter(user_site=u_site)
	for i in intg:
		ingg.append(i.grn_number)

	itrans = []
	tran = InternalGrnItems.objects.values_list('goodsid', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for s in ent:
		itra = InternalGrnItems.objects.filter(goodsid=s, grn__in=ingg, invoice_status="no").exclude(damage='all')
		n = len(itra)
		itrans.append([itra, range(1,n)])

	purinvoice = PurchaseEntry.objects.filter(issue_use='no')

	itemsel = []
	seen =set()
	seen_add = seen.add
	ent = StockItem.objects.values_list('main_url', flat=True)
	ent = [x for x in ent if not (x in seen or seen_add(x))]
	for e in ent:
		isel = StockItem.objects.filter(main_url=e)
		n = len(isel)
		itemsel.append([isel, range(1,n)])

	stock_cat = StockCategory.objects.all()
	psupaa = []
	seen = set()
	seen_add = seen.add
	tran = StockSubCategory.objects.values_list('cat_url', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for r in ent:
		pss = StockSubCategory.objects.filter(cat_url=r)
		n = len(ps)
		psupaa.append([pss, range(1,n)])

	context = {'psupa': psupa, 'itemsel': itemsel, 'stock_cat': stock_cat, 'psupaa': psupaa, 'purinvoice': purinvoice, 'igoods': igoods, 'itrans': itrans, 'pitem': pitem, 'sub_material': sub_material, 'item_real': item_real, 'vehis': vehis, 'v_type': v_type, 'supplier_dash': supplier_dash, 'problem': problem, 'ivoice': ivoice, 'porder': porder, 'newpei': newpei}
	return render(request, 'fuelmaintain/maintainance.html', context)


@user_access
def add_maintainance(request):
	if request.method=="POST":
		current_user = request.user.username
		u_site = user_site(request)
		entry_date = request.POST.get('date')
		billdate = request.POST.get('invoice_date')
		billnum = request.POST.get('invoice')
		maintain_number = request.POST.get('maintain_number')
		vehicle_type = request.POST.get('vehicle_type')
		vehicle_type_id = request.POST.get('vehicle_type_id')
		num_type = request.POST.get('num_type')
		vehicle = request.POST.get('vehiclee')
		kilometer = request.POST.get('kilometer')
		problem = request.POST.get('problem')
		subproblem = request.POST.get('subproblem')
		narrat = request.POST.get('narrat')
		pei = request.POST.get('pvn_count')
		jorder = request.POST.get('jorder')
		gjorder = request.POST.get('gjorder')
		subtotal = request.POST.get('subtotal')
		labour = request.POST.get('labour')
		total = request.POST.get('total')
		hour = request.POST.get('hour')
		itemadd = request.POST.getlist('itemadd')
		gitemadd = request.POST.getlist('gitemadd')
		exitemadd = request.POST.getlist('exitemadd')
		supplier = ''
		sup_name = ''
		sup_address = ''
		sup_contact = ''
		if len(itemadd) == 0 and len(gitemadd) == 0:
			messages.info(request, 'error')
			return redirect('manage_maintainance')
		if MaintainanceBill.objects.filter(vehicle_number=vehicle, hour=hour).exists():
			messages.info(request, 'error')
			return redirect('manage_maintainance')
		if jorder == 'yes':
			jobnumber = request.POST.get('jobnumber')
			jobnumber = jobnumber.replace(" ", "")
			jobnumber = jobnumber.upper()
			p = PurchaseOrder.objects.filter(purchase_number=jobnumber).first()
			status = p.status
			jedate = p.entry_date
			japprove = p.approved_by 
			
		if jorder == 'no':
			jobnumber = ''
			status = ''
			jedate = ''
			japprove = ''

		if jorder == 'yes':
			for i in itemadd:
				iid = str(i)
				if request.POST.get('inameid'+iid):
					item_id = request.POST.get('inameid'+iid)
					quantity = request.POST.get('iqty'+iid)
					if StockEntry.objects.filter(item_id=item_id, stock_site=u_site).exists():
						sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
						qt = float(sq.quantity)
						if qt>float(quantity) or qt==float(quantity):
							print('ok')
						else:
							messages.info(request, 'error')
							return redirect('manage_maintainance')
					else:
						messages.info(request, 'error')
						return redirect('manage_maintainance')
		if gjorder == 'yes':
			for i in gitemadd:
				iid = str(i)
				if request.POST.get('ginameid'+iid):
					item_id = request.POST.get('ginameid'+iid)
					quantity = request.POST.get('giqty'+iid)
					if StockEntry.objects.filter(item_id=item_id, stock_site=u_site).exists():
						sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
						qt = float(sq.quantity)
						if qt>float(quantity) or qt==float(quantity):
							print('ok')
						else:
							messages.info(request, 'error')
							return redirect('manage_maintainance')
					else:
						messages.info(request, 'error')
						return redirect('manage_maintainance')
		if len(exitemadd) > 0:
			for i in itemadd:
				iid = str(i)
				if request.POST.get('iid'+iid):
					item_id = request.POST.get('iid'+iid)
					quantity = request.POST.get('iqty'+iid)
					if StockEntry.objects.filter(item_id=item_id, stock_site=u_site).exists():
						sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
						qt = float(sq.quantity)
						if qt>float(quantity) or qt==float(quantity):
							print('ok')
						else:
							messages.info(request, 'error')
							return redirect('manage_maintainance')
					else:
						messages.info(request, 'error')
						return redirect('manage_maintainance')

		query = MaintainanceBill(entry_by=current_user, maintain_number=maintain_number, hour=hour, pei=pei, bill_number=billnum, purchase_order_number=jobnumber, purchase_entry_date=jedate, purchase_approve_by=japprove, number_type=num_type, vehicle_type_id=vehicle_type_id, vehicle_type=vehicle_type, vehicle_number=vehicle, purchase_status=status, kilometer=kilometer, problem_category=problem, problem_subcategory=subproblem, supplier_id=supplier, supplier_name=sup_name, supplier_address=sup_address, supplier_contact=sup_contact, narration=narrat, entry_date=entry_date, bill_date=billdate, sub_total=subtotal, labour_charge=labour, total=total, jorder=jorder, gjorder=gjorder, user_site=u_site)
		query.save()
		mid = query.id

		if jorder == 'yes':
			jobnumber = request.POST.get('jobnumber')
			jobnumber = jobnumber.replace(" ", "")
			pvnval = request.POST.getlist('pvnval')
			for p in pvnval:
				p = p.upper()
				pe = PurchaseEntry.objects.filter(voucher_number=p).first()
				voucher_number = pe.voucher_number
				invoice = pe.invoice_number
				invoice_type = pe.invoice_type
				supplier = pe.supplier_name
				subtotal = pe.sub_total
				discount_amt = pe.discount_amt
				discount_per = pe.discount_per
				vat = pe.vat
				total = pe.total
				query = MaintainInvoice(maintainid=mid, maintain_number=maintain_number, purchase_order_number=jobnumber, voucher_number=p, invoice_number=invoice, invoice_type=invoice_type, supplier=supplier, sub_total=subtotal, discount_amt=discount_amt, discount_per=discount_per, vat=vat, total=total)
				query.save()
				PurchaseEntry.objects.filter(voucher_number=p).update(issue_use='yes')

		if jorder == 'yes':
			for i in itemadd:
				iid = str(i)
				jobnumber = request.POST.get('jobnumber')
				jobnumber = jobnumber.replace(" ", "")
				jobnumber = jobnumber.upper()
				if request.POST.get('ipvn'+iid):
					pvn = request.POST.get('ipvn'+iid)
					item_id = request.POST.get('inameid'+iid)
					item_name = request.POST.get('iname'+iid)
					alias = request.POST.get('ialias'+iid)
					uom = request.POST.get('iuom'+iid)
					quantity = request.POST.get('iqty'+iid)
					rate = request.POST.get('irate'+iid)
					amount = request.POST.get('iamt'+iid)
					dper = request.POST.get('idisper'+iid)
					damt = request.POST.get('idisamt'+iid)
					itemquery = MaintainanceItem(bill_id=mid, purchase_id=jobnumber, pvn=pvn, item_id=item_id, item_name=item_name, alias=alias, uom=uom, quantity=quantity, rate=rate, amount=amount, discount_per=dper, discount_amt=damt)
					itemquery.save()
					InvoiceItem.objects.filter(pvn=pvn).update(issue_use='yes')
					sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
					qt = float(sq.quantity)
					newqty = qt - float(quantity)
					StockEntry.objects.filter(item_id=item_id, stock_site=u_site).update(quantity=newqty)

		ginvc = []
		if gjorder == 'yes':
			for i in gitemadd:
				iid = str(i)
				if request.POST.get('gipvn'+iid):
					pvn = request.POST.get('gipvn'+iid)
					item_id = request.POST.get('ginameid'+iid)
					item_name = request.POST.get('giname'+iid)
					alias = request.POST.get('gialias'+iid)
					uom = request.POST.get('giuom'+iid)
					quantity = request.POST.get('giqty'+iid)
					itemquery = MaintainanceItem(bill_id=mid, pvn=pvn, item_id=item_id, item_name=item_name, alias=alias, uom=uom, quantity=quantity, rate=0, amount=0, discount_per=0, discount_amt=0, itnn='yes')
					itemquery.save()
					ginvc.append(pvn)
					sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
					qt = float(sq.quantity)
					newqty = qt - float(quantity)
					StockEntry.objects.filter(item_id=item_id, stock_site=u_site).update(quantity=newqty)

		if len(ginvc) > 0:
			ginvc = list(set(ginvc))
			for i in ginvc:
				InternalGrn.objects.filter(grn_number=i).update(invoice_id=maintain_number, invoice_status='yes')
				InternalGrnItems.objects.filter(grn=i).update(invoice_id=maintain_number, invoice_status='yes')

		if len(exitemadd) > 0:
			for i in itemadd:
				iid = str(i)
				if request.POST.get('iid'+iid):
					item_id = request.POST.get('iid'+iid)
					item_name = request.POST.get('iname'+iid)
					alias = request.POST.get('ialias'+iid)
					uom = request.POST.get('iuom'+iid)
					quantity = request.POST.get('iqty'+iid)
					rate = request.POST.get('irate'+iid)
					amount = request.POST.get('iamt'+iid)
					dper = request.POST.get('idisper'+iid)
					damt = request.POST.get('idisamt'+iid)
					itemquery = MaintainanceItem(bill_id=mid, item_id=item_id, item_name=item_name, alias=alias, uom=uom, quantity=quantity, rate=rate, amount=amount, discount_per=dper, discount_amt=damt)
					itemquery.save()
					sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
					qt = float(sq.quantity)
					newqty = qt - float(quantity)
					StockEntry.objects.filter(item_id=item_id, stock_site=u_site).update(quantity=newqty)


		messages.info(request, 'done')
		return redirect('manage_maintainance')
	else:
		return redirect('manage_maintainance')


@user_access
def maintainance_display(request):
	u_site = user_site(request)
	u_status = user_role(request)
	s_item = []
	if u_status == 'main_admin' or u_status == 'main_staff':
		s_it = MaintainanceBill.objects.all().order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_it, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_item.append([product, range(1, n)])
	else:
		s_it = MaintainanceBill.objects.filter(user_site=u_site).order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_it, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_item.append([product, range(1, n)])
	context = {'s_item': s_item}
	return render(request, 'fuelmaintain/display/maintain_display.html', context)


@user_access
def maintainance_detail(request, mid):
	if MaintainanceBill.objects.filter(id=mid).exists():
		minvoice = []
		item = MaintainanceBill.objects.filter(id=mid).first()
		sgoods = MaintainanceItem.objects.filter(bill_id=mid)
		if MaintainInvoice.objects.filter(maintainid=mid).exists():
			minvoice = MaintainInvoice.objects.filter(maintainid=mid)
		context = {'item': item, 'sgoods': sgoods, 'minvoice': minvoice}
		return render(request, 'fuelmaintain/display/maintain_detail.html', context)
	else:
		return redirect('maintainance_display')


@user_access
def search_maintainance(request):
	if request.method == "POST":
		search = request.POST.get('search')
		sea = search.upper()
		se = search.title()
		s = search.lower()
		u_site = user_site(request)
		u_status = user_role(request)
		if u_status == 'main_admin' or u_status == 'main_staff':
			lookup = Q(maintain_number=search) | Q(vehicle_number__icontains=search) | Q(problem_category=search) | Q(problem_subcategory=search) | Q(supplier_name__icontains=search) | Q(purchase_order_number=search) | Q(vehicle_type__icontains=search) | Q(user_site__icontains=search) | Q(maintain_number=sea) | Q(vehicle_number=sea) | Q(problem_category=sea) | Q(problem_subcategory=sea) | Q(supplier_name=sea) | Q(purchase_order_number=sea) | Q(vehicle_type=sea) | Q(user_site=sea) | Q(maintain_number=se) | Q(vehicle_number=se) | Q(problem_category=se) | Q(problem_subcategory=se) | Q(supplier_name=se) | Q(purchase_order_number=se) | Q(vehicle_type=se) | Q(user_site=se) | Q(maintain_number=s) | Q(vehicle_number=s) | Q(problem_category=s) | Q(problem_subcategory=s) | Q(supplier_name=s) | Q(purchase_order_number=s) | Q(vehicle_type=s) | Q(user_site=s)
		else:
			lookup = Q(Q(maintain_number=search) | Q(vehicle_number__icontains=search) | Q(problem_category=search) | Q(problem_subcategory=search) | Q(supplier_name__icontains=search) | Q(purchase_order_number=search) | Q(vehicle_type__icontains=search) | Q(maintain_number=sea) | Q(vehicle_number=sea) | Q(problem_category=sea) | Q(problem_subcategory=sea) | Q(supplier_name=sea) | Q(purchase_order_number=sea) | Q(vehicle_type=sea) | Q(maintain_number=se) | Q(vehicle_number=se) | Q(problem_category=se) | Q(problem_subcategory=se) | Q(supplier_name=se) | Q(purchase_order_number=se) | Q(vehicle_type=se) | Q(maintain_number=s) | Q(vehicle_number=s) | Q(problem_category=s) | Q(problem_subcategory=s) | Q(supplier_name=s) | Q(purchase_order_number=s) | Q(vehicle_type=s)) & Q(user_site=u_site)
		s_item = []
		s_it = MaintainanceBill.objects.filter(lookup).order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(s_it, 30)
		try:
			product = paginator.page(page)
		except PageNotAnInteger:
			product = paginator.page(1)
		except EmptyPage:
			product = paginator.page(paginator.num_pages)
		n = len(product)
		s_item.append([product, range(1, n)])
		context = {'s_item': s_item, 'search': search}
		return render(request, 'fuelmaintain/display/maintainance_search.html', context)
	else:
		return redirect('maintainance_display')


@user_access
def print_maintainance(request):
	if request.method=="POST":
		minvoice = []
		jid = request.POST.get('jid')
		job = MaintainanceBill.objects.filter(id=jid).first()
		igoods = MaintainanceItem.objects.filter(bill_id=jid)
		if MaintainInvoice.objects.filter(maintainid=jid).exists():
			minvoice = MaintainInvoice.objects.filter(maintainid=jid)

		context = {'a': job, 'igoods': igoods, 'minvoice': minvoice}
		pdf = render_to_pdf('fuelmaintain/printmaintain.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			rnum = random.randint(11111111, 99999999)
			filename = "Reportmaintain_%s.pdf" %(rnum)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")
	else:
		return redirect('maintainance_display')


@user_access
def edit_maintainance(request, mid):
	item = MaintainanceBill.objects.filter(id=mid).first()
	iv = item.bill_number
	u_site = item.user_site
	bills = []
	gmitms = []
	bill = MaintainanceItem.objects.filter(bill_id=mid).exclude(itnn='yes')
	bill_count = []
	bill_len = len(bill)
	a = 0
	for b in bill:
		a = a+1
		bill_count.append(a)
	bills.append([bill, range(1, bill_len)])
	problem = ProblemCategory.objects.all()
	porder = PurchaseOrder.objects.filter(status='approved', issuing_site=u_site, po_vehi="yes")
	supplier_dash = Supplier.objects.all()
	v_type = VehicleType.objects.all()
	item_real = StockItem.objects.all()
	sub_material = []
	seen =set()
	seen_add = seen.add
	ent = ProblemSubCategory.objects.values_list('problem_url', flat=True)
	ent = [x for x in ent if not (x in seen or seen_add(x))]
	for s in ent:
		submat = ProblemSubCategory.objects.filter(problem_url=s)
		n = len(submat)
		sub_material.append([submat, range(1,n)])
	ivoice = []
	seen =set()
	seen_add = seen.add
	ent = MaintainanceBill.objects.values_list('bill_number', flat=True)
	ent = [x for x in ent if not (x in seen or seen_add(x))]
	for s in ent:
		if s != iv:
			ivoice.append(s)

	vehis = []
	seen =set()
	seen_add = seen.add
	ent = VehicleList.objects.values_list('vehicle_type_id', flat=True)
	ent = [x for x in ent if not (x in seen or seen_add(x))]
	for e in ent:
		vehi = VehicleList.objects.filter(vehicle_type_id=e, active_status='yes')
		n = len(vehi)
		vehis.append([vehi, range(1,n)])

	pitem = PurchaseItem.objects.all()

	psupa = []
	seen = set()
	seen_add = seen.add
	tran = PurchaseEntry.objects.values_list('purchase_order_number', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for r in ent:
		ps = PurchaseEntry.objects.filter(purchase_order_number=r)
		n = len(ps)
		psupa.append([ps, range(1,n)])

	minv = MaintainInvoice.objects.filter(maintainid=mid)
	mis = []
	for m in minv:
		mi = m.voucher_number
		mis.append(mi)

	igoods = []
	tran = InvoiceItem.objects.values_list('purchaseid', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for s in ent:
		igood = InvoiceItem.objects.filter(purchaseid=s, issue_use='no', grn_status='yes').exclude(Q(damage='all') | Q(retur='all'))
		n = len(igood)
		igoods.append([igood, range(1,n)])

	ingg = []
	intg = InternalGrn.objects.filter(user_site=u_site)
	for i in intg:
		ingg.append(i.grn_number)

	itrans = []
	tran = InternalGrnItems.objects.values_list('goodsid', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for s in ent:
		itra = InternalGrnItems.objects.filter(goodsid=s, grn__in=ingg, invoice_status="no").exclude(damage='all')
		n = len(itra)
		itrans.append([itra, range(1,n)])

	purinvoice = PurchaseEntry.objects.filter(Q(issue_use='no') | Q(voucher_number__in=mis))
	mitm = MaintainanceItem.objects.filter(bill_id=mid).exclude(Q(pvn='') | Q(itnn='yes'))
	gmm = MaintainanceItem.objects.filter(bill_id=mid, itnn='yes')
	gmitm = MaintainanceItem.objects.filter(bill_id=mid, itnn='yes')
	glen = len(gmitm)
	gmitms.append([gmitm, range(1, glen)])

	itemsel = []
	seen =set()
	seen_add = seen.add
	ent = StockItem.objects.values_list('main_url', flat=True)
	ent = [x for x in ent if not (x in seen or seen_add(x))]
	for e in ent:
		isel = StockItem.objects.filter(main_url=e)
		n = len(isel)
		itemsel.append([isel, range(1,n)])

	stock_cat = StockCategory.objects.all()
	psupaa = []
	seen = set()
	seen_add = seen.add
	tran = StockSubCategory.objects.values_list('cat_url', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for r in ent:
		pss = StockSubCategory.objects.filter(cat_url=r)
		n = len(ps)
		psupaa.append([pss, range(1,n)])

	context = {'psupa': psupa, 'itemsel': itemsel, 'stock_cat': stock_cat, 'psupaa': psupaa, 'mitm': mitm, 'gmm': gmm, 'gmitms': gmitms, 'bill': bill, 'minv': minv, 'purinvoice': purinvoice, 'igoods': igoods, 'itrans': itrans, 'pitem': pitem, 'item': item, 'item_real': item_real, 'vehis': vehis, 'v_type': v_type, 'supplier_dash': supplier_dash, 'bills': bills, 'bill_count': bill_count, 'sub_material': sub_material, 'problem': problem, 'porder': porder}
	return render(request, 'fuelmaintain/maintain_edit.html', context)


@user_access
def edit_maintainance_entry(request):
	if request.method=="POST":
		current_user = request.user.username
		entry_id = request.POST.get('entry_id')
		mb = MaintainanceBill.objects.filter(id=entry_id).first()
		u_site = mb.user_site
		entry_date = request.POST.get('date')
		billdate = request.POST.get('invoice_date')
		billnum = request.POST.get('invoice')
		maintain_number = request.POST.get('maintain_number')
		vehicle_type = request.POST.get('vehicle_type')
		vehicle_type_id = request.POST.get('vehicle_type_id')
		num_type = request.POST.get('num_type')
		vehicle = request.POST.get('vehiclee')
		kilometer = request.POST.get('kilometer')
		problem = request.POST.get('problem')
		subproblem = request.POST.get('subproblem')
		narrat = request.POST.get('narrat')
		pei = request.POST.get('pvn_count')
		jorder = request.POST.get('jorder')
		gjorder = request.POST.get('gjorder')
		subtotal = request.POST.get('subtotal')
		labour = request.POST.get('labour')
		total = request.POST.get('total')
		hour = request.POST.get('hour')
		itemadd = request.POST.getlist('itemadd')
		gitemadd = request.POST.getlist('gitemadd')
		exitemadd = request.POST.getlist('exitemadd')
		supplier = ''
		sup_name = ''
		sup_address = ''
		sup_contact = ''
		if len(itemadd) == 0 and len(gitemadd) == 0:
			messages.info(request, 'error')
			return redirect('/edit-maintainance/'+entry_id+'/')
		if MaintainanceBill.objects.filter(vehicle_number=vehicle, hour=hour).exclude(id=entry_id).exists():
			messages.info(request, 'error')
			return redirect('/edit-maintainance/'+entry_id+'/')
		if jorder == 'yes':
			jobnumber = request.POST.get('jobnumber')
			jobnumber = jobnumber.replace(" ", "")
			p = PurchaseOrder.objects.filter(purchase_number=jobnumber).first()
			status = p.status
			jedate = p.entry_date
			japprove = p.approved_by
			
		if jorder == 'no':
			jobnumber = ''
			status = ''
			jedate = ''
			japprove = ''

		ge = MaintainanceBill.objects.filter(id=entry_id).first()
		u_site = ge.user_site

		if jorder == 'yes':
			for i in itemadd:
				iid = str(i)
				if request.POST.get('inameid'+iid):
					item_id = request.POST.get('inameid'+iid)
					quantity = request.POST.get('iqty'+iid)
					if StockEntry.objects.filter(item_id=item_id, stock_site=u_site).exists():
						sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
						qt = float(sq.quantity)
						if qt>float(quantity) or qt==float(quantity):
							print('ok')
						else:
							messages.info(request, 'error')
							return redirect('/edit-maintainance/'+entry_id+'/')
					else:
						messages.info(request, 'error')
						return redirect('/edit-maintainance/'+entry_id+'/')
		if gjorder == 'yes':
			for i in gitemadd:
				iid = str(i)
				if request.POST.get('ginameid'+iid):
					item_id = request.POST.get('ginameid'+iid)
					quantity = request.POST.get('giqty'+iid)
					if StockEntry.objects.filter(item_id=item_id, stock_site=u_site).exists():
						sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
						qt = float(sq.quantity)
						if qt>float(quantity) or qt==float(quantity):
							print('ok')
						else:
							messages.info(request, 'error')
							return redirect('/edit-maintainance/'+entry_id+'/')
					else:
						messages.info(request, 'error')
						return redirect('/edit-maintainance/'+entry_id+'/')
		if len(exitemadd) > 0:
			for i in itemadd:
				iid = str(i)
				if request.POST.get('iid'+iid):
					item_id = request.POST.get('iid'+iid)
					quantity = request.POST.get('iqty'+iid)
					if StockEntry.objects.filter(item_id=item_id, stock_site=u_site).exists():
						sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
						qt = float(sq.quantity)
						if qt>float(quantity) or qt==float(quantity):
							print('ok')
						else:
							messages.info(request, 'error')
							return redirect('/edit-maintainance/'+entry_id+'/')
					else:
						messages.info(request, 'error')
						return redirect('/edit-maintainance/'+entry_id+'/')

		MaintainanceBill.objects.filter(id=entry_id).update(bill_number=billnum, purchase_order_number=jobnumber, hour=hour, purchase_entry_date=jedate, purchase_approve_by=japprove, number_type=num_type, vehicle_type_id=vehicle_type_id, vehicle_type=vehicle_type, vehicle_number=vehicle, purchase_status=status, kilometer=kilometer, problem_category=problem, problem_subcategory=subproblem, narration=narrat, entry_date=entry_date, bill_date=billdate, sub_total=subtotal, labour_charge=labour, total=total)

		if MaintainanceItem.objects.filter(bill_id=entry_id).exists():
			gq = MaintainanceItem.objects.filter(bill_id=entry_id)
			invt = []
			ginv = []
			for a in gq:
				itemid = a.item_id
				qty = a.quantity
				if a.pvn:
					pvn = a.pvn
					sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
					qt = float(sq.quantity)
					newqty = qt + float(qty)
					StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)
					if InvoiceItem.objects.filter(pvn=pvn).exists():
						invt.append(pvn)
					if InternalGrnItems.objects.filter(pvn=pvn).exists():
						ginv.append(pvn)
				else:
					sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
					qt = float(sq.quantity)
					newqty = qt + float(qty)
					StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)

			if len(invt) > 0:
				invt = list(set(invt))
				for i in invt:
					InvoiceItem.objects.filter(pvn=i).update(issue_use='no')
			if len(ginv) > 0:
				ginv = list(set(ginv))
				for i in ginv:
					InternalGrnItems.objects.filter(grn=i).update(invoice_id='', invoice_status='no')
					InternalGrn.objects.filter(grn_number=i).update(invoice_id='', invoice_status='no')

		if MaintainInvoice.objects.filter(maintainid=entry_id).exists():
			gm = MaintainInvoice.objects.filter(maintainid=entry_id)
			for m in gm:
				p = m.voucher_number
				PurchaseEntry.objects.filter(voucher_number=p).update(issue_use='no')

			MaintainInvoice.objects.filter(maintainid=entry_id).delete()
		if jorder == 'yes':
			jobnumber = request.POST.get('jobnumber')
			jobnumber = jobnumber.replace(" ", "")
			pvnval = request.POST.getlist('pvnval')
			for p in pvnval:
				p = p.upper()
				pe = PurchaseEntry.objects.filter(voucher_number=p).first()
				voucher_number = pe.voucher_number
				invoice = pe.invoice_number
				invoice_type = pe.invoice_type
				supplier = pe.supplier_name
				subtotal = pe.sub_total
				discount_amt = pe.discount_amt
				discount_per = pe.discount_per
				vat = pe.vat
				total = pe.total
				query = MaintainInvoice(maintainid=entry_id, maintain_number=maintain_number, purchase_order_number=jobnumber, voucher_number=p, invoice_number=invoice, invoice_type=invoice_type, supplier=supplier, sub_total=subtotal, discount_amt=discount_amt, discount_per=discount_per, vat=vat, total=total)
				query.save()
				PurchaseEntry.objects.filter(voucher_number=p).update(issue_use='yes')

		MaintainanceItem.objects.filter(bill_id=entry_id).delete()
		if jorder == 'yes':
			for i in itemadd:
				iid = str(i)
				jobnumber = request.POST.get('jobnumber')
				jobnumber = jobnumber.replace(" ", "")
				jobnumber = jobnumber.upper()
				if request.POST.get('ipvn'+iid):
					pvn = request.POST.get('ipvn'+iid)
					item_id = request.POST.get('inameid'+iid)
					item_name = request.POST.get('iname'+iid)
					alias = request.POST.get('ialias'+iid)
					uom = request.POST.get('iuom'+iid)
					quantity = request.POST.get('iqty'+iid)
					rate = request.POST.get('irate'+iid)
					amount = request.POST.get('iamt'+iid)
					dper = request.POST.get('idisper'+iid)
					damt = request.POST.get('idisamt'+iid)
					itemquery = MaintainanceItem(bill_id=entry_id, purchase_id=jobnumber, pvn=pvn, item_id=item_id, item_name=item_name, alias=alias, uom=uom, quantity=quantity, rate=rate, amount=amount, discount_per=dper, discount_amt=damt)
					itemquery.save()
					InvoiceItem.objects.filter(pvn=pvn).update(issue_use='yes')
					sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
					qt = float(sq.quantity)
					newqty = qt - float(quantity)
					StockEntry.objects.filter(item_id=item_id, stock_site=u_site).update(quantity=newqty)

		ginvc = []
		if gjorder == 'yes':
			for i in gitemadd:
				iid = str(i)
				if request.POST.get('gipvn'+iid):
					pvn = request.POST.get('gipvn'+iid)
					item_id = request.POST.get('ginameid'+iid)
					item_name = request.POST.get('giname'+iid)
					alias = request.POST.get('gialias'+iid)
					uom = request.POST.get('giuom'+iid)
					quantity = request.POST.get('giqty'+iid)
					itemquery = MaintainanceItem(bill_id=entry_id, pvn=pvn, item_id=item_id, item_name=item_name, alias=alias, uom=uom, quantity=quantity, rate=0, amount=0, discount_per=0, discount_amt=0, itnn='yes')
					itemquery.save()
					ginvc.append(pvn)
					sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
					qt = float(sq.quantity)
					newqty = qt - float(quantity)
					StockEntry.objects.filter(item_id=item_id, stock_site=u_site).update(quantity=newqty)

		if len(ginvc) > 0:
			ginvc = list(set(ginvc))
			for i in ginvc:
				InternalGrn.objects.filter(grn_number=i).update(invoice_id=maintain_number, invoice_status='yes')
				InternalGrnItems.objects.filter(grn=i).update(invoice_id=maintain_number, invoice_status='yes')

		if len(exitemadd) > 0:
			for i in itemadd:
				iid = str(i)
				if request.POST.get('iid'+iid):
					item_id = request.POST.get('iid'+iid)
					item_name = request.POST.get('iname'+iid)
					alias = request.POST.get('ialias'+iid)
					uom = request.POST.get('iuom'+iid)
					quantity = request.POST.get('iqty'+iid)
					rate = request.POST.get('irate'+iid)
					amount = request.POST.get('iamt'+iid)
					dper = request.POST.get('idisper'+iid)
					damt = request.POST.get('idisamt'+iid)
					itemquery = MaintainanceItem(bill_id=entry_id, item_id=item_id, item_name=item_name, alias=alias, uom=uom, quantity=quantity, rate=rate, amount=amount, discount_per=dper, discount_amt=damt)
					itemquery.save()
					sq = StockEntry.objects.filter(item_id=item_id, stock_site=u_site).first()
					qt = float(sq.quantity)
					newqty = qt - float(quantity)
					StockEntry.objects.filter(item_id=item_id, stock_site=u_site).update(quantity=newqty)


		messages.info(request, 'done')
		return redirect('/edit-maintainance/'+entry_id+'/')
	else:
		return redirect('maintainance_display')


@user_access
def maintainance_delete(request):
	if request.method=="POST":
		sid = request.POST.get('sid')
		gmm = MaintainanceBill.objects.filter(id=sid).first()
		u_site = gmm.user_site
		gq = MaintainanceItem.objects.filter(bill_id=sid)
		invt = []
		ginv = []
		for a in gq:
			itemid = a.item_id
			qty = a.quantity
			if a.pvn:
				pvn = a.pvn
				sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
				qt = float(sq.quantity)
				newqty = qt + float(qty)
				StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)
				if InvoiceItem.objects.filter(pvn=pvn).exists():
					invt.append(pvn)
				if InternalGrnItems.objects.filter(pvn=pvn).exists():
					ginv.append(pvn)
			else:
				sq = StockEntry.objects.filter(item_id=itemid, stock_site=u_site).first()
				qt = float(sq.quantity)
				newqty = qt + float(qty)
				StockEntry.objects.filter(item_id=itemid, stock_site=u_site).update(quantity=newqty)

		if len(invt) > 0:
			invt = list(set(invt))
			for i in invt:
				InvoiceItem.objects.filter(pvn=i).update(issue_use='no')
		if len(ginv) > 0:
			ginv = list(set(ginv))
			for i in ginv:
				InternalGrnItems.objects.filter(pvn=i).update(invoice_id='', invoice_status='no')
				InternalGrn.objects.filter(pvn=i).update(invoice_id='', invoice_status='no')

		if MaintainInvoice.objects.filter(maintainid=sid).exists():
			gm = MaintainInvoice.objects.filter(maintainid=sid)
			for m in gm:
				p = m.voucher_number
				PurchaseEntry.objects.filter(voucher_number=p).update(issue_use='no')

			MaintainInvoice.objects.filter(maintainid=sid).delete()

		MaintainanceBill.objects.filter(id=sid).delete()
		MaintainanceItem.objects.filter(bill_id=sid).delete()

		messages.info(request, 'done')
		return redirect('maintainance_display')
	else:
		return redirect('maintainance_display')


@user_access
def vehicle_dash(request):
	v_type = VehicleType.objects.all()
	context = {'v_type': v_type}
	return render(request, 'fuelmaintain/vehicles.html', context)


@user_access
def vehicle_display(request):
	s_item = VehicleList.objects.all().order_by('-id')
	v_type = VehicleType.objects.all().order_by('-id')
	context = {'s_item': s_item, 'v_type': v_type}
	return render(request, 'fuelmaintain/display/vehicle_display.html', context)


@user_access
def vehicle_add(request):
	if request.method == "POST":
		current_user = request.user.username
		vehicle_number = request.POST.get('vehicle_number')
		url = request.POST.get('vehi_url')
		chasis_url = request.POST.get('chasis_url')
		engine_url = request.POST.get('engine_url')
		chasis = request.POST.get('chasis_number')
		engine = request.POST.get('engine_number')
		vehicle_type = request.POST.get('vehicle_type')
		vehicle_type_name = request.POST.get('vehicle_type_name')
		owner = request.POST.get('owner_name')
		driver = request.POST.get('driver_name')
		helper = request.POST.get('helper_name')
		capacity = request.POST.get('capacity')
		contact1 = request.POST.get('contact1')
		contact2 = request.POST.get('contact2')
		if VehicleList.objects.filter(url=url).exists() or VehicleList.objects.filter(chasis_number=chasis).exists() or VehicleList.objects.filter(engine_number=engine).exists():
			messages.info(request, 'error')
			return redirect('manage_vehicle')
		else:
			query = VehicleList(vehicle_number=vehicle_number, url=url, chasis_url=chasis_url, engine_url=engine_url, chasis_number=chasis, engine_number=engine, vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name, owner_name=owner, driver_name=driver, helper_name=helper, capacity=capacity, contact1=contact1, contact2=contact2)
			query.save()

			messages.info(request, 'done')
			return redirect('vehicle')
	else:
		return redirect('vehicle')


@user_access
def vehicle_update(request):
	if request.method == "POST":
		vid = request.POST.get('suid')
		default_vehi = request.POST.get('defaultvehi')
		default_chasis = request.POST.get('defaultchasis')
		default_engine = request.POST.get('defaultengine')
		owner_name = request.POST.get('owner_name')
		vehicle_number = request.POST.get('vehicle_number')
		url = request.POST.get('vehi_url')
		chasis_url = request.POST.get('chasis_url')
		engine_url = request.POST.get('engine_url')
		chasis = request.POST.get('chasis_number')
		engine = request.POST.get('engine_number')
		vehicle_type = request.POST.get('vehicle_type')
		vehicle_type_name = request.POST.get('vehicle_type_name')
		driver = request.POST.get('driver_name')
		helper = request.POST.get('helper_name')
		capacity = request.POST.get('capacity')
		contact1 = request.POST.get('contact1')
		contact2 = request.POST.get('contact2')
		if VehicleList.objects.filter(url=url).exclude(id=vid).exists() or VehicleList.objects.filter(chasis_number=chasis).exclude(id=vid).exists() or VehicleList.objects.filter(engine_number=engine).exclude(id=vid).exists():
			messages.info(request, 'error')
			return redirect('vehicle_display')
		else:
			VehicleList.objects.filter(id=vid).update(vehicle_number=vehicle_number, url=url, chasis_url=chasis_url, engine_url=engine_url, chasis_number=chasis, engine_number=engine, vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name, owner_name=owner_name, driver_name=driver, helper_name=helper, capacity=capacity, contact1=contact1, contact2=contact2)
			if PurchaseOrder.objects.filter(vehicle_number=default_vehi).exists():
				PurchaseOrder.objects.filter(vehicle_number=default_vehi).update(vehicle_number=vehicle_number, vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)
			if MaintainanceBill.objects.filter(vehicle_number=default_vehi).exists():
				MaintainanceBill.objects.filter(vehicle_number=default_vehi).update(vehicle_number=vehicle_number, vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)
			if Fuel.objects.filter(vehicle_number=default_vehi).exists():
				Fuel.objects.filter(vehicle_number=default_vehi).update(vehicle_number=vehicle_number, vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)
			if VehicleTrack.objects.filter(vehicle_number=default_vehi).exists():
				VehicleTrack.objects.filter(vehicle_number=default_vehi).update(vehicle_number=vehicle_number, vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)
			if PurchaseOrder.objects.filter(vehicle_number=default_chasis).exists():
				PurchaseOrder.objects.filter(vehicle_number=default_chasis).update(vehicle_number=chasis, vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)
			if MaintainanceBill.objects.filter(vehicle_number=default_chasis).exists():
				MaintainanceBill.objects.filter(vehicle_number=default_chasis).update(vehicle_number=chasis, vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)
			if Fuel.objects.filter(vehicle_number=default_chasis).exists():
				Fuel.objects.filter(vehicle_number=default_chasis).update(vehicle_number=chasis, vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)
			if VehicleTrack.objects.filter(vehicle_number=default_chasis).exists():
				VehicleTrack.objects.filter(vehicle_number=default_chasis).update(vehicle_number=chasis, vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)
			if PurchaseOrder.objects.filter(vehicle_number=default_engine).exists():
				PurchaseOrder.objects.filter(vehicle_number=default_engine).update(vehicle_number=engine, vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)
			if MaintainanceBill.objects.filter(vehicle_number=default_engine).exists():
				MaintainanceBill.objects.filter(vehicle_number=default_engine).update(vehicle_number=engine, vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)
			if Fuel.objects.filter(vehicle_number=default_engine).exists():
				Fuel.objects.filter(vehicle_number=default_engine).update(vehicle_number=engine, vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)
			if VehicleTrack.objects.filter(vehicle_number=default_engine).exists():
				VehicleTrack.objects.filter(vehicle_number=default_engine).update(vehicle_number=engine, vehicle_type_id=vehicle_type, vehicle_type=vehicle_type_name)
			messages.info(request, 'done')
			return redirect('vehicle_display')
	else:
		return redirect('vehicle_display')


@user_access
def search_vehicle(request):
	if request.method == "POST":
		search = request.POST.get('search')
		sea = search.upper()
		se = search.title()
		s = search.lower()
		lookup = Q(vehicle_number=search) | Q(url=search) | Q(chasis_number=search) | Q(engine_number=search) | Q(vehicle_type=search) | Q(owner_name=search) | Q(vehicle_number=sea) | Q(url=sea) | Q(chasis_number=sea) | Q(engine_number=sea) | Q(vehicle_type=sea) | Q(owner_name=sea) | Q(vehicle_number=se) | Q(url=se) | Q(chasis_number=se) | Q(engine_number=se) | Q(vehicle_type=se) | Q(owner_name=se) | Q(vehicle_number=s) | Q(url=s) | Q(chasis_number=s) | Q(engine_number=s) | Q(vehicle_type=s) | Q(owner_name=s)
		s_item = VehicleList.objects.filter(lookup).order_by('-id')
		v_type = VehicleType.objects.all().order_by('-id')
		context = {'s_item': s_item, 'search': search, 'v_type': v_type}
		return render(request, 'fuelmaintain/display/search_vehicle.html', context)
	else:
		return redirect('vehicle_display')


@user_access
def vehicle_delete(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		VehicleList.objects.filter(id=sid).delete()
		messages.info(request, 'done')
		return redirect('vehicle_display')
	else:
		return redirect('vehicle_display')


@user_access
def deactivate_vehicle(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		VehicleList.objects.filter(id=sid).update(active_status='no')
		messages.info(request, 'done')
		return redirect('vehicle_display')
	else:
		return redirect('vehicle_display')

#==========================================================================

#damage_product======================================================

@user_access
def damage_stock(request):
	porder = PurchaseOrder.objects.filter(status='approved')
	uom_dash = UOM.objects.all()
	item_real = StockItem.objects.all()
	pvn = 0
	if DamageEntry.objects.last():
		good = DamageEntry.objects.last()
		ng = good.pvn_count
		pvn = int(ng) + 1
	else:
		pvn = pvn + 1

	pitem = InvoiceItem.objects.filter(issue_use="no", grn_status='no').exclude(Q(damage='all') | Q(retur='all'))
	psupa = []
	seen = set()
	seen_add = seen.add
	tran = PurchaseEntry.objects.values_list('purchase_order_number', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for r in ent:
		ps = PurchaseEntry.objects.filter(purchase_order_number=r)
		n = len(ps)
		psupa.append([ps, range(1,n)])

	igoods = []
	tran = InvoiceItem.objects.values_list('purchaseid', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for s in ent:
		igood = InvoiceItem.objects.filter(purchaseid=s, issue_use="no", grn_status='no')
		n = len(igood)
		igoods.append([igood, range(1,n)])

	purinvoice = PurchaseEntry.objects.filter(issue_use='no', grn_status='no')

	context = {'porder': porder, 'pitem': pitem, 'pvn': pvn, 'item_real': item_real, 'uom_dash': uom_dash, 'psupa': psupa, 'purinvoice': purinvoice, 'igoods': igoods}    
	return render(request, 'damage_product.html', context)


@user_access
def damage_display(request):
	u_site = user_site(request)
	u_status = user_role(request)
	if u_status == 'main_admin' or u_status == 'main_staff':
		s_item = DamageEntry.objects.all().order_by('-id')[:30]
	else:
		s_item = DamageEntry.objects.filter(user_site=u_site).order_by('-id')[:30]
	context = {'s_item': s_item}    
	return render(request, 'display/damage_display.html', context)


@user_access
def damage_detail(request,pid):
	if DamageEntry.objects.filter(id=pid).exists():
		item = DamageEntry.objects.filter(id=pid).first()
		s_goods = DamageItem.objects.filter(damageid=pid)
		dinvoice = DamageInvoice.objects.filter(damageid=pid)
		context = {'item': item, 's_goods': s_goods, 'dinvoice': dinvoice}    
		return render(request, 'display/damage_detail.html', context)
	else:
		return redirect('damage_display')


@user_access
def search_damage(request):
	if request.method == "POST":
		search = request.POST.get('search')
		sea = search.upper()
		se = search.title()
		s = search.lower()
		u_site = user_site(request)
		u_status = user_role(request)
		if u_status == 'main_admin' or u_status == 'main_staff':
			lookup = Q(purchase_order_number=search) | Q(damage_number=search) | Q(user_site=search) | Q(purchase_order_number=sea) | Q(damage_number=sea) | Q(user_site=sea) | Q(purchase_order_number=se) | Q(damage_number=se) | Q(user_site=se) | Q(purchase_order_number=s) | Q(damage_number=s) | Q(user_site=s)
		else:
			lookup = Q(Q(purchase_order_number=search) | Q(damage_number=search) | Q(purchase_order_number=sea) | Q(damage_number=sea) | Q(purchase_order_number=se) | Q(damage_number=se) | Q(purchase_order_number=s) | Q(damage_number=s)) & Q(user_site=u_site)
		s_item = DamageEntry.objects.filter(lookup).order_by('-id')
		context = {'s_item': s_item, 'search': search}
		return render(request, 'display/damage_search.html', context)
	else:
		return redirect('damage_display')


@user_access
def print_damage(request):
	if request.method=="POST":
		jid = request.POST.get('jid')
		s_good = DamageEntry.objects.filter(id=jid).first()
		igoods = DamageItem.objects.filter(damageid=jid)
		minvoice = DamageInvoice.objects.filter(damageid=jid)

		context = {'a': s_good, 'igoods': igoods, 'minvoice': minvoice}
		pdf = render_to_pdf('printdamage.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			rnum = random.randint(11111111, 99999999)
			filename = "Reportdamage_%s.pdf" %(rnum)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")
	else:
		return redirect('damage_display')


@user_access
def delete_damage(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		ge = DamageItem.objects.filter(damageid=sid)				
		for a in ge:
			itemid = a.item_id
			item = a.item
			qty = a.quantity
			po = a.po
			pvn = a.pvn
			if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
				itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
				quantity = itm.quantity
				dqty = float(quantity) + float(qty)
				InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(quantity=dqty, useable_quantity=dqty, damage='no', damage_qty='0')
				PurchaseEntry.objects.filter(voucher_number=pvn).update(damage='no')

		DamageEntry.objects.filter(id=sid).delete()
		DamageItem.objects.filter(damageid=sid).delete()
		if DamageInvoice.objects.filter(damageid=sid).exists():
			DamageInvoice.objects.filter(damageid=sid).delete()
		messages.info(request, 'done')
		return redirect('damage_display')
	else:
		return redirect('damage_display')


@user_access
def damage_edit(request, pid):
	if DamageEntry.objects.filter(id=pid).exists():
		porder = PurchaseOrder.objects.filter(status='approved')
		uom_dash = UOM.objects.all()
		item_real = StockItem.objects.all()
		item = DamageEntry.objects.filter(id=pid).first()
		bills = []
		pp = DamageItem.objects.filter(damageid=pid)
		bill_count = []
		a = 0
		for b in pp:
			a = a+1
			bill_count.append(a)

		seen = set()
		seen_add = seen.add
		tran = DamageItem.objects.values_list('pvn', flat=True).distinct()
		ent = [x for x in tran if not (x in seen or seen_add(x))]
		for r in ent:
			bill = DamageItem.objects.filter(pvn=r, damageid=pid)
			n = len(bill)
			bills.append([bill, range(1,n)])

		pitem = InvoiceItem.objects.filter(issue_use="no", grn_status='no').exclude(Q(damage='all') | Q(retur='all'))
		psupa = []
		seen = set()
		seen_add = seen.add
		tran = PurchaseEntry.objects.values_list('purchase_order_number', flat=True).distinct()
		ent = [x for x in tran if not (x in seen or seen_add(x))]
		for r in ent:
			ps = PurchaseEntry.objects.filter(purchase_order_number=r)
			n = len(ps)
			psupa.append([ps, range(1,n)])

		igoods = []
		tran = InvoiceItem.objects.values_list('purchaseid', flat=True).distinct()
		ent = [x for x in tran if not (x in seen or seen_add(x))]
		for s in ent:
			igood = InvoiceItem.objects.filter(purchaseid=s, issue_use="no", grn_status='no')
			n = len(igood)
			igoods.append([igood, range(1,n)])

		purinvoice = PurchaseEntry.objects.filter(issue_use='no', grn_status='no')

		minv = DamageInvoice.objects.filter(damageid=pid)
		mis = []
		for m in minv:
			mi = m.voucher_number
			mis.append(mi)

		mitm = DamageItem.objects.filter(damageid=pid)

		context = {'item': item, 'pp': pp, 'porder': porder, 'pitem': pitem, 'bill_count': bill_count, 'bills': bills, 'item_real': item_real, 'uom_dash': uom_dash, 'psupa': psupa, 'purinvoice': purinvoice, 'minv': minv, 'mitm': mitm}    
		return render(request, 'damage_edit.html', context)
	else:
		return redirect('damage_display')


@user_access
def add_damage(request):
	if request.method=="POST":
		current_user = request.user.username
		u_site = user_site(request)
		pvnl = []
		date = request.POST.get('date')
		damage_number = request.POST.get('damage_number')
		pvn_count = request.POST.get('pvn_count')
		narrat = request.POST.get('narrat')
		porder = request.POST.get('jobnumber')
		itemadd = request.POST.getlist('itemadd')
		pvnlist = request.POST.getlist('pvnval')
		if len(pvnlist) == 0:
			messages.info(request, 'error')
			return redirect('damage_product')

		for p in pvnlist:
			pvn = p.upper()
			pvnl.append(pvn)

		pvnl = list(set(pvnl))

		for a in itemadd:
			a = str(a)
			for p in pvnl:
				pvn = p
				rstr = str(p) + a
				if request.POST.get('inameid'+rstr):
					itemid = request.POST.get('inameid'+rstr)
					if DamageItem.objects.filter(item_id=itemid, pvn=pvn).exists():
						messages.info(request, 'error')
						return redirect('damage_product')

		for a in itemadd:
			a = str(a)
			for p in pvnl:
				pvn = p
				rstr = str(p) + a
				if request.POST.get('inameid'+rstr):
					itemid = request.POST.get('inameid'+rstr)
					quantity = request.POST.get('iqty'+rstr)
					if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
						itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
						qty = itm.quantity
						if float(quantity) > float(qty):
							messages.info(request, 'error')
							return redirect('damage_product')

		if DamageEntry.objects.filter(damage_number=damage_number).exists():
			messages.info(request, 'error')
			return redirect('damage_product')
		else:
			query = DamageEntry(entry_date=date, purchase_order_number=porder, narration=narrat, damage_number=damage_number, pvn_count=pvn_count, entry_by=current_user, user_site=u_site)
			query.save()
			# PurchaseOrder.objects.filter(purchase_number=porder).update(invoice_id=pid, invoice_status="yes")

		pid = query.id
		for p in pvnl:
			pe = PurchaseEntry.objects.filter(voucher_number=p).first()
			voucher_number = pe.voucher_number
			invoice = pe.invoice_number
			invoice_type = pe.invoice_type
			supplier = pe.supplier_name
			subtotal = pe.sub_total
			discount_amt = pe.discount_amt
			discount_per = pe.discount_per
			vat = pe.vat
			total = pe.total
			po = porder.upper()
			query = DamageInvoice(damageid=pid, damage_number=damage_number, purchase_order_number=po, voucher_number=p, invoice_number=invoice, invoice_type=invoice_type, supplier=supplier, sub_total=subtotal, discount_amt=discount_amt, discount_per=discount_per, vat=vat, total=total)
			query.save()

		for a in itemadd:
			a = str(a)
			po = porder.upper()
			for p in pvnl:
				pvn = p
				rstr = str(p) + a
				if request.POST.get('inameid'+rstr):
					itemid = request.POST.get('inameid'+rstr)
					item = request.POST.get('iname'+rstr)
					alias = request.POST.get('ialias'+rstr)
					uom = request.POST.get('iuom'+rstr)
					qty = request.POST.get('iqty'+rstr)
					if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
						itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
						quantity = itm.quantity
						que = DamageItem(damageid=pid, po=po, dn=damage_number, pvn=pvn, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty)
						que.save()
						dqty = float(quantity) - float(qty)
						if int(dqty) == 0:
							InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(quantity=dqty, useable_quantity=dqty, damage='all', damage_qty=qty)
						else:
							InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(quantity=dqty, useable_quantity=dqty, damage='partial', damage_qty=qty)
						PurchaseEntry.objects.filter(voucher_number=pvn).update(damage='yes')

		pod = porder.upper()
		po = PurchaseOrder.objects.filter(purchase_number=pod).first()

		notify_topic = 'damage_entry'
		content_id = pid
		content = 'damage_add'
		from_site = u_site
		from_user = current_user
		content_val = damage_number
		content_val2 = po.issuing_site

		q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, from_site=from_site, from_user=from_user, content_val=content_val, content_val2=content_val2)
		q.save()

		messages.info(request, 'done')
		return redirect('damage_product')
	else:
		return redirect('damage_product')


@user_access
def edit_damage(request):
	if request.method=="POST":
		pvnl = []
		pid = request.POST.get('pid')
		date = request.POST.get('date')
		damage_number = request.POST.get('damage_number')
		narrat = request.POST.get('narrat')
		porder = request.POST.get('jobnumber')
		itemadd = request.POST.getlist('itemadd')
		pvnlist = request.POST.getlist('pvnval')
		if len(pvnlist) == 0:
			messages.info(request, 'error')
			return redirect('/damage-edit/'+str(pid)+'/')

		for p in pvnlist:
			pvn = p.upper()
			pvnl.append(pvn)

		pvnl = list(set(pvnl))

		for a in itemadd:
			a = str(a)
			for p in pvnl:
				pvn = p
				rstr = str(p) + a
				if request.POST.get('inameid'+rstr):
					itemid = request.POST.get('inameid'+rstr)
					if DamageItem.objects.filter(item_id=itemid, pvn=pvn).exclude(damageid=pid).exists():
						messages.info(request, 'error')
						return redirect('/damage-edit/'+str(pid)+'/')

		if DamageItem.objects.filter(damageid=pid).exists():
			ge = DamageItem.objects.filter(damageid=pid)				
			for a in ge:
				itemid = a.item_id
				item = a.item
				qty = a.quantity
				po = a.po
				pvn = a.pvn
				if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
					itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
					quantity = itm.quantity
					dqty = float(quantity) + float(qty)
					InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(quantity=dqty, useable_quantity=dqty, damage='no', damage_qty='0')
					PurchaseEntry.objects.filter(voucher_number=pvn).update(damage='no')

		for a in itemadd:
			a = str(a)
			for p in pvnl:
				pvn = p
				rstr = str(p) + a
				if request.POST.get('inameid'+rstr):
					itemid = request.POST.get('inameid'+rstr)
					quantity = request.POST.get('iqty'+rstr)
					if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
						itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
						qty = itm.quantity
						if float(quantity) > float(qty):
							for a in ge:
								itemid = a.item_id
								item = ra.item
								qty = a.quantity
								po = a.po
								pvn = a.pvn
								if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
									itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
									quantity = itm.quantity
									dqty = float(quantity) - float(qty)
									if int(dqty) == 0:
										InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(quantity=dqty, useable_quantity=dqty, damage='all', damage_qty=qty)
									else:
										InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(quantity=dqty, useable_quantity=dqty, damage='partial', damage_qty=qty)
									PurchaseEntry.objects.filter(voucher_number=pvn).update(damage='yes')
							messages.info(request, 'error')
							return redirect('/damage-edit/'+str(pid)+'/')

		DamageEntry.objects.filter(id=pid).update(entry_date=date, purchase_order_number=porder, narration=narrat)
		DamageInvoice.objects.filter(damageid=pid).delete()
		DamageItem.objects.filter(damageid=pid).delete()

		for p in pvnl:
			pe = PurchaseEntry.objects.filter(voucher_number=p).first()
			voucher_number = pe.voucher_number
			invoice = pe.invoice_number
			invoice_type = pe.invoice_type
			supplier = pe.supplier_name
			subtotal = pe.sub_total
			discount_amt = pe.discount_amt
			discount_per = pe.discount_per
			vat = pe.vat
			total = pe.total
			po = porder.upper()
			query = DamageInvoice(damageid=pid, damage_number=damage_number, purchase_order_number=po, voucher_number=p, invoice_number=invoice, invoice_type=invoice_type, supplier=supplier, sub_total=subtotal, discount_amt=discount_amt, discount_per=discount_per, vat=vat, total=total)
			query.save()

		for a in itemadd:
			a = str(a)
			po = porder.upper()
			for p in pvnlist:
				pvn = p
				rstr = str(p) + a
				if request.POST.get('inameid'+rstr):
					itemid = request.POST.get('inameid'+rstr)
					item = request.POST.get('iname'+rstr)
					alias = request.POST.get('ialias'+rstr)
					uom = request.POST.get('iuom'+rstr)
					qty = request.POST.get('iqty'+rstr)
					if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
						itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
						quantity = itm.quantity
						que = DamageItem(damageid=pid, po=po, dn=damage_number, pvn=pvn, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty)
						que.save()
						dqty = float(quantity) - float(qty)
						if int(dqty) == 0:
							InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(quantity=dqty, useable_quantity=dqty, damage='all', damage_qty=qty)
						else:
							InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(quantity=dqty, useable_quantity=dqty, damage='partial', damage_qty=qty)
						PurchaseEntry.objects.filter(voucher_number=pvn).update(damage='yes')

		messages.info(request, 'done')
		return redirect('/damage-edit/'+str(pid)+'/')
	else:
		return redirect('damage_display')

#===============================================================================

#return_product======================================================

@user_access
def return_stock(request):
	porder = PurchaseOrder.objects.filter(status='approved')
	uom_dash = UOM.objects.all()
	item_real = StockItem.objects.all()
	pvn = 0
	if ReturnEntry.objects.last():
		good = ReturnEntry.objects.last()
		ng = good.pvn_count
		pvn = int(ng) + 1
	else:
		pvn = pvn + 1

	pitem = InvoiceItem.objects.filter(issue_use="no", grn_status='no').exclude(Q(damage='all') | Q(retur='all'))
	psupa = []
	seen = set()
	seen_add = seen.add
	tran = PurchaseEntry.objects.values_list('purchase_order_number', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for r in ent:
		ps = PurchaseEntry.objects.filter(purchase_order_number=r)
		n = len(ps)
		psupa.append([ps, range(1,n)])

	purinvoice = PurchaseEntry.objects.filter(issue_use='no', grn_status='no')

	context = {'porder': porder, 'pitem': pitem, 'pvn': pvn, 'item_real': item_real, 'uom_dash': uom_dash, 'psupa': psupa, 'purinvoice': purinvoice}    
	return render(request, 'return.html', context)


@user_access
def return_display(request):
	u_site = user_site(request)
	u_status = user_role(request)
	if u_status == 'main_admin' or u_status == 'main_staff':
		s_item = ReturnEntry.objects.all().order_by('-id')[:30]
	else:
		s_item = ReturnEntry.objects.filter(user_site=u_site).order_by('-id')[:30]
	context = {'s_item': s_item}    
	return render(request, 'display/return_display.html', context)


@user_access
def return_detail(request,pid):
	if ReturnEntry.objects.filter(id=pid).exists():
		item = ReturnEntry.objects.filter(id=pid).first()
		s_goods = ReturnItem.objects.filter(damageid=pid)
		dinvoice = ReturnInvoice.objects.filter(damageid=pid)
		context = {'item': item, 's_goods': s_goods, 'dinvoice': dinvoice}    
		return render(request, 'display/return_detail.html', context)
	else:
		return redirect('return_display')


@user_access
def search_return(request):
	if request.method == "POST":
		search = request.POST.get('search')
		sea = search.upper()
		se = search.title()
		s = search.lower()
		u_site = user_site(request)
		u_status = user_role(request)
		if u_status == 'main_admin' or u_status == 'main_staff':
			lookup = Q(purchase_order_number=search) | Q(damage_number=search) | Q(user_site=search) | Q(purchase_order_number=sea) | Q(damage_number=sea) | Q(user_site=sea) | Q(purchase_order_number=se) | Q(damage_number=se) | Q(user_site=se) | Q(purchase_order_number=s) | Q(damage_number=s) | Q(user_site=s)
		else:
			lookup = Q(Q(purchase_order_number=search) | Q(damage_number=search) | Q(purchase_order_number=sea) | Q(damage_number=sea) | Q(purchase_order_number=se) | Q(damage_number=se) | Q(purchase_order_number=s) | Q(damage_number=s)) & Q(user_site=u_site)
		s_item = ReturnEntry.objects.filter(lookup).order_by('-id')
		context = {'s_item': s_item, 'search': search}
		return render(request, 'display/return_search.html', context)
	else:
		return redirect('return_display')


@user_access
def print_return(request):
	if request.method=="POST":
		jid = request.POST.get('jid')
		s_good = ReturnEntry.objects.filter(id=jid).first()
		igoods = ReturnItem.objects.filter(damageid=jid)
		minvoice = ReturnInvoice.objects.filter(damageid=jid)

		context = {'a': s_good, 'igoods': igoods, 'minvoice': minvoice}
		pdf = render_to_pdf('printreturn.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			rnum = random.randint(11111111, 99999999)
			filename = "Reportreturn_%s.pdf" %(rnum)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")
	else:
		return redirect('return_display')


@user_access
def delete_return(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		ge = ReturnItem.objects.filter(damageid=sid)				
		for a in ge:
			itemid = a.item_id
			item = a.item
			qty = a.quantity
			rate = a.rate
			disp = a.discount_per
			dism = a.discount_amt
			amt = a.amount
			po = a.po
			pvn = a.pvn
			if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
				itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
				quantity = itm.quantity
				amount = itm.amount
				dim = itm.discount_amt
				amount = float(amount) + float(amt)
				dqty = float(quantity) + float(qty)
				if float(dism) > 0:
					dim = float(dim) + float(dism)
					dim = round(float(dim),2)
				InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(quantity=dqty, discount_amt=dim, amount=amount, useable_quantity=dqty, retur='no', retur_qty='0')
				pv = PurchaseEntry.objects.filter(voucher_number=pvn).first()
				subto = pv.sub_total
				subt = float(subto) + float(amt)
				dip = pv.discount_per
				dim = pv.discount_amt
				va = pv.vat
				tot = subt
				if float(dip) > 0:
					dim = float(tot) * (float(dip)/100)
					tot = float(tot) - float(dim)
					dim = round(float(dim),2)
				if va != '' and float(va) > 0:
					tot = float(tot) + float(va)
				tot = round(float(tot),2)
				subt = round(float(subt),2)
				PurchaseEntry.objects.filter(voucher_number=pvn).update(sub_total=subt, total=tot, discount_amt=dim, retur='no')

		ReturnEntry.objects.filter(id=sid).delete()
		ReturnInvoice.objects.filter(damageid=sid).delete()
		ReturnItem.objects.filter(damageid=sid).delete()
		messages.info(request, 'done')
		return redirect('return_display')
	else:
		return redirect('return_display')


@user_access
def return_edit(request, pid):
	if ReturnEntry.objects.filter(id=pid).exists():
		porder = PurchaseOrder.objects.filter(status='approved')
		uom_dash = UOM.objects.all()
		item_real = StockItem.objects.all()
		item = ReturnEntry.objects.filter(id=pid).first()
		bills = []
		pp = ReturnItem.objects.filter(damageid=pid)
		bill_count = []
		a = 0
		for b in pp:
			a = a+1
			bill_count.append(a)

		seen = set()
		seen_add = seen.add
		tran = ReturnItem.objects.values_list('pvn', flat=True).distinct()
		ent = [x for x in tran if not (x in seen or seen_add(x))]
		for r in ent:
			bill = ReturnItem.objects.filter(pvn=r, damageid=pid)
			n = len(bill)
			bills.append([bill, range(1,n)])

		pitem = InvoiceItem.objects.filter(issue_use="no", grn_status='no').exclude(Q(damage='all') | Q(retur='all'))
		psupa = []
		seen = set()
		seen_add = seen.add
		tran = PurchaseEntry.objects.values_list('purchase_order_number', flat=True).distinct()
		ent = [x for x in tran if not (x in seen or seen_add(x))]
		for r in ent:
			ps = PurchaseEntry.objects.filter(purchase_order_number=r)
			n = len(ps)
			psupa.append([ps, range(1,n)])

		purinvoice = PurchaseEntry.objects.filter(issue_use='no', grn_status='no')

		minv = ReturnInvoice.objects.filter(damageid=pid)
		mis = []
		for m in minv:
			mi = m.voucher_number
			mis.append(mi)

		mitm = ReturnItem.objects.filter(damageid=pid)

		context = {'item': item, 'pp': pp, 'porder': porder, 'pitem': pitem, 'bill_count': bill_count, 'bills': bills, 'item_real': item_real, 'uom_dash': uom_dash, 'psupa': psupa, 'purinvoice': purinvoice, 'minv': minv, 'mitm': mitm}    
		return render(request, 'return_edit.html', context)
	else:
		return redirect('return_display')


@user_access
def add_return(request):
	if request.method=="POST":
		current_user = request.user.username
		u_site = user_site(request)
		pvnl = []
		date = request.POST.get('date')
		damage_number = request.POST.get('damage_number')
		pvn_count = request.POST.get('pvn_count')
		narrat = request.POST.get('narrat')
		porder = request.POST.get('jobnumber')
		itemadd = request.POST.getlist('itemadd')
		pvnlist = request.POST.getlist('pvnval')
		if len(pvnlist) == 0:
			messages.info(request, 'error')
			return redirect('return_product')

		for p in pvnlist:
			pvn = p.upper()
			pvnl.append(pvn)

		pvnl = list(set(pvnl))

		for a in itemadd:
			a = str(a)
			for p in pvnl:
				pvn = p
				rstr = str(p) + a
				if request.POST.get('inameid'+rstr):
					itemid = request.POST.get('inameid'+rstr)
					if ReturnItem.objects.filter(item_id=itemid, pvn=pvn).exists():
						messages.info(request, 'error')
						return redirect('return_product')

		for a in itemadd:
			a = str(a)
			for p in pvnl:
				pvn = p
				rstr = str(p) + a
				if request.POST.get('inameid'+rstr):
					itemid = request.POST.get('inameid'+rstr)
					quantity = request.POST.get('iqty'+rstr)
					if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
						itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
						qty = itm.quantity
						if float(quantity) > float(qty):
							messages.info(request, 'error')
							return redirect('return_product')

		if ReturnEntry.objects.filter(damage_number=damage_number).exists():
			messages.info(request, 'error')
			return redirect('return_product')
		else:
			query = ReturnEntry(entry_date=date, purchase_order_number=porder, narration=narrat, damage_number=damage_number, pvn_count=pvn_count, entry_by=current_user, user_site=u_site)
			query.save()
			# PurchaseOrder.objects.filter(purchase_number=porder).update(invoice_id=pid, invoice_status="yes")

		pid = query.id
		for p in pvnl:
			pe = PurchaseEntry.objects.filter(voucher_number=p).first()
			voucher_number = pe.voucher_number
			invoice = pe.invoice_number
			invoice_type = pe.invoice_type
			supplier = pe.supplier_name
			subtotal = pe.sub_total
			discount_amt = pe.discount_amt
			discount_per = pe.discount_per
			vat = pe.vat
			total = pe.total
			po = porder.upper()
			query = ReturnInvoice(damageid=pid, damage_number=damage_number, purchase_order_number=po, voucher_number=p, invoice_number=invoice, invoice_type=invoice_type, supplier=supplier, sub_total=subtotal, discount_amt=discount_amt, discount_per=discount_per, vat=vat, total=total)
			query.save()

		for a in itemadd:
			a = str(a)
			po = porder.upper()
			for p in pvnl:
				pvn = p
				rstr = str(p) + a
				if request.POST.get('inameid'+rstr):
					itemid = request.POST.get('inameid'+rstr)
					item = request.POST.get('iname'+rstr)
					alias = request.POST.get('ialias'+rstr)
					uom = request.POST.get('iuom'+rstr)
					qty = request.POST.get('iqty'+rstr)
					if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
						itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
						quantity = itm.quantity
						rate = itm.rate
						disp = itm.discount_per
						dism = itm.discount_amt
						amt = float(qty) * float(rate)
						dm = 0
						if float(disp) > 0:
							dm = float(amt) * (float(disp)/100)
							amt = float(amt) - float(dm)
						que = ReturnItem(damageid=pid, po=po, dn=damage_number, pvn=pvn, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty, rate=rate, amount=amt, discount_per=disp, discount_amt=dm)
						que.save()
						dqty = float(quantity) - float(qty)
						if int(dqty) == 0:
							InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(quantity=dqty, amount=0, discount_per=0, discount_amt=0, useable_quantity=dqty, retur='all', retur_qty=qty)
						else:
							amtt = float(dqty) * float(rate)
							dm = 0
							if float(disp) > 0:
								dm = float(amtt) * (float(disp)/100)
								amtt = float(amtt) - float(dm)
								amtt = round(float(amtt),2)
								dm = round(float(dm),2)
							InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(quantity=dqty, amount=amtt, discount_amt=dm, useable_quantity=dqty, retur='partial', retur_qty=qty)

						pv = PurchaseEntry.objects.filter(voucher_number=pvn).first()
						subto = pv.sub_total
						subt = float(subto) - float(amt)
						dip = pv.discount_per
						dim = pv.discount_amt
						va = pv.vat
						tot = subt
						if float(dip) > 0:
							dim = float(tot) * (float(dip)/100)
							tot = float(tot) - float(dim)
							dim = round(float(dim),2)
						if va != '' and float(va) > 0:
							tot = float(tot) + float(va)
						tot = round(float(tot),2)
						subt = round(float(subt),2)
						PurchaseEntry.objects.filter(voucher_number=pvn).update(sub_total=subt, total=tot, discount_amt=dim, retur='yes')

		pod = porder.upper()
		po = PurchaseOrder.objects.filter(purchase_number=pod).first()

		notify_topic = 'return_entry'
		content_id = pid
		content = 'return_add'
		from_site = u_site
		from_user = current_user
		content_val = damage_number
		content_val2 = po.issuing_site

		q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, from_site=from_site, from_user=from_user, content_val=content_val, content_val2=content_val2)
		q.save()

		messages.info(request, 'done')
		return redirect('return_product')
	else:
		return redirect('return_product')


@user_access
def edit_return(request):
	if request.method=="POST":
		pvnl = []
		pid = request.POST.get('pid')
		date = request.POST.get('date')
		damage_number = request.POST.get('damage_number')
		narrat = request.POST.get('narrat')
		porder = request.POST.get('jobnumber')
		itemadd = request.POST.getlist('itemadd')
		pvnlist = request.POST.getlist('pvnval')
		if len(pvnlist) == 0:
			messages.info(request, 'error')
			return redirect('/return-edit/'+str(pid)+'/')

		for p in pvnlist:
			pvn = p.upper()
			pvnl.append(pvn)

		pvnl = list(set(pvnl))

		for a in itemadd:
			a = str(a)
			for p in pvnl:
				pvn = p
				rstr = str(p) + a
				if request.POST.get('inameid'+rstr):
					itemid = request.POST.get('inameid'+rstr)
					if ReturnItem.objects.filter(item_id=itemid, pvn=pvn).exclude(damageid=pid).exists():
						messages.info(request, 'error')
						return redirect('/return-edit/'+str(pid)+'/')

		if ReturnItem.objects.filter(damageid=pid).exists():
			ge = ReturnItem.objects.filter(damageid=pid)				
			for a in ge:
				itemid = a.item_id
				item = a.item
				qty = a.quantity
				rate = a.rate
				disp = a.discount_per
				dism = a.discount_amt
				amt = a.amount
				po = a.po
				pvn = a.pvn
				if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
					itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
					quantity = itm.quantity
					amount = itm.amount
					dim = itm.discount_amt
					amount = float(amount) + float(amt)
					dqty = float(quantity) + float(qty)
					if float(dism) > 0:
						dim = float(dim) + float(dism)
						dim = round(float(dim),2)
					InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(quantity=dqty, discount_amt=dim, amount=amount, useable_quantity=dqty, retur='no', retur_qty='0')
					pv = PurchaseEntry.objects.filter(voucher_number=pvn).first()
					subto = pv.sub_total
					subt = float(subto) + float(amt)
					dip = pv.discount_per
					dim = pv.discount_amt
					va = pv.vat
					tot = subt
					if float(dip) > 0:
						dim = float(tot) * (float(dip)/100)
						tot = float(tot) - float(dim)
						dim = round(float(dim),2)
					if va != '' and float(va) > 0:
						tot = float(tot) + float(va)
					tot = round(float(tot),2)
					subt = round(float(subt),2)
					PurchaseEntry.objects.filter(voucher_number=pvn).update(sub_total=subt, total=tot, discount_amt=dim, retur='no')

		for a in itemadd:
			a = str(a)
			for p in pvnl:
				pvn = p
				rstr = str(p) + a
				if request.POST.get('inameid'+rstr):
					itemid = request.POST.get('inameid'+rstr)
					quantity = request.POST.get('iqty'+rstr)
					if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
						itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
						qty = itm.quantity
						if float(quantity) > float(qty):
							for a in ge:
								itemid = a.item_id
								item = a.item
								qty = a.quantity
								rate = a.rate
								disp = a.discount_per
								dism = a.discount_amt
								amt = a.amount
								pvn = a.pvn
								if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
									itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
									quantity = itm.quantity
									amount = itm.amount
									dim = itm.discount_amt
									amount = float(amount) - float(amt)
									dqty = float(quantity) - float(qty)
									if float(dism) > 0:
										dim = float(dim) - float(dism)
										dim = round(float(dim),2)
									if int(dqty) == 0:
										InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(quantity=dqty, amount=0, discount_per=0, discount_amt=0, useable_quantity=dqty, retur='all', retur_qty=qty)
									else:
										InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(quantity=dqty, amount=amount, discount_amt=dim, useable_quantity=dqty, retur='partial', retur_qty=qty)
									pv = PurchaseEntry.objects.filter(voucher_number=pvn).first()
									subto = pv.sub_total
									subt = float(subto) - float(amt)
									dip = pv.discount_per
									dim = pv.discount_amt
									va = pv.vat
									tot = subt
									if float(dip) > 0:
										dim = float(tot) * (float(dip)/100)
										tot = float(tot) - float(dim)
										dim = round(float(dim),2)
									if va != '' and float(va) > 0:
										tot = float(tot) + float(va)
									tot = round(float(tot),2)
									subt = round(float(subt),2)
									PurchaseEntry.objects.filter(voucher_number=pvn).update(sub_total=subt, total=tot, discount_amt=dim, retur='yes')
							messages.info(request, 'error')
							return redirect('/return-edit/'+str(pid)+'/')

		ReturnEntry.objects.filter(id=pid).update(entry_date=date, purchase_order_number=porder, narration=narrat)
		ReturnInvoice.objects.filter(damageid=pid).delete()
		ReturnItem.objects.filter(damageid=pid).delete()

		for p in pvnl:
			pe = PurchaseEntry.objects.filter(voucher_number=p).first()
			voucher_number = pe.voucher_number
			invoice = pe.invoice_number
			invoice_type = pe.invoice_type
			supplier = pe.supplier_name
			subtotal = pe.sub_total
			discount_amt = pe.discount_amt
			discount_per = pe.discount_per
			vat = pe.vat
			total = pe.total
			po = porder.upper()
			query = ReturnInvoice(damageid=pid, damage_number=damage_number, purchase_order_number=po, voucher_number=p, invoice_number=invoice, invoice_type=invoice_type, supplier=supplier, sub_total=subtotal, discount_amt=discount_amt, discount_per=discount_per, vat=vat, total=total)
			query.save()

		for a in itemadd:
			a = str(a)
			po = porder.upper()
			for p in pvnl:
				pvn = p
				rstr = str(p) + a
				if request.POST.get('inameid'+rstr):
					itemid = request.POST.get('inameid'+rstr)
					item = request.POST.get('iname'+rstr)
					alias = request.POST.get('ialias'+rstr)
					uom = request.POST.get('iuom'+rstr)
					qty = request.POST.get('iqty'+rstr)
					if InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).exists():
						itm = InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).first()
						quantity = itm.quantity
						rate = itm.rate
						disp = itm.discount_per
						dism = itm.discount_amt
						amt = float(qty) * float(rate)
						dm = 0
						if float(disp) > 0:
							dm = float(amt) * (float(disp)/100)
							amt = float(amt) - float(dm)
						que = ReturnItem(damageid=pid, po=po, dn=damage_number, pvn=pvn, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty, rate=rate, amount=amt, discount_per=disp, discount_amt=dm)
						que.save()
						dqty = float(quantity) - float(qty)
						if int(dqty) == 0:
							InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(quantity=dqty, amount=0, discount_per=0, discount_amt=0, useable_quantity=dqty, retur='all', retur_qty=qty)
						else:
							amtt = float(dqty) * float(rate)
							dm = 0
							if float(disp) > 0:
								dm = float(amtt) * (float(disp)/100)
								amtt = float(amtt) - float(dm)
								amtt = round(float(amtt),2)
								dm = round(float(dm),2)
							InvoiceItem.objects.filter(item_id=itemid, pvn=pvn).update(quantity=dqty, amount=amtt, discount_amt=dm, useable_quantity=dqty, retur='partial', retur_qty=qty)

						pv = PurchaseEntry.objects.filter(voucher_number=pvn).first()
						subto = pv.sub_total
						subt = float(subto) - float(amt)
						dip = pv.discount_per
						dim = pv.discount_amt
						va = pv.vat
						tot = subt
						if float(dip) > 0:
							dim = float(tot) * (float(dip)/100)
							tot = float(tot) - float(dim)
							dim = round(float(dim),2)
						if va != '' and float(va) > 0:
							tot = float(tot) + float(va)
						tot = round(float(tot),2)
						subt = round(float(subt),2)
						PurchaseEntry.objects.filter(voucher_number=pvn).update(sub_total=subt, total=tot, discount_amt=dim, retur='yes')

		messages.info(request, 'done')
		return redirect('/return-edit/'+str(pid)+'/')
	else:
		return redirect('return_display')

#===============================================================================

#=====================vehicle_tracking============================

@user_access
def track_dash(request):
	v_type = VehicleType.objects.all()
	vehis = []
	seen =set()
	seen_add = seen.add
	ent = VehicleList.objects.values_list('vehicle_type_id', flat=True)
	ent = [x for x in ent if not (x in seen or seen_add(x))]
	for e in ent:
		vehi = VehicleList.objects.filter(vehicle_type_id=e, active_status='yes')
		n = len(vehi)
		vehis.append([vehi, range(1,n)])
	if VehicleTrack.objects.last():
		jd = VehicleTrack.objects.last()
		jn = jd.move_count
		newpei = int(jn)+1
	else:
		newpei = 1
	u_site = user_site(request)
	site_dash = Site.objects.filter(active_status='yes').exclude(name=u_site)
	context = {'v_type': v_type, 'u_site': u_site, 'vehis': vehis, 'newpei': newpei, 'site_dash': site_dash}
	return render(request, 'fuelmaintain/vehicle_track.html', context)


@user_access
def track_display(request):
	vehis = []
	seen =set()
	seen_add = seen.add
	ent = VehicleList.objects.values_list('vehicle_type_id', flat=True)
	ent = [x for x in ent if not (x in seen or seen_add(x))]
	for e in ent:
		vehi = VehicleList.objects.filter(vehicle_type_id=e, active_status='yes')
		n = len(vehi)
		vehis.append([vehi, range(1,n)])
	u_site = user_site(request)
	site_dash = Site.objects.filter(active_status='yes').exclude(name=u_site)
	s_item = VehicleTrack.objects.all().order_by('-id')
	v_type = VehicleType.objects.all()
	context = {'s_item': s_item, 'v_type': v_type, 'vehis': vehis, 'site_dash': site_dash}
	return render(request, 'fuelmaintain/display/move_display.html', context)


@user_access
def move_add(request):
	if request.method == "POST":
		current_user = request.user.username
		date = request.POST.get('date')
		mid = request.POST.get('mid')
		mcount = request.POST.get('mcount')
		vtype = request.POST.get('vehicle_type')
		vtypeid = request.POST.get('vehicle_type_id')
		vnum = request.POST.get('vehicle')
		tosite = request.POST.get('site')
		fromsite = request.POST.get('issue_locate')
		num_type = request.POST.get('num_type')
		u_site = user_site(request)
		if VehicleTrack.objects.filter(entry_date=date, from_site=fromsite, to_site=tosite, vehicle_number=vnum).exists():
			messages.info(request, 'error')
			return redirect('vehicle_move')
		else:
			query = VehicleTrack(entry_date=date, move_number=mid, move_count=mcount, vehicle_number=vnum, from_site=fromsite, to_site=tosite, vehicle_type_id=vtypeid, vehicle_type=vtype, num_type=num_type, user_site=u_site, entry_by=current_user)
			query.save()

			gid = query.id

			notify_topic = 'movement'
			content_id = gid
			content = 'move_add'
			from_site = fromsite
			from_user = current_user
			content_val = mid
			content_val1 = vnum
			content_val2 = tosite

			q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, from_site=from_site, from_user=from_user, content_val=content_val, content_val2=content_val2)
			q.save()

			messages.info(request, 'done')
			return redirect('vehicle_move')
	else:
		return redirect('vehicle_move')


@user_access
def move_update(request):
	if request.method == "POST":
		vid = request.POST.get('suid')
		date = request.POST.get('date')
		mid = request.POST.get('mid')
		vtype = request.POST.get('vehicle_type')
		vtypeid = request.POST.get('vehicle_type_id')
		vnum = request.POST.get('vehicle')
		tosite = request.POST.get('site')
		fromsite = request.POST.get('issue_locate')
		num_type = request.POST.get('num_type')
		if VehicleTrack.objects.filter(entry_date=date, from_site=fromsite, to_site=tosite, vehicle_number=vnum).exclude(id=vid).exists():
			messages.info(request, 'error')
			return redirect('move_display')
		else:
			VehicleTrack.objects.filter(id=vid).update(entry_date=date, num_type=num_type, vehicle_number=vnum, vehicle_type_id=vtypeid, vehicle_type=vtype, to_site=tosite)
			Notification.objects.filter(content_val=mid).update(content_val1=vnum, content_val2=tosite)
			messages.info(request, 'done')
			return redirect('move_display')
	else:
		return redirect('move_display')


@user_access
def search_move(request):
	if request.method == "POST":
		search = request.POST.get('search')
		sea = search.upper()
		se = search.title()
		s = search.lower()
		lookup = Q(vehicle_number__icontains=search) | Q(move_number__icontains=search) | Q(from_site__icontains=search) | Q(to_site__icontains=search) | Q(vehicle_type__icontains=search) | Q(vehicle_number__icontains=sea) | Q(move_number__icontains=sea) | Q(from_site__icontains=sea) | Q(to_site__icontains=sea) | Q(vehicle_type__icontains=sea) | Q(vehicle_number__icontains=se) | Q(move_number__icontains=se) | Q(from_site__icontains=se) | Q(to_site__icontains=se) | Q(vehicle_type__icontains=se) | Q(vehicle_number__icontains=s) | Q(move_number__icontains=s) | Q(from_site__icontains=s) | Q(to_site__icontains=s) | Q(vehicle_type__icontains=s)
		s_item = VehicleTrack.objects.filter(lookup).order_by('-id')
		v_type = VehicleType.objects.all()
		context = {'s_item': s_item, 'search': search, 'v_type': v_type}
		return render(request, 'fuelmaintain/display/search_move.html', context)
	else:
		return redirect('move_display')


@user_access
def move_delete(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		VehicleTrack.objects.filter(id=sid).delete()
		messages.info(request, 'done')
		return redirect('move_display')
	else:
		return redirect('move_display')


@user_access
def track_detail(request, vid):
	if VehicleTrack.objects.filter(id=vid).exists():
		u_site = user_site(request)
		site_dash = Site.objects.filter(active_status='yes').exclude(name=u_site)
		s_item = VehicleTrack.objects.filter(id=vid).first()
		v_type = VehicleType.objects.all()
		context = {'item': s_item, 'v_type': v_type, 'site_dash': site_dash}
		return render(request, 'fuelmaintain/display/move_detail.html', context)
	else:
		return redirect('move_display')


def move_status(request):
	if request.method=="POST":
		u_site = user_site(request)
		sid = request.POST.get('sid')
		vt = VehicleTrack.objects.filter(id=sid).first()
		tos = vt.to_site
		vnum = vt.vehicle_number
		ntype = vt.num_type
		if tos == u_site:
			date = request.POST.get('date')
			now = dt.now()
			current_time = now.strftime("%H:%M")
			arrive = date+' '+current_time
			VehicleTrack.objects.filter(id=sid).update(status="arrived", arrival_datetime=arrive)
			if ntype == 'vehicle':
				if VehicleList.objects.filter(vehicle_number=vnum).exists():
					VehicleList.objects.filter(vehicle_number=vnum).update(current=tos)
			if ntype == 'chasis':
				if VehicleList.objects.filter(chasis_number=vnum).exists():
					VehicleList.objects.filter(chasis_number=vnum).update(current=tos)
			if ntype == 'engine':
				if VehicleList.objects.filter(engine_number=vnum).exists():
					VehicleList.objects.filter(engine_number=vnum).update(current=tos)
			messages.info(request, 'done')
			return redirect('/movement-detail/'+str(sid)+'/')
		else:
			messages.info(request, 'error')
			return redirect('/movement-detail/'+str(sid)+'/')
	else:
		return redirect('move_display')

#=================================================================================

#fuel internal transfer===================================================================

@user_access
def fuel_internal_transfer(request):
	reserve = Reserviour.objects.all()
	f_type = FuelType.objects.all()
	u_site = user_site(request)
	if FuelInternalTransfer.objects.last():
		jd = FuelInternalTransfer.objects.last()
		jn = jd.pon
		newpon = jn+1
	else:
		newpon = 1

	context = {'newpon': newpon, 'f_type': f_type, 'reserve': reserve, 'u_site': u_site}
	return render(request, 'fuelmaintain/fuel_transfer.html', context)


@user_access
def add_fueltransfer(request):
	if request.method=="POST":
		current_user = request.user.username
		u_site = user_site(request)
		freserve = request.POST.get('freserviour')
		treserve = request.POST.get('treserviour')
		quantity = request.POST.get('quantity')
		date = request.POST.get('date')
		fuel_number = request.POST.get('fuel_number')
		pon = request.POST.get('pon')
		fuel_type = request.POST.get('fuel_type')
		narrat = request.POST.get('narrat')

		fre = Reserviour.objects.get(name=freserve)
		fqty = fre.stock
		if float(fqty) < 0 or float(fqty) == 0:
			messages.info(request, 'error')
			return redirect('fuel_internal_transfer')
		if float(fqty) < float(quantity):
			messages.info(request, 'error')
			return redirect('fuel_internal_transfer')

		query = FuelInternalTransfer(fuel_number=fuel_number, pon=pon, fuel_type=fuel_type, user_site=u_site, entry_date=date, from_reserviour=freserve, to_reserviour=treserve, quantity=quantity, narration=narrat, entry_by=current_user)
		query.save()

		tre = Reserviour.objects.get(name=treserve)
		tqty = tre.stock

		fup = float(fqty) - float(quantity)
		fup = round(float(fup),2)

		tup = float(tqty) + float(quantity)
		tup = round(float(tup),2)

		Reserviour.objects.filter(name=freserve).update(stock=fup)
		Reserviour.objects.filter(name=treserve).update(stock=tup)
		
		notify_topic = 'fuel_transfer'
		content_id = query.id
		content = 'fuel_transfer_add'
		from_site = u_site
		from_user = current_user
		content_val = fuel_number

		q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, from_site=from_site, from_user=from_user, content_val=content_val)
		q.save()


		messages.info(request, 'done')
		return redirect('fuel_internal_transfer')
	else:
		return redirect('fuel_internal_transfer')


@user_access
def fuel_internal_display(request):
	u_site = user_site(request)
	u_status = user_role(request)
	if u_status == 'main_admin' or u_status == 'main_staff':
		s_item = FuelInternalTransfer.objects.all().order_by('-id')[:30]
	else:
		s_item = FuelInternalTransfer.objects.filter(user_site=u_site).order_by('-id')[:30]
	context = {'s_item': s_item}
	return render(request, 'fuelmaintain/display/fuel_transfer_display.html', context)


@user_access
def fuel_internal_detail(request, fid):
	current_user = request.user.username
	u_site = user_site(request)
	item = FuelInternalTransfer.objects.filter(id=fid).first()
	context = {'item': item}
	return render(request, 'fuelmaintain/display/fuel_transfer_detail.html', context)


@user_access
def fuel_internal_edit(request, fid):
	u_site = user_site(request)
	item = FuelInternalTransfer.objects.filter(id=fid).first()
	reserve = Reserviour.objects.all()
	f_type = FuelType.objects.all()
	context = {'item': item, 'f_type': f_type, 'reserve': reserve}
	return render(request, 'fuelmaintain/fuel_transfer_edit.html', context)


@user_access
def update_fuel_transfer(request):
	if request.method=="POST":
		pid = request.POST.get('fid')
		freserve = request.POST.get('freserviour')
		treserve = request.POST.get('treserviour')
		quantity = request.POST.get('quantity')
		date = request.POST.get('date')
		fuel_number = request.POST.get('fuel_number')
		fuel_type = request.POST.get('fuel_type')
		narrat = request.POST.get('narrat')
		fre = Reserviour.objects.get(name=freserve)
		fqty = fre.stock
		if float(fqty) < 0 or float(fqty) == 0:
			messages.info(request, 'error')
			return redirect('/fuel-transfer-edit/'+str(pid)+'/')
		if float(fqty) < float(quantity):
			messages.info(request, 'error')
			return redirect('/fuel-transfer-edit/'+str(pid)+'/')

		rec = FuelInternalTransfer.objects.get(id=pid)
		rqty = rec.quantity
		rtreserve = rec.to_reserviour
		rfreserve = rec.from_reserviour

		rtre = Reserviour.objects.get(name=rtreserve)
		rtqty = rtre.stock
		rfre = Reserviour.objects.get(name=rfreserve)
		rfqty = rfre.stock

		if float(rtqty) < float(rqty):
			messages.info(request, 'error')
			return redirect('/fuel-transfer-edit/'+str(pid)+'/')
		else:
			rfup = float(rfqty) + float(rqty)
			rfup = round(float(rfup),2)

			rtup = float(rtqty) - float(rqty)
			rtup = round(float(rtup),2)

			Reserviour.objects.filter(name=rfreserve).update(stock=rfup)
			Reserviour.objects.filter(name=rtreserve).update(stock=rtup)

		FuelInternalTransfer.objects.filter(id=pid).update(fuel_type=fuel_type, entry_date=date, from_reserviour=freserve, to_reserviour=treserve, quantity=quantity, narration=narrat)

		tre = Reserviour.objects.get(name=treserve)
		fre = Reserviour.objects.get(name=freserve)
		tqty = tre.stock
		fqty = fre.stock

		fup = float(fqty) - float(quantity)
		fup = round(float(fup),2)

		tup = float(tqty) + float(quantity)
		tup = round(float(tup),2)

		Reserviour.objects.filter(name=freserve).update(stock=fup)
		Reserviour.objects.filter(name=treserve).update(stock=tup)

		messages.info(request, 'done')
		return redirect('/fuel-transfer-edit/'+str(pid)+'/')
	else:
		return redirect('fuel_internal_display')


@user_access
def delete_fuel_transfer(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		FuelInternalTransfer.objects.filter(id=sid).delete()
		messages.info(request, 'done')
		return redirect('fuel_internal_display')
	else:
		return redirect('fuel_internal_display')


@user_access
def search_fuel_transfer(request):
	if request.method == "POST":
		search = request.POST.get('search')
		sea = search.upper()
		se = search.title()
		s = search.lower()
		u_site = user_site(request)
		u_status = user_role(request)
		if u_status == 'main_admin' or u_status == 'main_staff':
			lookup = Q(fuel_number=search) | Q(from_reserviour__icontains=search) | Q(to_reserviour__icontains=search) | Q(fuel_type__icontains=search) | Q(user_site__icontains=search)
		else:
			lookup = Q(Q(fuel_number=search) | Q(from_reserviour__icontains=search) | Q(to_reserviour__icontains=search) | Q(fuel_type__icontains=search)) & Q(user_site=u_site)
		s_item = FuelInternalTransfer.objects.filter(lookup).order_by('-id')
		context = {'s_item': s_item, 'search': search}
		return render(request, 'fuelmaintain/display/fuel_transfer_search.html', context)
	else:
		return redirect('fuel_internal_display')


@user_access
def print_fueltransfer(request):
	if request.method=="POST":
		jid = request.POST.get('jid')
		job = FuelInternalTransfer.objects.filter(id=jid).first()

		context = {'a': job}
		pdf = render_to_pdf('fuelmaintain/printfuel_transfer.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			rnum = random.randint(11111111, 99999999)
			filename = "Reportfueltransfer_%s.pdf" %(rnum)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")
	else:
		return redirect('fuel_internal_display')

#===================================================================================

#damage_product======================================================

@user_access
def internal_damage_stock(request):
	porder = InternalGrn.objects.filter(invoice_status='no')
	uom_dash = UOM.objects.all()
	item_real = StockItem.objects.all()
	pvn = 0
	if InternalDamageEntry.objects.last():
		good = InternalDamageEntry.objects.last()
		ng = good.pvn_count
		pvn = int(ng) + 1
	else:
		pvn = pvn + 1

	pitem = InternalGrnItems.objects.filter(invoice_status="no").exclude(damage='all')

	igoods = []
	seen = set()
	seen_add = seen.add
	tran = InternalGrnItems.objects.values_list('goodsid', flat=True).distinct()
	ent = [x for x in tran if not (x in seen or seen_add(x))]
	for s in ent:
		igood = InternalGrnItems.objects.filter(goodsid=s, invoice_status='no').exclude(damage='all')
		n = len(igood)
		igoods.append([igood, range(1,n)])

	context = {'porder': porder, 'pitem': pitem, 'pvn': pvn, 'item_real': item_real, 'uom_dash': uom_dash, 'igoods': igoods}    
	return render(request, 'internal_damage.html', context)


@user_access
def internal_damage_display(request):
	u_site = user_site(request)
	u_status = user_role(request)
	if u_status == 'main_admin' or u_status == 'main_staff':
		s_item = InternalDamageEntry.objects.all().order_by('-id')[:30]
	else:
		s_item = InternalDamageEntry.objects.filter(user_site=u_site).order_by('-id')[:30]
	context = {'s_item': s_item}    
	return render(request, 'display/internal_damage_display.html', context)


@user_access
def internal_damage_detail(request,pid):
	if InternalDamageEntry.objects.filter(id=pid).exists():
		item = InternalDamageEntry.objects.filter(id=pid).first()
		s_goods = InternalDamageItem.objects.filter(damageid=pid)
		context = {'item': item, 's_goods': s_goods}    
		return render(request, 'display/internal_damage_detail.html', context)
	else:
		return redirect('internal_damage_display')


@user_access
def search_internal_damage(request):
	if request.method == "POST":
		search = request.POST.get('search')
		sea = search.upper()
		se = search.title()
		s = search.lower()
		u_site = user_site(request)
		u_status = user_role(request)
		if u_status == 'main_admin' or u_status == 'main_staff':
			lookup = Q(damage_number=search) | Q(user_site__icontains=search) | Q(damage_number=sea) | Q(user_site=sea) | Q(damage_number=se) | Q(user_site=se) | Q(damage_number=s) | Q(user_site=s)
		else:
			lookup = Q(Q(narration__icontains=search) | Q(damage_number=search) | Q(narration__icontains=sea) | Q(damage_number=sea) | Q(damage_number=se) | Q(damage_number=s)) & Q(user_site=u_site)
		s_item = InternalDamageEntry.objects.filter(lookup).order_by('-id')
		context = {'s_item': s_item, 'search': search}
		return render(request, 'display/internal_damage_search.html', context)
	else:
		return redirect('internal_damage_display')


@user_access
def print_internal_damage(request):
	if request.method=="POST":
		jid = request.POST.get('jid')
		s_good = InternalDamageEntry.objects.filter(id=jid).first()
		igoods = InternalDamageItem.objects.filter(damageid=jid)

		context = {'a': s_good, 'igoods': igoods}
		pdf = render_to_pdf('printinternaldamage.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			rnum = random.randint(11111111, 99999999)
			filename = "Reporttransferdamage_%s.pdf" %(rnum)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")
	else:
		return redirect('internal_damage_display')


@user_access
def delete_internal_damage(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		ge = InternalDamageItem.objects.filter(damageid=sid)				
		for a in ge:
			itemid = a.item_id
			item = a.item
			qty = a.quantity
			pvn = a.pvn
			if InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).exists():
				itm = InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).first()
				quantity = itm.quantity
				dqty = float(quantity) + float(qty)
				InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).update(quantity=dqty, damage='no', damage_qty='0')
				InternalGrn.objects.filter(grn_number=pvn).update(damage='no')

		InternalDamageEntry.objects.filter(id=sid).delete()
		InternalDamageItem.objects.filter(damageid=sid).delete()
		messages.info(request, 'done')
		return redirect('internal_damage_display')
	else:
		return redirect('internal_damage_display')


@user_access
def internal_damage_edit(request, pid):
	if InternalDamageEntry.objects.filter(id=pid).exists():
		porder = InternalGrn.objects.filter(invoice_status='no')
		uom_dash = UOM.objects.all()
		item_real = StockItem.objects.all()
		item = InternalDamageEntry.objects.filter(id=pid).first()
		bills = []
		pp = InternalDamageItem.objects.filter(damageid=pid)
		bill_count = []
		a = 0
		for b in pp:
			a = a+1
			bill_count.append(a)

		seen = set()
		seen_add = seen.add
		tran = InternalDamageItem.objects.values_list('pvn', flat=True).distinct()
		ent = [x for x in tran if not (x in seen or seen_add(x))]
		for r in ent:
			bill = InternalDamageItem.objects.filter(pvn=r, damageid=pid)
			n = len(bill)
			bills.append([bill, range(1,n)])

		pitem = InternalGrnItems.objects.filter(invoice_status='no').exclude(damage='all')

		igoods = []
		seen = set()
		seen_add = seen.add
		tran = InternalGrnItems.objects.values_list('goodsid', flat=True).distinct()
		ent = [x for x in tran if not (x in seen or seen_add(x))]
		for s in ent:
			igood = InternalGrnItems.objects.filter(goodsid=s, invoice_status='no').exclude(damage='all')
			n = len(igood)
			igoods.append([igood, range(1,n)])

		mitm = InternalDamageItem.objects.filter(damageid=pid)

		context = {'item': item, 'pp': pp, 'porder': porder, 'pitem': pitem, 'bill_count': bill_count, 'bills': bills, 'item_real': item_real, 'uom_dash': uom_dash, 'mitm': mitm}    
		return render(request, 'internal_damage_edit.html', context)
	else:
		return redirect('internal_damage_display')


@user_access
def add_internal_damage(request):
	if request.method=="POST":
		current_user = request.user.username
		u_site = user_site(request)
		pvnl = []
		date = request.POST.get('date')
		damage_number = request.POST.get('damage_number')
		pvn_count = request.POST.get('pvn_count')
		narrat = request.POST.get('narrat')
		itemadd = request.POST.getlist('itemadd')
		pvnlist = request.POST.getlist('pvnval')
		if len(pvnlist) == 0:
			messages.info(request, 'error')
			return redirect('internal_damage_stock')

		for p in pvnlist:
			pvn = p.upper()
			pvnl.append(pvn)

		pvnl = list(set(pvnl))

		for a in itemadd:
			a = str(a)
			for p in pvnl:
				pvn = p
				rstr = str(p) + a
				if request.POST.get('inameid'+rstr):
					itemid = request.POST.get('inameid'+rstr)
					if InternalDamageItem.objects.filter(item_id=itemid, pvn=pvn).exists():
						messages.info(request, 'error')
						return redirect('internal_damage_stock')

		for a in itemadd:
			a = str(a)
			for p in pvnl:
				pvn = p
				rstr = str(p) + a
				if request.POST.get('inameid'+rstr):
					itemid = request.POST.get('inameid'+rstr)
					quantity = request.POST.get('iqty'+rstr)
					if InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).exists():
						itm = InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).first()
						qty = itm.quantity
						if float(quantity) > float(qty):
							messages.info(request, 'error')
							return redirect('internal_damage_stock')

		if InternalDamageEntry.objects.filter(damage_number=damage_number).exists():
			messages.info(request, 'error')
			return redirect('internal_damage_stock')
		else:
			query = InternalDamageEntry(entry_date=date, narration=narrat, damage_number=damage_number, pvn_count=pvn_count, entry_by=current_user, user_site=u_site)
			query.save()
			# PurchaseOrder.objects.filter(purchase_number=porder).update(invoice_id=pid, invoice_status="yes")

		pid = query.id

		for a in itemadd:
			a = str(a)
			for p in pvnl:
				pvn = p
				rstr = str(p) + a
				if request.POST.get('inameid'+rstr):
					itemid = request.POST.get('inameid'+rstr)
					item = request.POST.get('iname'+rstr)
					alias = request.POST.get('ialias'+rstr)
					uom = request.POST.get('iuom'+rstr)
					qty = request.POST.get('iqty'+rstr)
					if InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).exists():
						itm = InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).first()
						quantity = itm.quantity
						que = InternalDamageItem(damageid=pid, dn=damage_number, pvn=pvn, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty)
						que.save()
						dqty = float(quantity) - float(qty)
						if int(dqty) == 0:
							InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).update(quantity=dqty, damage='all', damage_qty=qty)
						else:
							InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).update(quantity=dqty, damage='partial', damage_qty=qty)
						InternalGrn.objects.filter(grn_number=pvn).update(damage='yes')

		notify_topic = 'internal_damage_entry'
		content_id = pid
		content = 'internal_damage_add'
		from_site = u_site
		from_user = current_user
		content_val = damage_number

		q = Notification(notify_topic=notify_topic, content_id=content_id, content=content, from_site=from_site, from_user=from_user, content_val=content_val)
		q.save()

		messages.info(request, 'done')
		return redirect('internal_damage_stock')
	else:
		return redirect('internal_damage_stock')


@user_access
def edit_internal_damage(request):
	if request.method=="POST":
		pvnl = []
		pid = request.POST.get('pid')
		date = request.POST.get('date')
		damage_number = request.POST.get('damage_number')
		narrat = request.POST.get('narrat')
		itemadd = request.POST.getlist('itemadd')
		pvnlist = request.POST.getlist('pvnval')
		if len(pvnlist) == 0:
			messages.info(request, 'error')
			return redirect('/internal-damage-edit/'+str(pid)+'/')

		for p in pvnlist:
			pvn = p.upper()
			pvnl.append(pvn)

		pvnl = list(set(pvnl))

		for a in itemadd:
			a = str(a)
			for p in pvnl:
				pvn = p
				rstr = str(p) + a
				if request.POST.get('inameid'+rstr):
					itemid = request.POST.get('inameid'+rstr)
					if InternalDamageItem.objects.filter(item_id=itemid, pvn=pvn).exclude(damageid=pid).exists():
						messages.info(request, 'error')
						return redirect('/internal-damage-edit/'+str(pid)+'/')

		if InternalDamageItem.objects.filter(damageid=pid).exists():
			ge = InternalDamageItem.objects.filter(damageid=pid)				
			for a in ge:
				itemid = a.item_id
				item = a.item
				qty = a.quantity
				pvn = a.pvn
				if InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).exists():
					itm = InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).first()
					quantity = itm.quantity
					dqty = float(quantity) + float(qty)
					InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).update(quantity=dqty, damage='no', damage_qty='0')
					InternalGrn.objects.filter(grn_number=pvn).update(damage='no')

		for a in itemadd:
			a = str(a)
			for p in pvnl:
				pvn = p
				rstr = str(p) + a
				if request.POST.get('inameid'+rstr):
					itemid = request.POST.get('inameid'+rstr)
					quantity = request.POST.get('iqty'+rstr)
					if InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).exists():
						itm = InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).first()
						qty = itm.quantity
						if float(quantity) > float(qty):
							for a in ge:
								itemid = a.item_id
								item = ra.item
								qty = a.quantity
								pvn = a.pvn
								if InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).exists():
									itm = InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).first()
									quantity = itm.quantity
									dqty = float(quantity) - float(qty)
									if int(dqty) == 0:
										InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).update(quantity=dqty, damage='all', damage_qty=qty)
									else:
										InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).update(quantity=dqty, damage='partial', damage_qty=qty)
									InternalGrn.objects.filter(grn_number=pvn).update(damage='yes')
							messages.info(request, 'error')
							return redirect('/internal-damage-edit/'+str(pid)+'/')

		InternalDamageEntry.objects.filter(id=pid).update(entry_date=date, narration=narrat)
		InternalDamageItem.objects.filter(damageid=pid).delete()

		for a in itemadd:
			a = str(a)
			for p in pvnl:
				pvn = p
				rstr = str(p) + a
				if request.POST.get('inameid'+rstr):
					itemid = request.POST.get('inameid'+rstr)
					item = request.POST.get('iname'+rstr)
					alias = request.POST.get('ialias'+rstr)
					uom = request.POST.get('iuom'+rstr)
					qty = request.POST.get('iqty'+rstr)
					if InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).exists():
						itm = InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).first()
						quantity = itm.quantity
						que = InternalDamageItem(damageid=pid, dn=damage_number, pvn=pvn, item_id=itemid, item=item, alias=alias, uom=uom, quantity=qty)
						que.save()
						dqty = float(quantity) - float(qty)
						if int(dqty) == 0:
							InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).update(quantity=dqty, damage='all', damage_qty=qty)
						else:
							InternalGrnItems.objects.filter(item_id=itemid, grn=pvn).update(quantity=dqty, damage='partial', damage_qty=qty)
						InternalGrn.objects.filter(grn_number=pvn).update(damage='yes')

		messages.info(request, 'done')
		return redirect('/internal-damage-edit/'+str(pid)+'/')
	else:
		return redirect('internal_damage_display')

#===============================================================================

#==Fuel leakage entry========================================================

@user_access
def fuel_leakage(request):
	fueldash = []
	reserve = Reserviour.objects.all()
	f_type = FuelType.objects.all()
	if FuelLeakage.objects.last():
		jd = FuelLeakage.objects.last()
		jn = jd.fcn
		newpei = jn+1
	else:
		newpei = 1
	context = {'newpei': newpei, 'f_type': f_type, 'reserve':reserve}
	return render(request, 'fuelmaintain/lickage.html', context)


@user_access
def add_leakage(request):
	if request.method=="POST":
		current_user = request.user.username
		u_site = user_site(request)
		date = request.POST.get('date')
		leakage_number = request.POST.get('consump_number')
		fcn = request.POST.get('pvn_count')
		quantity = request.POST.get('quantity')
		reserve_val = request.POST.get('reserviour_name')
		reserve_id = request.POST.get('reserviour')
		fuel_type = request.POST.get('fuel_type')
		if FuelLeakage.objects.filter(leakage_number=leakage_number).exists():
			messages.info(request, 'error')
			return redirect('fuel_leakage')
		else:
			query = FuelLeakage(entry_date=date, leakage_number=leakage_number, fcn=fcn, fuel_type=fuel_type, user_site=u_site, reserviour=reserve_val, reserviour_id=reserve_id, quantity=quantity, entry_by=current_user)
			query.save()
			messages.info(request, 'done')
			return redirect('fuel_leakage')

		return HttpResponse()
	else:
		return redirect('fuel_leakage')


@user_access
def fuel_leakage_display(request):
	u_site = user_site(request)
	u_status = user_role(request)
	if u_status == 'main_admin' or u_status == 'main_staff':
		s_item = FuelLeakage.objects.all().order_by('-id')[:30]
	else:
		s_item = FuelLeakage.objects.filter(user_site=u_site).order_by('-id')[:30]
	context = {'s_item': s_item}
	return render(request, 'fuelmaintain/display/lickage_display.html', context)


@user_access
def leakage_detail(request, fid):
	current_user = request.user.username
	u_site = user_site(request)
	item = FuelLeakage.objects.filter(id=fid).first()
	context = {'item': item}
	return render(request, 'fuelmaintain/display/lickage_detail.html', context)


@user_access
def edit_leakage(request, fid):
	item = FuelLeakage.objects.filter(id=fid).first()
	reserve = Reserviour.objects.all()
	f_type = FuelType.objects.all()

	context = {'item': item, 'f_type': f_type, 'reserve':reserve}
	return render(request, 'fuelmaintain/lickage_edit.html', context)


@user_access
def update_fuel_leakage(request):
	if request.method=="POST":
		fid = request.POST.get('fid')
		date = request.POST.get('date')
		quantity = request.POST.get('quantity')
		default_quantity = request.POST.get('default_quantity')
		reserve_id = request.POST.get('reserviour')
		reserve_val = request.POST.get('reserviour_name')
		default_reserve_id = request.POST.get('default_reserve')
		fuel_type = request.POST.get('fuel_type')

		FuelLeakage.objects.filter(id=fid).update(fuel_type=fuel_type, entry_date=date, quantity=quantity, reserviour=reserve_val, reserviour_id=reserve_id)
		messages.info(request, 'done')
		return redirect('/edit-leakage/'+str(fid)+'/')
	else:
		return redirect('leakage_display')


@user_access
def search_fuel_leakage(request):
	if request.method == "POST":
		search = request.POST.get('search')
		sea = search.upper()
		se = search.title()
		s = search.lower()
		u_site = user_site(request)
		u_status = user_role(request)
		if u_status == 'main_admin' or u_status == 'main_staff':
			lookup = Q(leakage_number=search) | Q(user_site__icontains=search) | Q(reserviour__icontains=search) | Q(fuel_type__icontains=search) | Q(leakage_number=sea) | Q(user_site=sea) | Q(reserviour=sea) | Q(fuel_type=sea) | Q(leakage_number=se) | Q(user_site=se) | Q(reserviour=se) | Q(fuel_type=se) | Q(leakage_number=s) | Q(user_site=s) | Q(reserviour=s) | Q(fuel_type=s)
		else:
			lookup = Q(Q(leakage_number=search) | Q(reserviour__icontains=search) | Q(fuel_type__icontains=search) | Q(reserviour=sea) | Q(fuel_type=sea) | Q(reserviour=se) | Q(fuel_type=se) | Q(leakage_number=s) | Q(reserviour=s) | Q(fuel_type=s)) & Q(user_site=u_site)
		s_item = FuelLeakage.objects.filter(lookup).order_by('-id')
		context = {'s_item': s_item, 'search': search}
		return render(request, 'fuelmaintain/display/lickage_search.html', context)
	else:
		return redirect('leakage_display')


@user_access
def delete_fuel_leakage(request):
	if request.method=="POST":
		sid = request.POST.get('sid')

		FuelLeakage.objects.filter(id=sid).delete()
		messages.info(request, 'done')
		return redirect('leakage_display')
	else:
		return redirect('leakage_display')


@user_access
def print_fuelleakage(request):
	if request.method=="POST":
		jid = request.POST.get('jid')
		job = FuelLeakage.objects.filter(id=jid).first()

		context = {'a': job}
		pdf = render_to_pdf('fuelmaintain/printlickage.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			rnum = random.randint(11111111, 99999999)
			filename = "Reportfuelleakage_%s.pdf" %(rnum)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")
	else:
		return redirect('leakage_display')

#==========================================================================================





from django.db import models
from django.utils import timezone

class CompanyLetterhead(models.Model):
	title = models.CharField(max_length=255, default="Corporate Master Letterhead")
	letterhead_image = models.ImageField(upload_to='letterheads/')
	footer_image = models.ImageField(upload_to='letterheads/footers/', blank=True, null=True)
	site = models.CharField(max_length=255, default='All Sites', blank=True, null=True)
	header_height_cm = models.FloatField(default=3.5, help_text="Height reserved for the header banner in cm")
	top_margin_cm = models.FloatField(default=0.6, help_text="Top page margin for report body content in cm")
	bottom_margin_cm = models.FloatField(default=1.0, help_text="Bottom page margin in cm")
	left_margin_cm = models.FloatField(default=1.0, help_text="Left page margin in cm")
	right_margin_cm = models.FloatField(default=1.0, help_text="Right page margin in cm")
	is_active = models.BooleanField(default=True)
	uploaded_by = models.CharField(max_length=255, default='', blank=True, null=True)
	created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

	def __str__(self):
		return f"{self.title} ({'Active' if self.is_active else 'Inactive'})"

class Location(models.Model):
	location_name = models.CharField(max_length=255)
	location_url = models.CharField(max_length=255)
	entry_by = models.CharField(max_length=255, default='')
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)

class Supplier(models.Model):
	name = models.CharField(max_length=255)
	address = models.CharField(max_length=255)
	pan_number = models.CharField(max_length=255)
	landline = models.CharField(max_length=255)
	suppliers_category = models.CharField(max_length=255)
	person_one = models.CharField(max_length=255, blank=True, null=True)
	person_one_mobile = models.CharField(max_length=255, blank=True, null=True)
	person_one_email = models.CharField(max_length=255, blank=True, null=True)
	person_two = models.CharField(max_length=255, blank=True, null=True)
	person_two_mobile = models.CharField(max_length=255, blank=True, null=True)
	person_two_email = models.CharField(max_length=255, blank=True, null=True)
	entry_by = models.CharField(max_length=255, default='', blank=True, null=True)
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	opening = models.CharField(max_length=255, default='0', blank=True, null=True)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)

class CreditPay(models.Model):
	entry_date = models.CharField(max_length=100)
	supplier_id = models.CharField(max_length=255)
	supplier_name = models.CharField(max_length=255)
	supplier_contact = models.CharField(max_length=255)
	supplier_address = models.CharField(max_length=255, default='')
	amount = models.CharField(max_length=255)
	remaining = models.CharField(max_length=255)
	pay_method = models.CharField(max_length=255, blank=True, null=True)
	bank = models.CharField(max_length=255, blank=True, null=True)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)
	entry_by = models.CharField(max_length=255, default='', blank=True, null=True)
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)

class SupplierCategory(models.Model):
	name = models.CharField(max_length=255)
	url = models.CharField(max_length=255)
	entry_by = models.CharField(max_length=255, default='')
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)

class StockCategory(models.Model):
	name = models.CharField(max_length=255)
	url = models.CharField(max_length=255)
	entry_by = models.CharField(max_length=255, default='')
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)

class StockSubCategory(models.Model):
	cat_name = models.CharField(max_length=255)
	cat_url = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	url = models.CharField(max_length=255)
	entry_by = models.CharField(max_length=255, default='')
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)

class UOM(models.Model):
	uom = models.CharField(max_length=255)
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	entry_by = models.CharField(max_length=255, default='')
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)

class Vehicle(models.Model):
	vehicle_number = models.CharField(max_length=255, default='')
	entry_by = models.CharField(max_length=255, default='')

class GoodsEntry(models.Model):
	entry_by = models.CharField(max_length=255)
	grn_number = models.CharField(max_length=255)
	grn_count = models.CharField(max_length=255, default='')
	challan_number = models.CharField(max_length=255)
	purchase_order_number = models.CharField(max_length=255, default='', blank=True, null=True)
	bill_number = models.CharField(max_length=255)
	location = models.CharField(max_length=255, default='', blank=True, null=True)
	supplier_id = models.CharField(max_length=255, default='', blank=True, null=True)
	supplier_name = models.CharField(max_length=255, default='', blank=True, null=True)
	supplier_address = models.CharField(max_length=255, default='', blank=True, null=True)
	supplier_contact = models.CharField(max_length=255, default='', blank=True, null=True)
	vehicle_number = models.CharField(max_length=255, default='', blank=True, null=True)
	entry_date = models.CharField(max_length=100)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	invoice_id = models.CharField(max_length=255, default='')
	invoice_status = models.CharField(max_length=255, default='no')
	narration = models.CharField(max_length=255, default='', blank=True, null=True)
	
	def __str__(self):
		return self.grn_number

class Goods(models.Model):
	goodsid = models.CharField(max_length=255)
	grn = models.CharField(max_length=255, default='')
	pvn = models.CharField(max_length=255, default='')
	item_id = models.CharField(max_length=255, default='')
	item = models.CharField(max_length=255)
	alias = models.CharField(max_length=255, default='', blank=True, null=True)
	uom = models.CharField(max_length=255)
	quantity = models.CharField(max_length=255)
	remark = models.CharField(max_length=255, default='', blank=True, null=True)
	invoice_id = models.CharField(max_length=255, default='')
	invoice_status = models.CharField(max_length=255, default='no')
	
	def __str__(self):
		return self.grn

class GoodsExtra(models.Model):
	grn_number = models.CharField(max_length=255)
	goodsid = models.CharField(max_length=255)
	purchase_order_number = models.CharField(max_length=255, default='')
	voucher_number = models.CharField(max_length=255)
	supplier = models.CharField(max_length=255)

class PurchaseEntry(models.Model):
	entry_by = models.CharField(max_length=255)
	purchase_order_number = models.CharField(max_length=255, default='', blank=True, null=True)
	challan_number = models.CharField(max_length=255)
	voucher_number = models.CharField(max_length=255)
	pvn_count = models.CharField(max_length=255, default='')
	invoice_number = models.CharField(max_length=255)
	invoice_type = models.CharField(max_length=255)
	location = models.CharField(max_length=255, default='', blank=True, null=True)
	supplier_id = models.CharField(max_length=255, default='')
	supplier_name = models.CharField(max_length=255)
	supplier_address = models.CharField(max_length=255)
	supplier_contact = models.CharField(max_length=255)
	vehicle_number = models.CharField(max_length=255, default='', blank=True, null=True)
	entry_date = models.CharField(max_length=100)
	invoice_date = models.CharField(max_length=100)
	sub_total = models.CharField(default='', max_length=255)
	discount_per = models.CharField(default='', max_length=255)
	discount_amt = models.CharField(default='', max_length=255)
	vat = models.CharField(default='', max_length=255)
	total = models.CharField(default='', max_length=255)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	grn_id = models.CharField(max_length=255, default='', blank=True, null=True)
	grn_status = models.CharField(max_length=255, default='no', blank=True, null=True)
	narration = models.CharField(max_length=255, default='', blank=True, null=True)
	day = models.CharField(default='', max_length=255, blank=True, null=True)
	transaction_type = models.CharField(default='', max_length=255, blank=True, null=True)
	issue_use = models.CharField(max_length=255, default='no', blank=True, null=True)
	damage = models.CharField(max_length=255, default='no', blank=True, null=True)
	retur = models.CharField(max_length=255, default='no', blank=True, null=True)
	
	def __str__(self):
		return self.voucher_number

class InvoiceItem(models.Model):
	purchaseid = models.CharField(max_length=255)
	po = models.CharField(max_length=255, default='', blank=True, null=True)
	grn = models.CharField(max_length=255, default='', blank=True, null=True)
	pvn = models.CharField(max_length=255, default='', blank=True, null=True)
	item_id = models.CharField(max_length=255, default='')
	item = models.CharField(max_length=255)
	alias = models.CharField(max_length=255, default='', blank=True, null=True)
	uom = models.CharField(max_length=255)
	quantity = models.CharField(max_length=255)
	orig_quantity = models.CharField(max_length=255, default='', blank=True, null=True)
	useable_quantity = models.CharField(max_length=255, default='', blank=True, null=True)
	rate = models.CharField(max_length=255)
	amount = models.CharField(max_length=255)
	discount_per = models.CharField(max_length=255, default='0', blank=True, null=True)
	discount_amt = models.CharField(max_length=255, default='0', blank=True, null=True)
	issue_use = models.CharField(max_length=255, default='no', blank=True, null=True)
	grn_id = models.CharField(max_length=255, default='', blank=True, null=True)
	grn_status = models.CharField(max_length=255, default='no', blank=True, null=True)
	damage = models.CharField(max_length=255, default='no', blank=True, null=True)
	retur = models.CharField(max_length=255, default='no', blank=True, null=True)
	damage_qty = models.CharField(max_length=255, default='0', blank=True, null=True)
	retur_qty = models.CharField(max_length=255, default='0', blank=True, null=True)
	
	def __str__(self):
		return self.pvn

class StockEntry(models.Model):
	item = models.CharField(max_length=255)
	item_id = models.CharField(max_length=255, default='')
	url = models.CharField(max_length=255, default='')
	alias = models.CharField(max_length=255, default='', blank=True, null=True)
	stock_category = models.CharField(max_length=255)
	stock_subcategory = models.CharField(max_length=255, default='', blank=True, null=True)
	cat_url = models.CharField(max_length=255, default='', blank=True, null=True)
	subcat_url = models.CharField(max_length=255, default='', blank=True, null=True)
	uom = models.CharField(max_length=255)
	opening = models.CharField(max_length=255, default='')
	quantity = models.CharField(max_length=255)
	rate = models.CharField(max_length=255)
	amount = models.CharField(max_length=255)
	stock_type = models.CharField(max_length=255)
	stock_site = models.CharField(max_length=255, default='')
	entry_by = models.CharField(max_length=255, default='')
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)

class StockItem(models.Model):
	item = models.CharField(max_length=255)
	url = models.CharField(max_length=255, default='')
	alias = models.CharField(max_length=255, default='', blank=True, null=True)
	stock_category = models.CharField(max_length=255)
	stock_subcategory = models.CharField(max_length=255, default='', blank=True, null=True)
	cat_url = models.CharField(max_length=255, default='', blank=True, null=True)
	subcat_url = models.CharField(max_length=255, default='', blank=True, null=True)
	main_url = models.CharField(max_length=255, default='', blank=True, null=True)
	uom = models.CharField(max_length=255)
	stock_type = models.CharField(max_length=255)
	entry_by = models.CharField(max_length=255, default='')
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)

class QuotationEntry(models.Model):
	supplier = models.CharField(max_length=255, default='')
	supplier_name = models.CharField(max_length=255)
	supplier_address = models.CharField(max_length=255)
	supplier_contact = models.CharField(max_length=255)
	valid_date = models.CharField(max_length=100)
	entry_date = models.CharField(max_length=100)
	entry_by = models.CharField(max_length=100, default='')
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)

class QuotationItem(models.Model):
	quotationid = models.CharField(max_length=255)
	item_id = models.CharField(max_length=255, default='')
	item = models.CharField(max_length=255)
	uom = models.CharField(max_length=255)
	rate = models.CharField(max_length=255)

class MaterialIssueEntry(models.Model):
	issuing_location = models.CharField(max_length=100)
	mie_number = models.CharField(max_length=255, default='')
	mie_count = models.CharField(max_length=255, default='')
	purchase_order_number = models.CharField(max_length=100, default='', blank=True, null=True)
	receiving_location = models.CharField(max_length=100, default='', blank=True, null=True)
	vehicle_number = models.CharField(max_length=100, default='', blank=True, null=True)
	issue_for = models.CharField(max_length=100, default='', blank=True, null=True)
	issue_date = models.CharField(max_length=100)
	entry_by = models.CharField(max_length=255, default='')
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)
	narration = models.CharField(max_length=255, default='', blank=True, null=True)
	
	def __str__(self):
		return self.mie_number

class MaterialItem(models.Model):
	materialid = models.CharField(max_length=255)
	po = models.CharField(max_length=255, default='', blank=True, null=True)
	pvn = models.CharField(max_length=255, default='', blank=True, null=True)
	item_id = models.CharField(max_length=255, default='')
	item = models.CharField(max_length=255)
	alias = models.CharField(max_length=255, default='', blank=True, null=True)
	uom = models.CharField(max_length=255)
	quantity = models.CharField(max_length=255)
	
	def __str__(self):
		return self.pvn

class InternalTransfer(models.Model):
	issuing_location = models.CharField(max_length=100)
	itn_number = models.CharField(max_length=255, default='')
	itn_count = models.CharField(max_length=255, default='')
	receiving_location = models.CharField(max_length=100)
	issue_date = models.CharField(max_length=100)
	entry_by = models.CharField(max_length=255, default='')
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)
	narration = models.CharField(max_length=255, default='', blank=True, null=True)
	grn_id = models.CharField(max_length=255, default='', blank=True, null=True)
	grn_status = models.CharField(max_length=255, default='no', blank=True, null=True)
	
	def __str__(self):
		return self.itn_number

class TransferItem(models.Model):
	transferid = models.CharField(max_length=255)
	pvn = models.CharField(max_length=255, default='')
	item_id = models.CharField(max_length=255, default='')
	item = models.CharField(max_length=255)
	alias = models.CharField(max_length=255, default='', blank=True, null=True)
	uom = models.CharField(max_length=255)
	quantity = models.CharField(max_length=255)
	grn_id = models.CharField(max_length=255, default='', blank=True, null=True)
	grn_status = models.CharField(max_length=255, default='no', blank=True, null=True)
	
	def __str__(self):
		return self.pvn

class InternalGrn(models.Model):
	entry_by = models.CharField(max_length=255)
	grn_number = models.CharField(max_length=255)
	grn_count = models.CharField(max_length=255, default='')
	vehicle_number = models.CharField(max_length=255, default='', blank=True, null=True)
	entry_date = models.CharField(max_length=100)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	invoice_id = models.CharField(max_length=255, default='', blank=True, null=True)
	invoice_status = models.CharField(max_length=255, default='no')
	narration = models.CharField(max_length=255, default='', blank=True, null=True)
	damage = models.CharField(max_length=255, default='no', blank=True, null=True)
	
	def __str__(self):
		return self.grn_number

class InternalGrnItems(models.Model):
	goodsid = models.CharField(max_length=255)
	grn = models.CharField(max_length=255, default='')
	pvn = models.CharField(max_length=255, default='')
	item_id = models.CharField(max_length=255, default='')
	item = models.CharField(max_length=255)
	alias = models.CharField(max_length=255, default='', blank=True, null=True)
	uom = models.CharField(max_length=255)
	quantity = models.CharField(max_length=255)
	remark = models.CharField(max_length=255, default='', blank=True, null=True)
	orig_quantity = models.CharField(max_length=255, default='', blank=True, null=True)
	damage_qty = models.CharField(max_length=255, default='0', blank=True, null=True)
	damage = models.CharField(max_length=255, default='no', blank=True, null=True)
	invoice_id = models.CharField(max_length=255, default='', blank=True, null=True)
	invoice_status = models.CharField(max_length=255, default='no')
	
	def __str__(self):
		return self.grn

class OutSaleEntry(models.Model):
	issuing_location = models.CharField(max_length=100)
	sales_id = models.CharField(max_length=100)
	sid_count = models.CharField(max_length=100, default='')
	buyer = models.CharField(max_length=100)
	sub_total = models.CharField(default='', max_length=255)
	invoice_type = models.CharField(default='', max_length=255)
	discount_per = models.CharField(default='', max_length=255)
	discount_amt = models.CharField(default='', max_length=255)
	vat = models.CharField(default='', max_length=255)
	total = models.CharField(default='', max_length=255)
	sales_date = models.CharField(max_length=100)
	entry_by = models.CharField(default='', max_length=255)
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)

class SalesItem(models.Model):
	saleid = models.CharField(max_length=255)
	item_id = models.CharField(default='', max_length=255)
	item = models.CharField(max_length=255)
	uom = models.CharField(max_length=255)
	quantity = models.CharField(max_length=255)
	rate = models.CharField(max_length=255)
	amount = models.CharField(max_length=255)

class BudgetEstimateEntry(models.Model):
	location = models.CharField(max_length=100)
	stock_item = models.CharField(max_length=100)
	item_id = models.CharField(default='', max_length=255)
	quantity = models.CharField(max_length=255)
	rate = models.CharField(max_length=255)
	amount = models.CharField(max_length=255)
	entry_by = models.CharField(default='', max_length=255)
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)

class Site(models.Model):
	name = models.CharField(max_length=255)
	url = models.CharField(max_length=255)
	address = models.CharField(max_length=255)
	pan_number = models.CharField(max_length=255)
	contact = models.CharField(max_length=255)
	entry_by = models.CharField(max_length=255, default='')
	user_site = models.CharField(max_length=255, default='')
	role = models.CharField(max_length=255, default='staff')
	active_status = models.CharField(max_length=255, default='yes', blank=True, null=True)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)

class PurchaseOrder(models.Model):
	entry_by = models.CharField(max_length=255)
	purchase_number = models.CharField(max_length=255)
	pon_count = models.CharField(max_length=255, default='')
	issuing_site = models.CharField(max_length=255)
	entry_date = models.CharField(max_length=100)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	invoice_id = models.CharField(max_length=255, default='', blank=True, null=True)
	invoice_status = models.CharField(max_length=255, default='no')
	grn_id = models.CharField(max_length=255, default='', blank=True, null=True)
	grn_status = models.CharField(max_length=255, default='no')
	status = models.CharField(max_length=255, default='pending')
	approved_by = models.CharField(max_length=255, default='', blank=True, null=True)
	cancelled_by = models.CharField(max_length=255, default='', blank=True, null= True)
	vehicle_type = models.CharField(max_length=255, default='', blank=True, null=True)
	vehicle_type_id = models.CharField(max_length=255, default='', blank=True, null=True)
	vehicle_number = models.CharField(max_length=255, default='', blank=True, null= True)
	number_type = models.CharField(max_length=255, default='', blank=True, null=True)
	po_vehi = models.CharField(max_length=255, default='', blank=True, null=True)
	narration = models.CharField(max_length=255, default='', blank=True, null=True)
	issue_use = models.CharField(max_length=255, default='no', blank=True, null=True)
	
	def __str__(self):
		return self.purchase_number

class PurchaseItem(models.Model):
	purchase_order_id = models.CharField(max_length=255)
	pon = models.CharField(max_length=255, default='')
	item_id = models.CharField(max_length=255, default='')
	item = models.CharField(max_length=255)
	alias = models.CharField(max_length=255, default='', blank=True, null=True)
	uom = models.CharField(max_length=255)
	quantity = models.CharField(max_length=255)
	status = models.CharField(max_length=255, default='no')
	description = models.CharField(max_length=255, default='', blank=True, null=True)
	purchase_location = models.CharField(max_length=255, default='', blank=True, null=True)
	issue_use = models.CharField(max_length=255, default='no', blank=True, null=True)
	damage = models.CharField(max_length=255, default='no', blank=True, null=True)
	retur = models.CharField(max_length=255, default='no', blank=True, null=True)
	damage_qty = models.CharField(max_length=255, default='0', blank=True, null=True)
	retur_qty = models.CharField(max_length=255, default='0', blank=True, null=True)
	
	def __str__(self):
		return self.pon

class Notification(models.Model):
	notify_topic = models.CharField(max_length=255, default='', blank=True, null=True)
	content_id = models.CharField(max_length=255, default='', blank=True, null=True)
	content = models.CharField(max_length=255, default='', blank=True, null=True)
	from_site = models.CharField(max_length=255, default='', blank=True, null=True)
	from_user = models.CharField(max_length=255, default='', blank=True, null=True)
	content_val = models.CharField(max_length=255, default='', blank=True, null=True)
	content_val1 = models.CharField(max_length=255, default='', blank=True, null=True)
	content_val2 = models.CharField(max_length=255, default='', blank=True, null=True)
	content_val3 = models.CharField(max_length=255, default='', blank=True, null=True)
	entry_date = models.CharField(max_length=255, default='', blank=True, null=True)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date_on = models.DateField(default=timezone.localdate, blank=True, null=True)
	status = models.CharField(max_length=255, default='pending')
	user_type = models.CharField(max_length=255, default='', blank=True, null=True)

class MaintainanceBill(models.Model):
	maintain_number = models.CharField(max_length=255)
	purchase_order_number = models.CharField(max_length=255, blank=True, null=True)
	vehicle_number = models.CharField(default='', max_length=255)
	vehicle_type = models.CharField(max_length=255, default='')
	vehicle_type_id = models.CharField(default='', max_length=255, blank=True, null=True)
	number_type = models.CharField(default='', max_length=255, blank=True, null=True)
	driver = models.CharField(default='', max_length=255, blank=True, null=True)
	driver_id = models.IntegerField(default=0, blank=True, null=True)
	kilometer = models.CharField(default='', max_length=255)
	problem_category = models.CharField(default='', max_length=255, blank=True, null=True)
	problem_subcategory = models.CharField(default='', max_length=255, blank=True, null=True)
	supplier_id = models.CharField(max_length=255, default='', blank=True, null=True)
	supplier_name = models.CharField(max_length=255, default='', blank=True, null=True)
	supplier_address = models.CharField(max_length=255, default='', blank=True, null=True)
	supplier_contact = models.CharField(max_length=255, default='', blank=True, null=True)
	narration = models.CharField(default='', max_length=255, blank=True, null=True)
	replaced_part = models.CharField(default='', max_length=255, blank=True, null=True)
	estimated_cost = models.CharField(default='', max_length=255, blank=True, null=True)
	entry_date = models.CharField(max_length=255)
	hour = models.CharField(default='', max_length=255, blank=True, null=True)
	day = models.CharField(default='', max_length=255, blank=True, null=True)
	transaction_type = models.CharField(default='', max_length=255, blank=True, null=True)
	purchase_entry_date = models.CharField(max_length=255, blank=True, null=True)
	bill_date = models.CharField(max_length=255)
	bill_number = models.CharField(default='', max_length=255, blank=True, null=True)
	bill_type = models.CharField(max_length=255, default='', blank=True, null=True)
	purchase_status = models.CharField(max_length=255, default='', blank=True, null=True)
	purchase_approve_by = models.CharField(max_length=255, default='', blank=True, null=True)
	sub_total = models.CharField(default='', max_length=255)
	discount_per = models.CharField(default='', max_length=255, blank=True, null=True)
	discount_amt = models.CharField(default='', max_length=255, blank=True, null=True)
	labour_charge = models.CharField(default='', max_length=255)
	vat = models.CharField(default='', max_length=255, blank=True, null=True)
	total = models.CharField(default='', max_length=255)
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	entry_by = models.CharField(max_length=255, default='', blank=True, null=True)
	pei = models.IntegerField(default=0)
	jorder = models.CharField(max_length=255, default='', blank=True, null=True)
	gjorder = models.CharField(max_length=255, default='', blank=True, null=True)
	
	def __str__(self):
		return self.maintain_number

class MaintainanceItem(models.Model):
	bill_id = models.CharField(max_length=255)
	pvn = models.CharField(default='', max_length=255, blank=True, null=True)
	purchase_id = models.CharField(default='', max_length=255, blank=True, null=True)
	item_id = models.CharField(default='', max_length=255)
	item_name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255, default='', blank=True, null=True)
	uom = models.CharField(max_length=255, default='')
	quantity = models.CharField(max_length=255)
	rate = models.CharField(max_length=255)
	amount = models.CharField(max_length=255)
	discount_per = models.CharField(max_length=255, blank=True, null=True)
	discount_amt = models.CharField(max_length=255, blank=True, null=True)
	itnn = models.CharField(max_length=255, default='', blank=True, null=True)
	
	def __str__(self):
		return self.pvn

class MaintainInvoice(models.Model):
	maintainid = models.CharField(max_length=255, default='', blank=True, null=True)
	maintain_number = models.CharField(max_length=255, default='', blank=True, null=True)
	purchase_order_number = models.CharField(max_length=255, default='', blank=True, null=True)
	voucher_number = models.CharField(max_length=255, default='', blank=True, null=True)
	invoice_number = models.CharField(max_length=255, default='', blank=True, null=True)
	invoice_type = models.CharField(max_length=255, default='', blank=True, null=True)
	supplier = models.CharField(max_length=255, default='', blank=True, null=True)
	sub_total = models.CharField(max_length=255, default='', blank=True, null=True)
	discount_per = models.CharField(max_length=255, default='', blank=True, null=True)
	discount_amt = models.CharField(max_length=255, default='', blank=True, null=True)
	vat = models.CharField(max_length=255, default='', blank=True, null=True)
	total = models.CharField(max_length=255, default='', blank=True, null=True)
	
	def __str__(self):
		return self.maintain_number

class ProblemCategory(models.Model):
	name = models.CharField(max_length=255)
	problem_url = models.CharField(max_length=255)

class ProblemSubCategory(models.Model):
	name = models.CharField(max_length=255)
	problem_suburl = models.CharField(max_length=255)
	problem_url = models.CharField(max_length=255)
	problem_name = models.CharField(max_length=255)

class Fuel(models.Model):
	date = models.CharField(max_length=255)
	coupon_number = models.CharField(max_length=255)
	consump_number = models.CharField(default='', max_length=255)
	fcn = models.IntegerField(default=0)
	vehicle_number = models.CharField(default='', max_length=255)
	vehicle_type = models.CharField(default='', max_length=255)
	vehicle_type_id = models.CharField(default='', max_length=255, blank=True, null=True)
	number_type = models.CharField(default='', max_length=255, blank=True, null=True)
	fuel_type = models.CharField(default='', max_length=255)
	kilometer = models.CharField(max_length=255)
	quantity = models.CharField(max_length=255)
	user_site = models.CharField(max_length=255, default='')
	reserviour = models.CharField(max_length=255, default='')
	reserviour_id = models.CharField(max_length=255, default='')
	location = models.CharField(max_length=255, default='', blank=True, null=True)
	entry_datetime_on = models.DateTimeField(default=timezone.now, blank=True)
	entry_date_on = models.DateField(default=timezone.localdate, blank=True)
	entry_by = models.CharField(max_length=255, default='', blank=True, null=True)

class Reserviour(models.Model):
	name = models.CharField(max_length=255)
	url = models.CharField(max_length=255, default='')
	site = models.CharField(max_length=255, blank=True, null=True)
	location = models.CharField(max_length=255, blank=True, null=True)
	capacity = models.CharField(max_length=255)
	opening = models.CharField(max_length=255, default='')
	stock = models.CharField(max_length=255, default='')
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	entry_by = models.CharField(max_length=255, default='', blank=True, null=True)

class FuelPurchase(models.Model):
	issuing_site = models.CharField(max_length=255)
	purchase_number = models.CharField(max_length=255, default='')
	reserviour = models.CharField(max_length=255, default='')
	quantity = models.CharField(max_length=255, blank=True, null=True)
	rate = models.CharField(max_length=255, blank=True, null=True)
	amount = models.CharField(max_length=255, blank=True, null=True)
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	entry_by = models.CharField(max_length=255, default='', blank=True, null=True)
	entry_date = models.CharField(max_length=255, default='')
	status = models.CharField(max_length=255, default='pending')
	approved_by = models.CharField(max_length=255, default='', blank=True, null=True)
	cancelled_by = models.CharField(max_length=255, default='', blank=True, null=True)
	pon = models.IntegerField(default=0)
	grand_stock = models.CharField(max_length=255, default='', blank=True, null=True)
	fuel_type = models.CharField(default='', max_length=255)
	location = models.CharField(default='', max_length=255, blank=True, null=True)
	purchase_location = models.CharField(default='', max_length=255, blank=True, null=True)
	approved_datetime_on = models.DateTimeField(default=timezone.now, blank=True, null=True)
	approved_date_on = models.DateField(default=timezone.localdate, blank=True, null=True)
	narration = models.CharField(default='', max_length=255, blank=True, null=True)
	
	def __str__(self):
		return self.purchase_number

class FuelBill(models.Model):
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	issuing_site = models.CharField(max_length=255, default='', blank=True, null=True)
	entry_by = models.CharField(max_length=255, default='', blank=True, null=True)
	purchase_bill_number = models.CharField(max_length=255, default='')
	purchase_order_number = models.CharField(max_length=255, default='')
	invoice_number = models.CharField(max_length=255, default='', blank=True, null=True)
	reserviour = models.CharField(max_length=255, default='')
	quantity = models.CharField(max_length=255, blank=True, null=True)
	rate = models.CharField(max_length=255, blank=True, null=True)
	vat = models.CharField(max_length=255, blank=True, null=True)
	amount = models.CharField(max_length=255, blank=True, null=True)
	entry_date = models.CharField(max_length=255, default='')
	po_entry_date = models.CharField(max_length=255, default='')
	po_status = models.CharField(max_length=255, default='pending')
	po_approved_by = models.CharField(max_length=255, default='', blank=True, null=True)
	pbn = models.IntegerField(default=0)
	grand_stock = models.CharField(max_length=255, default='')
	fuel_type = models.CharField(default='', max_length=255)
	supplier_id = models.CharField(max_length=255, default='')
	supplier_name = models.CharField(max_length=255, default='', blank=True, null=True)
	supplier_address = models.CharField(max_length=255, default='', blank=True, null=True)
	supplier_contact = models.CharField(max_length=255, default='', blank=True, null=True)
	transaction_type = models.CharField(default='', max_length=255, blank=True, null=True)
	day = models.CharField(default='', max_length=255, blank=True, null=True)
	location = models.CharField(default='', max_length=255, blank=True, null=True)
	purchase_location = models.CharField(default='', max_length=255, blank=True, null=True)
	approved_datetime_on = models.DateTimeField(default=timezone.now, blank=True, null=True)
	approved_date_on = models.DateField(default=timezone.localdate, blank=True, null=True)
	narration = models.CharField(default='', max_length=255, blank=True, null=True)
	
	def __str__(self):
		return self.purchase_bill_number

class VehicleType(models.Model):
	type_name = models.CharField(max_length=255)
	url = models.CharField(max_length=255)

class FuelType(models.Model):
	name = models.CharField(max_length=255)
	url = models.CharField(max_length=255)

class VehicleList(models.Model):
	owner_name = models.CharField(max_length=255, default='', blank=True, null=True)
	vehicle_number = models.CharField(max_length=255, blank=True, null=True)
	url = models.CharField(max_length=255, default='', blank=True, null=True)
	chasis_url = models.CharField(max_length=255, default='', blank=True, null=True)
	engine_url = models.CharField(max_length=255, default='', blank=True, null=True)
	chasis_number = models.CharField(max_length=255, blank=True, null=True)
	engine_number = models.CharField(max_length=255, blank=True, null=True)
	vehicle_type_id = models.CharField(max_length=255, blank=True, null=True)
	vehicle_type = models.CharField(max_length=255, blank=True, null=True)
	driver_name = models.CharField(max_length=255, default='', blank=True, null=True)
	helper_name = models.CharField(max_length=255, default='', blank=True, null=True)
	contact1 = models.CharField(max_length=255, default='', blank=True, null=True)
	contact2 = models.CharField(max_length=255, default='', blank=True, null=True)
	capacity = models.CharField(max_length=255, default='', blank=True, null=True)
	current = models.CharField(max_length=255, default='Chitwan', blank=True, null=True)
	active_status = models.CharField(max_length=255, default='yes', blank=True, null=True)

class DamageEntry(models.Model):
	entry_by = models.CharField(max_length=255)
	purchase_order_number = models.CharField(max_length=255, default='', blank=True, null=True)
	damage_number = models.CharField(max_length=255)
	pvn_count = models.CharField(max_length=255, default='')
	entry_date = models.CharField(max_length=100)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	pvn_id = models.CharField(max_length=255, default='', blank=True, null=True)
	pvn_status = models.CharField(max_length=255, default='no', blank=True, null=True)
	narration = models.CharField(max_length=255, default='', blank=True, null=True)
	issue_use = models.CharField(max_length=255, default='no', blank=True, null=True)
	
	def __str__(self):
		return self.damage_number

class DamageItem(models.Model):
	damageid = models.CharField(max_length=255)
	po = models.CharField(max_length=255, default='', blank=True, null=True)
	dn = models.CharField(max_length=255, default='', blank=True, null=True)
	pvn = models.CharField(max_length=255, default='', blank=True, null=True)
	item_id = models.CharField(max_length=255, default='')
	item = models.CharField(max_length=255)
	alias = models.CharField(max_length=255, default='', blank=True, null=True)
	uom = models.CharField(max_length=255)
	quantity = models.CharField(max_length=255)
	issue_use = models.CharField(max_length=255, default='no', blank=True, null=True)
	pvn_id = models.CharField(max_length=255, default='', blank=True, null=True)
	pvn_status = models.CharField(max_length=255, default='no', blank=True, null=True)
	
	def __str__(self):
		return self.dn

class DamageInvoice(models.Model):
	damageid = models.CharField(max_length=255, default='', blank=True, null=True)
	damage_number = models.CharField(max_length=255, default='', blank=True, null=True)
	purchase_order_number = models.CharField(max_length=255, default='', blank=True, null=True)
	voucher_number = models.CharField(max_length=255, default='', blank=True, null=True)
	invoice_number = models.CharField(max_length=255, default='', blank=True, null=True)
	invoice_type = models.CharField(max_length=255, default='', blank=True, null=True)
	supplier = models.CharField(max_length=255, default='', blank=True, null=True)
	sub_total = models.CharField(max_length=255, default='', blank=True, null=True)
	discount_per = models.CharField(max_length=255, default='', blank=True, null=True)
	discount_amt = models.CharField(max_length=255, default='', blank=True, null=True)
	vat = models.CharField(max_length=255, default='', blank=True, null=True)
	total = models.CharField(max_length=255, default='', blank=True, null=True)

class ReturnEntry(models.Model):
	entry_by = models.CharField(max_length=255)
	purchase_order_number = models.CharField(max_length=255, default='', blank=True, null=True)
	damage_number = models.CharField(max_length=255)
	pvn_count = models.CharField(max_length=255, default='')
	entry_date = models.CharField(max_length=100)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	pvn_id = models.CharField(max_length=255, default='', blank=True, null=True)
	pvn_status = models.CharField(max_length=255, default='no', blank=True, null=True)
	narration = models.CharField(max_length=255, default='', blank=True, null=True)
	issue_use = models.CharField(max_length=255, default='no', blank=True, null=True)
	
	def __str__(self):
		return self.damage_number

class ReturnItem(models.Model):
	damageid = models.CharField(max_length=255)
	po = models.CharField(max_length=255, default='', blank=True, null=True)
	dn = models.CharField(max_length=255, default='', blank=True, null=True)
	pvn = models.CharField(max_length=255, default='', blank=True, null=True)
	item_id = models.CharField(max_length=255, default='')
	item = models.CharField(max_length=255)
	alias = models.CharField(max_length=255, default='', blank=True, null=True)
	uom = models.CharField(max_length=255)
	quantity = models.CharField(max_length=255)
	rate = models.CharField(max_length=255, default='', blank=True, null=True)
	discount_per = models.CharField(max_length=255, default='', blank=True, null=True)
	discount_amt = models.CharField(max_length=255, default='', blank=True, null=True)
	amount = models.CharField(max_length=255, default='', blank=True, null=True)
	issue_use = models.CharField(max_length=255, default='no', blank=True, null=True)
	pvn_id = models.CharField(max_length=255, default='', blank=True, null=True)
	pvn_status = models.CharField(max_length=255, default='no', blank=True, null=True)
	
	def __str__(self):
		return self.dn

class ReturnInvoice(models.Model):
	damageid = models.CharField(max_length=255, default='', blank=True, null=True)
	damage_number = models.CharField(max_length=255, default='', blank=True, null=True)
	purchase_order_number = models.CharField(max_length=255, default='', blank=True, null=True)
	voucher_number = models.CharField(max_length=255, default='', blank=True, null=True)
	invoice_number = models.CharField(max_length=255, default='', blank=True, null=True)
	invoice_type = models.CharField(max_length=255, default='', blank=True, null=True)
	supplier = models.CharField(max_length=255, default='', blank=True, null=True)
	sub_total = models.CharField(max_length=255, default='', blank=True, null=True)
	discount_per = models.CharField(max_length=255, default='', blank=True, null=True)
	discount_amt = models.CharField(max_length=255, default='', blank=True, null=True)
	vat = models.CharField(max_length=255, default='', blank=True, null=True)
	total = models.CharField(max_length=255, default='', blank=True, null=True)

class VehicleTrack(models.Model):
	move_number = models.CharField(max_length=255, default='', blank=True, null=True)
	move_count = models.CharField(max_length=255, default='', blank=True, null=True)
	entry_date = models.CharField(max_length=255, default='', blank=True, null=True)
	vehicle_number = models.CharField(max_length=255, blank=True, null=True)
	from_site = models.CharField(max_length=255, default='', blank=True, null=True)
	to_site = models.CharField(max_length=255, default='', blank=True, null=True)
	vehicle_type_id = models.CharField(max_length=255, default='', blank=True, null=True)
	vehicle_type = models.CharField(max_length=255, blank=True, null=True)
	num_type = models.CharField(max_length=255, default='', blank=True, null=True)
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	entry_by = models.CharField(max_length=255, default='', blank=True, null=True)
	status = models.CharField(max_length=255, default='travelling', blank=True, null=True)
	arrival_datetime = models.CharField(max_length=255, default='', blank=True, null=True)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)

class FuelInternalTransfer(models.Model):
	fuel_number = models.CharField(max_length=255)
	from_reserviour = models.CharField(max_length=255)
	to_reserviour = models.CharField(max_length=255)
	quantity = models.CharField(max_length=255, blank=True, null=True)
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	entry_by = models.CharField(max_length=255, default='', blank=True, null=True)
	entry_date = models.CharField(max_length=255)
	status = models.CharField(max_length=255, default='', blank=True, null=True)
	pon = models.IntegerField(default=0)
	fuel_type = models.CharField(default='', max_length=255)
	narration = models.CharField(default='', max_length=255, blank=True, null=True)
	
	def __str__(self):
		return self.fuel_number

class InternalDamageEntry(models.Model):
	entry_by = models.CharField(max_length=255)
	damage_number = models.CharField(max_length=255)
	pvn_count = models.CharField(max_length=255, default='')
	entry_date = models.CharField(max_length=100)
	datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
	date = models.DateField(default=timezone.localdate, blank=True, null=True)
	user_site = models.CharField(max_length=255, default='', blank=True, null=True)
	pvn_id = models.CharField(max_length=255, default='', blank=True, null=True)
	pvn_status = models.CharField(max_length=255, default='no', blank=True, null=True)
	narration = models.CharField(max_length=255, default='', blank=True, null=True)
	issue_use = models.CharField(max_length=255, default='no', blank=True, null=True)
	
	def __str__(self):
		return self.damage_number

class InternalDamageItem(models.Model):
	damageid = models.CharField(max_length=255)
	dn = models.CharField(max_length=255, default='', blank=True, null=True)
	pvn = models.CharField(max_length=255, default='', blank=True, null=True)
	item_id = models.CharField(max_length=255, default='')
	item = models.CharField(max_length=255)
	alias = models.CharField(max_length=255, default='', blank=True, null=True)
	uom = models.CharField(max_length=255)
	quantity = models.CharField(max_length=255)
	issue_use = models.CharField(max_length=255, default='no', blank=True, null=True)
	pvn_id = models.CharField(max_length=255, default='', blank=True, null=True)
	pvn_status = models.CharField(max_length=255, default='no', blank=True, null=True)
	
	def __str__(self):
		return self.dn

class FuelLeakage(models.Model):
	entry_date = models.CharField(max_length=255)
	leakage_number = models.CharField(default='', max_length=255)
	fcn = models.IntegerField(default=0)
	fuel_type = models.CharField(default='', max_length=255)
	quantity = models.CharField(max_length=255)
	user_site = models.CharField(max_length=255, default='')
	reserviour = models.CharField(max_length=255, default='')
	reserviour_id = models.CharField(max_length=255, default='')
	entry_datetime_on = models.DateTimeField(default=timezone.now, blank=True)
	entry_date_on = models.DateField(default=timezone.localdate, blank=True)
	entry_by = models.CharField(max_length=255, default='', blank=True, null=True)
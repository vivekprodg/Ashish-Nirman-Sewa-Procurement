from django.contrib import admin
from django.utils.html import format_html
from .models import *


class CompanyLetterheadAdmin(admin.ModelAdmin):
	list_display = ('title', 'site', 'is_active', 'header_height_cm', 'top_margin_cm', 'uploaded_by', 'created_at', 'letterhead_preview')
	list_filter = ('is_active', 'site')
	search_fields = ('title', 'site', 'uploaded_by')

	def letterhead_preview(self, obj):
		if obj.letterhead_image:
			return format_html('<img src="{}" style="max-height: 40px; border-radius: 4px; border: 1px solid #ccc;" />', obj.letterhead_image.url)
		return "No Image"
	letterhead_preview.short_description = "Preview"

	def has_module_permission(self, request):
		return request.user.is_superuser

	def has_view_permission(self, request, obj=None):
		return request.user.is_superuser

	def has_add_permission(self, request):
		return request.user.is_superuser

	def has_change_permission(self, request, obj=None):
		return request.user.is_superuser

	def has_delete_permission(self, request, obj=None):
		return request.user.is_superuser


admin.site.register(CompanyLetterhead, CompanyLetterheadAdmin)
admin.site.register(Location)
admin.site.register(Supplier)
admin.site.register(Vehicle)
admin.site.register(GoodsEntry)
admin.site.register(Goods)
admin.site.register(PurchaseEntry)
admin.site.register(InvoiceItem)
admin.site.register(StockEntry)
admin.site.register(QuotationEntry)
admin.site.register(QuotationItem)
admin.site.register(MaterialIssueEntry)
admin.site.register(MaterialItem)
admin.site.register(InternalTransfer)
admin.site.register(TransferItem)
admin.site.register(InternalGrn)
admin.site.register(InternalGrnItems)
admin.site.register(OutSaleEntry)
admin.site.register(SalesItem)
admin.site.register(BudgetEstimateEntry)
admin.site.register(SupplierCategory)
admin.site.register(UOM)
admin.site.register(StockCategory)
admin.site.register(StockSubCategory)
admin.site.register(Site)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseItem)
admin.site.register(Notification)
admin.site.register(StockItem)
admin.site.register(MaintainInvoice)
admin.site.register(MaintainanceBill)
admin.site.register(MaintainanceItem)
admin.site.register(ProblemCategory)
admin.site.register(ProblemSubCategory)
admin.site.register(Fuel)
admin.site.register(Reserviour)
admin.site.register(FuelPurchase)
admin.site.register(FuelBill)
admin.site.register(VehicleType)
admin.site.register(FuelType)
admin.site.register(VehicleList)
admin.site.register(GoodsExtra)
admin.site.register(CreditPay)
admin.site.register(DamageEntry)
admin.site.register(DamageItem)
admin.site.register(DamageInvoice)
admin.site.register(ReturnEntry)
admin.site.register(ReturnItem)
admin.site.register(ReturnInvoice)
admin.site.register(VehicleTrack)
admin.site.register(FuelInternalTransfer)
admin.site.register(InternalDamageEntry)
admin.site.register(InternalDamageItem)
admin.site.register(FuelLeakage)
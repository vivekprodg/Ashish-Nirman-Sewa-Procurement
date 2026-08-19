import datetime
from datetime import date
from django.shortcuts import render, redirect
from django.db.models import Sum, Q, Count
from django.contrib.auth.decorators import user_passes_test

from eproc.models import (
    PurchaseOrder, PurchaseEntry, GoodsEntry, StockEntry, 
    MaterialIssueEntry, InternalTransfer, MaintainanceBill, 
    Fuel, Reserviour, FuelBill, FuelPurchase, VehicleList, 
    VehicleTrack, Supplier, CreditPay, Notification, Site
)
from account.models import UserDetail
from account.views import check_staff

def user_site(request):
    """Retrieves the assigned site name for the logged-in user."""
    current_user = request.user.id
    use = UserDetail.objects.filter(user_id=current_user).first()
    if use:
        return use.site
    return ''

def user_role(request):
    """Retrieves the user's role status (main_admin, main_staff, site_admin, site_staff)."""
    current_user = request.user.id
    use = UserDetail.objects.filter(user_id=current_user).first()
    if use:
        return use.status
    return ''

@user_passes_test(check_staff, login_url='login_user')
def home(request):
    tod = date.today()
    u_site = user_site(request)
    u_status = user_role(request)

    # -------------------------------------------------------------
    # 1. Background Reconciliation & Automated Alert Generation
    # -------------------------------------------------------------
    # Alert for Purchase Invoices with missing GRN for > 14 days
    if PurchaseEntry.objects.filter(grn_status='no').exists():
        pe = PurchaseEntry.objects.filter(grn_status='no')
        for p in pe:
            pid = p.id
            pvn = p.voucher_number
            po = p.purchase_order_number
            edate = p.date
            if edate:
                dtt = tod - edate
                if dtt.days > 14:
                    notify_topic = 'grn_notify'
                    content_id = pid
                    content = 'gnoti_add'
                    content_val = pvn
                    content_val1 = po
                    if not Notification.objects.filter(content='gnoti_add', content_val=pvn).exists():
                        q = Notification(
                            notify_topic=notify_topic, 
                            content_id=content_id, 
                            content=content, 
                            content_val=content_val, 
                            content_val1=content_val1,
                            from_site=p.user_site or u_site,
                            from_user=p.entry_by or 'System'
                        )
                        q.save()

    # Alert for Credit Purchases nearing maturity (within 5 days of due date)
    if PurchaseEntry.objects.filter(transaction_type='credit').exists():
        pe = PurchaseEntry.objects.filter(transaction_type='credit')
        for p in pe:
            pid = p.id
            pvn = p.voucher_number
            po = p.purchase_order_number
            cre = p.day
            edate = p.date
            if edate and cre:
                try:
                    dtt = tod - edate
                    dy = int(cre) - 5
                    if dtt.days >= dy:
                        notify_topic = 'credit_notify'
                        content_id = pid
                        content = 'crnoti_add'
                        content_val = pvn
                        content_val1 = po
                        if not Notification.objects.filter(content='crnoti_add', content_val=pvn).exists():
                            q = Notification(
                                notify_topic=notify_topic, 
                                content_id=content_id, 
                                content=content, 
                                content_val=content_val, 
                                content_val1=content_val1,
                                from_site=p.user_site or u_site,
                                from_user=p.entry_by or 'System'
                            )
                            q.save()
                except (ValueError, TypeError):
                    pass

    # -------------------------------------------------------------
    # 2. Executive Metrics & Summary Calculations
    # -------------------------------------------------------------
    total_sites = Site.objects.filter(active_status='yes').count()
    total_suppliers = Supplier.objects.count()

    # Purchase Orders Scope
    if u_status in ['main_admin', 'main_staff']:
        pending_pos = PurchaseOrder.objects.filter(status='pending').count()
        approved_pos = PurchaseOrder.objects.filter(status='approved').count()
        recent_pos = PurchaseOrder.objects.all().order_by('-id')[:5]
        recent_invoices = PurchaseEntry.objects.all().order_by('-id')[:5]
    else:
        pending_pos = PurchaseOrder.objects.filter(status='pending', issuing_site=u_site).count()
        approved_pos = PurchaseOrder.objects.filter(status='approved', issuing_site=u_site).count()
        recent_pos = PurchaseOrder.objects.filter(issuing_site=u_site).order_by('-id')[:5]
        recent_invoices = PurchaseEntry.objects.filter(user_site=u_site).order_by('-id')[:5]

    # Total Procurement Expenditure (Total Billed Invoices)
    all_invoices = PurchaseEntry.objects.all()
    total_invoice_sum = 0.0
    for inv in all_invoices:
        try:
            total_invoice_sum += float(inv.total or 0)
        except (ValueError, TypeError):
            pass

    # Total Outstanding Credit Payables (Opening + Invoices + Fuel Bills - Payments)
    total_credit_due = 0.0
    for sup in Supplier.objects.all():
        opening = float(sup.opening or 0)
        sup_credit_invoices = PurchaseEntry.objects.filter(supplier_id=sup.id, transaction_type='credit')
        inv_sum = sum(float(x.total or 0) for x in sup_credit_invoices)
        fuel_credit = FuelBill.objects.filter(supplier_id=sup.id, transaction_type='credit')
        fuel_sum = sum(float(x.amount or 0) for x in fuel_credit)
        paid = CreditPay.objects.filter(supplier_id=sup.id).aggregate(Sum('amount'))['amount__sum'] or 0
        total_credit_due += (opening + inv_sum + fuel_sum - float(paid))

    # Total Inventory Valuation across all stock entries
    stock_items = StockEntry.objects.all()
    total_inventory_val = 0.0
    for item in stock_items:
        try:
            total_inventory_val += float(item.amount or 0)
        except (ValueError, TypeError):
            pass
    total_stock_count = StockEntry.objects.count()

    # Fleet & Active Transit Log
    total_vehicles = VehicleList.objects.filter(active_status='yes').count()
    vehicles_in_transit = VehicleTrack.objects.filter(status='travelling').count()
    recent_movements = VehicleTrack.objects.all().order_by('-id')[:5]

    # Fuel Reservoirs Capacities & Health
    reservoirs = Reserviour.objects.all()
    total_fuel_capacity = sum(float(r.capacity or 0) for r in reservoirs)
    total_fuel_stock = sum(float(r.stock or 0) for r in reservoirs)
    fuel_stock_percentage = round((total_fuel_stock / total_fuel_capacity * 100), 1) if total_fuel_capacity > 0 else 0

    # Maintenance Work Orders
    recent_maintenance = MaintainanceBill.objects.all().order_by('-id')[:5]
    total_maintenance_cost = sum(float(m.total or 0) for m in MaintainanceBill.objects.all())

    # Filter Actionable Alerts for User Scope
    if u_status in ['main_admin', 'main_staff']:
        pending_grn_alerts = Notification.objects.filter(content='gnoti_add', status='pending')[:3]
        pending_credit_alerts = Notification.objects.filter(content='crnoti_add', status='pending')[:3]
    else:
        pending_grn_alerts = Notification.objects.filter(content='gnoti_add', status='pending', from_site=u_site)[:3]
        pending_credit_alerts = Notification.objects.filter(content='crnoti_add', status='pending', from_site=u_site)[:3]

    context = {
        'total_sites': total_sites,
        'total_suppliers': total_suppliers,
        'pending_pos': pending_pos,
        'approved_pos': approved_pos,
        'total_invoice_sum': total_invoice_sum,
        'total_credit_due': total_credit_due,
        'total_inventory_val': total_inventory_val,
        'total_stock_count': total_stock_count,
        'total_vehicles': total_vehicles,
        'vehicles_in_transit': vehicles_in_transit,
        'total_fuel_capacity': total_fuel_capacity,
        'total_fuel_stock': total_fuel_stock,
        'fuel_stock_percentage': fuel_stock_percentage,
        'reservoirs': reservoirs,
        'total_maintenance_cost': total_maintenance_cost,
        'recent_movements': recent_movements,
        'recent_maintenance': recent_maintenance,
        'recent_pos': recent_pos,
        'recent_invoices': recent_invoices,
        'pending_grn_alerts': pending_grn_alerts,
        'pending_credit_alerts': pending_credit_alerts,
        'u_site': u_site,
    }
    return render(request, 'index.html', context)
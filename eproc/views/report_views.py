import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Sum, Q

from eproc.models import (
    StockItem, StockEntry, Site, FuelType, VehicleType, Reserviour, 
    Supplier, VehicleList, GoodsEntry, Goods, GoodsExtra, PurchaseEntry, 
    InvoiceItem, MaterialIssueEntry, MaterialItem, InternalTransfer, 
    TransferItem, InternalGrn, InternalGrnItems, FuelBill, Fuel, 
    MaintainanceBill, VehicleTrack, CompanyLetterhead
)
from eproc.decorators import user_access
from procurement.utils import render_to_pdf

def get_active_letterhead(site_name=None):
    """
    Helper to fetch site-specific active letterhead or fallback to the master corporate letterhead.
    """
    if site_name:
        lh = CompanyLetterhead.objects.filter(site=site_name, is_active=True).first()
        if lh:
            return lh
    return CompanyLetterhead.objects.filter(is_active=True).first()

@user_access
def reports(request):
    item_dash = StockItem.objects.all()
    site_dash = Site.objects.all()
    f_type = FuelType.objects.all()
    v_type = VehicleType.objects.all()
    reserve = Reserviour.objects.all()
    supplier_dash = Supplier.objects.all()
    
    vehis = []
    seen = set()
    seen_add = seen.add
    ent = VehicleList.objects.values_list('vehicle_type_id', flat=True)
    ent = [x for x in ent if not (x in seen or seen_add(x))]
    for e in ent:
        vehi = VehicleList.objects.filter(vehicle_type_id=e)
        n = len(vehi)
        vehis.append([vehi, range(1, n)])
        
    context = {
        'item_dash': item_dash, 'site_dash': site_dash, 'f_type': f_type, 
        'vehis': vehis, 'v_type': v_type, 'reserve': reserve, 
        'supplier_dash': supplier_dash
    }    
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
        report_head = ''
        report_val = request.POST.get('report_val')

        if report_val == 'stock_report':
            report_head = 'Stock Report'
            if request.POST.get('item'):
                item_val = request.POST.get('item')
                if request.POST.get('site'):
                    site_val = request.POST.get('site')
                    report = StockEntry.objects.filter(item=item_val, stock_site=site_val)
                    total_opening = StockEntry.objects.filter(item=item_val, stock_site=site_val).aggregate(Sum('opening'))
                    total_qty = StockEntry.objects.filter(item=item_val, stock_site=site_val).aggregate(Sum('quantity'))
                else:
                    report = StockEntry.objects.filter(item=item_val)
                    total_opening = StockEntry.objects.filter(item=item_val).aggregate(Sum('opening'))
                    total_qty = StockEntry.objects.filter(item=item_val).aggregate(Sum('quantity'))
            else:
                if request.POST.get('site'):
                    site_val = request.POST.get('site')
                    report = StockEntry.objects.filter(stock_site=site_val)

        elif report_val == 'grn_report':
            report_head = 'GRN Report'
            if request.POST.get('fromdate') and request.POST.get('todate'):
                fromdate = request.POST.get('fromdate')
                todate = request.POST.get('todate')
                if request.POST.get('item'):
                    item_val = request.POST.get('item')
                    if request.POST.get('site'):
                        site_val = request.POST.get('site')
                        grrn = GoodsEntry.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val)
                        for r in grrn:
                            goo = Goods.objects.filter(goodsid=r.id, item=item_val)
                            gex = GoodsExtra.objects.filter(goodsid=r.id)
                            report.append([r, gex, goo])
                    else:
                        grrn = GoodsEntry.objects.filter(entry_date__range=[fromdate, todate])
                        for r in grrn:
                            gex = GoodsExtra.objects.filter(goodsid=r.id)
                            goo = Goods.objects.filter(goodsid=r.id, item=item_val)
                            if goo.exists():
                                report.append([r, gex, goo])
                else:
                    if request.POST.get('site'):
                        site_val = request.POST.get('site')
                        grrn = GoodsEntry.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val)
                        for r in grrn:
                            goo = Goods.objects.filter(goodsid=r.id)
                            gex = GoodsExtra.objects.filter(goodsid=r.id)
                            report.append([r, gex, goo])

        elif report_val == 'invoice_report':
            report_head = 'Invoice Report'
            if request.POST.get('fromdate') and request.POST.get('todate'):
                fromdate = request.POST.get('fromdate')
                todate = request.POST.get('todate')
                if request.POST.get('item'):
                    item_val = request.POST.get('item')
                    if request.POST.get('site'):
                        site_val = request.POST.get('site')
                        grrn = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val)
                        total_amt = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val).aggregate(Sum('total'))
                        credit = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val, transaction_type='credit').aggregate(Sum('total'))
                        cash = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val, transaction_type='cash').aggregate(Sum('total'))
                        for r in grrn:
                            goo = InvoiceItem.objects.filter(purchaseid=r.id, item=item_val)
                            report.append([r, goo])
                    else:
                        ppid = []
                        grrn = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate])
                        for r in grrn:
                            goo = InvoiceItem.objects.filter(purchaseid=r.id, item=item_val)
                            if goo.exists():
                                ppid.append(r.id)
                                report.append([r, goo])
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
                            goo = InvoiceItem.objects.filter(purchaseid=r.id)
                            report.append([r, goo])

        elif report_val == 'material_report':
            report_head = 'Material Issue Report'
            if request.POST.get('fromdate') and request.POST.get('todate'):
                fromdate = request.POST.get('fromdate')
                todate = request.POST.get('todate')
                if request.POST.get('item'):
                    item_val = request.POST.get('item')
                    if request.POST.get('site'):
                        site_val = request.POST.get('site')
                        grrn = MaterialIssueEntry.objects.filter(issue_date__range=[fromdate, todate], user_site=site_val)
                        for r in grrn:
                            goo = MaterialItem.objects.filter(materialid=r.id, item=item_val)
                            report.append([r, goo])
                    else:
                        grrn = MaterialIssueEntry.objects.filter(issue_date__range=[fromdate, todate])
                        for r in grrn:
                            goo = MaterialItem.objects.filter(materialid=r.id, item=item_val)
                            if goo.exists():
                                report.append([r, goo])
                else:
                    if request.POST.get('site'):
                        site_val = request.POST.get('site')
                        grrn = MaterialIssueEntry.objects.filter(issue_date__range=[fromdate, todate], user_site=site_val)
                        for r in grrn:
                            goo = MaterialItem.objects.filter(materialid=r.id)
                            report.append([r, goo])

        elif report_val == 'internal_report':
            report_head = 'Internal Transfer Report'
            if request.POST.get('fromdate') and request.POST.get('todate'):
                fromdate = request.POST.get('fromdate')
                todate = request.POST.get('todate')
                if request.POST.get('item'):
                    item_val = request.POST.get('item')
                    if request.POST.get('site'):
                        site_val = request.POST.get('site')
                        grrn = InternalTransfer.objects.filter(issue_date__range=[fromdate, todate], user_site=site_val)
                        for r in grrn:
                            goo = TransferItem.objects.filter(transferid=r.id, item=item_val)
                            report.append([r, goo])
                    else:
                        grrn = InternalTransfer.objects.filter(issue_date__range=[fromdate, todate])
                        for r in grrn:
                            goo = TransferItem.objects.filter(transferid=r.id, item=item_val)
                            if goo.exists():
                                report.append([r, goo])
                else:
                    if request.POST.get('site'):
                        site_val = request.POST.get('site')
                        grrn = InternalTransfer.objects.filter(issue_date__range=[fromdate, todate], user_site=site_val)
                        for r in grrn:
                            goo = TransferItem.objects.filter(transferid=r.id)
                            report.append([r, goo])

        elif report_val == 'transfer_grn':
            report_head = 'Internal Transfer GRN Report'
            if request.POST.get('fromdate') and request.POST.get('todate'):
                fromdate = request.POST.get('fromdate')
                todate = request.POST.get('todate')
                if request.POST.get('item'):
                    item_val = request.POST.get('item')
                    if request.POST.get('site'):
                        site_val = request.POST.get('site')
                        grrn = InternalGrn.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val)
                        for r in grrn:
                            goo = InternalGrnItems.objects.filter(goodsid=r.id, item=item_val)
                            report.append([r, goo])
                    else:
                        grrn = InternalGrn.objects.filter(entry_date__range=[fromdate, todate])
                        for r in grrn:
                            goo = InternalGrnItems.objects.filter(goodsid=r.id, item=item_val)
                            if goo.exists():
                                report.append([r, goo])
                else:
                    if request.POST.get('site'):
                        site_val = request.POST.get('site')
                        grrn = InternalGrn.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val)
                        for r in grrn:
                            goo = InternalGrnItems.objects.filter(goodsid=r.id)
                            report.append([r, goo])

        elif report_val == 'fuel_purchase':
            report_head = 'Reserviour-wise Fuel Purchase Report'
            if request.POST.get('fromdate') and request.POST.get('todate'):
                fromdate = request.POST.get('fromdate')
                todate = request.POST.get('todate')
                if request.POST.get('item'):
                    item_val = request.POST.get('item')
                    if request.POST.get('site'):
                        site_val = request.POST.get('site')
                        report = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val, fuel_type=item_val).order_by('entry_date')
                        total_qty = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val, fuel_type=item_val).aggregate(Sum('quantity'))
                        total_amt = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val, fuel_type=item_val).aggregate(Sum('amount'))
                    else:
                        report = FuelBill.objects.filter(entry_date__range=[fromdate, todate], fuel_type=item_val).order_by('entry_date')
                        total_qty = FuelBill.objects.filter(entry_date__range=[fromdate, todate], fuel_type=item_val).aggregate(Sum('quantity'))
                        total_amt = FuelBill.objects.filter(entry_date__range=[fromdate, todate], fuel_type=item_val).aggregate(Sum('amount'))
                else:
                    if request.POST.get('site'):
                        site_val = request.POST.get('site')
                        report = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val).order_by('entry_date')
                        total_qty = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val).aggregate(Sum('quantity'))
                        total_amt = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val).aggregate(Sum('amount'))

        elif report_val == 'vehicle_fuel':
            report_head = 'Vehicle-wise Fuel Consumption Report'
            if request.POST.get('fromdate') and request.POST.get('todate'):
                fromdate = request.POST.get('fromdate')
                todate = request.POST.get('todate')
                filters = Q(date__range=[fromdate, todate])
                
                if request.POST.get('site'):
                    site_val = request.POST.get('site')
                    filters &= Q(reserviour=site_val)
                if request.POST.get('item'):
                    item_val = request.POST.get('item')
                    filters &= Q(fuel_type=item_val)
                if request.POST.get('vehicle_type_name'):
                    vehicle_type_val = request.POST.get('vehicle_type_name')
                    filters &= Q(vehicle_type=vehicle_type_val)
                if request.POST.get('vehicle'):
                    vehicle_val = request.POST.get('vehicle')
                    num_type = request.POST.get('num_type')
                    vd = VehicleList.objects.filter(
                        Q(vehicle_number=vehicle_val) | Q(engine_number=vehicle_val) | Q(chasis_number=vehicle_val)
                    ).first()
                    if vd:
                        vh, eng, ch = vd.vehicle_number, vd.engine_number, vd.chasis_number
                        filters &= Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))

                report = Fuel.objects.filter(filters).order_by('date')
                total_qty = Fuel.objects.filter(filters).aggregate(Sum('quantity'))

        elif report_val == 'maintain_log':
            report_head = 'All Maintainance Log'
            if request.POST.get('fromdate') and request.POST.get('todate'):
                fromdate = request.POST.get('fromdate')
                todate = request.POST.get('todate')
                filters = Q(entry_date__range=[fromdate, todate])
                if request.POST.get('site'):
                    site_val = request.POST.get('site')
                    filters &= Q(user_site=site_val)
                report = MaintainanceBill.objects.filter(filters).order_by('entry_date')
                total_amt = MaintainanceBill.objects.filter(filters).aggregate(Sum('total'))

        elif report_val == 'vehicle_maintain':
            report_head = 'Vehicle-wise Maintainance Log'
            if request.POST.get('fromdate') and request.POST.get('todate'):
                fromdate = request.POST.get('fromdate')
                todate = request.POST.get('todate')
                filters = Q(entry_date__range=[fromdate, todate])
                
                if request.POST.get('site'):
                    site_val = request.POST.get('site')
                    filters &= Q(user_site=site_val)
                if request.POST.get('vehicle_type_name'):
                    vehicle_type_val = request.POST.get('vehicle_type_name')
                    filters &= Q(vehicle_type=vehicle_type_val)
                if request.POST.get('vehicle'):
                    vehicle_val = request.POST.get('vehicle')
                    num_type = request.POST.get('num_type')
                    vd = VehicleList.objects.filter(
                        Q(vehicle_number=vehicle_val) | Q(engine_number=vehicle_val) | Q(chasis_number=vehicle_val)
                    ).first()
                    if vd:
                        vh, eng, ch = vd.vehicle_number, vd.engine_number, vd.chasis_number
                        filters &= Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))

                report = MaintainanceBill.objects.filter(filters).order_by('entry_date')
                total_amt = MaintainanceBill.objects.filter(filters).aggregate(Sum('total'))

        elif report_val == 'vendor_maintain':
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

        elif report_val == 'vehicle_move':
            report_head = 'Vehicle Movement Report'
            if request.POST.get('fromdate') and request.POST.get('todate'):
                fromdate = request.POST.get('fromdate')
                todate = request.POST.get('todate')
                filters = Q(entry_date__range=[fromdate, todate])
                
                if request.POST.get('fromsite'):
                    fsite = request.POST.get('fromsite')
                    filters &= Q(from_site=fsite)
                if request.POST.get('tosite'):
                    tsite = request.POST.get('tosite')
                    filters &= Q(to_site=tsite)
                if request.POST.get('vehicle_type_name'):
                    vehicle_type_val = request.POST.get('vehicle_type_name')
                    filters &= Q(vehicle_type=vehicle_type_val)
                if request.POST.get('vehicle'):
                    vehicle_val = request.POST.get('vehicle')
                    num_type = request.POST.get('num_type')
                    vd = VehicleList.objects.filter(
                        Q(vehicle_number=vehicle_val) | Q(engine_number=vehicle_val) | Q(chasis_number=vehicle_val)
                    ).first()
                    if vd:
                        vh, eng, ch = vd.vehicle_number, vd.engine_number, vd.chasis_number
                        filters &= Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))

                report = VehicleTrack.objects.filter(filters).order_by('entry_date')

        context = {
            'report': report, 'report_val': report_val, 'report_head': report_head, 
            'item_val': item_val, 'site_val': site_val, 'fromdate': fromdate, 
            'todate': todate, 'total_opening': total_opening, 'total_qty': total_qty, 
            'total_amt': total_amt, 'vehicle_val': vehicle_val, 
            'vehicle_type_val': vehicle_type_val, 'credit': credit, 'cash': cash, 
            'fsite': fsite, 'tsite': tsite, 'num_type': num_type
        }    
        return render(request, 'report_generation.html', context)
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
        report_head = ''
        report_val = request.POST.get('report_val')

        if report_val == 'stock_report':
            report_head = 'Stock Report'
            if request.POST.get('item'):
                item_val = request.POST.get('item')
                if request.POST.get('site'):
                    site_val = request.POST.get('site')
                    report = StockEntry.objects.filter(item=item_val, stock_site=site_val)
                    total_opening = StockEntry.objects.filter(item=item_val, stock_site=site_val).aggregate(Sum('opening'))
                    total_qty = StockEntry.objects.filter(item=item_val, stock_site=site_val).aggregate(Sum('quantity'))
                else:
                    report = StockEntry.objects.filter(item=item_val)
                    total_opening = StockEntry.objects.filter(item=item_val).aggregate(Sum('opening'))
                    total_qty = StockEntry.objects.filter(item=item_val).aggregate(Sum('quantity'))
            else:
                if request.POST.get('site'):
                    site_val = request.POST.get('site')
                    report = StockEntry.objects.filter(stock_site=site_val)

        elif report_val == 'grn_report':
            report_head = 'GRN Report'
            if request.POST.get('fromdate') and request.POST.get('todate'):
                fromdate = request.POST.get('fromdate')
                todate = request.POST.get('todate')
                if request.POST.get('item'):
                    item_val = request.POST.get('item')
                    if request.POST.get('site'):
                        site_val = request.POST.get('site')
                        grrn = GoodsEntry.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val)
                        for r in grrn:
                            goo = Goods.objects.filter(goodsid=r.id, item=item_val)
                            gex = GoodsExtra.objects.filter(goodsid=r.id)
                            report.append([r, gex, goo])
                    else:
                        grrn = GoodsEntry.objects.filter(entry_date__range=[fromdate, todate])
                        for r in grrn:
                            gex = GoodsExtra.objects.filter(goodsid=r.id)
                            goo = Goods.objects.filter(goodsid=r.id, item=item_val)
                            if goo.exists():
                                report.append([r, gex, goo])
                else:
                    if request.POST.get('site'):
                        site_val = request.POST.get('site')
                        grrn = GoodsEntry.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val)
                        for r in grrn:
                            goo = Goods.objects.filter(goodsid=r.id)
                            gex = GoodsExtra.objects.filter(goodsid=r.id)
                            report.append([r, gex, goo])

        elif report_val == 'invoice_report':
            report_head = 'Invoice Report'
            if request.POST.get('fromdate') and request.POST.get('todate'):
                fromdate = request.POST.get('fromdate')
                todate = request.POST.get('todate')
                if request.POST.get('item'):
                    item_val = request.POST.get('item')
                    if request.POST.get('site'):
                        site_val = request.POST.get('site')
                        grrn = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val)
                        total_amt = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val).aggregate(Sum('total'))
                        credit = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val, transaction_type='credit').aggregate(Sum('total'))
                        cash = MaintainanceBill.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val, transaction_type='cash').aggregate(Sum('total'))
                        for r in grrn:
                            goo = InvoiceItem.objects.filter(purchaseid=r.id, item=item_val)
                            report.append([r, goo])
                    else:
                        ppid = []
                        grrn = PurchaseEntry.objects.filter(entry_date__range=[fromdate, todate])
                        for r in grrn:
                            goo = InvoiceItem.objects.filter(purchaseid=r.id, item=item_val)
                            if goo.exists():
                                ppid.append(r.id)
                                report.append([r, goo])
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
                            goo = InvoiceItem.objects.filter(purchaseid=r.id)
                            report.append([r, goo])

        elif report_val == 'material_report':
            report_head = 'Material Issue Report'
            if request.POST.get('fromdate') and request.POST.get('todate'):
                fromdate = request.POST.get('fromdate')
                todate = request.POST.get('todate')
                if request.POST.get('item'):
                    item_val = request.POST.get('item')
                    if request.POST.get('site'):
                        site_val = request.POST.get('site')
                        grrn = MaterialIssueEntry.objects.filter(issue_date__range=[fromdate, todate], user_site=site_val)
                        for r in grrn:
                            goo = MaterialItem.objects.filter(materialid=r.id, item=item_val)
                            report.append([r, goo])
                    else:
                        grrn = MaterialIssueEntry.objects.filter(issue_date__range=[fromdate, todate])
                        for r in grrn:
                            goo = MaterialItem.objects.filter(materialid=r.id, item=item_val)
                            if goo.exists():
                                report.append([r, goo])
                else:
                    if request.POST.get('site'):
                        site_val = request.POST.get('site')
                        grrn = MaterialIssueEntry.objects.filter(issue_date__range=[fromdate, todate], user_site=site_val)
                        for r in grrn:
                            goo = MaterialItem.objects.filter(materialid=r.id)
                            report.append([r, goo])

        elif report_val == 'internal_report':
            report_head = 'Internal Transfer Report'
            if request.POST.get('fromdate') and request.POST.get('todate'):
                fromdate = request.POST.get('fromdate')
                todate = request.POST.get('todate')
                if request.POST.get('item'):
                    item_val = request.POST.get('item')
                    if request.POST.get('site'):
                        site_val = request.POST.get('site')
                        grrn = InternalTransfer.objects.filter(issue_date__range=[fromdate, todate], user_site=site_val)
                        for r in grrn:
                            goo = TransferItem.objects.filter(transferid=r.id, item=item_val)
                            report.append([r, goo])
                    else:
                        grrn = InternalTransfer.objects.filter(issue_date__range=[fromdate, todate])
                        for r in grrn:
                            goo = TransferItem.objects.filter(transferid=r.id, item=item_val)
                            if goo.exists():
                                report.append([r, goo])
                else:
                    if request.POST.get('site'):
                        site_val = request.POST.get('site')
                        grrn = InternalTransfer.objects.filter(issue_date__range=[fromdate, todate], user_site=site_val)
                        for r in grrn:
                            goo = TransferItem.objects.filter(transferid=r.id)
                            report.append([r, goo])

        elif report_val == 'transfer_grn':
            report_head = 'Internal Transfer GRN Report'
            if request.POST.get('fromdate') and request.POST.get('todate'):
                fromdate = request.POST.get('fromdate')
                todate = request.POST.get('todate')
                if request.POST.get('item'):
                    item_val = request.POST.get('item')
                    if request.POST.get('site'):
                        site_val = request.POST.get('site')
                        grrn = InternalGrn.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val)
                        for r in grrn:
                            goo = InternalGrnItems.objects.filter(goodsid=r.id, item=item_val)
                            report.append([r, goo])
                    else:
                        grrn = InternalGrn.objects.filter(entry_date__range=[fromdate, todate])
                        for r in grrn:
                            goo = InternalGrnItems.objects.filter(goodsid=r.id, item=item_val)
                            if goo.exists():
                                report.append([r, goo])
                else:
                    if request.POST.get('site'):
                        site_val = request.POST.get('site')
                        grrn = InternalGrn.objects.filter(entry_date__range=[fromdate, todate], user_site=site_val)
                        for r in grrn:
                            goo = InternalGrnItems.objects.filter(goodsid=r.id)
                            report.append([r, goo])

        elif report_val == 'fuel_purchase':
            report_head = 'Reserviour-wise Fuel Purchase Report'
            if request.POST.get('fromdate') and request.POST.get('todate'):
                fromdate = request.POST.get('fromdate')
                todate = request.POST.get('todate')
                if request.POST.get('item'):
                    item_val = request.POST.get('item')
                    if request.POST.get('site'):
                        site_val = request.POST.get('site')
                        report = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val, fuel_type=item_val).order_by('entry_date')
                        total_qty = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val, fuel_type=item_val).aggregate(Sum('quantity'))
                        total_amt = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val, fuel_type=item_val).aggregate(Sum('amount'))
                    else:
                        report = FuelBill.objects.filter(entry_date__range=[fromdate, todate], fuel_type=item_val).order_by('entry_date')
                        total_qty = FuelBill.objects.filter(entry_date__range=[fromdate, todate], fuel_type=item_val).aggregate(Sum('quantity'))
                        total_amt = FuelBill.objects.filter(entry_date__range=[fromdate, todate], fuel_type=item_val).aggregate(Sum('amount'))
                else:
                    if request.POST.get('site'):
                        site_val = request.POST.get('site')
                        report = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val).order_by('entry_date')
                        total_qty = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val).aggregate(Sum('quantity'))
                        total_amt = FuelBill.objects.filter(entry_date__range=[fromdate, todate], reserviour=site_val).aggregate(Sum('amount'))

        elif report_val == 'vehicle_fuel':
            report_head = 'Vehicle-wise Fuel Consumption Report'
            if request.POST.get('fromdate') and request.POST.get('todate'):
                fromdate = request.POST.get('fromdate')
                todate = request.POST.get('todate')
                filters = Q(date__range=[fromdate, todate])
                
                if request.POST.get('site'):
                    site_val = request.POST.get('site')
                    filters &= Q(reserviour=site_val)
                if request.POST.get('item'):
                    item_val = request.POST.get('item')
                    filters &= Q(fuel_type=item_val)
                if request.POST.get('vehicle_type_name'):
                    vehicle_type_val = request.POST.get('vehicle_type_name')
                    filters &= Q(vehicle_type=vehicle_type_val)
                if request.POST.get('vehicle'):
                    vehicle_val = request.POST.get('vehicle')
                    num_type = request.POST.get('num_type')
                    vd = VehicleList.objects.filter(
                        Q(vehicle_number=vehicle_val) | Q(engine_number=vehicle_val) | Q(chasis_number=vehicle_val)
                    ).first()
                    if vd:
                        vh, eng, ch = vd.vehicle_number, vd.engine_number, vd.chasis_number
                        filters &= Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))

                report = Fuel.objects.filter(filters).order_by('date')
                total_qty = Fuel.objects.filter(filters).aggregate(Sum('quantity'))

        elif report_val == 'maintain_log':
            report_head = 'All Maintainance Log'
            if request.POST.get('fromdate') and request.POST.get('todate'):
                fromdate = request.POST.get('fromdate')
                todate = request.POST.get('todate')
                filters = Q(entry_date__range=[fromdate, todate])
                if request.POST.get('site'):
                    site_val = request.POST.get('site')
                    filters &= Q(user_site=site_val)
                report = MaintainanceBill.objects.filter(filters).order_by('entry_date')
                total_amt = MaintainanceBill.objects.filter(filters).aggregate(Sum('total'))

        elif report_val == 'vehicle_maintain':
            report_head = 'Vehicle-wise Maintainance Log'
            if request.POST.get('fromdate') and request.POST.get('todate'):
                fromdate = request.POST.get('fromdate')
                todate = request.POST.get('todate')
                filters = Q(entry_date__range=[fromdate, todate])
                
                if request.POST.get('site'):
                    site_val = request.POST.get('site')
                    filters &= Q(user_site=site_val)
                if request.POST.get('vehicle_type_name'):
                    vehicle_type_val = request.POST.get('vehicle_type_name')
                    filters &= Q(vehicle_type=vehicle_type_val)
                if request.POST.get('vehicle'):
                    vehicle_val = request.POST.get('vehicle')
                    num_type = request.POST.get('num_type')
                    vd = VehicleList.objects.filter(
                        Q(vehicle_number=vehicle_val) | Q(engine_number=vehicle_val) | Q(chasis_number=vehicle_val)
                    ).first()
                    if vd:
                        vh, eng, ch = vd.vehicle_number, vd.engine_number, vd.chasis_number
                        filters &= Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))

                report = MaintainanceBill.objects.filter(filters).order_by('entry_date')
                total_amt = MaintainanceBill.objects.filter(filters).aggregate(Sum('total'))

        elif report_val == 'vendor_maintain':
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

        elif report_val == 'vehicle_move':
            report_head = 'Vehicle Movement Report'
            if request.POST.get('fromdate') and request.POST.get('todate'):
                fromdate = request.POST.get('fromdate')
                todate = request.POST.get('todate')
                filters = Q(entry_date__range=[fromdate, todate])
                
                if request.POST.get('fromsite'):
                    fsite = request.POST.get('fromsite')
                    filters &= Q(from_site=fsite)
                if request.POST.get('tosite'):
                    tsite = request.POST.get('tosite')
                    filters &= Q(to_site=tsite)
                if request.POST.get('vehicle_type_name'):
                    vehicle_type_val = request.POST.get('vehicle_type_name')
                    filters &= Q(vehicle_type=vehicle_type_val)
                if request.POST.get('vehicle'):
                    vehicle_val = request.POST.get('vehicle')
                    num_type = request.POST.get('num_type')
                    vd = VehicleList.objects.filter(
                        Q(vehicle_number=vehicle_val) | Q(engine_number=vehicle_val) | Q(chasis_number=vehicle_val)
                    ).first()
                    if vd:
                        vh, eng, ch = vd.vehicle_number, vd.engine_number, vd.chasis_number
                        filters &= Q(Q(vehicle_number=vh) | Q(vehicle_number=eng) | Q(vehicle_number=ch))

                report = VehicleTrack.objects.filter(filters).order_by('entry_date')

        letterhead = get_active_letterhead(site_val if site_val else None)

        context = {
            'report': report, 'report_val': report_val, 'report_head': report_head, 
            'item_val': item_val, 'site_val': site_val, 'fromdate': fromdate, 
            'todate': todate, 'total_opening': total_opening, 'total_qty': total_qty, 
            'total_amt': total_amt, 'vehicle_val': vehicle_val, 
            'vehicle_type_val': vehicle_type_val, 'credit': credit, 'cash': cash, 
            'fsite': fsite, 'tsite': tsite, 'num_type': num_type,
            'letterhead': letterhead
        }    
        pdf = render_to_pdf('report_pdf.html', context)
        if pdf:
            rnum = random.randint(11111111, 99999999)
            filename = "Report_%s.pdf" % (rnum)
            content = 'inline; filename="%s"' % (filename)
            if request.GET.get("download"):
                content = 'attachment; filename="%s"' % (filename)
            pdf['Content-Disposition'] = content
            return pdf
        return HttpResponse("Not found")
    return redirect('reports')

def report_redirects(request, rst, rval):
    if rst == 'invoice':
        rval_upper = rval.upper()
        if PurchaseEntry.objects.filter(voucher_number=rval_upper).exists():
            pe = PurchaseEntry.objects.get(voucher_number=rval_upper)
            return redirect('/ashish-invoice-detail/' + str(pe.id) + '/')
    return HttpResponse("Not Found")
import csv
from django.http import HttpResponse
from django.utils import timezone
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def export_coupons_csv(modeladmin, request, queryset):
    """
    Export selected coupons to a CSV file.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="coupons.csv"'

    writer = csv.writer(response)
    writer.writerow(['Code', 'Discount Amount'])

    for coupon in queryset:
        if coupon.active and coupon.valid_from <= timezone.now() <= coupon.valid_to:
            writer.writerow([coupon.code, coupon.discount])

    return response


export_coupons_csv.short_description = 'Export selected coupons to CSV'


def export_coupons_pdf(modeladmin, request, queryset):
    """
    Export selected coupons to a PDF file.
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="coupons.pdf"'

    # Create a PDF document
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    p.drawString(100, height - 50, "Coupon Code")
    p.drawString(300, height - 50, "Discount Amount")

    y = height - 80
    for coupon in queryset:
        if coupon.active and coupon.valid_from <= timezone.now() <= coupon.valid_to:
            p.drawString(100, y, coupon.code)
            p.drawString(300, y, str(coupon.discount))
            y -= 20

    p.showPage()
    p.save()

    return response


export_coupons_pdf.short_description = 'Export selected coupons to PDF'

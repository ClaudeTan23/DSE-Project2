from openpyxl import Workbook
from django.http import HttpResponse
from apps.home.services.fetch_report_service import get_report_data


def export_report_excel(request):
    period = request.GET.get("period", "daily")

    data = get_report_data(period)

    wb = Workbook()
    ws = wb.active
    ws.append(["Date", "Total Quantity"])

    for row in data:
        ws.append([row["time"], row["total_qty"]])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=report.xlsx"

    wb.save(response)
    return response

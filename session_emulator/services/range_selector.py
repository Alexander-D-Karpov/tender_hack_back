from competence.models import CompanyPriceMin, Company
from session_emulator.models import Lot


def range_buyer(price: float, quotation_session_id: int) -> float:
    for session in CompanyPriceMin.objects.filter(quotation_session_id=quotation_session_id):
        if session.price <= price:
            price = price * 0.99
            Lot.objects.create(comp_quotation_session_id=quotation_session_id, price=price)

    return price

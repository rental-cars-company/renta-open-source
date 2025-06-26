from datetime import datetime

from api.validate_uz.models import ValidateUz


def parse_validate_uz_data(user, data, debts_sum):
    person = data.get("ModelPerson", {})
    dl = data.get("ModelDL", {})
    category = data.get("ModelDLCategory", [{}])[0]
    birth = data.get("driverBirthPlace", {})
    address = data.get("driverAddress", {})

    def parse_date(date_str):
        try:
            return datetime.strptime(date_str, "%d.%m.%Y").date()
        except:
            return None

    validate_uz, _ = ValidateUz.objects.update_or_create(
        user=user,
        defaults={
            "passport": person.get("pDoc"),
            "fio": person.get("pOwner"),
            "surname": person.get("pSurname"),
            "name": person.get("pName"),
            "middlename": person.get("pPatronym"),
            "date_of_birth": parse_date(person.get("pOwner_date")),
            "dl_begin": parse_date(dl.get("pBegin")),
            "dl_end": parse_date(dl.get("pEnd")),
            "dl_issued_by": dl.get("pIssuedBy"),
            "dl_serial_number": dl.get("pSerialNumber"),
            "dl_category": category.get("pCategory"),
            "dl_category_begin": parse_date(category.get("pBegin")),
            "dl_category_end": parse_date(category.get("pEnd")),
            "birth_region_id": birth.get("pRegionId"),
            "birth_city_id": birth.get("pCityId"),
            "birth_place": birth.get("pPlace"),
            "address_region_id": address.get("pRegionId"),
            "address_city_id": address.get("pCityId"),
            "address_place": address.get("pPlace"),
            "debts_sum": debts_sum,
        },
    )

    return validate_uz

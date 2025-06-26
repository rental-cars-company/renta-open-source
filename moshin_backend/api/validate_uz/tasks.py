# tasks/verification.py
import json

from celery import shared_task

from api.driverlicenses.models import DriverLicense
from api.passports.models import Passport
from common.document_service.verification_services.utils import (
    parse_validate_uz_data,
)
from common.document_service.verification_services.validate_all import (
    validate_dl_debts_criminals,
)
from common.documents import (
    DOCUMENT_APPROVED,
    DOCUMENT_EXTRACT_FAILED,
    DOCUMENT_EXTRACT_VERIFIED,
)


@shared_task
def verify_dl_debts_task(user_id):
    try:
        license = DriverLicense.objects.filter(user_id=user_id).first()
        if not license:
            print("❌ Нет водительских прав у пользователя")
            return

        passport = Passport.objects.filter(user_id=user_id).first()
        if not passport:
            print("❌ Нет паспорта у пользователя")
            return

        if (
            license.status == DOCUMENT_APPROVED
            and passport.status == DOCUMENT_APPROVED
        ):
            print("✅ Документы уже одобрены, validate.uz не нужен")
            return

        print(
            f"📄 Паспорт: {passport.pinfl}, ВУ: {license.serial_number}, ДР: {license.date_of_birth}"
        )

        response_driver, response_debts, response_criminal_records = (
            validate_dl_debts_criminals(pinfl=passport.pinfl)
        )
        license_data = json.loads(response_driver.text)
        debts_data = json.loads(response_debts.text)

        if not (license_data.get("success") and "data" in license_data):
            print("⚠️ Валидация ВУ неуспешна")
            license.status = DOCUMENT_EXTRACT_FAILED
            license.save(update_fields=["status"])
            return

        debts_sum = debts_data.get("data", {}).get("residual_sum", 0)
        parse_validate_uz_data(
            user=license.user, data=license_data["data"], debts_sum=debts_sum
        )

        license.status = DOCUMENT_EXTRACT_VERIFIED
        license.save(update_fields=["status"])

        print("✅ Данные из validate.uz успешно сохранены")
        # print(
        #     f"Данные по судимости: {json.loads(response_criminal_records.text)}"
        # )

    except Exception as e:
        print(f"❌ Ошибка проверки через validation.uz: {e}")

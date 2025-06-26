import base64
import time
import requests
from django.conf import settings


class AtmosClient:
    # Token & Sale/Hold URLs
    token_url            = settings.ATMOS_TOKEN_URL
    create_url           = settings.ATMOS_CREATE_URL
    preapply_url         = settings.ATMOS_PREAPPLY_URL
    apply_url            = settings.ATMOS_APPLY_URL
    reverse_url          = settings.ATMOS_REVERSE_URL
    get_url              = settings.ATMOS_GET_URL
    hold_create_url      = settings.ATMOS_HOLD_CREATE_URL
    hold_apply_url       = settings.ATMOS_HOLD_APPLY_URL
    hold_capture_url     = settings.ATMOS_HOLD_CAPTURE_URL
    hold_cancel_url      = settings.ATMOS_HOLD_CANCEL_URL
    hold_get_url         = settings.ATMOS_HOLD_GET_URL

    # Card binding URLs
    bind_init_url        = settings.ATMOS_BIND_INIT_URL
    bind_confirm_url     = settings.ATMOS_BIND_CONFIRM_URL
    bind_dial_url        = settings.ATMOS_BIND_DIAL_URL
    list_cards_url       = settings.ATMOS_LIST_CARDS_URL
    remove_card_url      = settings.ATMOS_REMOVE_CARD_URL

    def __init__(self):
        self._token   = None
        self._expires = 0

    def _get_token(self):
        if not self._token or time.time() > self._expires:
            creds = f"{settings.ATMOS_CONSUMER_KEY}:{settings.ATMOS_CONSUMER_SECRET}".encode()
            basic = base64.b64encode(creds).decode()
            r = requests.post(
                self.token_url,
                headers={"Authorization": f"Basic {basic}"},
                data={"grant_type": "client_credentials"},
                timeout=10
            )
            r.raise_for_status()
            data = r.json()
            self._token   = data['access_token']
            self._expires = time.time() + data.get('expires_in', 3600) - 60
        return self._token

    def _headers(self):
        return {
            'Authorization': f"Bearer {self._get_token()}",
            'Content-Type' : 'application/json'
        }

    # --- Sale endpoints ---
    def create(self, amount, account, store_id, terminal_id=None, lang='ru'):
        payload = {
            'amount': amount,
            'account': account,
            'store_id': store_id,
            'lang': lang
        }
        if terminal_id:
            payload['terminal_id'] = terminal_id
        r = requests.post(self.create_url, json=payload, headers=self._headers(), timeout=10)
        r.raise_for_status()
        return r.json()

    def pre_apply(self, transaction_id, store_id, card_token):
        payload = {
            'transaction_id': transaction_id,
            'store_id': store_id,
            'card_token': card_token
        }
        r = requests.post(self.preapply_url, json=payload, headers=self._headers(), timeout=10)
        r.raise_for_status()
        return r.json()

    def apply(self, transaction_id, otp, store_id):
        payload = {
            'transaction_id': transaction_id,
            'otp': otp,
            'store_id': store_id
        }
        r = requests.post(self.apply_url, json=payload, headers=self._headers(), timeout=10)
        r.raise_for_status()
        return r.json()

    def reverse(self, transaction_id, reason=None, hold_amount=None):
        payload = {'transaction_id': transaction_id}
        if reason:
            payload['reason'] = reason
        if hold_amount:
            payload['hold_amount'] = hold_amount
        r = requests.post(self.reverse_url, json=payload, headers=self._headers(), timeout=10)
        r.raise_for_status()
        return r.json()

    def get_transaction(self, store_id, transaction_id):
        payload = {'store_id': store_id, 'transaction_id': transaction_id}
        r = requests.post(self.get_url, json=payload, headers=self._headers(), timeout=10)
        r.raise_for_status()
        return r.json()

    # --- Hold endpoints ---
    def hold_create(self, store_id, account, amount, duration, card_token, payment_details=''):
        payload = {
            "store_id": str(store_id),
            "account": str(account),
            "amount": str(amount),
            "duration": str(duration),
            "card_token": card_token,
            "payment_details": payment_details or "",
        }
        r = requests.post(self.hold_create_url, json=payload,
                          headers=self._headers(), timeout=10)
        r.raise_for_status()
        return r.json()

    def hold_apply(self, hold_id, otp):
        url = f"{self.hold_apply_url}/{hold_id}"
        r = requests.put(url, json={"otp": otp},
                         headers=self._headers(), timeout=10)
        r.raise_for_status()
        return r.json()

    def hold_capture(self, hold_id):
        r = requests.post(f"{self.hold_capture_url}/{hold_id}", headers=self._headers(), timeout=10)
        r.raise_for_status()
        return r.json()

    def hold_cancel(self, hold_id):
        r = requests.delete(f"{self.hold_cancel_url}/{hold_id}", headers=self._headers(), timeout=10)
        r.raise_for_status()
        return r.json()

    def hold_get(self, hold_id):
        r = requests.get(f"{self.hold_get_url}/{hold_id}", headers=self._headers(), timeout=10)
        r.raise_for_status()
        return r.json()

    # --- Card binding endpoints ---
    def bind_card_init(self, card_number, expiry):
        payload = {'card_number': card_number, 'expiry': expiry}
        r = requests.post(self.bind_init_url, json=payload, headers=self._headers(), timeout=10)
        r.raise_for_status()
        return r.json()

    def bind_card_confirm(self, transaction_id, otp):
        payload = {'transaction_id': transaction_id, 'otp': otp}
        r = requests.post(self.bind_confirm_url, json=payload, headers=self._headers(), timeout=10)
        r.raise_for_status()
        return r.json()

    def bind_card_dial(self, transaction_id):
        payload = {'transaction_id': transaction_id}
        r = requests.put(self.bind_dial_url, json=payload, headers=self._headers(), timeout=10)
        r.raise_for_status()
        return r.json()

    def list_cards(self, page=1, page_size=10):
        payload = {'page': page, 'page_size': page_size}
        r = requests.post(self.list_cards_url, json=payload, headers=self._headers(), timeout=10)
        r.raise_for_status()
        return r.json()

    def remove_card(self, id, token):
        payload = {'id': id, 'token': token}
        r = requests.post(self.remove_card_url, json=payload, headers=self._headers(), timeout=10)
        r.raise_for_status()
        return r.json()

    # --- Convenience methods using stored card_token ---
    def pay_with_token(self, amount, account, store_id, card_token, terminal_id=None, lang='ru'):
        # 1) create transaction
        cr = self.create(amount, account, store_id, terminal_id=terminal_id, lang=lang)
        tid = cr['transaction_id']
        # 2) pre-apply по token
        self.pre_apply(tid, store_id, card_token)
        # 3) apply (OTP эмулируем "111111")
        ap = self.apply(tid, '111111', store_id)
        # возвращаем оригинальный tid + данные apply
        return {'transaction_id': tid, **ap}

    def hold_with_token(self, store_id, account, amount, duration,
                        card_token, payment_details=""):
        # 1) create hold
        cr = self.hold_create(store_id, account, amount, duration,
                              card_token, payment_details)
        # ATMOS возвращает:
        # {'result': {'code': 'OK', ...}, 'hold_id': 123, 'account': '...'}
        code = cr.get("result", {}).get("code")
        hid  = cr.get("hold_id")
        if code != "OK" or hid is None:
            # возвращаем сами данные — во вьюхе поймаем и отдадим клиенту 400
            raise RuntimeError(f"hold_create_error: {cr}")

        # 2) confirm hold
        ap = self.hold_apply(hid, "111111")
        if ap.get("result", {}).get("code") != "OK":
            raise RuntimeError(f"hold_apply_error: {ap}")

        return {"hold_id": hid, **ap}


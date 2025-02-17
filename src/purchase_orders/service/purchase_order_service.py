# purchase_order/services.py
from .repositories import PurchaseOrderRepository
from user.repositories import UserRepository


class PurchaseOrderService:
    def __init__(self):
        self.purchase_order_repo = PurchaseOrderRepository()
        self.user_repo = UserRepository()

    def create_purchase_order(self, data):

        if data["total_price"] > 50000:
            coo = self.user_repo.get_coo_user()
            if not coo:
                raise ValueError("COO user not found.")

            self._notify_coo(coo, data)

        return self.purchase_order_repo.create(data)

    def _notify_coo(self, coo, data):

        print(
            f"Notifying COO ({coo.email}) for approval of purchase order: {data['po_number']}"
        )

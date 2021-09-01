from dataclasses import dataclass, field

from .customer import Customer
from .email import EmailGateway
from .product import Product
from .store import Store


class ProductRepository:
    @classmethod
    def get_by_id(cls, product_id: int) -> Product:
        return Product(product_id, f'product-{product_id}')


class CustomerRepository:
    @classmethod
    def get_by_id(cls, customer_id: int) -> Customer:
        return Customer(customer_id, f'{customer_id}@email.com')


@dataclass(frozen=True)
class CustomerController:
    email_gateway: EmailGateway
    store: Store = field(default_factory=Store)
    customer_repo: CustomerRepository = field(default_factory=CustomerRepository)
    product_repo: ProductRepository = field(default_factory=ProductRepository)

    def purchase(self, customer_id: int, product_id: int, quantity: int) -> bool:
        customer = self.customer_repo.get_by_id(customer_id)
        product = self.product_repo.get_by_id(product_id)

        success = customer.purchase(self.store, product, quantity)
        if success:
            self.email_gateway.send_receipt(customer.email, product.name, quantity)
        return success

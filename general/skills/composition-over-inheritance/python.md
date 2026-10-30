# In Python

A class's bases are the names in parentheses after its name.

## Violation

- `class InvoiceNotifier(EmailClient):` whose methods call `self.send(...)` to mail
  invoices.
- `class ReportBuilder(DatabaseHelper):` that inherits only to call `self.query(...)`.

## Not a violation

- `class SavingsAccount(Account):` that overrides how interest is earned.
- `class Order(models.Model):`, `class OrderView(View):`, `class OrderIn(BaseModel):`,
  `class PaymentDeclined(Exception):`, `class TestOrder(TestCase):`.
- `class TimestampMixin:` combined into models, and `class Order(TimestampMixin,
  models.Model):`.
- `class FileStore(Storage):` where `Storage` is a `Protocol` or `ABC`.

from decimal import Decimal, InvalidOperation
from datetime import datetime
from app.ui.table_module import TableModuleFrame, FieldSpec
from app.database.csv_manager import CSVManager
from app.utils.validators import is_valid_date, normalize_date


def patient_values():
    rows = CSVManager("patients.csv").read()
    return [f"{r['patient_id']} — {r['first_name']} {r['last_name']}".strip() for r in rows]


class PaymentsFrame(TableModuleFrame):
    store_name = "invoices.csv"
    id_field = "invoice_id"
    id_prefix = "INV"
    title = "Payments & Invoices"
    subtitle = "Create invoices, calculate totals automatically, and track payment status."
    search_fields = ["invoice_id", "patient", "payment_status"]
    filters = [("payment_status", "Status", ("Paid", "Pending", "Partially Paid", "Cancelled"))]
    export_filename = "invoices_export.csv"
    fields = [
        FieldSpec("patient", "Patient", "combo", patient_values, True), FieldSpec("invoice_date", "Invoice date", required=True),
        FieldSpec("description", "Description"), FieldSpec("amount", "Amount"), FieldSpec("discount", "Discount"),
        FieldSpec("tax", "Tax"), FieldSpec("total", "Total", readonly=True),
        FieldSpec("payment_method", "Payment method", "combo", ("Cash", "Card", "Bank transfer", "Other")),
        FieldSpec("payment_status", "Payment status", "combo", ("Paid", "Pending", "Partially Paid", "Cancelled"), True, True),
        FieldSpec("notes", "Notes", "text"),
    ]
    columns = ["invoice_id", "patient", "invoice_date", "amount", "discount", "tax", "total", "payment_method", "payment_status"]
    column_labels = {"invoice_id":"Invoice","patient":"Patient","invoice_date":"Date","amount":"Amount","discount":"Discount","tax":"Tax","total":"Total","payment_method":"Method","payment_status":"Status"}

    def _build(self):
        super()._build()
        for key in ("amount", "discount", "tax"):
            self.vars[key].trace_add("write", lambda *_: self.calculate_total())

    def clear_form(self):
        super().clear_form()
        self.vars["invoice_date"].set(datetime.now().strftime("%Y-%m-%d"))
        self.vars["payment_status"].set("Pending"); self.vars["payment_method"].set("Cash")

    def calculate_total(self):
        try:
            amount = Decimal(self.vars["amount"].get() or "0")
            discount = Decimal(self.vars["discount"].get() or "0")
            tax = Decimal(self.vars["tax"].get() or "0")
            self.vars["total"].set(f"{max(amount - discount + tax, Decimal('0')):.2f}")
        except InvalidOperation:
            self.vars["total"].set("")

    def before_save(self, record):
        if not is_valid_date(record["invoice_date"]):
            return record, "Invoice date must use YYYY-MM-DD or DD/MM/YYYY."
        record["invoice_date"] = normalize_date(record["invoice_date"])
        try:
            amount = Decimal(record["amount"] or "0"); discount = Decimal(record["discount"] or "0"); tax = Decimal(record["tax"] or "0")
        except InvalidOperation:
            return record, "Amount, discount, and tax must be valid non-negative numbers."
        if amount < 0 or discount < 0 or tax < 0: return record, "Amount, discount, and tax cannot be negative."
        if discount > amount: return record, "Discount cannot exceed amount."
        record["amount"] = f"{amount:.2f}"; record["discount"] = f"{discount:.2f}"; record["tax"] = f"{tax:.2f}"
        record["total"] = f"{amount - discount + tax:.2f}"
        return record, None

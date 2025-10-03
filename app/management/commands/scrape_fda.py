import requests
from django.core.management.base import BaseCommand
from app.models import Product

class Command(BaseCommand):
    help = "Scrape FDA validation products into Postgres"

    def handle(self, *args, **kwargs):
        url = "http://196.61.32.245:55/publicsearch"

        start = 0
        length = 50
        total_records = None
        inserted = 0

        while True:
            params = {
                "draw": 1,
                "columns[0][data]": "DT_RowIndex",
                "columns[0][searchable]": "false",
                "columns[1][data]": "client_name",
                "columns[1][name]": "tbl_client_details.client_name",
                "columns[2][data]": "product_name",
                "columns[3][data]": "product_category",
                "columns[4][data]": "expiry_date",
                "columns[5][data]": "status",
                "columns[5][name]": "tbl_products_details.status",
                "columns[6][data]": "action",
                "columns[6][searchable]": "false",
                "columns[6][orderable]": "false",
                "order[0][column]": 1,
                "order[0][dir]": "desc",
                "start": start,
                "length": length,
                "search[value]": "",
            }
            headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                                    "Chrome/129.0 Safari/537.36",
                        "Accept": "application/json, text/javascript, */*; q=0.01",
                        "X-Requested-With": "XMLHttpRequest",
                        "Referer": "http://196.61.32.245:55/",
                    }


            response = requests.get(url, params=params, headers=headers)

            if response.status_code != 200:
                self.stderr.write(f"❌ Request failed at start={start}, status={response.status_code}")
                break

            # check content-type
            if "application/json" not in response.headers.get("Content-Type", ""):
                self.stderr.write("⚠️ Got HTML instead of JSON")
                self.stderr.write(response.text[:300])  # print preview
                break

            data = response.json()
            def safe_strip(value):
                if isinstance(value, str):
                    return value.strip()
                return ""


            if total_records is None:
                total_records = data.get("recordsFiltered", 0)
                self.stdout.write(f"Total records found: {total_records}")

            rows = data.get("data", [])
            if not rows:
                break

            for row in rows:
                product, created = Product.objects.update_or_create(
                    client_name=safe_strip(row.get("client_name", "")),
                    product_name=safe_strip(row.get("product_name", "")),
                    defaults={
                        "product_category": safe_strip(row.get("product_category")),
                        "expiry_date": safe_strip(row.get("expiry_date")),
                        "status": safe_strip(row.get("status")),
                    },
                )
                if created:
                    inserted += 1

            self.stdout.write(f"Fetched {len(rows)} rows (start={start})")
            start += length

            if start >= total_records:
                break

        self.stdout.write(self.style.SUCCESS(f"✅ Done. Inserted {inserted} new products."))


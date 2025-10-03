import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from app.models import Product, Company
from datetime import datetime
import time

BASE_URL = "http://196.61.32.245:55/publicsearch"

class Command(BaseCommand):
    help = "Scrape FDA Ghana Public Search Portal for products"

    def handle(self, *args, **kwargs):
        session = requests.Session()

        # Step 1: Load main page to get viewstate (ASP.NET trick)
        response = session.get(BASE_URL)
        soup = BeautifulSoup(response.text, "lxml")

        viewstate = soup.select_one("#__VIEWSTATE")["value"]
        eventvalidation = soup.select_one("#__EVENTVALIDATION")["value"]

        # Step 2: Perform a search (you may need to tweak params)
        payload = {
            "__VIEWSTATE": viewstate,
            "__EVENTVALIDATION": eventvalidation,
            "txtSearch": "",  # blank = fetch all products
            "btnSearch": "Search"
        }

        response = session.post(BASE_URL, data=payload)
        soup = BeautifulSoup(response.text, "lxml")

        # Step 3: Parse results (example table structure, needs inspection)
        rows = soup.select("table#ContentPlaceHolder1_gvProducts tr")[1:]  # skip header row
        for row in rows:
            cols = [c.get_text(strip=True) for c in row.find_all("td")]
            if not cols:
                continue

            try:
                name = cols[0]
                company_name = cols[1]
                category = cols[2]
                expiry_date = cols[3] if cols[3] else None
                status = cols[4].lower() == "approved"

                company, _ = Company.objects.get_or_create(name=company_name)

                product, created = Product.objects.update_or_create(
                    name=name,
                    company=company,
                    defaults={
                        "category": category,
                        "expiry_date": datetime.strptime(expiry_date, "%d/%m/%Y").date() if expiry_date else None,
                        "approved": status,
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Added: {name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Updated: {name}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error parsing row: {e}"))

        # Optional: add delay if scraping multiple pages
        time.sleep(2)

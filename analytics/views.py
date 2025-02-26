import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("Agg")
import pandas as pd
import io
from django.http import HttpResponse
from rest_framework.views import APIView

from clients.models.deals import Deal


class AnalyticsGraphView(APIView):
    def get(self, request):
        deals = Deal.objects.all()
        deals_df = pd.DataFrame.from_records(deals.values("amount", "created_at"))

        if not deals_df.empty:
            deals_df["created_at"] = pd.to_datetime(deals_df["created_at"]).dt.tz_localize(None)
            deals_df["month"] = deals_df["created_at"].dt.to_period("M")
            monthly_income = deals_df.groupby("month")["amount"].sum()
        else:
            monthly_income = pd.Series()

        # Создаём график
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(monthly_income.index.astype(str), monthly_income.values, marker="o", linestyle="-", color="b")
        ax.set_title("Доход по месяцам")
        ax.set_xlabel("Месяц")
        ax.set_ylabel("Доход")
        ax.grid(True)

        # Сохраняем график в буфер
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)

        return HttpResponse(buffer.getvalue(), content_type="image/png")


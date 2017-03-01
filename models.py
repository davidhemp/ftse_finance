from django.db import models
from django.db import connection
# Create your models here.

class News(models.Model):
    def __str__(self):
        return self.title
    link = models.CharField(max_length=200)
    title = models.CharField(max_length=30)
    abstract = models.CharField(max_length=200)
    pub_date = models.DateTimeField("pub date")

class StockManager(models.Manager):
    def nth_entry(self, ticker, startdate, step):
        cursor = connection.cursor()
        selects = "q.min_price, q.max_price, q.close_price, q.open_price, q.date, q.ticker"
        table = "ftsefinance_stock_data"
        query = """SELECT {0}
                    FROM {1} q
                    WHERE q.date >= '{2}' AND q.ticker == '{3}'
                    ORDER BY q.date DESC """.format(selects, table, startdate, ticker)
        print(cursor)
        cursor.execute(query)
        n = 0
        min_price = []
        max_price = []
        close_price = []
        open_price = []
        date = []
        for row in cursor.fetchall():
            if n%step==0:
                min_price.append(row[0])
                max_price.append(row[1])
                close_price.append(row[2])
                open_price.append(row[3])
                date.append(row[4])
            n+=1
        p = self.model(min_price=min_price,
                        max_price=max_price,
                        close_price=close_price,
                        open_price=open_price,
                        date=date)
        return p

class Which_Stock(models.Model):
    def __str__(self):
        return self.ticker

    ticker = models.CharField(max_length=20)
    name = models.CharField(max_length=200, default=" ")
    change = models.DecimalField(max_digits=8, decimal_places=2, default=0)

class Stock_Data(models.Model):
    ticker = models.ForeignKey( Which_Stock,
                                on_delete=models.CASCADE,
                                unique_for_date="date")

    min_price = models.DecimalField(max_digits=8, decimal_places=2)
    max_price = models.DecimalField(max_digits=8, decimal_places=2)
    close_price = models.DecimalField(max_digits=8, decimal_places=2)
    open_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    date = models.DateTimeField("trading date")
    objects = StockManager()

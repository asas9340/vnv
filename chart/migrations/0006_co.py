# Generated by Django 3.0.3 on 2020-06-14 13:42
import csv
import os
from django.db import migrations
from django.conf import settings

Date = 0
China = 1
France = 2
Germany = 3
Korea_South = 4
US = 5
United_Kingdom = 6

def covid_confirmed(apps, schema_editor):
    Covid_confirmed = apps.get_model('chart', 'Covid_confirmed')  # (app_label, model_name)
    csv_file = os.path.join(settings.BASE_DIR, 'covid_co.csv')
    with open(csv_file) as dataset:                   # 파일 객체 dataset
        reader = csv.reader(dataset)                    # 파일 객체 dataset에 대한 판독기 획득
        next(reader)  # ignore first row (headers)      # __next__() 호출 때마다 한 라인 판독
        for entry in reader:                            # 판독기에 대하여 반복 처리
            Covid_confirmed.objects.create(                       # DB 행 생성
                Date=entry[Date],
                China=float(entry[China]),
                France=float(entry[France]),
                Germany=float(entry[Germany]),
                Korea_South=float(entry[Korea_South]),
                US=float(entry[US]),
                United_Kingdom=float(entry[United_Kingdom]),
            )



class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0005_covid_confirmed'),
    ]

    operations = [
        migrations.RunPython(covid_confirmed),

    ]

from datetime import datetime

from django.shortcuts import render
from .models import Passenger, Covid_recovered, Covid_confirmed, Covid_deaths
from django.db.models import Count, Q
import json

def home(request):
    return render(request, 'home.html')


def world_population(request):
    return render(request, 'world_population.html')


def ticket_class_view_1(request):  # 방법 1
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(
        survived_count=Count('ticket_class',
                             filter=Q(survived=True)),
        not_survived_count=Count('ticket_class',
                                 filter=Q(survived=False))) \
        .order_by('ticket_class')
    return render(request, 'ticket_class_1.html', {'dataset': dataset})


#  dataset = [
#    {'ticket_class': 1, 'survived_count': 200, 'not_survived_count': 123},
#    {'ticket_class': 2, 'survived_count': 119, 'not_survived_count': 158},
#    {'ticket_class': 3, 'survived_count': 181, 'not_survived_count': 528}
#  ]


def ticket_class_view_2(request):  # 방법 2
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
        .order_by('ticket_class')



    # 빈 리스트 3종 준비
    categories = list()  # for xAxis
    survived_series = list()  # for series named 'Survived'
    not_survived_series = list()  # for series named 'Not survived'



    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append('%s Class' % entry['ticket_class'])  # for xAxis
        survived_series.append(entry['survived_count'])  # for series named 'Survived'
        not_survived_series.append(entry['not_survived_count'])  # for series named 'Not survived'




    # json.dumps() 함수로 리스트 3종을 JSON 데이터 형식으로 반환
    return render(request, 'ticket_class_2.html', {
        'categories': json.dumps(categories),
        'survived_series': json.dumps(survived_series),
        'not_survived_series': json.dumps(not_survived_series),

    })


def ticket_class_view_3(request):  # 방법 3
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
        .order_by('ticket_class')


    # 빈 리스트 3종 준비 (series 이름 뒤에 '_data' 추가)
    categories = list()  # for xAxis
    survived_series_data = list()  # for series named 'Survived'
    not_survived_series_data = list()  # for series named 'Not survived'
    survived_rate_data = list()

    # 리스트 3종에 형식화된 값을 등록



    for entry in dataset:
        categories.append('%s Class' % entry['ticket_class'])  # for xAxis
        survived_series_data.append(entry['survived_count'])  # for series named 'Survived'
        not_survived_series_data.append(entry['not_survived_count'])  # for series named 'Not survived'
        survived_rate_data.append(entry['survived_count'] \
               / (entry['survived_count'] + entry['not_survived_count']) * 100)



    survived_series = {
        'name': '생존',
        'data': survived_series_data,
        'color': 'green',
        'type': 'column',
        'yAxis': 1,

    }
    not_survived_series = {
        'name': '비생존',
        'data': not_survived_series_data,
        'color': 'red',
        'type': 'column',
        'yAxis': 1,
    }

    survived_rate = {
        'name': '생존율',
        'data': survived_rate_data,
        'type': 'spline',

    }

    chart = {
        'chart': {'zoomType': 'xy'},
        'title': {'text': 'Titanic Survivors by Ticket Class'},
        'xAxis': {'categories': categories},
        "yAxis": [{'labels': {'format': '{value} %', 'style': {'color': 'blue'}}, 'title': {'text': '생존율', 'style': {'color': 'blue'}}},
                  {'labels': {'format': '{value} 명', 'style': {'color': 'black'}}, 'opposite': 'true', 'title': {'text': '인원', 'style': {'color': 'black'}}}],
        "tooltip": {"shared": "true"},
        'series': [survived_series, not_survived_series, survived_rate]
    }

    dump = json.dumps(chart)

    return render(request, 'ticket_class_3.html', {'chart': dump})

def json_example(request):  # 방법 4
    pass

def chart_data(request):  # 방법 4
    pass


def covid_recovered(request):
    dataset = Covid_recovered.objects \
        .values('China','France','Germany','Korea_South','US','United_Kingdom', 'Date') \
        .order_by('Date')

    return render(request, 'covid_recovered.html',{'dataset': dataset})

def covid_confirmed(request):
    dataset = Covid_confirmed.objects \
        .values('China', 'France', 'Germany', 'Korea_South', 'US', 'United_Kingdom', 'Date') \
        .order_by('Date')

    return render(request, 'covid_confirmed.html',{'dataset': dataset})

def covid_deaths(request):
    dataset = Covid_deaths.objects \
        .values('China', 'France', 'Germany', 'Korea_South', 'US', 'United_Kingdom', 'Date') \
        .order_by('Date')

    return render(request, 'covid_deaths.html',{'dataset': dataset})


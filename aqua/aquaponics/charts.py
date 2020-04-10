import random
import django
import datetime
from .models import fish, testing
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter


def simple(request):
    

    fig=Figure()
    fshamt = fish.objects.all()
    ax=fig.add_subplot(111)

    
    grp = []
    spamt = []
    #now=datetime.datetime.now()
    #delta=datetime.timedelta(days=1)
    for i in fshamt:
        grp.append(i.batch)
        spamt.append(i.spawn_amount)
    #plott = plt.plot(grp,spamt)
    #plt.savefig('static/images/test.png')
    #plt.show()
    
    
    
    
    # for i in range(10):
    #     x.append(now)
    #     now+=delta
    #     y.append(random.randint(0, 1000))
    ax.bar(grp, spamt)
    fig.suptitle("Fish Information")
    
    #ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    #fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

def ph(request):

    watergraph = testing.objects.all()


    dat = len(watergraph)

    fig=Figure()

    ax=fig.add_subplot(111)

    dati=[]

    values=[]

    

    for i in watergraph:

        dati.append(i.test_date)

        values.append(i.ph)

    ax.plot_date(dati, values, '-')
    ax.set_xlabel('Date')
    ax.set_ylabel('Values')
    ax.set_title('PH')
    ax.xaxis.set_major_formatter(DateFormatter('%m-%d-%Y'))

    fig.autofmt_xdate()

    canvas=FigureCanvas(fig)

    response=django.http.HttpResponse(content_type='image/png')

    canvas.print_png(response)

    return response

def amonia(request):

    watergraph = testing.objects.all()

    dat = len(watergraph)

    fig=Figure()

    ax=fig.add_subplot(111)

    dati=[]

    values=[]

    

    for i in watergraph:

        dati.append(i.test_date)

        values.append(i.amonia)

    ax.plot_date(dati, values, '-')
    ax.set_xlabel('Date')
    ax.set_ylabel('Values')
    ax.set_title('Amonia (PPM)')
    ax.xaxis.set_major_formatter(DateFormatter('%m-%d-%Y'))

    fig.autofmt_xdate()

    canvas=FigureCanvas(fig)

    response=django.http.HttpResponse(content_type='image/png')

    canvas.print_png(response)

    return response

def nitrite(request):

    watergraph = testing.objects.all()

    dat = len(watergraph)

    fig=Figure()

    ax=fig.add_subplot(111)

    dati=[]

    values=[]

    

    for i in watergraph:

        dati.append(i.test_date)

        values.append(i.nitrite)

    ax.plot_date(dati, values, '-')
    ax.set_xlabel('Date')
    ax.set_ylabel('Values')
    ax.set_title('Nitrite (PPM)')
    ax.xaxis.set_major_formatter(DateFormatter('%m-%d-%Y'))

    fig.autofmt_xdate()

    canvas=FigureCanvas(fig)

    response=django.http.HttpResponse(content_type='image/png')

    canvas.print_png(response)

    return response

def nitrate(request):

    watergraph = testing.objects.all()

    fig=Figure()

    ax=fig.add_subplot(111)

    dati=[]

    values=[]

    

    for i in watergraph:

        dati.append(i.test_date)

        values.append(i.nitrate)

    ax.plot_date(dati, values, '-')
    ax.set_xlabel('Date')
    ax.set_ylabel('Values')
    ax.set_title('Nitrate (PPM)')
    ax.xaxis.set_major_formatter(DateFormatter('%m-%d-%Y'))

    fig.autofmt_xdate()

    canvas=FigureCanvas(fig)

    response=django.http.HttpResponse(content_type='image/png')

    canvas.print_png(response)

    return response


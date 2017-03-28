from django.shortcuts import *
from .forms import InternForm
from find import *
from api import  *
from iitb import *
from iitm import *
from iitr import *
#from iitkgp import *
from iith import *
from iisc import *
# Create your views here.

def index(request):
    form = InternForm(request.POST or None)
    f = {'form':form}
    if request.method != 'POST':
        form = InternForm()
        return render(request,'search/index.html',{'form':form})
    try:
        form = InternForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            college = data['college']
            area = data['area']
            tmp= correctexp(area)
            college=college.lower()
            if college in "iitd":
            	proff_data = get_data_iitd("http://ee.iitd.ernet.in/people/faculty.html", tmp)
            	return render(request, 'search/index.html', {'proff_data': proff_data, 'form': form, 'c': True})
            elif college in "iitb":
                proff_data= get_data_iitb("https://www.ee.iitb.ac.in/web/people/faculty/",tmp)
                return render(request,'search/index.html',{'proff_data':proff_data,'form':form,'c':True})
            elif college in "iitm":
                proff_data= get_data_iitm("http://www.ee.iitm.ac.in/faculty-members/",tmp)
                return render(request,'search/index.html',{'proff_data':proff_data,'form':form,'c':True})
            elif college in "iitr":
                proff_data= get_data_iitr("http://www.iitr.ac.in/departments/EE/pages/Faculty_List.html",tmp)
                return render(request,'search/index.html',{'proff_data':proff_data,'form':form,'c':True})
            #elif college in "iitkgp":
                #proff_data= get_data_iitkgp("http://www.iitkgp.ac.in/department/EE/faculties",tmp)
                #return render(request,'search/index.html',{'proff_data':proff_data,'form':form,'c':True})
	    elif college in "iith":
                proff_data= get_data_iith("http://ee.iith.ac.in/joomla/index.php/en/people",tmp)
                return render(request,'search/index.html',{'proff_data':proff_data,'form':form,'c':True})
	    elif college in "iisc":
                proff_data= get_data_iisc("http://www.ee.iisc.ac.in/people-faculty.php",tmp)
                return render(request,'search/index.html',{'proff_data':proff_data,'form':form,'c':True})

    except Exception as E:
        return render(request,'search/index.html',{'error':True,'error_value':E})
    return render(request,'search/index.html',f)

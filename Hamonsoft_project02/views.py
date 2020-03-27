from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views import generic
from django.views import View

from .models import DB_impo
from .forms import DB_impoForm
from .scheduler import Scheduler


class Project_main(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'project_2/index.html'
        db_impo_list = DB_impo.objects.all()
        return render(request, template_name, {"db_impo_list" : db_impo_list})


#스케줄러 전체 리스트 생성
scheduler = Scheduler()


#스케줄러 off 함수
def off(request, idx):
    db = DB_impo.objects.get(idx=idx)
    sched_id = db.sched_id
    
    scheduler.kill_scheduler(sched_id)

    template_name = 'project_2/common/test.html'
    return render(request, template_name)


#스케줄러 on 함수
def on(request, idx):
    db = DB_impo.objects.get(idx=idx)
    read = db.content
    sched_id = db.sched_id
    period = db.period

    print(read)

    scheduler.scheduler(sched_id, read, period, idx)

    template_name = 'project_2/common/test.html'
    return render(request, template_name)


#DB_impo 추가 함수
def add(request):
    template_name = 'project_2/common/add_db_impo.html'

    if request.method == 'POST':
        form = DB_impoForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.db_impo = DB_impo.objects.filter()
            comment.save()

            return HttpResponseRedirect(reverse('project_2'))

    else:
        form = DB_impoForm()
    return render(request, template_name, {'form': form, })


#DB_impo 수정 함수
def edit(request, idx):
    db = DB_impo.objects.get(idx=idx)

    if request.method == 'POST':
        form = DB_impoForm(request.POST)
        if form.is_valid():
            db.name = form.cleaned_data['name']
            db.content = form.cleaned_data['content']
            db.period = form.cleaned_data['period']
            db.save()

            return redirect('project_2')

    else:
        form = DB_impoForm(instance=db)
        context = {
            'form' : form,
            'writing' : True,
            'now' : 'edit'
        }
        return render(request, 'project_2/common/edit_db_impo.html', context)
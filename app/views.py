from django.shortcuts import render, redirect
from .models import Classroom, Student
from .forms import ClassroomForm

def index(request):
    data = {
        'classrooms': Classroom.objects.all(),
    }

    return render(request, 'index.html', data)

def create_classroom_view(request):
    context = {}
    
    if request.method == 'GET':
        context['classroom_form'] = ClassroomForm()
        return render(request, 'create-classroom.html', context)
    else:
        form = ClassroomForm(request, request.POST)

        if form.is_valid:
            name=request.POST.get('name')
            id_list1=request.POST.get('id_list1')
            id_list2=request.POST.get('id_list2')
            id_list3=request.POST.get('id_list3')
            id_list4=request.POST.get('id_list4')
            id_list5=request.POST.get('id_list5')
            id_list6=request.POST.get('id_list6')
            id_list7=request.POST.get('id_list7')
            id_list8=request.POST.get('id_list8')
            id_test1=request.POST.get('id_test1')
            id_test2=request.POST.get('id_test2')
            id_test3=request.POST.get('id_test3')
            id_test4=request.POST.get('id_test4')
            id_reav=request.POST.get('id_reav')
            id_final=request.POST.get('id_final')

            try:
                Classroom.objects.create(name=name,
                                        id_list1=id_list1,
                                        id_list2=id_list2,
                                        id_list3=id_list3,
                                        id_list4=id_list4,
                                        id_list5=id_list5,
                                        id_list6=id_list6,
                                        id_list7=id_list7,
                                        id_list8=id_list8,
                                        id_test1=id_test1,
                                        id_test2=id_test2,
                                        id_test3=id_test3,
                                        id_test4=id_test4,
                                        id_reav=id_reav,
                                        id_final=id_final)
            except:
                context['error'] = 'Já existe uma turma com esse nome!'
                context['classroom_form'] = ClassroomForm(data=request.POST)
                return render(request, 'create-classroom.html', context)
            
        return redirect('index')

def classroom_view(request, name):
    context = {}
    context['classroom'] = Classroom.objects.get(name=name)

    return render(request, 'classroom.html', context)

def delete_classroom(request, name):
    classroom = Classroom.objects.get(name=name)
    classroom.delete()
    
    return redirect('index')

def edit_classroom(request, name):
    context = {}
    
    if request.method == 'GET':
        context['classroom'] = Classroom.objects.get(name=name)
        return render(request, 'edit-classroom.html', context)
    else:
        classroom = Classroom.objects.get(name=name)
        try:
            classroom.name=request.POST.get('name')
            classroom.id_list1=request.POST.get('id_list1')
            classroom.id_list2=request.POST.get('id_list2')
            classroom.id_list3=request.POST.get('id_list3')
            classroom.id_list4=request.POST.get('id_list4')
            classroom.id_list5=request.POST.get('id_list5')
            classroom.id_list6=request.POST.get('id_list6')
            classroom.id_list7=request.POST.get('id_list7')
            classroom.id_list8=request.POST.get('id_list8')
            classroom.id_test1=request.POST.get('id_test1')
            classroom.id_test2=request.POST.get('id_test2')
            classroom.id_test3=request.POST.get('id_test3')
            classroom.id_test4=request.POST.get('id_test4')
            classroom.id_reav=request.POST.get('id_reav')
            classroom.id_final=request.POST.get('id_final')
            classroom.save()   
        except:
            context['error'] = 'Já existe uma turma com esse nome!'
            context['classroom'] = Classroom.objects.get(name=request.POST.get('name'))
            return render(request, 'edit-classroom.html', context)

        return redirect('index')



    


    
    
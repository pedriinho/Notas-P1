from django.shortcuts import render, redirect
from .models import Classroom, Student, StateThread
from .forms import ClassroomForm
import threading
import requests
import json
import matplotlib.pyplot as plt
from django.conf import settings
import os
from io import BytesIO
import base64
from django.contrib.auth.decorators import user_passes_test

def setStudentScoreTestsReassessmentsOnDatabase(userScores, list_number):
	for userScore in userScores:
		student = Student.objects.get(id_huxley=userScore['id_huxley'])
		if list_number == 1:
			setattr(student, 'reav', userScore['score'])
		else:
			setattr(student, 'final', userScore['score'])
		student.save()

def setStudentScoreTestsOnDatabase(userScores, list_number):
	for userScore in userScores:
		student = Student.objects.get(id_huxley=userScore['id_huxley'])
		setattr(student, 'test'+str(list_number), userScore['score'])
		student.save()

def setStudentScoreListOnDatabase(userScores, list_number):
	for userScore in userScores:
		student = Student.objects.get(id_huxley=userScore['id_huxley'])
		setattr(student, 'list'+str(list_number), userScore['score'])
		student.save()

def getScoreUrlsLists(id_lists):
	urls = []
	
	for id in id_lists:
		urls.append('https://www.thehuxley.com/api/v1/quizzes/' + str(id) + '/scores')

	return urls

def getScoreUrlsTests(ids_urls):
	urls = []
	
	for ids in ids_urls:
		urls.append('https://www.thehuxley.com/api/v1/quizzes/' + str(ids) + '/scores')

	return urls

def getUserScores(url, headers, type_score):
	userScores = []

	response = requests.get(url, headers=headers).json()
	for user in response:
		userScore = {}
		userScore['id_huxley'] = user['userId']

		score = 0
		for correctProblem in user['correctProblems']:
			if type_score == 1:
				score += correctProblem['score']
			else:
				score += round(correctProblem['partialScore'], 1) if correctProblem['partialScore'] > correctProblem['penalty'] else correctProblem['penalty']
		
		userScore['score'] = score

		userScores.append(userScore)

	return userScores

def get_token(login, password):
    headers = {
        "Content-type": "application/json"
    }
    data = {
		"username": login,
		"password": password
	}
    response = requests.post("https://thehuxley.com/api/login", headers=headers, data=json.dumps(data))
    token_json = response.json()
    return token_json["access_token"]

def setStudentDataOnDatabase(students, classroom):
    student_table = Student.objects.all()
    classroom_students = Classroom.objects.get(name=classroom)

    for student in students:
        if(not student_table.filter(id_huxley=student['id_huxley']).exists()):
            new_student = Student(name=student['nome'], classroom=classroom_students, id_huxley=student['id_huxley'])
            new_student.save()

def getStudentData(headers, id):
	data_url = f'https://www.thehuxley.com/api/v1/quizzes/{id}/users?max=100&offset=0'

	data_response = requests.get(data_url, headers=headers)

	students = []
	
	for students_data in data_response.json():
		students.append({
			'nome': students_data['name'].lower(),
			'id_huxley': students_data['id']
		})

	return students

def get_submission(access_token):
    classrooms = Classroom.objects.all()

    for classroom in classrooms:
        id_list = [classroom.id_list1, classroom.id_list2, classroom.id_list3, classroom.id_list4, classroom.id_list5, classroom.id_list6, classroom.id_list7, classroom.id_list8]
        id_test = [classroom.id_test1, classroom.id_test2, classroom.id_test3, classroom.id_test4]
        id_reavs = [classroom.id_reav, classroom.id_final]

        headers = {"Authorization": "Bearer " + access_token}
        students = getStudentData(headers, id_list[0])
        setStudentDataOnDatabase(students, classroom.name)

        urls_lists = getScoreUrlsLists(id_list)

        for index, url in enumerate(urls_lists):
            userScores = getUserScores(url, headers, 1)
            setStudentScoreListOnDatabase(userScores, index+1)

        urls_tests = getScoreUrlsTests(id_test)
        
        for index, url in enumerate(urls_tests):
            userScores = getUserScores(url, headers, 2)
            setStudentScoreTestsOnDatabase(userScores, index+1)
        
        urls_tests_reassessments = getScoreUrlsTests(id_reavs)
        
        for index, url in enumerate(urls_tests_reassessments):
            userScores = getUserScores(url, headers, 2)
            setStudentScoreTestsReassessmentsOnDatabase(userScores, index+1)

def calculate_mean():
    students = Student.objects.all()
    for student in students:
        nota = 0
        ab1 = round(((((student.test1 + student.test2)*7)/20) + (((student.list1 + student.list2 + student.list3 + student.list4)*3)/59)), 2)
        ab2 = round(((((student.test3 + student.test4)*7)/20) + (((student.list5 + student.list6 + student.list7 + student.list8)*3)/66)), 2)

        if (ab1 + ab2)/2 >= 7 or (ab1 + student.reav)/2 >= 7 or (ab2 + student.reav)/2 >= 7:
            continue
        if (student.reav >= ab1 and student.reav >= ab2 and ab1 >= ab2) or (ab1 >= ab2 and ab1 >= student.reav and student.reav >= ab2):
            nota = round((ab1 + student.reav)/2, 2)
        elif (student.reav >= ab1 and student.reav >= ab2 and ab2 >= ab1) or (ab2 >= ab1 and ab2 >= student.reav and student.reav >= ab1):
            nota = round((ab2 + student.reav)/2, 2)
        elif (ab1 >= ab2 and ab1 >= student.reav and ab2 >= student.reav) or (ab2 >= ab1 and ab2 >= student.reav and ab1 >= student.reav):
            nota = round((ab1 + ab2)/2, 2)
        
        if nota >= 10:
            student.mean = 10
            student.save()
            continue
        elif nota >= 7:
            print(student.name, nota)
            student.mean = nota
            student.situation = 'APROVADO'
            student.save()
            continue

        if student.mean >= 5 and student.mean < 7:
            if ((6 * student.mean) + ( 4 * student.final)/10) >= 5.5 and student.situation == 'EM ANÁLISE':
                student.situation = 'APROVADO'
                student.mean = round(((6 * student.mean) + ( 4 * student.final)/10), 2)
        if nota >= 5.5 and student.mean >= 5.5:
            student.mean = round(nota, 2)
            student.situation = 'APROVADO'
        elif student.final >= 7:
            student.situation = 'EM ANÁLISE'
        elif nota < 5.5:
            student.situation = 'REPROVADO'

        student.save()
             

def update_grade():
    while StateThread.objects.get().state == 'active':
        login = 'pedriinho1'
        password = 'pekfnddnf123ccpal'
        token = get_token(login, password)
        get_submission(token)
        calculate_mean()

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

def classroom_view_individual(request, name):
    context = {}
    classroom = Classroom.objects.get(name=name)
    context['headers'] = [   'Nome', 'Turma','Prova 1', 'Lista 1',
                            'Lista 2', 'Prova 2', 'Lista 3',
                            'Lista 4', 'Prova 3', 'Lista 5',
                            'Lista 6', 'Prova 4', 'Lista 7', 'Lista 8']
    context['students'] = classroom.student_set.all()
    context['nameClassroom'] = name
    context['thread'] = StateThread.objects.get().state

    return render(request, 'classroom-individual.html', context)

def classroom_view_computed(request, name):
    context = {}
    classroom = Classroom.objects.get(name=name)
    context['headers'] = [   'Nome', 'Turma','Ab1', 'Ab2',
                            'Reav', 'Final', 'Média','Situação'
                        ]
    students = classroom.student_set.all()
    data = []
    for student in students:
        data.append({
            'name': student.name,
            'course': student.course,
            'ab1': round(((((student.test1 + student.test2)*7)/20) + (((student.list1 + student.list2 + student.list3 + student.list4)*3)/59)), 2),
            'ab2': round(((((student.test3 + student.test4)*7)/20) + (((student.list5 + student.list6 + student.list7 + student.list8)*3)/66)), 2),
            'reav': student.reav,
            'final': student.final,
            'mean': student.mean,
            'situation': student.situation
        })
    context['students'] = data
    context['nameClassroom'] = name
    context['thread'] = StateThread.objects.get().state

    return render(request, 'classroom-computed.html', context)

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

@user_passes_test(lambda u: u.is_superuser)
def state_thread(request, name):
    if len(StateThread.objects.all()) == 0:
        StateThread.objects.create(state='deactive')
    
    thread = StateThread.objects.get()
    if thread.state == 'deactive': 
        print('entrou')
        thread.state = 'active'
        thread.save()
        gradesThread = threading.Thread(target=update_grade)
        gradesThread.start()

    else:
        print('saiu')
        thread.state = 'deactive'
        thread.save()

    return redirect(f'/classroom/{name}/individual')
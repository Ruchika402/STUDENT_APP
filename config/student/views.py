from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

def home(request):
    data = {
        "app" : "student",
        "topic": "Django Fundamentals",
        "message": "Welcome to Django Fundamentals"   
    }
    return JsonResponse(data)



def index(request):
    data1 = {
        "name": "Ruchika",
        "course": "Django Backend",
        "level": "Beginner"

    }    
    return JsonResponse(data1)




def details(request):
    data2 = {
        "student_id": 101,
        "student_name": "Ruchika Adak",
        "student_course": "Django Backend Development"

    }
    return JsonResponse(data2)



def version(request):
    return JsonResponse({"version": "1.0.0"})



def test(request):
    if request.method == 'GET':
        data3 = {
            "status": "success",
            "message": "This is a test endpoint"
        }    
        return JsonResponse(data3)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)
    


def test_method(request):
    return JsonResponse({
        "method_used": request.method
    })




def greet(request):
    name = request.GET.get('name', 'Ru')
    course = request.GET.get('course', 'Django')
    return JsonResponse({
        "message": f"Hello, {name}!"
                   f" Welcome to the {course} course."
    })



def square(request):
    number = request.GET.get('number')

    if number is None:
        return JsonResponse({
            "error": "Please provide a number parameter."
        }, status=400)
    try:
        num = int(number)
    except ValueError:
        return JsonResponse({
            "error": "Invalid number parameter. Please provide a valid integer."
        }, status=400)    

    squared_value = num ** 2
    return JsonResponse({
        "number": num,
        "square": squared_value
    })



""" def add(request):
    if request.method == "POST":
        name = request.POST.get('name')
        age = request.POST.get('age')

        if not name or not age:
            return JsonResponse(
                {"error": "name and age are required"},
                status=400
            )

        return JsonResponse({
            "message": "Student received",
            "name": name,
            "age": age
        })

    return JsonResponse(
        {"error": "Only POST method allowed"},
        status=405
    )
 """


from .models import Student

def all_students(request):
    students = Student.objects.all()
    total = students.count()
    sorted_students = students.order_by('age')

    data4 = []
    for s in sorted_students:
        data4.append({
            "name": s.name,
            "age": s.age,
            "course": s.course
        })  
    return JsonResponse({"students": data4, "total students": total})  




def one_student(request):
    name = request.GET.get('name')  
    if not name:
        return JsonResponse(
            {"error": "name parameter is required"},
            status=400
        )
    try:
        student = Student.objects.get(name=name) # Give me exactly one student whose name matches
    except Student.DoesNotExist:
        return JsonResponse(
            {"error": "Student not found"},
            status=404
        )
    data5 = {
        "name": student.name,
        "age": student.age,
        "course": student.course
    }
    return JsonResponse(data5)      



def teen(request):
    students = Student.objects.filter(age__gte=13, age__lte=19)
    data6 = []
    for s in students:
        data6.append({  
            "name": s.name,
            "age": s.age,
            "course": s.course
        })
    return JsonResponse({"teen_students": data6})   





from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm

def Login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({"message": "Login successful"})
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=401)
    return render(request, 'student/login.html')  


def Logout_user(request):
    logout(request)
    return JsonResponse({"message": "Logout successful"})



from django.contrib.auth.decorators import login_required, permission_required

@login_required
def dashboard(request):
    return JsonResponse({"message": f"Hello, {request.user.username}! This is a protected view."})


@permission_required('student.add_student', raise_exception=True)
def add_student(request):
    Student.objects.create(name="x", age=20, course="Django")
    return JsonResponse({"status": "added"})

# UPDATE
@permission_required('student.change_student', raise_exception=True)
def update_student(request, id):
    s = Student.objects.get(id=id)
    s.age = 21
    s.save()
    return JsonResponse({"msg": "updated"})

# DELETE
@permission_required('student.delete_student', raise_exception=True)
def delete_student(request, id):
    Student.objects.get(id=id).delete()
    return JsonResponse({"msg": "deleted"})


def student_list(request):
    students = Student.objects.all()

    data = []
    for s in students:
        data.append({
            "id": s.id,
            "name": s.name,
            "age": s.age,
            "course": s.course
        })

    return JsonResponse({"students": data})


from django.shortcuts import get_object_or_404
    
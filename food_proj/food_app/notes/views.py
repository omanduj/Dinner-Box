from django.shortcuts import render
from users.db_operations import add_note
# Create your views here.

def create_note(request):
    if request.method == "GET":
        return render(request, 'create_note.html')
    if request.method == "POST":
        name = request.POST.get('restaurant')
        note = request.POST.get('restaurant_note')
        rating = request.POST.get('personal_rating')
        email = request.session['user']['email']
        add_note(email, name, note, rating)
        return render(request, 'create_note.html')

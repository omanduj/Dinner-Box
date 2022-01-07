from django.shortcuts import render
from users.db_operations import add_note, check_note_exists, get_user_notes
from django.http import JsonResponse

# Create your views here.

def create_note(request):
    if request.method == "GET":
        return render(request, 'create_note.html')
    if request.method == "POST":
        name = request.POST.get('restaurant')
        note = request.POST.get('restaurant_note')
        rating = int(request.POST.get('personal_rating'))
        email = request.session['user']['email']
        result = check_note_exists(email, name)
        if len(result) == 1:
            add_note(email, name, note, rating)
            return JsonResponse({'success': name})
        if len(result['Notes']) == 0:
            add_note(email, name, note, rating)
            return JsonResponse({'success': name})
        return JsonResponse({'Error': 'Note Already Exists'})

def view_notes(request):
    if request.method == "GET":
        email = request.session["user"]['email']
        user_notes = get_user_notes(email)
        for doc in user_notes:
            print(doc)
    return JsonResponse(user_notes)

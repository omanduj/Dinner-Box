from django.shortcuts import render
from users.db_operations import add_note, check_note_exists, get_user_notes
from django.http import JsonResponse
from users.db_operations import get_one_user, delete_note

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
        note_collection = []
        email = request.session["user"]['email']
        user_notes = get_one_user(email)
        del user_notes['_id']
        del user_notes['email']
        del user_notes['password']
        if len(user_notes['Notes']) > 0:
            return render(request, 'note_viewer.html', {'notes': user_notes})
        return render(request, 'note_viewer.html', {'error': 'Add Some Notes!'})

def delete_user_note(request):
    restaurant_name = request.POST.get('restaurant_name')
    email = request.session["user"]['email']
    notes_found = delete_note(email, restaurant_name)
    print(notes_found, 'GG')
    if notes_found:
        return JsonResponse({'Success': notes_found})
    return JsonResponse({'Error': 'Not Foundsss'})

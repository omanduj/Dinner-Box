from django.shortcuts import render
from users.db_operations import (
    add_note,
    check_note_exists,
    get_user_notes,
    get_one_user,
    delete_note,
)
from django.http import JsonResponse
import collections

# from users.db_operations import get_one_user, delete_note, get_user_notes


# Create your views here.
def order_notes_name(
    request,
):  # have this and next switch between reverse depending on user selection (form, ect)
    """Purpose: To order notes alphabetically
    Parameters: N/a
    Return Value: standard_note - Notes sorted in alphabetical order
    """
    notes = get_user_notes(request.session["user"]["email"])
    notes = list(notes)[0]["Notes"]  # used to format returned information into a dict
    # notes = dict(sorted(notes.items(), reverse=True))
    notes = dict(
        sorted(notes.items())
    )  # used to sort notes based on name of restaurant
    standard_note = {"Notes": notes}
    # print(standard_note)
    return standard_note


def order_notes_rating(request):
    """Purpose: To order notes by rating
    Parameters: N/a
    Return Value: standard_note - Notes sorted by rating
    """
    notes = get_user_notes(request.session["user"]["email"])
    notes = list(notes)[0]["Notes"]
    notes_order = {}
    for key, value in notes.items():
        notes_order[key] = value["rating"]
    # notes_order = dict(sorted(notes_order.items(), key=lambda item: item[1], reverse=True))
    notes_order = dict(sorted(notes_order.items(), key=lambda item: item[1]))
    for key, value in notes.items():
        notes_order[key] = value
    standard_note = {"Notes": notes_order}
    del notes_order
    # print(standard_note)
    return standard_note


def order_notes_date(request):
    """Purpose: To order notes by date added
    Parameters: N/a
    Return Value: standard_note - Notes sorted in order by date
    """
    notes = get_user_notes(request.session["user"]["email"])
    notes = list(notes)[0]["Notes"]
    notes_order = {}
    for key, value in notes.items():
        notes_order[key] = value["date"]
    # notes_order = dict(sorted(notes_order.items(), key=lambda item: item[1], reverse=True))
    notes_order = dict(sorted(notes_order.items(), key=lambda item: item[1]))
    for key, value in notes.items():
        notes_order[key] = value
    standard_note = {"Notes": notes_order}
    del notes_order
    # print(standard_note)
    return standard_note


def order_notes(request):  # to be worked on
    """Purpose: To order notes a certain way
    Parameters: N/a
    Return Value: Notes in an ordered way
    """
    ordering = request.POST.get("ordering")
    return JsonResponse({"Ordering": ordering})


def create_note(request):
    """Purpose: To create a note for the user
    Parameters: N/a
    Return Value: On Get will display the create_note.html file to add a note
                    On Post will either create the note and notify user it was successful or
                        will notify user the note for that restaurant already exists
    """
    if request.method == "GET":
        return render(request, "create_note.html")

    if request.method == "POST":
        name = request.POST.get("restaurant")
        note = request.POST.get("restaurant_note")
        rating = int(request.POST.get("personal_rating"))
        email = request.session["user"]["email"]
        result = check_note_exists(email, name)
        if len(result) == 1:
            add_note(email, name, note, rating)
            return JsonResponse({"success": name})
        if len(result["Notes"]) == 0:
            add_note(email, name, note, rating)
            return JsonResponse({"success": name})
        return JsonResponse({"Error": "Note Already Exists"})


def view_notes(request):
    """Purpose: To view notes of a given user
    Parameters: N/a
    Return Value: On success note_viewer.html page with users notes
                    On no notes found it will display note_viewer.html with window telling user to add notes
    """
    if request.method == "GET":
        # note_collection = []
        email = request.session["user"]["email"]
        user_notes = get_one_user(email)
        del user_notes["_id"]
        del user_notes["email"]
        del user_notes["password"]
        try:
            if len(user_notes["Notes"]) > 0:
                # user_notes = order_notes_name(request)
                # user_notes = order_notes_rating(request)
                # user_notes = order_notes_date(request)
                return render(request, "note_viewer.html", {"notes": user_notes})
        except Exception as e:
            return render(request, "note_viewer.html", {"error": "Add Some Notes!"})
        return render(request, "note_viewer.html", {"error": "Add Some Notes!"})

    # if request.method == "POST":
    #     ordering = request.POST.get('ordering')
    #     print(ordering)
    #     if ordering == 'name':
    #         user_notes = order_notes_name(request)
    #     if ordering == 'rating':
    #         user_notes = order_notes_rating(request)
    #         user_notes['Notes'][-1] = 'AAA'
    #         print(user_notes)
    #     if ordering == 'date':
    #         user_notes = order_notes_date(request)
    #     return JsonResponse({'Success': user_notes})


def delete_user_note(request):
    """Purpose: To remove a users note
    Parameters: N/a
    Return Value: JsonResponse notifying the user whether note is successfuly removed or not
    """
    restaurant_name = request.POST.get("restaurant_name")
    email = request.session["user"]["email"]
    notes_found = delete_note(email, restaurant_name)
    # print(notes_found, 'GG')
    if notes_found:
        return JsonResponse({"Success": notes_found})
    return JsonResponse({"Error": "Not Founds"})

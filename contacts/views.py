from django.shortcuts import render
from .models import Contact

# Create your views here.
def index(request):
    _contacts = Contact.objects.all()
    return render(request, 'contacts/index.html', {
        'contacts': _contacts
    })

def show_contact(request, contact_id):
    _contact = Contact.objects.get(id=contact_id)
    return render(request, 'contacts/show_contact.html', {
        'contact': _contact
    })
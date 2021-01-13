from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages
from .models import Contact


def index(request):
    _contacts = Contact.objects.order_by('id').filter(
        show=True
    )  # order_by('-name') desc order
    paginator = Paginator(_contacts, 10)  # Show 10 contacts per page.
    page_number = request.GET.get('p')
    _contacts = paginator.get_page(page_number)

    return render(request, 'contacts/index.html', {
        'contacts': _contacts
    })


def show_contact(request, contact_id):
    _contact = get_object_or_404(Contact, id=contact_id)

    if not _contact.show:
        raise Http404()

    return render(request, 'contacts/show_contact.html', {
        'contact': _contact
    })


def search(request):
    _search_term = request.GET.get('search_term')

    if _search_term is None or not _search_term:
        messages.add_message(
            request,
            messages.ERROR,
            'Search field cannot be empty.'
        )
        return redirect('index')

    fields = Concat('name', Value(' '), 'last_name')

    _contacts = Contact.objects.annotate(
        full_name=fields
    ).filter(
        Q(full_name__icontains=_search_term) | Q(phone__icontains=_search_term)
    )

    paginator = Paginator(_contacts, 10)  # Show 10 contacts per page.
    page_number = request.GET.get('p')
    _contacts = paginator.get_page(page_number)

    return render(request, 'contacts/index.html', {
        'contacts': _contacts
    })

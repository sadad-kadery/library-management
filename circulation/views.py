import json
import logging
from collections import defaultdict
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from catalog.models import Item, Book, Music, Toy
from .forms import BorrowForm, ReturnForm
from .models import Borrower, Loan, Fine

logger = logging.getLogger(__name__)

DAILY_LATE_RATE = 0.50
LOAN_PERIOD_DAYS = 14


def is_reception(user):
    return user.is_superuser or user.groups.filter(name='Reception').exists()


@never_cache
@login_required(login_url='/reception/login/')
@user_passes_test(is_reception, login_url='/reception/login/')
def borrow_item(request):
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if not form.is_valid():
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect('borrow_item')

        code = form.cleaned_data['library_code'].strip().upper()

        try:
            with transaction.atomic():
                item = Item.objects.select_for_update().get(library_code=code)

                if item.status != 'AVAILABLE':
                    messages.error(
                        request,
                        f"'{item.name}' can't be borrowed — current status is {item.get_status_display()}."
                    )
                    return redirect('borrow_item')

                borrower, _ = Borrower.objects.get_or_create(
                    email=form.cleaned_data['email'],
                    defaults={
                        'name': form.cleaned_data['name'],
                        'phone': form.cleaned_data.get('phone', ''),
                    },
                )

                due_date = timezone.now() + timedelta(days=LOAN_PERIOD_DAYS)
                item.borrow()
                Loan.objects.create(item=item, borrower=borrower, due_at=due_date)

            messages.success(
                request,
                f"'{item.name}' borrowed by {borrower.name}. Due back {due_date.strftime('%d %b %Y')}."
            )
        except Item.DoesNotExist:
            messages.error(request, f"No item found with code '{code}'.")
        except Exception:
            logger.exception("Unexpected error while borrowing '%s'", code)
            messages.error(request, "Something went wrong on our end — please try again.")

        return redirect('borrow_item')

    return render(request, 'circulation/borrow.html', {'form': BorrowForm()})


@never_cache
@login_required(login_url='/reception/login/')
@user_passes_test(is_reception, login_url='/reception/login/')
def return_item(request):
    if request.method == 'POST':
        form = ReturnForm(request.POST)
        if not form.is_valid():
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect('return_item')

        code = form.cleaned_data['library_code'].strip().upper()

        try:
            with transaction.atomic():
                item = Item.objects.select_for_update().get(library_code=code)

                loan = (
                    Loan.objects.select_for_update()
                    .filter(item=item, status='BORROWED')
                    .order_by('-borrowed_at')
                    .first()
                )
                if loan is None:
                    messages.error(request, f"'{item.name}' isn't currently marked as borrowed.")
                    return redirect('return_item')

                loan.returned_at = timezone.now()
                loan.status = 'RETURNED'
                loan.save()
                item.return_item()

                if loan.returned_at > loan.due_at:
                    days_late = (loan.returned_at.date() - loan.due_at.date()).days
                    fine_amount = days_late * DAILY_LATE_RATE
                    Fine.objects.create(loan=loan, amount=fine_amount)
                    messages.warning(
                        request,
                        f"'{item.name}' returned {days_late} day(s) late — a ${fine_amount:.2f} fine was added."
                    )
                else:
                    messages.success(request, f"'{item.name}' returned. Thanks!")
        except Item.DoesNotExist:
            messages.error(request, f"No item found with code '{code}'.")
        except Exception:
            logger.exception("Unexpected error while returning '%s'", code)
            messages.error(request, "Something went wrong on our end — please try again.")

        return redirect('return_item')

    return render(request, 'circulation/return.html', {'form': ReturnForm()})


@never_cache
@login_required(login_url='/reception/login/')
@user_passes_test(is_reception, login_url='/reception/login/')
def add_item(request):
    if request.method == 'POST':
        item_type = request.POST.get('item_type')
        code = request.POST.get('library_code', '').strip().upper()
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()

        if Item.objects.filter(library_code=code).exists():
            messages.error(request, f"Library code '{code}' is already in use.")
            return redirect('add_item')

        try:
            if item_type == 'BOOK':
                Book.objects.create(
                    library_code=code,
                    name=name,
                    description=description,
                    author=request.POST.get('author', ''),
                    genre=request.POST.get('genre', ''),
                )
            elif item_type == 'MUSIC':
                Music.objects.create(
                    library_code=code,
                    name=name,
                    description=description,
                    artist=request.POST.get('artist', ''),
                    year=request.POST.get('year') or None,
                )
            elif item_type == 'TOY':
                Toy.objects.create(
                    library_code=code,
                    name=name,
                    description=description,
                    type=request.POST.get('type', ''),
                    age=request.POST.get('age', ''),
                )
            else:
                messages.error(request, "Please select an item type.")
                return redirect('add_item')

            messages.success(request, f"'{name}' added with code {code}.")
        except Exception:
            logger.exception("Error adding new item")
            messages.error(request, "Something went wrong — please check the details and try again.")

        return redirect('add_item')

    return render(request, 'circulation/add_item.html')


@never_cache
@login_required(login_url='/reception/login/')
@user_passes_test(is_reception, login_url='/reception/login/')
def manage_fines(request):
    if request.method == 'POST':
        try:
            fine = Fine.objects.select_related('loan__borrower').get(
                id=request.POST.get('fine_id'),
                status='UNPAID',
            )
            fine.status = 'PAID'
            fine.save()
            messages.success(
                request,
                f"${fine.amount:.2f} fine for {fine.loan.borrower.name} marked as paid.",
            )
        except Fine.DoesNotExist:
            messages.error(request, "That fine wasn't found, or was already marked paid.")
        return redirect('manage_fines')

    fines = (
        Fine.objects.select_related('loan__borrower', 'loan__item')
        .filter(status='UNPAID')
        .order_by('-id')
    )
    return render(request, 'circulation/manage_fines.html', {'fines': fines})

def is_manager(user):
    return user.is_superuser or user.groups.filter(name='Manager').exists()


@never_cache
def reception_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if is_reception(user):
                auth_login(request, user)
                return redirect('reception_dashboard')
            messages.error(request, "This account doesn't have Reception access.")
    else:
        form = AuthenticationForm()
    return render(request, 'circulation/reception_login.html', {'form': form})


@never_cache
def manager_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if is_manager(user):
                auth_login(request, user)
                return redirect('manager_dashboard')
            messages.error(request, "This account doesn't have Manager access.")
    else:
        form = AuthenticationForm()
    return render(request, 'circulation/manager_login.html', {'form': form})


class ReceptionRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/reception/login/'

    def test_func(self):
        return is_reception(self.request.user)


@method_decorator(never_cache, name='dispatch')
class BorrowerListView(ReceptionRequiredMixin, ListView):
    model = Borrower
    template_name = 'circulation/borrower_list.html'
    context_object_name = 'borrowers'


@method_decorator(never_cache, name='dispatch')
class BorrowerCreateView(ReceptionRequiredMixin, CreateView):
    model = Borrower
    fields = ['name', 'email', 'phone']
    template_name = 'circulation/borrower_form.html'
    success_url = reverse_lazy('borrower_list')


@method_decorator(never_cache, name='dispatch')
class BorrowerUpdateView(ReceptionRequiredMixin, UpdateView):
    model = Borrower
    fields = ['name', 'email', 'phone']
    template_name = 'circulation/borrower_form.html'
    success_url = reverse_lazy('borrower_list')


@method_decorator(never_cache, name='dispatch')
class BorrowerDeleteView(ReceptionRequiredMixin, DeleteView):
    model = Borrower
    template_name = 'circulation/borrower_confirm_delete.html'
    success_url = reverse_lazy('borrower_list')


@never_cache
@login_required(login_url='/manager/login/')
@user_passes_test(is_manager, login_url='/manager/login/')
def stats_borrowing(request):
    counts = defaultdict(lambda: defaultdict(int))
    for loan in Loan.objects.select_related('item'):
        counts['All'][loan.item.name] += 1
        counts[loan.item.item_type][loan.item.name] += 1

    tabs = {}
    for category in ['All', 'Book', 'Music', 'Toy']:
        top = sorted(counts[category].items(), key=lambda pair: -pair[1])[:10]
        tabs[category] = {
            'rows': top,
            'labels': json.dumps([name for name, _ in top]),
            'values': json.dumps([count for _, count in top]),
        }

    return render(request, 'circulation/stats_borrowing.html', {
        'tabs': tabs,
    })


@never_cache
@login_required(login_url='/manager/login/')
@user_passes_test(is_manager, login_url='/manager/login/')
def stats_items(request):
    items = Item.objects.all().order_by('name')
    by_status = Item.objects.values('status').annotate(count=Count('id'))
    return render(request, 'circulation/stats_items.html', {
        'items': items,
        'by_status': by_status,
        'chart_labels': json.dumps([row['status'] for row in by_status]),
        'chart_values': json.dumps([row['count'] for row in by_status]),
    })


@never_cache
@login_required(login_url='/manager/login/')
@user_passes_test(is_manager, login_url='/manager/login/')
def stats_fines(request):
    fines = Fine.objects.select_related('loan__borrower', 'loan__item').order_by('-id')
    by_status = Fine.objects.values('status').annotate(total=Sum('amount'))
    owed_by_borrower = (
        Fine.objects.filter(status='UNPAID')
        .values('loan__borrower__name')
        .annotate(total_owed=Sum('amount'))
        .order_by('-total_owed')
    )
    return render(request, 'circulation/stats_fines.html', {
        'fines': fines,
        'owed_by_borrower': owed_by_borrower,
        'by_status': by_status,
        'chart_labels': json.dumps([row['status'] for row in by_status]),
        'chart_values': json.dumps([float(row['total'] or 0) for row in by_status]),
    })


def public_search(request):
    q = request.GET.get('q', '').strip()
    items = Item.objects.exclude(status='DESTROY').order_by('name')
    if q:
        items = items.filter(name__icontains=q)

    active_loans = {
        loan.item_id: loan.borrower.name
        for loan in Loan.objects.filter(status='BORROWED').select_related('borrower')
    }
    for item in items:
        item.borrowed_by = active_loans.get(item.id)

    return render(request, 'circulation/public_search.html', {'items': items, 'q': q})


@login_required(login_url='/reception/login/')
@user_passes_test(is_reception, login_url='/reception/login/')
def item_lookup(request):
    code = request.GET.get('code', '').strip().upper()
    try:
        item = Item.objects.get(library_code=code)
    except Item.DoesNotExist:
        return JsonResponse({'found': False})
    return JsonResponse({
        'found': True,
        'name': item.name,
        'status_display': item.get_status_display(),
    })


@login_required(login_url='/reception/login/')
@user_passes_test(is_reception, login_url='/reception/login/')
def borrower_lookup(request):
    email = request.GET.get('email', '').strip()
    try:
        borrower = Borrower.objects.get(email=email)
    except Borrower.DoesNotExist:
        return JsonResponse({'found': False})
    return JsonResponse({'found': True, 'name': borrower.name, 'phone': borrower.phone})


@login_required(login_url='/reception/login/')
@user_passes_test(is_reception, login_url='/reception/login/')
def reception_dashboard(request):
    return render(request, 'circulation/reception_dashboard.html')


@login_required(login_url='/manager/login/')
@user_passes_test(is_manager, login_url='/manager/login/')
def manager_dashboard(request):
    return render(request, 'circulation/manager_dashboard.html')
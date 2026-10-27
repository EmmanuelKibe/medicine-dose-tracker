from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Medicine
from .forms import MedicineForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('medicine_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# 1. READ & CREATE View (Account Dashboard)
@login_required
def medicine_list(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.user = request.user  # Attach current user before saving
            medicine.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm()
    
    # Filter medicines so users only see their own
    medicines = Medicine.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tracker/medicine_list.html', {'medicines': medicines, 'form': form})

# 2. UPDATE View
@login_required
def medicine_update(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'tracker/medicine_form.html', {'form': form, 'medicine': medicine})

# 3. DELETE View
@login_required
def medicine_delete(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk, user=request.user)
    if request.method == 'POST':
        medicine.delete()
        return redirect('medicine_list')
    return render(request, 'tracker/medicine_confirm_delete.html', {'medicine': medicine})
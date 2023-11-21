from django.shortcuts import render
from django.views.generic import View
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

# Create your views here.
@method_decorator(staff_member_required, name='dispatch')
class Dashboard(View, LoginRequiredMixin ):

    def get(self, request):

        return render(request,'dashboard/index.html')
 
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect

from .models import Group, Sticker, Team


def get_progress_class(progress):
    if progress <= 30:
        return 'bg-danger'

    if progress > 30 and progress <= 60:
        return 'bg-warning'

    return 'bg-success'


class MissingStickersView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'album/missing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams'] = []
        for group in Group.objects.all().order_by('sort_order'):
            for team in group.teams.all().order_by('sort_order'):
                range = list(team.sticker_range)
                stickers = Sticker.objects.filter(team=team, owner=self.request.user)
                for sticker in stickers:
                    range.remove(sticker.number)

                context['teams'].append({
                    'name': team.name,
                    'code': team.code,
                    'missing': range
                })

        return context


class MarkView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'album/mark.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        context['stickers'] = []
        for sticker in Sticker.objects.filter(owner=self.request.user):
            context['stickers'].append(f'{sticker.team.pk}_{sticker.number}')

        return context


class StatsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'album/stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['stats'] = {
            'global': {
                'total': 0,
                'owned': 0,
                'missing': 0,
                'progress': 0
            },
            'groups': []
        }

        for group in Group.objects.all().order_by('sort_order'):
            group_obj = {
                'total': 0,
                'id': group.pk,
                'name': group.name,
                'owned': 0,
                'missing': 0,
                'progress': 0,
                'teams': []
            }

            for team in group.teams.all().order_by('sort_order'):
                team_sticker_count = Sticker.objects.filter(team=team, owner=self.request.user).count()
                team_obj = {
                    'total': team.sticker_max,
                    'name': team.name,
                    'code': team.code,
                    'flag': team.flag,
                    'owned': team_sticker_count,
                    'missing': team.sticker_max - team_sticker_count,
                    'progress': round((team_sticker_count * 100) / team.sticker_max),
                    'progress_class': get_progress_class(round((team_sticker_count * 100) / team.sticker_max))
                }

                group_obj['total'] += team_obj['total']
                group_obj['owned'] += team_obj['owned']
                group_obj['missing'] += team_obj['missing']
                group_obj['teams'].append(team_obj)

            group_obj['progress'] = round((group_obj['owned'] * 100) / group_obj['total'])
            group_obj['progress_class'] = get_progress_class(round((group_obj['owned'] * 100) / group_obj['total']))

            context['stats']['global']['total'] += group_obj['total']
            context['stats']['global']['owned'] += group_obj['owned']
            context['stats']['global']['missing'] += group_obj['missing']
            context['stats']['global']['progress'] = round((context['stats']['global']['owned'] * 100) / context['stats']['global']['total'])
            context['stats']['global']['progress_class'] = get_progress_class(round((context['stats']['global']['owned'] * 100) / context['stats']['global']['total']))

            context['stats']['groups'].append(group_obj)

        return context


class LoginView(View):
    def get(self, request):
        return render(request, 'album/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        
        return render(request, 'album/login.html')

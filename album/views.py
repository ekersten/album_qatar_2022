from django.views.generic import TemplateView

from .models import Group, Sticker, Team


class MissingStickersView(TemplateView):
    template_name = 'album/missing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams'] = []
        for team in Team.objects.all():
            range = list(team.sticker_range)
            stickers = Sticker.objects.filter(team=team)
            for sticker in stickers:
                range.remove(sticker.number)

            context['teams'].append({
                'name': team.name,
                'missing': range
            })

        print(context)

        return context


class MarkView(TemplateView):
    template_name = 'album/mark.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        context['stickers'] = []
        for sticker in Sticker.objects.all():
            context['stickers'].append(f'{sticker.team.pk}_{sticker.number}')

        return context

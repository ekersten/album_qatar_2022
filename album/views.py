from django.views.generic import TemplateView

from .models import Group, Sticker


class GroupsView(TemplateView):
    template_name = 'album/groups.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        context['stickers'] = []
        for sticker in Sticker.objects.all():
            context['stickers'].append(f'{sticker.team.pk}_{sticker.number}')

        return context

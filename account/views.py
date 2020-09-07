from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import Profile, Relationship
from .forms import ProfileModelForm, SearchForm
from django.views.generic import ListView, DetailView


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password_repeat = request.POST['password_repeat']

        if password == password_repeat:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username already taken')
                return render(request, 'account/register.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exist')
                return render(request, 'account/register.html')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
               # Profile.objects.create(user=user)

                return render(request, 'account/register_done.html')

        else:
            messages.info(request, 'Passwords did not match.')
            return render(request, 'account/register.html')

    else:
        return render(request, 'account/register.html')


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'account/detail.html'

    def get_object(self, slug=None):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user.username)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['posts'] = self.get_object().get_all_authors_post()
        context['len_post'] = True if len(self.get_object().get_all_authors_post()) > 0 else False

        return context

def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'profile.html', context)


def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True

    context = {'qs': results,
               'is_empty': is_empty, }

    print(results)
    print('-----------')
    print(qs)
    return render(request, 'profiles/my_invites.html', context)


def invites_received_view2(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True

    context = {'qs': results,
               'is_empty': is_empty, }

   # print(results)
    #print('-----------')
   # print(qs)
    return render(request, 'profiles/my_invites2.html', context)


def accept_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('my-invites-view')


def reject_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('my-invites-view')


def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {'qs': qs}

    return render(request, 'profiles/to_invite_list.html', context)


def invite_profiles_list_views(request):
    user = request.user
    ap = Profile.objects.get_all_profiles_to_invite(user)

    context = {'ap': ap}

    return render(request, 'profiles/to_invite_list1.html', context)


def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {'qs': qs}

    return render(request, 'profiles/profile_list.html', context)


class ProfileLIstView(ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'

    context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=str(self.request.user))
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context


def send_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('my-profile-view')


def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get((Q(sender=sender)
                                        & Q(receiver=receiver)) | Q(sender=receiver) & Q(receiver=sender))
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('my-profile-view')


def friends_list(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    qs = Profile.get_friends(user)
    print(qs)
    context = {
        'qs': qs,
    }

    return render(request, 'profiles/friend_lists.html', context)


def people_you_mayKnow(request):
    profile = Profile.objects.get(user=request.user)
    people = Profile.objects.all()
    user = request.user
    people_you_mayknow = Profile.objects.get_all_profiles_to_invite(user)

    context = {
        'people': people_you_mayknow,
    }
    print(people_you_mayknow)
    print(profile)
    return render(request, 'profiles/peopple-you-may-know.html', context)


def user_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Profile.objects.annotate(search=SearchVector('first_name', 'last_name', 'user'),).filter(search=query)
    return render(request, 'profiles/search.html', {'form': form, 'query': query, 'results': results})
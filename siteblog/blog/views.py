from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
from .tasks import send_spam_email
from .models import *
from .forms import ContactForm
from .service import send
from django.db.models import F


class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Космос'
        return context


class PostByCategory(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class PostByTag(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Записи по тегу: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
        return context


class GetPost(FormMixin, DetailView):
    model = Post
    form_class = ContactForm
    template_name = 'blog/single.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


class Search(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context


# def index(request):
#     zastavka = Zastavka.objects.get(id=1)
#     return render(request, 'blog/index.html', {'zAsTaVkA': zastavka,)


def zastavka(request):
    zastavka = Zastavka.objects.all()
    return render(request, 'blog/zastavka.html', {'zAsTaVkA': zastavka, 'nazvanie': 'Заставка'})

#
# def contact(request):
#     return render(request, 'blog/contact.html')


class ContactView(CreateView):
    """Отображение формы подписки по email"""
    model = Contact
    form_class = ContactForm
    success_url = '/'
    template_name = 'blog/single.html'

    def form_valid(self, form):
        form.save()
        # send(form.instance.email)
        send_spam_email.delay(form.instance.email)
        return super().form_valid(form)


# def send_email(request):
#     if request.method == 'POST':
#         form = ContactEmail(request.POST)
#         if form.is_valid():
#             Contact.objects.create(**form.cleaned_data)
#             # print(form.cleaned_data)
#             return redirect('home')
#     else:
#         form = ContactEmail()
#     return render(request, 'blog/send_email.html', {'form': form})
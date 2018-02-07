from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail
from .models import Post
from .forms import EmailPostForm




class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


# def post_list(request):
#     posts = Post.published.all()
#
#     # Paginator
#     object_list = Post.objects.all()
#     paginator = Paginator(object_list, 3)
#     page = request.GET.get('page')
#     # context = {'page':page,'posts': posts}
#
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)
#     return render(request, 'blog/post/list.html',{'page':page,'posts': posts})



def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    context = {'post': post}
    return render(request,'blog/post/detail.html', context)


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # if the forms is valid, we retrieve the validated data accessing
            # form.cleaned_data.This attribute is a dictionary of form fields
            # and their values.
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} recomendou você ler "{}"'.format(cd['name'], post.title)
            message = 'Leia "{}" no seguinte link: \n{}\n\n{} comentou: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'marshalmori@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

from django.shortcuts import render,redirect
from django.views.generic import TemplateView,DetailView,FormView
from writers_app.models import Blog
from .forms import CommentForm
from .models import Comment
from django.contrib import messages
from django.urls import reverse_lazy
# Create your views here.

class ViewerHomeView(TemplateView):
    template_name="viewer_home.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["blog"]=Blog.objects.all()
        return context

    
class ViewerDetailView(TemplateView):
    template_name = "viewer_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # blog = get_object_or_404(Blog, pk=kwargs["pk"])
        blog=Blog.objects.get(id=kwargs["id"])
        context['blog']=blog
        context['form']=CommentForm()
        context['comments']=Comment.objects.filter(blog=blog)
        return context
        


    def post(self, request, *args, **kwargs):
        # blog = get_object_or_404(Blog, pk=kwargs["pk"])
        blog=Blog.objects.get(id=kwargs["id"])
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            messages.success(request,"Comment posted!")
            return redirect('viewerdetail_view', id=blog.id)

        # context = self.get_context_data()
        # context['form'] = form
        # context['comments'] = Comment.objects.filter(blog=blog).order_by('-created_at')
        # return self.render_to_response(context)




class AddCommentView(FormView):
    form_class=CommentForm
    model=Comment
    success_url=reverse_lazy('viewerdetail_view')

    def form_valid(self, form):
        # form.instance.blog=blog
        form.instance.user=self.request.user
        messages.success(self.request,"Comment Added!")
        return super().form_valid(form)
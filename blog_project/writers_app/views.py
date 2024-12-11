from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView,DetailView,DeleteView,UpdateView
from writers_app.forms import RegisterForm,LoginForm,CreateBlogForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User
from .models import Blog,UserProfile
from django.urls import reverse_lazy
from django.http import HttpResponse
from viewers_app.models import Comment
from viewers_app.forms import CommentForm
# from .models import UserProfile
# Create your views here.

class Home(TemplateView):
    template_name="index.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["blog"]=Blog.objects.filter(user=self.request.user)
        return context


class RegisterView(CreateView):
    template_name='reg.html'
    form_class=RegisterForm
    model=User
    # success_url=reverse_lazy('signin_view')

    def form_valid(self,form):
        User.objects.create_user(**form.cleaned_data)
        messages.success(self.request,"Registration Successful!")
        return redirect('login_view')
    
    def form_invalid(self, form):
        messages.warning(self.request,"User already registered!!")
        return redirect('reg_view')



class LoginView(View):
    def get(self,request):
        form=LoginForm()
        return render(request,'login.html',{"form":form})
    
    def post(self,request):
        form=LoginForm(request.POST)
        if form.is_valid():
            usname=form.cleaned_data['username']
            psw=form.cleaned_data['password']
            ust=form.cleaned_data['usertype']

        # usname=request.POST.get("username")
        # psw=request.POST.get("password")
        # ust=request.POST.get("usertype")
        user=authenticate(request,username=usname,password=psw)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            if ust=='writer':
                # login(request, user)
                # messages.success(request, "Login successful!")
                return redirect("home_view")
            elif ust=='viewer':
                    # login(request, user)
                    # messages.success(request, "Login successful!")
                return redirect("viewerhome_view")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login_view')
            # user=authenticate(request,username=usname,password=psw)
        # if user:
        #     login(request,user)
        #     messages.success(request,"Login Successful!")
        #     return redirect('home_view')
        # else:
        #     messages.warning(request,"Invalid Credentials!")
        #     return redirect('signin_view')
        
class LogoutView(View):
    def get(self,request):
        logout(request)
        messages.success(request,"Logout Successful!")
        return redirect('login_view')
    

class CreateBlogView(CreateView):
    template_name='create_blog.html'
    form_class=CreateBlogForm
    model=Blog
    success_url=reverse_lazy('home_view')

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"Blog Created!")
        return super().form_valid(form)
    

# class BlogListView(ListView):
#     template_name='index.html'
#     model=Blog
#     context_object_name="blog"

#     def get_queryset(self):
#         return Blog.objects.all(user=self.request.user)

class BlogDetailView(DetailView):
    model=Blog
    template_name="detail.html"
    context_object_name='blog'
    pk_url_kwarg="id"

    def get_queryset(self):
        return Blog.objects.filter(user=self.request.user)
        # return Blog.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog=self.get_object()
        context['form']=CommentForm()
        context['comments']=Comment.objects.filter(blog=blog)
        return context
    
    def post(self, request, *args, **kwargs):
        blog=self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog=blog
            comment.user=request.user
            comment.save()
            return redirect('detail_view', id=blog.id)
    
class BlogDeleteView(DeleteView):
    template_name="blog_delete.html"
    model=Blog
    pk_url_kwarg="id"
    success_url=reverse_lazy('home_view')

class BlogUpdateView(UpdateView):
    form_class=CreateBlogForm
    template_name='edit_blog.html'
    model=Blog
    pk_url_kwarg="id"
    success_url=reverse_lazy('home_view')
    
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Course, Video
from .forms import VideoForm

def index(request):
    """The home page for eLearning"""
    course_list = Course.objects.all()
    course1 = course_list[0]
    course2 = course_list[1]
    video = Video.objects.filter(course= course1)
    video1 = video[0]
    video = Video.objects.filter(course= course2)
    video2 = video[0]
    context = {
        'course1': course1,
        'course2': course2,
        'video1': video1,
        'video2': video2,
    }
    return render(request, 'eLearn/index.html', context)

@login_required
def main(request, course_id=0):
    """The main page for eLearning"""
    my_courses=[]
    authenticated_user = request.user

    if authenticated_user.userType == 2:
        my_courses = Course.objects.filter(professor_id=authenticated_user)
        if len(my_courses)!=0 and course_id == 0:
            selected_course = Course.objects.filter(professor_id=authenticated_user).latest('uploadDate')
        elif len(my_courses) == 0:
            selected_course = None
        else:
            selected_course = get_object_or_404(Course, id=course_id)
        videos = selected_course.modules.order_by('id')
        context = {'courses': my_courses,
                   'selected_course': selected_course,
                   'userType': "professor",
                   'videos': videos,
                   'user': authenticated_user}
        return render(request, 'eLearn/main.html', context)
    else:
        my_courses = Course.objects.all()
        if course_id == 0:
            selected_course = my_courses.latest('uploadDate')
        else:
            selected_course = get_object_or_404(Course, id=course_id)
        videos = selected_course.modules.order_by('id')
        context = {'courses': my_courses,
                   'selected_course': selected_course,
                   'userType': "student",
                   'videos': videos,
                   'user': authenticated_user
                   }
        return render(request, 'eLearn/main.html', context)

    return render(request, 'eLearn/main.html')

class CourseListView(ListView):
    model = Course
    template_name = 'eLearn/list.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_course = Course.objects.latest('uploadDate')
        context['selected_course'] = latest_course
        my_courses = Course.objects.filter(professor_id=self.request.user)

        authenticated_user = self.request.user
        if authenticated_user.userType == 2:
            context['userType'] = "professor"
        else:
            context['userType'] = "student"

        context['courses'] = my_courses

        return context

class CourseCreateView(CreateView):
    model = Course
    fields = ['name', 'slug', 'description']
    success_url = reverse_lazy('eLearn:list_course')
    template_name = 'eLearn/form.html'

    def form_valid(self, form):
         professor = self.request.user
         form.instance.professor = professor
         return super(CourseCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_course = Course.objects.latest('uploadDate')
        context['selected_course'] = latest_course

        authenticated_user = self.request.user
        context['courses'] = Course.objects.filter(professor_id=self.request.user)
        if authenticated_user.userType == 2:
            context['userType'] = "professor"
        else:
            context['userType'] = "student"

        return context

class CourseUpdateView(UpdateView):
    model = Course
    fields = ['name', 'slug', 'description']
    success_url = reverse_lazy('eLearn:list_course')
    template_name = 'eLearn/form.html'

    def form_valid(self, form):
         professor = self.request.user
         form.instance.professor = professor
         return super(CourseUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_course = Course.objects.latest('uploadDate')
        context['selected_course'] = latest_course
        context['courses'] = Course.objects.filter(professor_id=self.request.user)

        authenticated_user = self.request.user
        if authenticated_user.userType == 2:
            context['userType'] = "professor"
        else:
            context['userType'] = "student"

        return context

class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'eLearn/delete.html'
    success_url = reverse_lazy('eLearn:list_course')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_course = Course.objects.latest('uploadDate')
        context['selected_course'] = latest_course
        context['courses'] = Course.objects.filter(professor_id=self.request.user)

        authenticated_user = self.request.user
        if authenticated_user.userType == 2:
            context['userType'] = "professor"
        else:
            context['userType'] = "student"

        return context

def list_video(request, course_id):
    """Show a single course and it's videos."""
    courses = Course.objects.filter(professor_id = request.user)
    course = get_object_or_404(Course, id=course_id)

    latest_course = Course.objects.latest('uploadDate')

    if course.professor != request.user:
        raise Http404

    videos = course.modules.order_by('id')
    context = {'courses': courses,
               'course': course,
               'videos': videos,
               'userType': "professor",
               'selected_course': latest_course}
    return render(request, 'eLearn/videolist.html', context)

def create_video(request, course_id):
    """Create a new video for the course."""
    courses = Course.objects.filter(professor_id = request.user)
    course = get_object_or_404(Course, id=course_id)
   
    latest_course = Course.objects.latest('uploadDate')

    if course.professor != request.user:
        raise Http404

    if request.method != 'POST':
        form = VideoForm()
    else:
        form = VideoForm(data=request.POST)
        if form.is_valid():
            new_video = form.save(commit=False)
            new_video.course = course
            new_video.save()
            return HttpResponseRedirect(reverse('eLearn:list_video',
                                                args=[course_id]))

    context = {'form': form,
               'courses': courses,
               'userType': "professor",
               'selected_course': latest_course}
    return render(request, 'eLearn/create_video.html', context)

def edit_video(request, video_id):
    """Edit a single video."""
    courses = Course.objects.filter(professor_id = request.user)
    video = get_object_or_404(Video, id=video_id)
    course = video.course

    latest_course = Course.objects.latest('uploadDate')

    if course.professor != request.user:
        raise Http404

    if request.method != 'POST':
        form = VideoForm(instance=video)
    else:
        # POST data submitted; process data.
        form = VideoForm(instance=video, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('eLearn:list_video',
                                                args=[course.id]))

    context = {'form': form,
               'courses': courses,
               'userType': "professor",
               'selected_course': latest_course}
    return render(request, 'eLearn/create_video.html', context)
    

def delete_video(request, video_id):
    """Delete a single video."""
    video = get_object_or_404(Video, id=video_id)
    course = video.course

    if course.professor != request.user:
        raise Http404

    video.delete()
    return HttpResponseRedirect(reverse('eLearn:list_video',
                                        args=[course.id]))



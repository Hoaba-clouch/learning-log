from django.shortcuts import render
from django.shortcuts import render,  redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
	"""The home page for Learning Log"""
	return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
	"""Show all topics."""
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')
	context = {'topics': topics}
	return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
	"""Show a single topic and all its entries."""
	topic = get_object_or_404(Topic, id=topic_id)

	# Make sure the topic belongs to the current user.
	if topic.owner != request.user:
		raise Http404

	entries = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entries': entries}
	return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
	"""Add a new topic."""
	if request.method != 'POST':
		# No data submitted; create a blank form.
		form = TopicForm()
	else:
		# POST data submitted; process data.
		form = TopicForm(request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
			return HttpResponseRedirect(reverse('learning_logs:topics'))
	
	context = {'form': form}
	return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
	"""Add a new entry for a particular topic."""
	topic = Topic.objects.get(id=topic_id)

	if request.method != 'POST':
		# No data submitted; create a blank form.
		form = EntryForm()
	else:
		# POST data submitted; process data.
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
	context = {'topic': topic, 'form': form}
	return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
	"""Edit an existing entry."""
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic

	if topic.owner != request.user:
		raise Http404

	if request.method != 'POST':
		# Initial request; pre-fill form with the current entry.
		form = EntryForm(instance=entry)
	else:
		# POST data submitted; process data.
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('learning_logs:topic',
			args=[topic.id]))
			
	context = {'entry': entry, 'topic': topic, 'form': form}
	return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def delete_entry(request, entry_id):
    """Xóa một ghi chú (Entry) cụ thể."""
    entry = get_object_or_404(Entry, id=entry_id)

    # 1. KIỂM TRA QUYỀN SỞ HỮU (BẢO MẬT BẮT BUỘC)
    if entry.topic.owner != request.user:
        raise Http404

    # Lấy ID của Topic trước khi xóa Entry (để chuyển hướng về trang Topic đó)
    topic_id = entry.topic.id

    if request.method == 'POST':
        # 2. XÓA DỮ LIỆU
        entry.delete()
        # 3. CHUYỂN HƯỚNG
        return redirect('learning_logs:topic', topic_id=topic_id)
        
    # Nếu là GET request, có thể hiển thị trang xác nhận xóa
    return render(request, 'learning_logs/delete_confirm.html', {'entry': entry})\
@login_required
def delete_topic(request, topic_id):
    """Xóa một chủ đề (Topic) cụ thể."""
    
    # 1. Truy vấn đối tượng Topic
    topic = get_object_or_404(Topic, id=topic_id)
    
    # 2. KIỂM TRA QUYỀN SỞ HỮU (Bảo mật bắt buộc)
    if topic.owner != request.user:
        raise Http404

    if request.method == 'POST':
        # 3. THỰC HIỆN XÓA (CASCADE sẽ xóa tất cả Entry liên quan)
        topic.delete()
        
        # 4. CHUYỂN HƯỚNG về trang danh sách Topics
        return redirect('learning_logs:topics')
    
    # Tùy chọn: nếu huynh muốn có trang xác nhận riêng, hãy render template đó
    # Ví dụ: return render(request, 'learning_logs/topic_delete_confirm.html', {'topic': topic})

    # Nếu không có trang xác nhận, ta có thể chuyển hướng về trang topics nếu không phải POST
    return redirect('learning_logs:topics')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def index(request):
    context = {}
    return render(request, 'learning_logs/index.html', context)


def topics(request):
    if request.user.is_authenticated:
        own_topics = Topic.objects.filter(owner=request.user)
        public_topics = Topic.objects.filter(public=True).exclude(owner=request.user)
        topic_list = own_topics | public_topics
    else:
        topic_list = Topic.objects.filter(public=True)
    topic_list = topic_list.order_by('-date_added')

    # 分页
    paginator = Paginator(topic_list, 15)
    page_num = request.GET.get('page', 1)
    topics = paginator.get_page(page_num)

    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    is_owner = request.user == topic.owner

    if (topic.owner != request.user) and (not topic.public):
        return render(request, "404.html", status=404)

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries, 'is_owner': is_owner}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            if request.LANGUAGE_CODE == "zh-hans":
                request.session["toast_msg"] = "主题创建成功"
            else:
                request.session["toast_msg"] = "Topic created successfully"
            return redirect('learning_logs:topics')
        else:
            if request.LANGUAGE_CODE == "zh-hans":
                request.session["toast_msg"] = "主题名称不能为空"
            else:
                request.session["toast_msg"] = "Topic name cannot be empty"

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            if request.LANGUAGE_CODE == "zh-hans":
                request.session["toast_msg"] = "笔记新增成功"
            else:
                request.session["toast_msg"] = "Entry added successfully"
            return redirect('learning_logs:topic', topic_id=topic_id)
        else:
            if request.LANGUAGE_CODE == "zh-hans":
                request.session["toast_msg"] = "笔记内容不能为空"
            else:
                request.session["toast_msg"] = "Entry content cannot be empty"

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        return render(request, "404.html", status=404)

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            if request.LANGUAGE_CODE == "zh-hans":
                request.session["toast_msg"] = "笔记修改成功"
            else:
                request.session["toast_msg"] = "Entry saved successfully"
            return redirect('learning_logs:topic', topic_id=topic.id)
        else:
            if request.LANGUAGE_CODE == "zh-hans":
                request.session["toast_msg"] = "笔记内容不能为空"
            else:
                request.session["toast_msg"] = "Entry content cannot be empty"

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)

    if request.method == "POST":
        topic.delete()
        if request.LANGUAGE_CODE == "zh-hans":
            request.session["toast_msg"] = "主题已删除"
        else:
            request.session["toast_msg"] = "Topic deleted"
        return redirect("learning_logs:topics")

    context = {"topic": topic}
    return render(request, "learning_logs/confirm_delete_topic.html", context)


@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        return render(request, "404.html", status=404)

    if request.method == "POST":
        entry.delete()
        if request.LANGUAGE_CODE == "zh-hans":
            request.session["toast_msg"] = "笔记已删除"
        else:
            request.session["toast_msg"] = "Entry deleted"
        return redirect("learning_logs:topic", topic_id=topic.id)

    context = {"entry": entry, "topic": topic}
    return render(request, "learning_logs/confirm_delete_entry.html", context)
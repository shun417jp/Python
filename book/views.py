from django.views import generic
from .models import Shelf, Review, Note
from .form import NoteForm
from django.core.exceptions import PermissionDenied
from django.urls import reverse,reverse_lazy
from django.db.models import Avg
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin


class ListBookView(generic.ListView):
    template_name = 'book/book_list.html'
    model = Shelf
    context_object_name = 'Shelf'
    queryset = Shelf.objects.all().order_by('-id')  # 登録順（降順）に並べ替え

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # レビュー平均でソートして上位3冊を取得
        ranking_list = (
            Shelf.objects.annotate(avg_rating=Avg('reviews__rate')).order_by('-avg_rating')[:3]  # 修正部分
        )
        context['ranking_list'] = ranking_list
        return context
    
class DetailBookView(generic.DetailView):
    template_name = 'book/book_detail.html'
    model = Shelf
    context_object_name = 'Shelf'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 本に関連するレビューを取得
        reviews = Review.objects.filter(book=self.object).order_by('-id')  # 最新のレビュー順
        paginator = Paginator(reviews, 3)  # 1ページに3件表示
        page_number = self.request.GET.get('page')
        context['reviews'] = paginator.get_page(page_number)
        
        # ノートは削除して、ノートを表示するのは NoteListView に変更
        return context
    
        
class CreateBookView(LoginRequiredMixin, generic.CreateView):
    template_name = 'book/book_create.html'
    model = Shelf
    context_object_name = 'Shelf'
    fields = ('title', 'text', 'category', 'thumbnail')
    success_url = reverse_lazy('list-book')
    
    def form_valid(self, form):
        form.instance.user = self.request.user  # ログイン中のユーザーを設定
        return super().form_valid(form)
    
class DeleteBookView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'book/book_confirm_delete.html'
    model = Shelf
    context_object_name = 'Shelf'
    success_url = reverse_lazy('list-book')
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied('削除権限がありません。')
        return super(DeleteBookView, self).dispatch(request, *args, **kwargs)
    
class UpdateBookView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'book/book_update.html'
    model = Shelf
    context_object_name = 'Shelf'
    fields = ('title', 'text', 'category', 'thumbnail')
    success_url = reverse_lazy('list-book')
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied('編集権限がありません。')
        return super(UpdateBookView, self).dispatch(request, *args, **kwargs)
        
class CreateReviewView(LoginRequiredMixin, generic.CreateView):
    model = Review
    fields = ('book', 'title', 'text', 'rate')
    template_name = 'book/review_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Shelf.objects.get(pk=self.kwargs['book_id'])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk':self.object.book.id})
    
class CreateNoteView(LoginRequiredMixin, generic.CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'book/note_add.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.book = Shelf.objects.get(pk=self.kwargs['book_id'])  # ノートと本を紐づける
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('note-list')  # ノート一覧へ遷移


class DeleteNoteView(LoginRequiredMixin, generic.DeleteView):
    model = Note
    template_name = 'book/note_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied('削除権限がありません。')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk': self.object.book.id})
    
class UpdateNoteView(LoginRequiredMixin, generic.UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'book/note_update.html'  # ここを確認
    context_object_name = 'note'

    def get_success_url(self):
        return reverse('note-detail', kwargs={'pk': self.object.pk})  # 更新後に詳細ページへ

class NoteListView(LoginRequiredMixin, generic.ListView):
    model = Note
    template_name = 'book/note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by('-created_at')  # ユーザーのノートを取得

class NoteDetailView(LoginRequiredMixin, generic.DetailView):
    model = Note
    template_name = 'book/note_detail.html'
    context_object_name = 'note'  # ここを追加
    
class UserNoteListView(LoginRequiredMixin, generic.ListView):
    model = Note
    template_name = 'book/note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by('-created_at')  # ログインユーザーのノートのみ


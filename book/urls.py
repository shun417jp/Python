from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListBookView.as_view(), name='list-book'),
    path('book/<int:pk>/detail/', views.DetailBookView.as_view(), name='detail-book'),
    path('book/create/', views.CreateBookView.as_view(), name='create-book'),
    path('book/<int:pk>/delete/', views.DeleteBookView.as_view(), name='delete-book'),
    path('book/<int:pk>/update/', views.UpdateBookView.as_view(), name='update-book'),
    path('book/<int:book_id>/review/', views.CreateReviewView.as_view(), name='review'),
    path('book/<int:book_id>/note/add/', views.CreateNoteView.as_view(), name='add-note'),
    path('notes/', views.NoteListView.as_view(), name='note-list'),  # ノート一覧
    path('note/<int:pk>/', views.NoteDetailView.as_view(), name='note-detail'),  # ノート詳細
    path('note/<int:pk>/update/', views.UpdateNoteView.as_view(), name='update-note'),  # ノート編集
    path('note/<int:pk>/delete/', views.DeleteNoteView.as_view(), name='delete-note'),  # ノート削除

# ログインユーザーのノート一覧（ヘッダーのリンク用）
path('notes/', views.UserNoteListView.as_view(), name='note-list'),


    

]
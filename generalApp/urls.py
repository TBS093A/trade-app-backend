from django.urls import path

from . import views

urlpatterns = [
    path('authUser', views.authUser),
    path('user', views.users),
    path('user/<int:id>', views.user),

    path('thread', views.threads),
    path('thread/<int:id>', views.thread),
    path('thread/<int:threadID>/subject', views.subjects),
    path('subject/<int:id>', views.subject),
    path('subject/<int:subjectID>/comment', views.comments),
    path('comment/<int:id>', views.comment),
    path('comment/<int:commentID>/rating', views.ratings),
    path('rating/<int:id>', views.rating),

    path('exchange/<int:time>', views.exchangeGraph),
    path('exchange/<int:time>/prognosis/<int:price>', views.exchangePrognosis),
    path('user/<int:userID>/transaction', views.transactions),
    path('transaction/<int:id>', views.transaction),
    path('transaction/all', views.transactionsAll),
    path('user/<int:userID>/trigger', views.triggers),
    path('trigger/<int:id>', views.trigger),
    path('trigger/all', views.triggersAll),
    path('user/<int:userID>/notification', views.notifications),
    path('notification/<int:id>', views.notification)

]

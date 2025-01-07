from web import models

def navbar_context_processor(request):
    if request.user.is_authenticated:
        unread_message_count = models.Message.objects.filter(receiver=request.unicom_userid, is_read=False).count()
    else:
        unread_message_count = 0
    return {'unread_message_count': unread_message_count}
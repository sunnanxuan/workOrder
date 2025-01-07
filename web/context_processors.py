from web import models

def navbar_context_processor(request):
    unread_message_count = models.Message.objects.filter(receiver=request.unicom_userid, is_read=False).count()
    return {'unread_message_count': unread_message_count}
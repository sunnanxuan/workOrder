from web import models


def navbar_context_processor(request):
    # 从会话中获取 unicom_userid
    unicom_userid = request.session.get('unicom_userid', None)

    if unicom_userid:
        unread_message_count = models.Message.objects.filter(receiver=unicom_userid, is_read=False).count()
    else:
        unread_message_count = 0  # 或者其他处理逻辑

    return {'unread_message_count': unread_message_count}
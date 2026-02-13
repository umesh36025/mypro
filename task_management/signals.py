import os
from django.db.models.signals import post_delete,post_save,pre_save,post_init
from .models import *
from django.dispatch import receiver
from notifications.models import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@receiver(post_save, sender=TaskAssignies)
def add_task_count_for_Assignee(sender,created, instance:TaskAssignies, **kwargs):
    if created:
        user=instance.assigned_to
        try:
            obj=AssingnedTasksCount.objects.get(assignee=user)
        except AssingnedTasksCount.DoesNotExist:
            obj=AssingnedTasksCount.objects.create(assignee=user)
            for i in ["1 Day","SOS","10 Day","Monthly","Quaterly"]:
                if instance.task.type.type_name==i:
                    value=getattr(obj,"count_"+i.replace(" ","_"))
                    setattr(obj,"count_"+i.replace(" ","_"),value+1)
                    obj.save()
                    break
        else:
            for i in ["1 Day","SOS","10 Day","Monthly","Quaterly"]:
                if instance.task.type.type_name==i:
                    value=getattr(obj,"count_"+i.replace(" ","_"))
                    setattr(obj,"count_"+i.replace(" ","_"),value+1)
                    obj.save()
                    break
                
@receiver(post_save, sender=Task)
def add_task_count_for_Assignee(sender,created, instance:Task, **kwargs):
    if created:
        user=instance.created_by
        try:
            obj=CreatedTasksCount.objects.get(creator=user)
        except CreatedTasksCount.DoesNotExist:
            obj=CreatedTasksCount.objects.create(creator=user)
            for i in ["1 Day","SOS","10 Day","Monthly","Quaterly"]:
                if instance.type.type_name==i:
                    value=getattr(obj,"count_"+i.replace(" ","_"))
                    setattr(obj,"count_"+i.replace(" ","_"),value+1)
                    obj.save()
                    break
        else:
            for i in ["1 Day","SOS","10 Day","Monthly","Quaterly"]:
                if instance.type.type_name==i:
                    value=getattr(obj,"count_"+i.replace(" ","_"))
                    setattr(obj,"count_"+i.replace(" ","_"),value+1)
                    obj.save()
                    break
            
@receiver(post_save, sender=Task)
def task_edit_and_create_logs(sender,created,instance:Task, **kwargs):
    if created:
        TaskCreateAndEditLogs.objects.create(task=instance)

@receiver(post_save, sender=Task)
def task_status_change_logs(sender,instance:Task, **kwargs):
    ...

# @receiver(post_save, sender=Task)
# def task_assigned_notification(sender, instance:Task, created, **kwargs):

#     if created and instance.assignees:

#         notif = Notification.objects.create(
#             recipient=instance.assignees,
#             notification_type="TASK",
#             title="New Task Assigned",
#             message=f"You have been assigned: {instance.title}"
#         )

#         # realtime push
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             f"user_{instance.assigned_to.id}",
#             {
#                 "type": "send_notification",
#                 "title": notif.title,
#                 "message": notif.message,
#                 "type": notif.notification_type,
#             }
#         )


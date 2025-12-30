from django.urls import path
from . import views

urlpatterns = [
    path("getbyRoleandDesignation/",views.get_usernames_from_selected_role_and_desigantion,name="Tasks_management"),
    path("getAvailableRoles/",views.get_available_roles,name="Tasks_management"),
    path("createTask/",views.create_task,name="Tasks_management"),
    path("<int:task_id>/change_status/",views.change_status,name="Tasks_management"),
    path("viewByType/<str:type>/",views.get_tasks_by_type,name="sortTasks"),
    path("viewTasks/",views.show_created_tasks,name="Tasks_management"),
    path("viewAssignedTasks/",views.show_assigned_tasks,name="Tasks_management"),
    path("",views.home,name="Tasks_management"),
    path("getTaskTypes/",views.get_types,name="sort")
]

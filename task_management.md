# 1.Get Task Types

URL- {{BASEURL}}/tasks/getTaskTypes/

response-

\[

&nbsp;   {

&nbsp;       "type\_name": "1 Day"

&nbsp;   },

&nbsp;   {

&nbsp;       "type\_name": "SOS"

&nbsp;   },

&nbsp;   {

&nbsp;       "type\_name": "10 Day"

&nbsp;   },

&nbsp;   {

&nbsp;       "type\_name": "Monthly"

&nbsp;   },

&nbsp;   {

&nbsp;       "type\_name": "Quaterly"

&nbsp;   }

]



# 2.Get Name from Roles and Designation.

URL- {{BASEURL}}/tasks/getNamesfromRoleandDesignation/?role=Admin\&designation=

query\_parameter=\["role","designation"]

response-

\[

&nbsp;   {

&nbsp;       "Name": "Jadhav"

&nbsp;   }

]



# 3.Create Task.

URL- {{BASEURL}}/tasks/createTask/

response-

{

&nbsp;   "message": "Task created"

}



# 4.View Created Tasks.

URL- {{BASEURL}}/tasks/viewTasks/

response-

\[{"task\_id": 18, "title": "creating task 123", "description": "testing the task creation api", "status": "PENDING", "due-date": "16/03/2026", "assignees": \[{"assignee": "tejraj D"}], "type": "10 Day"}, {"task\_id": 19, "title": "creating task 245", "description": "testing the task creation api", "status": "PENDING", "due-date": "16/03/2026", "assignees": \[{"assignee": "tejraj D"}], "type": "10 Day"}]



# 5.View Assigned Tasks.

URL- {{BASEURL}}/tasks/viewAssignedTasks/

response-

&nbsp;   {

&nbsp;       "task\_id": 18,

&nbsp;       "title": "creating task 123",

&nbsp;       "description": "testing the task creation api",

&nbsp;       "status": "PENDING",

&nbsp;       "created\_by": "Jadhav",

&nbsp;       "due-date": "16/03/2026"

&nbsp;   },

&nbsp;   {

&nbsp;       "task\_id": 19,

&nbsp;       "title": "creating task 245",

&nbsp;       "description": "testing the task creation api",

&nbsp;       "status": "PENDING",

&nbsp;       "created\_by": "Jadhav",

&nbsp;       "due-date": "16/03/2026"

&nbsp;   },

&nbsp;   {

&nbsp;       "task\_id": 20,

&nbsp;       "title": "creating task 786",

&nbsp;       "description": "testing the task creation api",

&nbsp;       "status": "PENDING",

&nbsp;       "created\_by": "Jadhav",

&nbsp;       "due-date": "16/03/2026"

&nbsp;   },

&nbsp;   {

&nbsp;       "task\_id": 3,

&nbsp;       "title": "ASxcszx",

&nbsp;       "description": "azXC VXZ ",

&nbsp;       "status": "PENDING",

&nbsp;       "created\_by": "tejraj D",

&nbsp;       "due-date": "22/01/2026"

&nbsp;   },

&nbsp;   {

&nbsp;       "task\_id": 17,

&nbsp;       "title": "creating a task for testing",

&nbsp;       "description": "testing the task creation api",

&nbsp;       "status": "PENDING",

&nbsp;       "created\_by": "tejraj D",

&nbsp;       "due-date": "16/03/2026"

&nbsp;   }

]



# 5.Change Status.

URL- {{BASEURL}}/tasks/changeStatus/<int:task\_id>/

response-

{

&nbsp;   "message": "Status Changed to Completed"

}



# 6.Delete Task.

URL- {{BASEURL}}/tasks/deleteTask/<[int:task\_id](int:task\\_id)>/

response-

{

&nbsp;   "Message": "task-task\_id 2 deleted successfully"

}



# 7.Send Message inside the task.

URL- {{BASEURL}}/tasks/sendMessage/

response-

{

&nbsp;   "status": "Message sent"

}



# 8.Get Message inside the task.

URL- {{BASEURL}}/tasks/getMessage/<int:task\_id>/

response-

\[

&nbsp;   {

&nbsp;       "sender": "20011",

&nbsp;       "message": "hey, how are you?",

&nbsp;       "date": "27/01/26",

&nbsp;       "time": "18:32",

&nbsp;       "seen": true

&nbsp;   }

]



# 9.Get Message inside the task.

URL- {{BASEURL}}/tasks/updateTask/<[int:task\_id](int:task\\_id)>/

response-

1. only creator can update the task:{"message": "Task updated successfully"}
2. If not the creator:{"message": "you cannot update or edit this task"}












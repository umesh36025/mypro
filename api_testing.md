1. ## Login

##### URL-{{base URL}}/accounts/login/

response-{

    "message": "You are logged in",

    "username": "0001",

    "Role": "Admin"

}



## 2\. Get Employee

##### URL-{{base URL}}/accounts/employee/dashboard/

response-\[

    {

        "Employee\_id": "0001",

        "Email\_id": "admin@planetfarm.ai",

        "Date\_of\_birth": "2020-02-02",

        "Date\_of\_join": "2020-02-04",

        "Name": "Jadhav",

        "Photo\_link": "",

        "role": "Admin"

    }

]



## 3.AllEmployees

##### URL-{{base URL}}/accounts/employees/

response-\[

    {

        "Employee\_id": "2000",

        "Name": "Tushar Patil",

        "Role": "MD",

        "Branch": null,

        "Designation": null,

        "Date\_of\_birth": "1995-01-01",

        "Date\_of\_join": "2026-01-20",

        "Number\_of\_days\_from\_joining": "0 years 3 days",

        "Email\_id": "Tushar@gmail.com",

        "Photo\_link": "/media/profile\_images/Screenshot\_2025-10-29\_154813.png",

        "teamlead": null,

        "function": null

    },

    {

        "Employee\_id": "20011",

        "Name": "tejraj D",

        "Role": "TeamLead",

        "Branch": "Farm Core",

        "Designation": "Precision Agriculture Manager",

        "Date\_of\_birth": "1999-02-02",

        "Date\_of\_join": "2025-01-01",

        "Number\_of\_days\_from\_joining": "1 years 22 days",

        "Email\_id": "Tejarj@gmail.com",

        "Photo\_link": "/media/profile\_images/Tejraj\_Dhongade.jfif",

        "department": "Sales",

        "Teamleader": null,

        "function": "IP"

    },

    {

        "Employee\_id": "3000",

        "Name": "Snighdha",

        "Role": "TeamLead",

        "Branch": "Technology",

        "Designation": "Software Developer",

        "Date\_of\_birth": "2020-02-02",

        "Date\_of\_join": "2020-12-01",

        "Number\_of\_days\_from\_joining": "5 years 53 days",

        "Email\_id": "dummy@nashik.com",

        "Photo\_link": "/media/profile\_images/vendor.jpg",

        "department": "Production",

        "Teamleader": null,

        "function": "IP"

    },

    {

        "Employee\_id": "3001",

        "Name": "siddhi borse",

        "Role": "Employee",

        "Branch": "Farm Core",

        "Designation": "Digital Marketing Manager",

        "Date\_of\_birth": "2001-01-02",

        "Date\_of\_join": "2025-01-02",

        "Number\_of\_days\_from\_joining": "1 years 21 days",

        "Email\_id": "siddhi@gmail.com",

        "Photo\_link": "/media/profile\_images/Siddhi\_Borase.jfif",

        "department": "Sales",

        "Teamleader": null,

        "function": "IP"

    },

    {

        "Employee\_id": "9000",

        "Name": "Himalaya",

        "Role": "Intern",

        "Branch": "Farm Tech",

        "Designation": "Software Developer",

        "Date\_of\_birth": "2020-02-02",

        "Date\_of\_join": "2020-12-12",

        "Number\_of\_days\_from\_joining": "5 years 42 days",

        "Email\_id": "dummy@gmail.com",

        "Photo\_link": "/media/profile\_images/IMG\_0395.jpg",

        "department": "Business Strategy",

        "Teamleader": "Snighdha",

        "function": "HC"

    },

    {

        "Employee\_id": "00110011",

        "Name": "abcdefg",

        "Role": "MD",

        "Branch": null,

        "Designation": null,

        "Date\_of\_birth": "2002-11-10",

        "Date\_of\_join": "2002-11-10",

        "Number\_of\_days\_from\_joining": "23 years 74 days",

        "Email\_id": "user@planeteye",

        "Photo\_link": "/media/profile\_images/Screenshot\_2025-05-29\_182812.png",

        "teamlead": null,

        "function": null

    }

]



## 4.ChangePassword

##### URL-{{base URL}}/accounts/admin/changePassword/[slug:u](slug:u)/

path parameter- username(u)

body-{"new\_password":"123"}

response-

{"message": "Password is changed to 123"}



## 5.CreateLogin

##### URL-{{base URL}}/accounts/admin/createEmployeeLogin/

response-

{

    "message": "user profile created successfully"

}



## 6.GetBranches

##### URL-{{base URL}}/accounts/getBranch/?Role=

response-

\[

    {

        "branch\_name": "Farm Core"

    },

    {

        "branch\_name": "Farm Tech"

    },

    {

        "branch\_name": "Infra Core"

    },

    {

        "branch\_name": "Infra Tech"

    },

    {

        "branch\_name": "Technology"

    }

]



## 7.GetDepartments\&Functions

##### URL-{{base URL}}/accounts/getDepartmentsandFunctions/?Role=

response-



{

    "Departments": \[

        "Accounts\&Finance",

        "Business Strategy",

        "HR",

        "Legal\&Document",

        "Marketing",

        "NPC",

        "NPD",

        "Production",

        "Purchase",

        "R\&D",

        "Sales",

        "Vigil"

    ],

    "functions": \[

        "NPD",

        "MMR",

        "RG",

        "HC",

        "IP"

    ]

}



## 8.GetRoles

##### URL-{{base URL}}/accounts/getRoles/

response-

\[

    {

        "role\_name": "MD"

    },

    {

        "role\_name": "Intern"

    },

    {

        "role\_name": "TeamLead"

    },

    {

        "role\_name": "Employee"

    }

]



## 9.GetDesignations

##### URL-{{base URL}}/accounts/getDesignations/?Role=

response-

\[

    {

        "designation": "Software Developer"

    },

    {

        "designation": "Python Developer"

    },

    {

        "designation": "AI/ML Developer"

    },

    {

        "designation": "Web Developer"

    },

    {

        "designation": "Backend Developer"

    },

    {

        "designation": "Precision Agriculture Manager"

    },

    {

        "designation": "Digital Marketing Manager"

    },

    {

        "designation": "Project Supervisor"

    },

    {

        "designation": "Designer Engineer"

    },

    {

        "designation": "Site Engineer"

    },

    {

        "designation": "Field Officer"

    }

]





## 10.GetTeamleads

##### URL-{{base URL}}/accounts/getTeamleads/?Role

response-

\[

    {

        "Name": "Snighdha",

        "Employee\_id": "3000"

    },

    {

        "Name": "tejraj D",

        "Employee\_id": "20011"

    }

]



## 11.DeleteUser

##### URL-{{base URL}}/accounts/admin/deleteEmployee/[slug:u](slug:u)/

path parameter-username(u)

response-

{"message": "user deleted successfully"}



## 12.UpdateUser

##### URL-{{base URL}}/accounts/admin/updateProfile/[slug:username](slug:username)/

path parameter- username

response-





## 13.Logout

##### URL-{{base URL}}/accounts/logout/

response-

{

    "message": "Logout successfully 0001"

}


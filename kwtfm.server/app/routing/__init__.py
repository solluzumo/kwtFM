from routing.user import user_router


routers_list = [ 
    {"router": user_router, "prefix": "/api/user", "tags": ["User"]},

                
]
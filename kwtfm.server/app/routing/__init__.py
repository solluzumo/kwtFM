from app.routing.user import user_router
from app.routing.auth import auth_router 
from app.routing.track import track_router 


routers_list = [ 
    {"router": user_router, "prefix": "/api/user", "tags": ["User"]},
    {"router": auth_router, "prefix": "/api/auth", "tags": ["Auth"]},
    {"router": track_router, "prefix": "/api/track", "tags": ["Track"]},
                
]
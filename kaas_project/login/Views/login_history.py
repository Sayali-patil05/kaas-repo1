# from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Login
from datetime import datetime

# # @api_view()
# def get_login_history(request):
#     history = Login.objects.filter(user=request.user)

#     # This really bad one liner extracts the unique days this user has logged in on
#     # in sorted order
#     logins = sorted(
#         list(set((map(lambda x: x.login_date.date(), history))))
#     )  # Probably move to into query later

#     return logins

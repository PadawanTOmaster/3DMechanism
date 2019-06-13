def jwt_response_payload_handler(token, user=None, request=None):

   return {
   "username":user.username,
   "nickname": user.nickname,
   "token": token,
   'flag':user.flag,
   }

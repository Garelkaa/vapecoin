from schemas.user import UserRequest, UserResponse
from signature import MyBot



async def check_subscribes(request: UserRequest, bot_instance: MyBot) -> UserResponse:
    channel_id = "-1002308005447" # ID канала
    member = await bot_instance.bot.get_chat_member(chat_id=channel_id, user_id=request.user_id)

    
    if member.status in ["member", "administrator", "creator"]:
        answer = True
    else:
        answer = False

    return UserResponse(answer=answer)
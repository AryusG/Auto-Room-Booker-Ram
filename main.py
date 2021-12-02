from auto_room_booker import AutoRoomBooker

preferred_rooms = ['CK21', 'CK22', 'CK23']

bot = AutoRoomBooker()
bot.login()
bot.book_general_practice_room(preferred_rooms)



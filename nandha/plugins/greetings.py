

import random
import asyncio

from nandha.helpers.decorator import ChatMembers
from nandha.helpers.utils import get_method_by_type, convert_greetings_text, auto_delete
from nandha.helpers.misc import dict_to_keyboard
from nandha import LOGS_CHANNEL

from nandha.db.chats import add_chat
from nandha.db.users import add_user, update_users_status

from nandha.db.greetings import get_welcome, get_goodbye
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Chat, ChatMember, constants, ChatMemberUpdated, helpers
from telegram.ext import ChatMemberHandler
from typing import Optional, Tuple




WEL_STRING = [
   "Ah, <b>{username}</b> has entered the domain of <b>{chatname}</b>! You're just in time to witness greatness. Don't get too comfortable, though - we're always pushing the limits here.",
   "Welcome, <b>{username}</b>! You've just stepped into the lair of <b>{chatname}</b>, where the strong thrive and the weak... well, they get stronger too. Either way, you're in for a wild ride.",
   "{username} has joined the fray! <b>{chatname}</b> just got a whole lot more interesting. Don't worry, we won't bite... hard. Unless you're a cursed spirit, of course.",
   "Ah, <b>{username}</b> has decided to join the chaos! Welcome to <b>{chatname}</b>, where the boundaries between sanity and madness are tested daily. Buckle up, friend!",
   "<b>{username}</b> has entered the battlefield! <b>{chatname}</b> is where the strong come to play, and the weak... well, they come to get stronger. Either way, it's gonna be a blast!",
   "Welcome, <b>{username}</b>! You've just stepped into the domain of <b>{chatname}</b>, where the cursed and the blessed coexist. Don't worry, we won't curse you... unless you ask nicely.",
   "<b>{username}</b> has joined the squad! <b>{chatname}</b> is where the Jujutsu Sorcerers come to hang out, and we're always up for a challenge. What's your cursed technique?",
   "Ah, <b>{username}</b> has arrived! <b>{chatname}</b> is the perfect place for those who crave adventure, excitement, and a dash of cursed energy. What's your story, friend?",
   "Well, well, <b>{username}</b> has arrived! Welcome to <b>{chatname}</b>, where power meets purpose. Don't be shy; we thrive on excitement here!",
   "Ah, <b>{username}</b> has joined <b>{chatname}</b>! You've stepped into a realm where nothing is impossible, and everything is a little... chaotic.",
   "Welcome, <b>{username}</b>! You've entered <b>{chatname}</b>, a place where even the strongest know no limits. Can you keep up?",
   "<b>{username}</b> just entered <b>{chatname}</b>! Brace yourself for intensity, energy, and maybe a few friendly curses. You good with that?",
   "Ah, another brave soul enters <b>{chatname}</b>! Welcome, <b>{username}</b>. Ready to unlock your inner strength?",
   "<b>{username}</b>, you've wandered into <b>{chatname}</b>. I hope you're prepared because things here aren't always what they seem!",
   "Welcome, <b>{username}</b>, to <b>{chatname}</b>! Get ready for cursed techniques, epic battles, and more fun than you can handle!",
   "Looks like <b>{username}</b> just entered the domain of <b>{chatname}</b>. Power flows through these walls, and now you're a part of it!",
   "<b>{username}</b> has joined <b>{chatname}</b>! Here, we're not just strong – we're untouchable. Ready to rise to the occasion?",
   "Welcome, <b>{username}</b>! You've stepped into <b>{chatname}</b>, where even curses become blessings. Let the adventure begin!",
   "Ah, <b>{username}</b>! You've found your way into <b>{chatname}</b>. Hope you're ready for a challenge or two – we don't do 'easy' here!",
   "Well, look who just showed up! <b>{username}</b>, welcome to <b>{chatname}</b>, where sorcery meets chaos in a beautiful dance.",
   "<b>{username}</b> has entered <b>{chatname}</b>! Here, we laugh in the face of danger and smile at the edge of chaos.",
   "Welcome, <b>{username}</b>! <b>{chatname}</b> is a world where the impossible becomes reality. Ready to make some magic?",
   "<b>{username}</b> just stepped into <b>{chatname}</b>! Get comfortable, but not too comfortable. Adventure waits!",
   "Ah, <b>{username}</b> has entered the domain of <b>{chatname}</b>. The power here is real – and now you're part of it!",
   "Welcome, <b>{username}</b>! You've joined <b>{chatname}</b>, where strength, skill, and a little madness collide.",
   "<b>{username}</b> has joined <b>{chatname}</b>, and things just got a lot more interesting. Ready for some action?",
   "Ah, <b>{username}</b>, welcome to <b>{chatname}</b>! We've been waiting for someone with your potential. Let’s see what you’ve got!",
   "Welcome, <b>{username}</b>, to the battlefield of <b>{chatname}</b>! Ready to show the world what you're made of?",
   "<b>{username}</b> just stepped into <b>{chatname}</b>. Here, we challenge reality and make the impossible look easy!",
   "Ah, <b>{username}</b>! You've arrived at <b>{chatname}</b>. It's not for the faint of heart, but you look like you'll fit right in.",
   "Welcome, <b>{username}</b>! You've joined the ranks of <b>{chatname}</b>, where we rewrite the rules of strength daily."
]


LEFT_STRING = [
   "<b>{username}</b> has vanished into the void of <b>{chatname}</b>...",
   "<b>{username}</b> has abandoned the mortal realm of <b>{chatname}</b>...",
   "<b>{username}</b> has succumbed to the darkness within <b>{chatname}</b>...",
   "<b>{username}</b> has departed for the great beyond from <b>{chatname}</b>...",
   "<b>{username}</b> has been consumed by the shadows of <b>{chatname}</b>...",
   "<b>{username}</b> has left to face the unknown beyond <b>{chatname}</b>...",
   "<b>{username}</b> has disappeared into the abyss of <b>{chatname}</b>...",
   "<b>{username}</b> has faded from <b>{chatname}</b>'s grasp...",
   "The light of <b>{username}</b> has dimmed and left <b>{chatname}</b> behind...",
   "<b>{username}</b> has slipped beyond the reach of <b>{chatname}</b>...",
   "Gone without a trace, <b>{username}</b> has left <b>{chatname}</b>...",
   "<b>{username}</b> has chosen to walk a path beyond <b>{chatname}</b>...",
   "Like a shadow at dawn, <b>{username}</b> has quietly departed <b>{chatname}</b>...",
   "<b>{username}</b> has crossed the threshold into the unknown, leaving <b>{chatname}</b> behind...",
   "<b>{username}</b> has vanished like a fleeting dream from <b>{chatname}</b>...",
   "In an instant, <b>{username}</b> is no longer part of <b>{chatname}</b>...",
   "With a quiet exit, <b>{username}</b> is gone from <b>{chatname}</b>...",
   "A step into the shadows, <b>{username}</b> is no longer with <b>{chatname}</b>...",
   "<b>{username}</b> has left <b>{chatname}</b>, disappearing like smoke on the wind...",
   "With a final breath, <b>{username}</b> has left the confines of <b>{chatname}</b>...",
   "<b>{username}</b> has become a memory, leaving <b>{chatname}</b> behind...",
   "A fleeting presence, <b>{username}</b> has departed <b>{chatname}</b>...",
   "<b>{username}</b> has faded from <b>{chatname}</b>, leaving only silence...",
   "Like mist in the morning, <b>{username}</b> has left <b>{chatname}</b> behind...",
   "In a quiet whisper, <b>{username}</b> is no longer with <b>{chatname}</b>...",
   "Gone in a blink, <b>{username}</b> has left <b>{chatname}</b>...",
   "Another soul departs as <b>{username}</b> steps away from <b>{chatname}</b>...",
   "<b>{username}</b> has chosen to leave the chaos of <b>{chatname}</b> behind...",
   "The energy of <b>{username}</b> has left <b>{chatname}</b>, leaving only echoes...",
   "<b>{username}</b> has left the world of <b>{chatname}</b> and embraced the unknown...",
   "<b>{username}</b> has left us, their presence only a fleeting memory in <b>{chatname}</b>..."
]


def extract_status_change(chat_member_update: ChatMemberUpdated) -> Optional[Tuple[bool, bool]]:
    """Takes a ChatMemberUpdated instance and extracts whether the 'old_chat_member' was a member
    of the chat and whether the 'new_chat_member' is a member of the chat. Returns None, if
    the status didn't change.
    """
    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = old_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (old_status == ChatMember.RESTRICTED and old_is_member is True)
    is_member = new_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (new_status == ChatMember.RESTRICTED and new_is_member is True)

    return was_member, is_member


@ChatMembers(chat_member_types=ChatMemberHandler.MY_CHAT_MEMBER, group=17)
async def track_chats(update, context) -> None:
    """Tracks the chats the bot is in."""

    bot = context.bot
    m = update.effective_message
    chat = update.effective_chat
   
    if chat.type == constants.ChatType.CHANNEL: return
   
    result = extract_status_change(update.my_chat_member)
   
    if result is None:
        return
    was_member, is_member = result

    # Let's check who is responsible for the change
    user = update.effective_user
    cause_name = user.full_name
    
    # Handle chat types differently:   
    if chat.type == Chat.PRIVATE:
        if not was_member and is_member:
            # This may not be really needed in practice because most clients will automatically
            # send a /start command after the user unblocks the bot, and start_private_chat()
            # will add the user to "user_ids".
            # We're including this here for the sake of the example.
            await update_users_status([chat.id], status=True)
            await bot.send_message(
                 chat_id=LOGS_CHANNEL,
                 text=f"*{cause_name}* - (`{chat.id}`) unblocked the bot 🙋",
                 parse_mode=constants.ParseMode.MARKDOWN
            )
                 
        elif was_member and not is_member:
            await update_users_status([chat.id], status=False)
            await bot.send_message(
                 chat_id=LOGS_CHANNEL,
                 text=f"*{cause_name}* - (`{chat.id}`) blocked the bot 🙋",
                 parse_mode=constants.ParseMode.MARKDOWN
            )
           
    elif chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
        if not was_member and is_member:
            await chat.send_photo(
                 photo="https://graph.org/file/5848ea5fdabc0cdf8d2e3.jpg",
                 caption="*⚡ Thank you for adding for me  here (: to know my help commands do clicks*.",
                 reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                  "🆘 Commands", url=f"t.me/{bot.username}?start=help"
                )
                  ]]),
                 parse_mode=constants.ParseMode.MARKDOWN
            )
            await bot.send_message(
                 chat_id=LOGS_CHANNEL,
                 text=f"*{cause_name}* - (`{user.id}`) added the bot to the group *{chat.title}* — (`{chat.id}`) ✨ ",
                 parse_mode=constants.ParseMode.MARKDOWN
            )
           
        elif was_member and not is_member:
            await bot.send_message(
                 chat_id=LOGS_CHANNEL,
                 text=f"*{cause_name}* - (`{user.id}`) removed the bot from the group *{chat.title}* — (`{chat.id}`) 🤷 ",
                 parse_mode=constants.ParseMode.MARKDOWN
            )
           
    elif not was_member and is_member:
          await bot.send_message(
                 chat_id=LOGS_CHANNEL,
                 text=f"*{cause_name}* - (`{user.id}`) added the bot to the channel *{chat.title}* — (`{chat.id}`) ✨ ",
                 parse_mode=constants.ParseMode.MARKDOWN
        )
        
    elif was_member and not is_member:
          await bot.send_message(
                 chat_id=LOGS_CHANNEL,
                 text=f"*{cause_name}* - (`{user.id}`) removed the bot from the channel *{chat.title}* — (`{chat.id}`) 🤷 ",
                 parse_mode=constants.ParseMode.MARKDOWN
        )



@ChatMembers(chat_member_types=ChatMemberHandler.CHAT_MEMBER, group=13)
async def WelcomeMembers(update, context):
    """ greetings members in chat """
    result = extract_status_change(update.chat_member)
    bot = context.bot
   
    if result is None: return
    was_member, is_member = result
    cause_name = update.chat_member.from_user.mention_html()
    member_name = update.chat_member.new_chat_member.user.mention_html()
    member = update.chat_member.new_chat_member.user
    member_data = {
         'id': member.id,
         'first_name': member.first_name,
         'username': member.username if member.username else None
    }
    self_action = False
    chat = update.effective_chat
    if chat.type == constants.ChatType.CHANNEL: return
  
    if update.chat_member.from_user.id == update.chat_member.new_chat_member.user.id:
         self_action = True
    
    if not was_member and is_member:
         if not self_action:
             await add_chat(chat.id)
             if not member.is_bot: await add_user(member_data) # only add user's
             msg = await chat.send_message(
                  f"<b>{member_name} was added by {cause_name}. Welcome!</b>",
                  parse_mode=constants.ParseMode.HTML,
                 )
             await auto_delete(msg, 1*60)
            
             
         else:
             await add_chat(chat.id)
             if not member.is_bot: await add_user(member_data) # only add user's
             welcome = await get_welcome(chat.id)
             if not welcome:
                welcome_str = random.choice(WEL_STRING)
                msg = await chat.send_message(
                       welcome_str.format(username=member_name, chatname=chat.title),
                       parse_mode=constants.ParseMode.HTML
                )
                await auto_delete(msg, 5*60)
             else:
                 data = welcome
                 text = convert_greetings_text(data['text'], member, chat) if data.get('text') else None
                 file_id = data.get('file_id')
                 time = int(data.get('time', 5*60))
                 file_type = data.get('file_type')
                 method = get_method_by_type(bot, file_type)
                 keyboard = dict_to_keyboard(data['keyboard']) if data.get('keyboard') else None
                
                 if file_type == "text":
                     msg = await method(chat.id, text=text, reply_markup=keyboard, parse_mode=constants.ParseMode.MARKDOWN)
                 else:
                     msg = await method(chat.id, file_id, caption=text, reply_markup=keyboard, parse_mode=constants.ParseMode.MARKDOWN)
                    
                 await auto_delete(msg, time)
            
             
    elif was_member and not is_member:
        if not self_action:
            msg = await chat.send_message(
                text=f"<b>{member_name} is no longer with us. Thanks a lot, {cause_name} ...</b>",
                parse_mode=constants.ParseMode.HTML,
           )
            await auto_delete(msg, 1*60)
            
            
        else:
      
             goodbye = await get_goodbye(chat.id)
             if not goodbye:
                 return #skip
                 left_str = random.choice(LEFT_STRING)
                 msg = await chat.send_message(
                      left_str.format(
                      username=member_name,
                      chatname=chat.title
                 ),
                 parse_mode=constants.ParseMode.HTML
             )
                 await auto_delete(msg, 1*60)
             else:
                 data = goodbye
                 text = convert_greetings_text(data['text'], member, chat) if data.get('text') else None
                 file_id = data.get('file_id')
                 time = int(data.get('time', 5*60))
                 file_type = data.get('file_type')
                 method = get_method_by_type(bot, file_type)
                 keyboard = dict_to_keyboard(data['keyboard']) if data.get('keyboard') else None
                
                 if file_type == "text":
                     msg = await method(chat.id, text=text, reply_markup=keyboard, parse_mode=constants.ParseMode.MARKDOWN)
                 else:
                     msg = await method(chat.id, file_id, caption=text, reply_markup=keyboard, parse_mode=constants.ParseMode.MARKDOWN)
                    
                 await auto_delete(msg, time)
            
             


import logging
import Calendario_Main
import datetime
import telegram
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler,Filters,CallbackContext
import responses as R
import Calendario_privateInfo
import pytz


#users enable to access to database
#Modify Calendario_privateInfo.py file to add your user
users=[Calendario_privateInfo.user1, Calendario_privateInfo.user2]
matched="KO"


#enable logging
#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s %(message)s', level=logging.INFO)
#logger = logging.getLogger(__name__)

def callback_everyday(context:telegram.ext.CallbackContext):
    cur,conn = Calendario_Main.connect_to_database()
    current_table = Calendario_Main.show_table(cur, conn)
    today = datetime.date.today()
    for row in current_table:
        if today > row[1]:
            row_to_send = "*** EXPIRED *** - "
            my_date = datetime.datetime.strptime(str(row[1]), '%Y-%m-%d')
            my_date_IT = my_date.strftime('%d/%m/%Y')
            row_to_send = row_to_send + str(my_date_IT) + " - "  + str(row[2])
            try:
                row_to_send = row_to_send + " - " + str(row[3])
            except:
                pass    
            try:
                row_to_send = row_to_send + " - " + str(row[4])
            except:
                pass
            row_to_send = row_to_send + "- (" + str(row[0])+ ")"
            context.bot.send_message(chat_id=Calendario_privateInfo.chat_id, text=row_to_send)
        elif today == row[1]:
            row_to_send = "*** EXPIRES TODAY *** - "
            my_date = datetime.datetime.strptime(str(row[1]), '%Y-%m-%d')
            my_date_IT = my_date.strftime('%d/%m/%Y')
            row_to_send = row_to_send + str(my_date_IT) + " - "  + str(row[2])
            try:
                row_to_send = row_to_send + " - " + str(row[3])
            except:
                pass    
            try:
                row_to_send = row_to_send + " - " + str(row[4])
            except:
                pass
            row_to_send = row_to_send + "- (" + str(row[0])+ ")"
            context.bot.send_message(chat_id=Calendario_privateInfo.chat_id, text=row_to_send)
        else:
            pass

#function that show all rows saved in tables. Needs command "show" on telegram
def show_table(update, cur, conn):
    current_table = Calendario_Main.show_table(cur, conn)
    today = datetime.date.today()
    for row in current_table:
        if today > row[1]:
            row_to_send = "<u><b> EXPIRED - </b></u>"
        elif today == row[1]:
            row_to_send = "<u><b> EXPIRES TODAY - </b></u>"
        else:
            row_to_send = ""
        my_date = datetime.datetime.strptime(str(row[1]), '%Y-%m-%d')
        my_date_IT = my_date.strftime('%d/%m/%Y')
        row_to_send = row_to_send + str(my_date_IT) + " - "  + str(row[2])
        try:
            row_to_send = row_to_send + " - " + str(row[3])
        except:
            pass    
        try:
            row_to_send = row_to_send + " - " + str(row[4])
        except:
            pass

        row_to_send = row_to_send + "- (" + str(row[0])+ ")"

        #for i in row:
        #    if(row[1]):
        #        update.message.reply_text("OK")
        #    row_to_send = row_to_send+" - ("+ str(i)+ ")"
        update.message.reply_text(row_to_send,parse_mode='HTML')


#function that manage the message sent on telgram by user
def handle_message(update, context):
    text = str(update.message.text)
    msg = update.message
    try:
        first_name = msg['chat']['first_name']
    except:
        first_name = "NONE"
    try:
        last_name = msg['chat']['last_name']
    except:
        last_name = "NONE"

    for utente in users: #approve only users in users list
        if ((first_name == utente[0]) and (last_name == utente[1])):
            matched="OK"
            break
        else:
            continue
    
    #if user is qualified, message is splitted to understand command, date, time, description of event. Comman available are show, A=add, C=erase
    if (matched=="OK"):
        cur,conn = Calendario_Main.connect_to_database()
        split_time=[]
        testo = text
        split_text = testo.split(".")
        split_command_date = split_text[0].split()
        len_command = len(split_command_date)
        try:
            split_time=split_text[2].split()
            l_split_time = len(split_time)
            if l_split_time==1:
                time_present="OK_1"
            elif l_split_time==2:
                time_present="OK_2"
            else:
                time_present="NO_TIME"
        except:
            time_present="KO"
            split_time.append("Null")
            split_time.append("Null")

        if len(split_text)<2:
            if ((split_command_date[0]).lower() == "show"):
                show_table(update, cur, conn)
            elif ((split_command_date[0]).lower() == "r"):
                if(split_command_date[1]=="all"):
                    Calendario_Main.delete_all_rows(cur, conn)
                    Calendario_Main.reset_id_counter(cur, conn)
                    update.message.reply_text( "Table Removed")
                else:    
                    try:
                        elem_to_erase = 1
                        while elem_to_erase < len_command:
                            Calendario_Main.remove_row(cur, conn, split_command_date[elem_to_erase])
                            Calendario_Main.reset_id_counter(cur, conn)
                            elem_to_erase+=1
                    except:
                        update.message.reply_text( "None has been removed")
                    else:
                        show_table(update, cur, conn)
            else:
                update.message.reply_text( "Some details are missing to save the event correctly")
        else:
            if ((split_command_date[0]).lower() == "a"):
                #print("Add")
                try:
                    my_date = datetime.datetime.strptime(split_command_date[1], '%d-%m-%Y')
                    my_date_date = str(my_date.date())
                    if (time_present=="KO" or time_present=="NO_TIME"):
                        Calendario_Main.add_row(cur, conn, my_date_date, split_text[1])
                    elif (time_present=="OK_1"):
                        Calendario_Main.add_row(cur, conn, my_date_date, split_text[1],split_time[0])
                    elif (time_present=="OK_2"):
                        Calendario_Main.add_row(cur, conn, my_date_date, split_text[1],split_time[0],split_time[1])
                    else:
                        pass
                    update.message.reply_text( "Event OK")
                except:
                    update.message.reply_text( "Event not added")
            #elif split_command_date[0] == "M":
            #    print("Modify")
            else:
                update.message.reply_text("Not correct action")


    
#main function that connect to database and manage in polling all function seen above
def main_runnable() -> None:
    """Start the BOT"""
    try:
        updater = Updater(Calendario_privateInfo.TOKEN)
        job = updater.job_queue
        job.run_repeating(callback_everyday, interval=datetime.timedelta(1), first=datetime.time(hour=6,minute=45))
        dp = updater.dispatcher
        dp.add_handler(MessageHandler(Filters.text,handle_message))
        updater.start_polling(5)
    except Exception as e:
        pass
    updater.idle()

if __name__ == '__main__':
    main_runnable()

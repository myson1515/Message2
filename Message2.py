import curses
import curses.textpad
import smtplib
import imapclient
import sys
import time
import pyzmail
from pick import *


sys.setrecursionlimit(10000)
screen = curses.initscr()
screen.keypad(True)
curses.start_color()
curses.noecho()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)
c1 = 1
c2 = 1
q = -1
x = 0

# Signs user in to google's gmail services
def signIn():
    curses.noecho()
    c1 = 1
    c2 = 1
    screen.clear()
    screen.refresh()
    screen.addstr(0,0,"Starting sign in script...")
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    screen.addstr(5,5,"THE NEXT FEW PROMPTS ARE INPUTS ")
    screen.addstr(7,5, "PLEASE TYPE CRTL-G WHEN DONE INPUTING EACH PROMPT ")
    screen.addstr(9,5, "IF YOU MAKE A MISTAKE PRESS CRTL-H TO GO BACK")
    screen.addstr(11, 5, "('s' to continue)")
    q = screen.getch()
    if q == ord("s"):
        pass
    else:
        time.sleep(4)
    screen.clear()
    screen.refresh()
    x = 0
    while True:

        if x == 0:
            screen.addstr(5, 0,"EMAIL:  ")
            screen.refresh()
            time.sleep(1)
            screen.clear()
            tb = curses.textpad.Textbox(screen, insert_mode=True)
            curses.cbreak()
            email = tb.edit()
            screen.clear()
            curses.flash()
            finEmail = email.replace("\n", "").replace(" ", "")

            screen.addstr(5, 5,"CORRECT? (" + finEmail + ")")
        screen.addstr(7, 5, "YES", curses.color_pair(c2))
        screen.addstr(9, 5, "NO", curses.color_pair(c1))

        x = 1
        q = screen.getch()
        screen.refresh()
        if q == curses.KEY_UP:
            c1 = 1
            c2 = 2


        if q == curses.KEY_DOWN:
            c1 = 2
            c2 = 1
        if q ==ord("\n") and c1 == 2:
            screen.clear()
            x = 0
            pass

        if q == ord("\n") and c2 == 2:
            screen.clear()
            break
    screen.clear()
    screen.addstr(5, 0,"PASSWORD:  ")
    screen.refresh()
    time.sleep(1)
    screen.clear()
    tb2 = curses.textpad.Textbox(screen, insert_mode=True)
    curses.cbreak()
    passwd = tb2.edit()
    screen.clear()
    curses.flash()
    finpasswd =  passwd.replace("\n", "").replace(" ", "")
    screen.clear()
    screen.refresh()
    try:
        smtpObj.login(finEmail, finpasswd)
    except smtplib.SMTPAuthenticationError:
        screen.clear()
        screen.addstr(5,5,"WRONG USERNAME OR PASSWORD")
        screen.addstr(7,5,"RESTARTING SIGN IN...")
        screen.refresh()
        time.sleep(2)
        screen.clear()
        signIn()
    return(finEmail, finpasswd, smtpObj)

# The function for sending emails
def loopySend():
    c1 = 1
    c2 = 1
    finEmail, finpasswd, smtpObj = signIn()
    x = 0
    while True:
        if x == 0:
            screen.addstr(5, 5,"EMAIL2:  ")
            screen.refresh()
            time.sleep(1)
            screen.clear()
            tb3 = curses.textpad.Textbox(screen, insert_mode=True)
            email2 = tb3.edit()
            screen.clear()
            curses.flash()
            finEmail2 = email2.replace("\n", "").replace(" ", "")
            screen.addstr(5, 5,"CORRECT? (" + finEmail2 + ")")
        screen.addstr(7, 5, "YES", curses.color_pair(c2))
        screen.addstr(9, 5, "NO", curses.color_pair(c1))

        x = 1
        q = screen.getch()
        screen.refresh()
        if q == curses.KEY_UP:
            c1 = 1
            c2 = 2


        if q == curses.KEY_DOWN:
            c1 = 2
            c2 = 1
        if q ==ord("\n") and c1 == 2:
            screen.clear()
            x = 0
            pass

        if q == ord("\n") and c2 == 2:
            screen.clear()
            break
    screen.clear()
    screen.addstr(5, 5,"SUBJECT:  ")
    screen.refresh()
    time.sleep(1)
    screen.clear()
    tb4 = curses.textpad.Textbox(screen, insert_mode=True)
    subject = tb4.edit()
    screen.clear()
    curses.flash()
    finsubject = subject.replace("\n", "")
    screen.clear()
    screen.addstr(5, 5,"BODY:  ")
    screen.refresh()
    time.sleep(1)
    screen.clear()
    tb5 = curses.textpad.Textbox(screen, insert_mode=True)
    body = tb5.edit()
    screen.clear()
    curses.flash()
    finbody = body
    screen.clear()
    smtpObj.sendmail(finEmail, finEmail2, "Subject: " + finsubject + "\n" + finbody)
    screen.clear()
    screen.addstr(5, 5,"EMAIL SENT!")
    screen.clear()
    x = 0
    while True:
        if x == 0:
            screen.addstr(5, 5,"SEND ANOTHER EMAIL?")
        screen.addstr(7, 5, "YES", curses.color_pair(c2))
        screen.addstr(9, 5, "NO", curses.color_pair(c1))

        x = 1
        q = screen.getch()
        screen.clear()
        if q == curses.KEY_UP:
            c1 = 1
            c2 = 2


        if q == curses.KEY_DOWN:
            c1 = 2
            c2 = 1
        if q ==ord("\n") and c1 == 2:
            screen.clear()
            x = 0
            sys.exit()
        if q == ord("\n") and c2 == 2:
            screen.clear()
            loopySend()

# The function for recieving IMAP emails.
def loopyRecieve():
    c1 = 1
    c2 = 1
    screen.clear()
    screen.refresh()
    screen.addstr(0,0,"Starting IMAP client...")
    email, passwd, smtpObj = signIn()
    imapObj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
    imapObj.login(email, passwd)
    imapObj.select_folder('INBOX', readonly=True)
    screen.addstr(5, 5,"SEARCH:  ")
    screen.refresh()
    time.sleep(1)
    screen.clear()
    tb6 = curses.textpad.Textbox(screen, insert_mode=True)
    search = tb6.edit()
    curses.flash()
    gotoStr = "FROM " + search.replace("\n", "").replace(" ", "")
    try:
        UID = imapObj.search(gotoStr)[0]
    except IndexError:
        screen.clear()
        screen.addstr(5, 5, "NO EMAIL WAS FOUND RELATING TO YOUR SEARCH")
        screen.addstr(7, 5, "RESTARTING RECIEVE EMAIL SCRIPTS...")
        screen.refresh()
        time.sleep(3)
        screen.clear()
        screen.refresh()
        loopyRecieve()
    options = UID
    screen.clear()
    screen.refresh()
    rawMessages = imapObj.fetch(int(UID), ['BODY[]'])
    RecentString = "YOUR MOST RECENT EMAIL FROM " + search.replace("\n", "").replace(" ", "").upper() + " IS THE FOLLOWING..."
    screen.addstr(5, 5,RecentString)
    screen.refresh()
    time.sleep(2)
    screen.clear()
    message = pyzmail.PyzMessage.factory(rawMessages[int(UID)]['BODY[]'])
    #ENDED HERE
    fromRec = "FROM: " + str(message.get_addresses('from'))
    subRec = "SUBJECT: " + message.get_subject()
    bodRec = "BODY: " + message.text_part.get_payload().decode(message.text_part.charset)
    x = 0
    while True:
        if x == 0:
            screen.addstr(5, 5,fromRec)
            screen.addstr(7, 5, subRec)
            screen.addstr(9, 5, bodRec)
        x = 1
        screen.addstr(11, 5, "DONE?", curses.color_pair(2))
        q = screen.getch()
        screen.clear()
        if q ==ord("\n"):
            screen.clear()
            x = 0
            break
        screen.refresh()
    x = 0
    while True:
        if x == 0:
            screen.addstr(5, 5,"RECIEVE ANOTHER EMAIL?")
        screen.addstr(7, 5, "YES", curses.color_pair(c2))
        screen.addstr(9, 5, "NO", curses.color_pair(c1))

        x = 1
        q = screen.getch()
        screen.clear()
        if q == curses.KEY_UP:
            c1 = 1
            c2 = 2


        if q == curses.KEY_DOWN:
            c1 = 2
            c2 = 1
        if q ==ord("\n") and c1 == 2:
            screen.clear()
            x = 0
            sys.exit()
        if q == ord("\n") and c2 == 2:
            screen.clear()
            loopyRecieve()



while True:
    if x == 0:
        screen.addstr(5, 5, "WRITE EMAIL",curses.color_pair(c1))
        screen.addstr(7, 5, "RECIEVE EMAIL", curses.color_pair(c2))
    q = screen.getch()
    screen.clear()
    if x == 1:
        break
    if q == curses.KEY_UP:
        c1 = 2
        c2 = 1
        if q == ord("\n"):
            loopySend()

    if q == curses.KEY_DOWN:
        c1 = 1
        c2 = 2
    if q == ord("\n") and c2 == 2:
        x = 1
        screen.clear()
        loopyRecieve()

    if q ==ord("\n") and c1 == 2:
        x = 1
        screen.clear()
        loopySend()

    if q == ord("e"):
        sys.exit()
    screen.refresh()
curses.endwin()

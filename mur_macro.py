import pyautogui
import time

SHORT_WAIT_TIME = 0.5
WAIT_TIME = 2
LONG_WAIT_TIME = 4
SCREEN_RIGHT = pyautogui.size()[0]
SCREEN_BOTTOM = 818
ARTICLE_COUNT = int(input("how many articles for this candidate?"))



#switch to article on left
pyautogui.click(x=0, y=400)


#initialize to 16 tabs (17 except first)
tab_count = 16
finished = False
while (True):

    #copy article
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    
    #switch to input and paste
    pyautogui.click(x=SCREEN_RIGHT, y=SCREEN_BOTTOM)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep(WAIT_TIME)
    #type end article at end
    pyautogui.typewrite("end article")
    pyautogui.press('enter')
    time.sleep(SHORT_WAIT_TIME)
    

    ARTICLE_COUNT = ARTICLE_COUNT - 1
    if (ARTICLE_COUNT == 0):
        #ARTICLE COUNT IS ZERO LEAVE THE WHILE LOOP
        break
    
    #WE'RE STILL GOING TYPE Y AND CONTINUE
    pyautogui.typewrite("y")
    pyautogui.press('enter')

    #switch to article on left
    pyautogui.click(x=0, y=400)

    #arrange tabs
    tabs = ['tab' for i in range(0, tab_count)]
    tab_count = 17 #17 beyond first
    
    #tab to article
    pyautogui.typewrite(tabs)
    
    #navigate to article
    pyautogui.press('enter')

    #wait for load
    time.sleep(LONG_WAIT_TIME)
    




#we're done type n
pyautogui.press('n')
pyautogui.press('enter')

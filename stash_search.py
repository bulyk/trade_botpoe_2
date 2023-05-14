import requests
import time
import pyautogui
import win32gui
from PIL import ImageGrab, ImageChops, Image

POESESSID = '*******************'
accountName = '************'

number_tabs = 0
search_tab = 'cluster'
all_stesh_tabs = 3
hwnd = win32gui.FindWindow(None, "Path of Exile")

class Stash:       
    def __init__(self, base_x, base_y):
        self.base_x = base_x 
        self.base_y = base_y 

    def stesh_tabs(self, all_stesh_tabs, number_tabs, search_tab):
        cookies = {
            'POESESSID': POESESSID,
        }

        headers = {
            'accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.5.715 Yowser/2.5 Safari/537.36',
        }

        params = {
            'league': 'Crucible',
            'realm': 'pc',
            'accountName': accountName,
            'tabs':'1',
            'tabIndex': number_tabs,
            
        }

        response = requests.get(
            'https://www.pathofexile.com/character-window/get-stash-items',
            params=params,
            cookies=cookies,
            headers=headers,
            stream=True 
        )
        print(response)
        response_json = response.json()
        all_stesh_tabs = response_json['numTabs']
        dict_tabs = {}
        while number_tabs < int(all_stesh_tabs):
            name_tabs = response_json['tabs'][number_tabs]['n']
            dict_tabs[name_tabs] = number_tabs
            number_tabs += 1
        print(dict_tabs)
        if search_tab in dict_tabs:
            number_tab = dict_tabs[search_tab]        
        time.sleep(1)
        return number_tab, all_stesh_tabs

    def click_stash():
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(.05)
        stash = pyautogui.locateOnScreen('stash.png', confidence=0.7)
        stash_center = pyautogui.center(stash)
        pyautogui.moveTo(stash_center[0]-5, stash_center[1])
        pyautogui.click()
        
    def clear(self):
        inventory = Stash.dict_cell(self)
        number_cell = 0
        hwnd = win32gui.FindWindow(None, "Path of Exile")
        hdc = win32gui.GetDC(hwnd)
        screenshot_stash = ImageGrab.grab(bbox=(self.base_x, self.base_y,int(inventory[59][0]), int(inventory[59][1])))
        # screenshot_stash.save('empty stash.png')
        empty_stash = Image.open('empty stash.png')
        diff = ImageChops.difference(screenshot_stash, empty_stash)
        bbox = diff.getbbox()
        if bbox is None or (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) <= 80: #если изобаржения сопадают
            pass
        else:
            screenshot_stash = ImageGrab.grab(bbox=(self.base_x, self.base_y, int(inventory[19][0]), int(inventory[19][1])))
            # screenshot_stash.save('empty stash1_3.png')
            empty_stash1_3 = Image.open('empty stash1_3.png')
            diff = ImageChops.difference(screenshot_stash, empty_stash1_3)
            bbox = diff.getbbox()
            if bbox is None or (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) <= 80:
                screenshot_stash = ImageGrab.grab(bbox=(int(inventory[20][0]), int(inventory[20][1]),int(inventory[39][0]), int(inventory[39][1])))
                # screenshot_stash.save('empty stash2_3.png')
                empty_stash1_3 = Image.open('empty stash2_3.png')
                diff = ImageChops.difference(screenshot_stash, empty_stash1_3)
                bbox = diff.getbbox()     
                if bbox is None or (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) <= 180:
                    # print('3/3 stash check')
                    number_cell = 40
                    while number_cell != 60:
                        coord = (int(inventory[number_cell][0]), int(inventory[number_cell][1]))    
                        pixel1 = win32gui.GetPixel(hdc, coord[0], coord[1])
                        r_pixel2 = (1)
                        r_pixel1 = pixel1 & 0xff
                        tolerance = 20
                        if abs(r_pixel1 - r_pixel2) > tolerance:
                            pyautogui.keyDown('ctrl') 
                            pyautogui.moveTo(coord)
                            pyautogui.click()
                        pyautogui.keyUp('ctrl') 
                        number_cell += 1
                    win32gui.ReleaseDC(hwnd, hdc)
                    Stash.clear()
                else:
                    # print('2/3 stash check')
                    number_cell = 20
                    while number_cell != 40:
                        coord = (int(inventory[number_cell][0]), int(inventory[number_cell][1]))    
                        pixel1 = win32gui.GetPixel(hdc, coord[0], coord[1])
                        r_pixel2 = (1)
                        r_pixel1 = pixel1 & 0xff
                        tolerance = 20
                        if abs(r_pixel1 - r_pixel2) > tolerance:
                            pyautogui.keyDown('ctrl') 
                            pyautogui.moveTo(coord)                            
                            pyautogui.click()
                        pyautogui.keyUp('ctrl') 
                        number_cell += 1
                    win32gui.ReleaseDC(hwnd, hdc)    
                    Stash.clear(self)    
            else:
                # 1/3 stash check
                while number_cell != 20:
                    coord = (int(inventory[number_cell][0]), int(inventory[number_cell][1]))    
                    pixel1 = win32gui.GetPixel(hdc, coord[0], coord[1])
                    r_pixel2 = (1)
                    r_pixel1 = pixel1 & 0xff
                    tolerance = 20
                    if abs(r_pixel1 - r_pixel2) > tolerance:
                        pyautogui.keyDown('ctrl') 
                        pyautogui.moveTo(coord)
                        pyautogui.click()
                    pyautogui.keyUp('ctrl') 
                    number_cell += 1
                win32gui.ReleaseDC(hwnd, hdc)
                Stash.clear(self)

    def dict_cell(self):
        number_x = 0
        number_y = 0
        inventory = {}
        number_cell = 0
        while number_cell != 60:
            if number_y != 5:
                x_coord = self.base_x+number_x*53
                y_coord = self.base_y+number_y*52
                inventory[number_cell] = [x_coord, y_coord]
                number_cell += 1
                number_y += 1
            else:
                number_y = 0
                number_x += 1
                x_coord = self.base_x+number_x*53
                y_coord = self.base_y+number_y*52
                inventory[number_cell] = [x_coord, y_coord]
                number_cell += 1
                number_y = 1   
        return inventory






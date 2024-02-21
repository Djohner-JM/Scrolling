from os import system, name
from time import sleep
from yaml import safe_load, dump
from sys import exit
from collections.abc import Callable


class Scrolling:    
    TIME_DIVISION = 50
    CONFIG_FILE = "config.yml"
    SEPARATOR = ("|", "-")
    POSSIBLE_DIRECTION = (("left", "up"), ("right", "down"))
    MESSAGE = "Élément de modification non valide"

    def __init__(self)-> None:
        self._direction = False
        self._data = self._load_data(Scrolling.CONFIG_FILE)
        self._PATH = tuple(self._data.keys())
        self._SCROLL_DIR = tuple(self._data[self._PATH[0]].keys())
        self._KEY_SCROLL = tuple(self._data[self._PATH[0]][self._SCROLL_DIR[0]].keys())
        self._KEY_TEXT = tuple(self._data[self._PATH[1]].keys())
        
        self._ALL_KEYS = self._KEY_TEXT + self._KEY_SCROLL
        for elem in self._ALL_KEYS:
            exec(f"self.{elem.upper()} = {self._ALL_KEYS.index(elem)}")
       
    @property
    def direction(self) -> str:
        return self._direction
    
    @direction.setter
    def direction(self, value:str) -> None:
        self._direction = self._SCROLL_DIR[1] == value
        
    def _data_initialization(self) -> list:
        data_text = [self._data[self._PATH[1]][t] for t in self._KEY_TEXT]
        data_scrolling = [self._data[self._PATH[0]][self._SCROLL_DIR[self._direction]][s] for s in self._KEY_SCROLL]
        data_text[0] = f"{data_text[0]:^{data_scrolling[1]}}"
        data_text[1] = f"{data_text[1]:^{data_scrolling[2] * 2 + len(data_text[1])}}"
        data_text.extend(data_scrolling)
    
        return data_text
        
    def _load_data(self, config:str) -> dict:
        with open(config, mode="r", encoding="utf-8") as f:
            return safe_load(f)
         
    def _scroll_display(self, data:list, index:int=0) -> Callable[[list, int], Callable]: 
        sep = Scrolling.SEPARATOR[self._direction]
        while True: 
            if data[self.DIRECTION] in Scrolling.POSSIBLE_DIRECTION[0]:
                scroll_text = data[self.SCROLL][index:index+data[self.LENGTH]]
            else:
                scroll_text = data[self.SCROLL][index-data[self.LENGTH]:index if index else None]
                
            index += 1 if data[self.DIRECTION] in Scrolling.POSSIBLE_DIRECTION[0] else -1
            if abs(index) >= len(data[self.SCROLL]) - data[self.LENGTH]: index = 0
            
            list_display = [f"{'':<{data[self.POSITION][self._direction]}}", data[self.FIXED], scroll_text]
            display = [elem + sep for elem in list_display]
            if not self._direction:
                display = f"{"\n" * data[self.POSITION][not self._direction]}{"".join(display)}"
            else:
                display = "".join((f"\n{(' ' * data[self.POSITION][not self._direction])}{elem}") for elem in "".join(display))
            
            system('cls') if name == 'nt' else system('clear')
            print(display)
            sleep(Scrolling.TIME_DIVISION/data[self.SPEED])
           
    def modify(self, elem_to_change:str, value:str|int|list) -> None:
        if elem_to_change not in self._ALL_KEYS:
            exit(Scrolling.MESSAGE)
            
        if elem_to_change in self._KEY_SCROLL:
            self._data[self._PATH[0]][self._SCROLL_DIR[self._direction]][elem_to_change] = value
        else:
            self._data[self._PATH[1]][elem_to_change] = value

        with open(Scrolling.CONFIG_FILE, "w") as f:
            dump(self._data, f)
        
    def __call__(self) -> Callable[[Callable], list]:
        return self._scroll_display(self._data_initialization())



if __name__ == "__main__" :
    scroll = Scrolling()
    scroll.direction = "vertical"
    # scroll.direction = "horizontal"
    # scroll.modify("scroll", "La fleur en bouquet fane… Et jamais ne renaît !")
    # scroll.modify("fixed", "你好")
    # scroll.modify("fixed_text", 10)
    # scroll.modify("length", 20)
    # scroll.modify("position", [2,2])
    # scroll.modify("speed", 500)
    scroll()
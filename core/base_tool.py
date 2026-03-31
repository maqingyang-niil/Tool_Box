from abc import ABC, abstractmethod

class BaseTool(ABC):
    name:str=""
    icon:str=""
    description:str=""

    @abstractmethod
    def get_widget(self,parent)->"QWidget":
        """"返回UI"""
        pass
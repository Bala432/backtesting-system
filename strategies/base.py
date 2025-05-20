from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC):
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        
    @abstractmethod
    def generate_signals(self):
        pass
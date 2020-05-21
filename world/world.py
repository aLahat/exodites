import zipfile,io
import pandas
class world:

    def __init__(self,f=None):
        self.sort_char=('name',True)

        if f==None:
            pass
        else:
            with zipfile.ZipFile(f,'r') as z:
                    with z.open('characters.csv') as f:
                        self.characters= pandas.read_csv(f,index_col=0)#.head()
                        self.characters.index=[i.replace(' ','') for i in self.characters.index]
                    with z.open('events.csv') as f:
                        self.events= pandas.read_csv(f,index_col=0)
    def sort_characters(self,q):
        ascending=self.sort_char[1]
        self.characters.sort_values(
            q,
            ascending=ascending,
            inplace=True
            )
        self.sort_char=(q,not ascending)

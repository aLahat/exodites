import os
from world import world
from world.thisfacedoesnotexist import download as gt_face
import tornado.ioloop
import tornado.web
from tornado.escape import url_escape
from glob import glob
import random
from pprint import pprint
import string
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = [['a','f'],['a','f']]
        header=['1','2']
        self.render("templates/cards", title="My title", rows=items,header=header)


class charactersHandler(tornado.web.RequestHandler):
    def get(self):
        sort=self.get_argument("sort_by", None, True)
        change=self.get_argument("change", None, True)
        change_from=self.get_argument("from", None, True)
        change_to=self.get_argument("to", None, True)
        refresh_image=self.get_argument("refresh_image", None, True)
        newface=self.get_argument("newface", None, True)
        if sort!=None:
            w.sort_characters(sort)
        if refresh_image!=None:
            refresh_image=url_escape(refresh_image,plus=False)
            ID=gt_face(refresh_image)
            os.replace()

        if newface!=None:
            ID = self.get_argument("ID", None, True)
            if not os.path.exists(newface):
                os.replace(
                    newface,
                    "static/img/"+ID+'.jpeg'
                )

        self.render("templates/cards_characters", title="My title", data=w.characters.fillna('-'))#rows=items,header=header)

class change_faceHandler(tornado.web.RequestHandler):
    def get(self):
        ID=self.get_argument("refresh_image", None, True)
        rndStr=lambda x: ''.join([random.choice(string.ascii_lowercase) for _ in range(x)])
        while len(glob('static/img/temp_faces/*'))<100:
            gt_face('temp_faces/'+rndStr(9))
        self.render("templates/change_face", title="My title", data=w.characters.fillna('-'),files=glob('static/img/temp_faces/*'),
                    ID=ID)#rows=ichange_facetems,header=header)

class eventsHandler(tornado.web.RequestHandler):
    def get(self):
        sort=self.get_argument("sort_by", None, True)
        change=self.get_argument("change", None, True)
        change_from=self.get_argument("from", None, True)
        change_to=self.get_argument("to", None, True)
        if sort!=None:
            pass
        self.render("templates/cards_characters", )

class edit_characterHandler(tornado.web.RequestHandler):
    def get(self):
        ID=self.get_argument("ID", None, True)
        if ID=='':
            data={key:'' for key in w.characters.columns}
            self.render("templates/edit_char", ID='' , data=data)

        else:
            self.render("templates/edit_char", ID=ID , data=w.characters.fillna('').loc[ID])#rows=items,header=header)

char_items={
    "name":str,
    "surname":str,
    "gender":str,
    "birth":float,
    "death":float,
    "parents":str,
    "Main":bool
            }

class submit_char_changeHandler(tornado.web.RequestHandler):
    def get(self):
        ID=self.get_argument("ID", None, True)
        if ID != '':
            items=[char_items[key](self.get_argument(key, None, True)) for key in w.characters.columns]
            w.characters.loc[ID]=items

        self.redirect("/characters")

def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/characters",charactersHandler),
            (r"/change_face",change_faceHandler),
            (r"/edit_character",edit_characterHandler),
            (r"/events",eventsHandler),
            (r"/submit_char_change",submit_char_changeHandler),
            (r'/img/(.*)', tornado.web.StaticFileHandler,{"path":"./static"}),

        ],
        static_path=os.path.join(os.getcwd(), "static"),
        autoreload=True
    )


w=world.world('Exodus.zip')

if __name__ == "__main__":
    app = make_app()
    app.listen(8881)
    tornado.ioloop.IOLoop.current().start()

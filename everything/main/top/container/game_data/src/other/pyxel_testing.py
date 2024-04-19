#import pip
#pip.main(['install', 'pyxel'])
print('------------------------')
import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Hello Pyxel")
        #pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)
        pyxel.blt(61, 66, 0, 0, 0, 38, 16)


App()

# https://kitao.github.io/pyxel/wasm/launcher/?run=SketchedDoughnut.Development.main.top.game_data.src.other.pyxel_testing
# https://github.com/kitao/pyxel/wiki/How-To-Use-Pyxel-Web
# import pyxel
# pyxel on PyPi
class Gatto:
    def __init__(self,nome):
        self.nome = nome

    def miagola(self,verso):
        return "il gatto di nome {} fa {}".format(self.nome,verso)

    def __str__(self):
        return str(self.nome)

class Cane:
    def __init__(self, nome):
        self.nome = nome

    def abbaia(self, verso):
        return "il cane di nome {} fa {}".format(self.nome, verso)

    def __str__(self):
        return str(self.nome)

class Mucca:
    def __init__(self, nome):
        self.nome = nome

    def muggito(self, verso):
        return "il cane di nome {} fa {}".format(self.nome, verso)

    def __str__(self):
        return str(self.nome)

class Adapter:
    def __init__(self, obj, adapted_method):
        self.obj = obj
        self.__dict__.update(adapted_method)

    def __str__(self):
        return str(self.obj)

class Animale:
    def __init__(self,nome):
        self.nome = nome

    def verso(self,verso):
        return "l'animale di nome {} fa {}".format(self.nome,verso)

    def __str__(self):
        return str(self.nome)

"""Main"""

object = []
animale = Animale("Zanzara")
object.append(Adapter(animale,dict(verso = animale.verso,nomeVerso = "ziz ziz")))
cane = Cane("Tommy")
object.append(Adapter(cane,dict(verso = cane.abbaia,nomeVerso="bau bau")))
gatto = Gatto("Garfield")
object.append(Adapter(gatto,dict(verso = gatto.miagola,nomeVerso = "miao miao")))
mucca = Mucca("Giorgio")
object.append(Adapter(mucca,dict(verso = mucca.muggito, nomeVerso = "muuu muuuu")))

for elem in object:
    print("{}".format(elem.verso(elem.nomeVerso)))
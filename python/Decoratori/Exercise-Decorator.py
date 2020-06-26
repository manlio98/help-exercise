"""• Definire un decoratore di classe che permette alla classe decorata di
contare le sue istanze."""


def decorator(aClass):
    aClass.instance = 0
    aClass.__old__init = aClass.__init__

    def mod(self, *args, **kwargs):
        aClass.instance = aClass.instance + 1
        aClass.__old__init(self, *args, **kwargs)

    aClass.__init__ = mod
    return aClass


@decorator
class C:
    def ciao(self):
        print("ciao")


"""
C()
C()
C()

print(C.instance)
"""


"""Definire un decoratore di funzione che trasforma una funzione che
prende in input un numero variabile di numeri in una funzione che
prende in input una lista e opera solo sugli elementi della lista di tipo
float, int e str convertiti in int.
• la funzione somma non decorata viene invocata in questo modo:
somma(3.5, 6, 1.2)
• se usiamo il decoratore, possiamo invocare somma([1.3, 4 ,"6"])"""


def castInt(function):
    def wrappper(list, *args, **kwargs):
        args = []
        for i in list:
            if isinstance(i, int) or isinstance(i, float) or isinstance(i, str):
                args.append(int(i))
        return function(*args, **kwargs)

    return wrappper


@castInt
def somma(*args):
    sum = 0
    for elem in args:
        sum = sum + elem
    return sum



"""• Scrivere una classe di base ClsBase in cui c’e` un metodo addAttr che
• prende in input due argomenti: una stringa s e un valore v,
• controlla se la classe ha l’attributo di nome s e se tale attributo non e`
presente allora aggiunge alla classe l’attributo s con valore v; in caso contrario
non fa niente.
• Il metodo deve funzionare anche per le eventuali sottoclassi di ClsBase"""


class ClsBase:
    def addAttr(self, stringa, val):
        try:
            attr = getattr(ClsBase, "s")
        except:
            AttributeError
        setattr(ClsBase, "s", val)

"""Soluzione alternativa"""
""" flag = False
for elem in ClsBase.__dict__:
if elem is "s":
flag = True
if flag == False:
setattr(ClsBase, "s", val)"""
"""
class Sub(ClsBase):
    def addAttr(self, stringa, val):
        ClsBase.addAttr(self,stringa,val)
"""



"""• Scrivere una classe che contiene un metodo che restituisce il numero
di invocazioni degli altri metodi della classe. Il codice dei suddetti
metodi non deve essere modificato."""


def count(function):
    def wrapper(*args, **kwargs):
        C.numMetodi += 1
        function(*args, *kwargs)

    return wrapper


class C:
    numMetodi = 0

    @count
    def ciao(self):
        print("ciao")

    @count
    def meth1(self):
        print("sono meth1")

    @staticmethod
    def getNumMetodi():
        return C.numMetodi



"""Scrivere un decorator factory che genera un decoratore di classe che
dota la classe di un metodo che restituisce il numero di invocazioni
del metodo passato come parametro al decorator factory."""


def countInvocationMetodo(function):
    def decorator(aClass):
        aClass.numInstance = 0

        def wrapper(*args, **kwargs):
            aClass.numInstance += 1
            getattr(aClass, function)

        setattr(aClass, function, wrapper)

        def nTimes():
            return DecFactory.numInstance

        aClass.nTimes = staticmethod(nTimes)
        return aClass

    return decorator


@countInvocationMetodo("metodo1")
class DecFactory():
    def metodo1(self):
        print("Sono metodo 1")

    def metodo2(self):
        print("Sono metodo 2")




"""Modificare il codice di cui all’esercizio 2 in modo tale che il decoratore possa essere
parametrizzato con un intero i che indica il numero massimo di istanze che possono essere
create. Se si tenta di creare piu` di i istanze della classe decorata si ha un RuntimeError. Il
codice di questo esercizio deve essere scritto nel file esercizio3.py."""


def decoraClasse1(argomenti):
    def decoratore(aClass):
        aClass.numInstance = 0
        setattr(aClass, "old_init", aClass.__init__)

        def new_init(*args, **kwargs):
            aClass.numInstance = aClass.numInstance + 1
            if (aClass.numInstance > argomenti):
                raise RuntimeError("Impossibile creare più di un'istanza")
            getattr(aClass, "old_init")

        aClass.__init__ = new_init
        return aClass

    return decoratore


@decoraClasse1(3)
class Prova1:
    def __init__(self):
        self.x = 0

    def ciao(self):
        print("ciao")


"""Scrivere nel file esercizio2.py un decoratore di classe contaIstanze che dota la classe
decorata di un metodo istanzeDiClassiDer che conta quante sono le istanze di classi
derivate direttamente dalla classe decorata. Ad esempio, supponiamo che la classe
decorata sia la classe CL e supponiamo di definire le due classi CLF1 e CLF2 come segue
class CLF1(CL): … e class CLF2(CL): … e di creare 5 oggetti di tipo CLF1 e 3 oggetti di tipo
CLF2. Supponiamo inoltre che non vi sia nessuna altra classe che estende direttamente CL.
In questo caso istanzeDiClassiDer deve restituire 8 indipendentemente dal numero totale
di oggetti di tipo CL. Ovviamente il metodo deve funzionare per un numero arbitrario di
sottoclassi immediate della classe base e il decoratore NON deve essere usato per
decorare le sottoclassi."""


def contaIstanze(aClass):
    aClass.num = 0
    setattr(aClass, "old_init", aClass.__init__)

    def new_init(self, *args, **kwargs):
        if self.__class__.__bases__.__contains__(CL):
            aClass.num = aClass.num + 1
            getattr(aClass, "old_init")(*args,**kwargs)
        getattr(aClass, "old_init")

    aClass.__init__ = new_init

    def istanzeDiClasseDer(self):
        return aClass.num

    aClass.istanzeDiClasseDer = istanzeDiClasseDer
    return aClass


@contaIstanze
class CL:
    def __init__(self, x, y):
        self.x = x
        self.y = x


class CL1(CL):
    pass


class CL2(CL):
    pass


"""Scrivere nel file esercizio2.py il decoratore di funzione decoratore che trasforma in interi
gli argomenti non keyword della funzione decorata utilizzando int(); se un argomento non
e` trasformabile in intero con int() allora la funzione stampa "L'argomento {} non puo`
essere convertito" e lo fa per ogni argomento non convertibile. Nel caso in cui la
conversione di tutti gli argomenti non keyword vada a buon fine, il decoratore deve
stampare il risultato della funzione invocata con gli argomenti non keyword convertiti in
interi. Le docstring delle funzioni decorate non devono essere modificate dal decoratore."""


def converti_int(function):
    def wrapper(*args, **kwargs):
        cast = []
        try:
            for elem in args:
                cast.append(int(elem))
            print(cast)
        except ValueError:
            print("L'argomento {} non può essere convertito".format(elem))
        return function(*args, **kwargs)

    return wrapper


@converti_int
def stampaInteri(*args):
    pass



""""Scrivere un decorator factory che genera un decoratore di classe che
dota la classe di un metodo che restituisce il numero di invocazioni
del metodo passato come parametro al decorator factory."""


def countInvocationMetodo(meth1, meth2):
    def countdecorator(aClass):
        aClass.numInstanceMeth1 = 0 #setto le due var a 0
        aClass.numInstanceMeth2 = 0
        setattr(aClass, "old_meth1", meth1) #metto la funzione da contare in oldmeth
        setattr(aClass, "old_meth2", meth2)

        def new_meth1(*args, **kwargs):  #modificare il metodo passato
            aClass.numInstanceMeth1 += 1 #incremento
            getattr(aClass, "old_meth1") #invocare il metodo vecchio

        setattr(aClass, meth1, new_meth1) #rimetto il nuovo metodo(incremento) nuovamente in meth1(originale)

        def new_meth2(*args, **kwargs):
            aClass.numInstanceMeth2 += 1
            getattr(aClass, "old_meth2")

        setattr(aClass, meth2, new_meth2)

        def getIstance():
            return DecFactory.numInstanceMeth1 + DecFactory.numInstanceMeth2

        aClass.getInstance = staticmethod(getIstance)
        return aClass

    return countdecorator


@countInvocationMetodo("metodo1", "metodo2")
class DecFactory():
    def metodo1(self):
        print("Sono metodo 1")

    def metodo2(self):
        print("Sono metodo 2")



"""Si consideri la classe ClasseBase inserita tra i commenti nel file esercizio3.py. Si scriva un
decoratore di nome ClasseBase che possa essere applicato ad una qualsiasi classe in modo
che la classe cosi` decorata si comporti come se fosse derivata da ClasseBase"""
def classBase(aClass):
    setattr(aClass,"somma",0)
    def somma(self,a,b):
        self.somma = a + b
    setattr(aClass,"somma",somma)
    def getSomma(self):
        return self.somma
    setattr(aClass,"getSomma",getSomma)
    return aClass


class ClasseBase:
    def __init__(self):
        self.somma = 0
    def somma(self,a,b):
        self.somma = a + b
    def getSomma(self):
        return self.somma


@classBase
class MyClass:
    pass

def main():
    a = MyClass()
    a.somma(4,6)
    print(a.getSomma())

if __name__ == "__main__":
    main()




"""2. Scrivere nel file esercizio2.py un decorator factory decFact(L1,L2) che prende in input una
lista di stringhe e una stringa di oggetti e produce un decoratore che fa in modo che le
istanze della classe nascano non solo con le variabili di istanza aggiunte dal metodo
__init__ della classe ma anche con le seguenti variabili di istanza:
• per ogni i =1,…, len(L1), una variabile con nome uguale a quello della i-esima
stringa di L1 e valore uguale all’i-esimo oggetto di L2. Nel caso in cui __init__
della classe originaria aggiungeva gia` una variabile di istanza con nome uguale
all’i-esima stringa di L1 allora il valore della variabile deve essere quello
assegnato da __init__ della classe originaria. """
def decFact(lista1, lista2):
    def decora(aClass):
        aClass.old_init = aClass.__init__

        def check_nome_variabile(nome_variabile):
            flag = False
            for elem in aClass.__dict__:
                if elem == nome_variabile:
                    flag = True
            return flag

        def new_init(self, *args, **kwargs):
            for elem1, elem2 in zip(lista1, lista2):
                if not check_nome_variabile(elem1):
                    setattr(aClass, elem1, elem2)
            aClass.old_init(self, *args, **kwargs)

        aClass.__init__ = new_init
        return aClass

    return decora


@decFact(["var1", "var2", "var3", "var4"], ["pop", "ciao", [100, 21], 2])
class C1:
    def __init__(self, v1, v2, v3):
        self.x1 = v1
        self.x2 = v2
        self.x3 = v3


@decFact(["var1", "var2", "var3"], ["Pallone", "orto", {"y": 4}])
class C2:
    def __init__(self, *args):
        if len(args) < 3:
            print("numero errato di argomenti")
        else:
            self.var1 = args[0]
            self.x1 = args[1]
            self.x2 = args[2]


c = C1('a', 'b', 10)
print(c.x1, c.x2, c.x3, c.var1, c.var2, c.var3, c.var4)

c = C2('a', 'b', 10, 23)
print(c.x1, c.x2, c.var1, c.var2, c.var3)




"""
Il programma deve stampare:

a b 10 pop ciao [100, 21] 2
b 10 a orto {'y': 4}

"""
from calendar import c
from dis import dis, disco
from re import S
from select import select
import sys
import textwrap
from this import d

VER = 1.02

SPACER0 = 80 * "─"
SPACER1 = 28 * "="
SPACER2 = 28 * "-"

UNKNOWN_ERROR = "Tapahtui odottamaton virhe: {0}."
UNKNOWN_SELECTION = "Virheellinen valinta, yritä uudelleen."
BAD_VALUE = "Virheellinen {0}, yritä uudelleen."
NO_ITEMS = "Et ole vielä lisännyt yhtään tuotetta."


class ITEM():
    name = "item_name"      # Tuotteen nimi.
    price = 0.00            # Kappalehinti.
    count = 0               # Lukumäärä.
    discount_percent = 0.00 # Alennusprosentti.

    discount = 0.00         # Yhdestä kappaleesta saatava alennus (€).
    total_discount = 0.00   # Kappalealennusten summa (€).
    sub_total = 0.00        # Kokonaishinta ILMAN alennusta (€).
    total = 0.00            # Lopullinen kokonaishinta (€).

    """ def __init__(self, name, price, count, discount_percent):
        self.setName(name)
        self.setPrice(price)
        self.setCount(count)
        self.setDiscount(discount_percent) """
    
    def setName(self):
        self.name = input("Anna nimi: ").upper()
    
    def setPrice(self):
        # Kysytään tuotteen hinta
        while (True):
            temp_error = BAD_VALUE.format("hinta")
            try:
                temp_price = float(input("Anna hinta (€): "))
                if (temp_price >= 0):
                    break
                else:
                    print(temp_error)
                    continue
            except ValueError:
                print(temp_error)
                continue
            except Exception as temp_error:
                print(UNKNOWN_ERROR.format(temp_error))
                sys.exit(-2)
        self.price = temp_price
        self.calculateVariables()
    
    def setCount(self):
        # Kysytään tuotteiden lukumäärä. try estää virheellisen datan syöttämisen
        while (True):
            temp_error = BAD_VALUE.format("lukumäärä")
            try:
                temp_count = int(input("Anna lukumäärä (kpl): "))
                if (temp_count > 0):
                    break
                else:
                    print(temp_error)
                    continue
            except ValueError:
                print(temp_error)
                continue
            except Exception as temp_error:
                print(UNKNOWN_ERROR.format(temp_error))
                sys.exit(-3)
        self.count = temp_count
        self.calculateVariables()
    
    def setDiscountPercent(self):
        # Kysytään tuotteen aleprosentti. try estää virheellisen datan syöttämisen
        while (True):
            temp_error = BAD_VALUE.format("alennusprosentti")
            try:
                temp_discount_percent = float(input("Anna alennusprosentti (%): "))
                if (0 <= temp_discount_percent <= 100):
                    break
                else:
                    print(temp_error)
                    continue
            except ValueError:
                print(temp_error)
                continue
            except Exception as temp_error:
                print(UNKNOWN_ERROR.format(temp_error))
                sys.exit(-4)
        self.discount_percent = temp_discount_percent
        self.calculateVariables()

    # Lasketaan alennettu hinta yhdelle kappaleelle.
    def calcDiscount(self):
        self.discount = self.price * (self.discount_percent / 100)
    
    # Lasketaan kokonaisalennus.
    def calcTotalDiscount(self):
        self.total_discount = self.count * self.discount

    # Lasketaan välisumma.
    def calcSubTotal(self):
        self.sub_total = self.count * self.price
    
    # Lasketaan maksettava hinta.
    def calcTotalPrice(self):
        self.total_price = self.sub_total - self.total_discount

    # Lasketaan kaikki muuttujat uudelleen.
    def calculateVariables(self):
        self.calcDiscount()
        self.calcSubTotal()
        self.calcTotalDiscount()
        self.calcTotalPrice()


def printList(ls, i):
    print("┌────┬─────────────────────┬───────────┬──────────┬───────────┬─────────┬───────────┬───────────┐")
    print("│ ID │ NIMI                │ HINTA     │ MÄÄRÄ    │ VÄLISUMMA │ ALE (%) │ ALE (€)   │ YHTEENSÄ  │")

    for item in ls:
        print("├────┼─────────────────────┼───────────┼──────────┼───────────┼─────────┼───────────┼───────────┤")
        text = ""
        text += "│ {id:>2} "
        text += "│ {name:<19} "
        text += "│ {price:>7.2f} € "
        text += "│ {count:>4} kpl "
        text += "│ {sub_total:>7.2f} € "
        text += "│ {discount_percent:>5.1f} % "
        text += "│ {discount:>7.2f} € "
        text += "│ {total:>7.2f} € "
        text += "│"
        text = text.format(id=i,
                           name=textwrap.shorten(item.name, width=19),
                           price=item.price,
                           count=item.count,
                           sub_total=item.sub_total,
                           discount_percent=item.discount_percent,
                           discount=item.total_discount,
                           total=item.total
                          )
        print(text)
        i += 1
    print("└────┴─────────────────────┴───────────┴──────────┴─────────┘")


def modifyMenu():
    while (True):
        print()
        print("Valitse muutettava ominaisuus:")
        print("1) Nimi")
        print("2) Hinta")
        print("3) Määrä")
        print("4) Alennusprosentti")
        print("0) Peruuta")
        try:
            selection = int(input("Valintasi: "))
            if (0 <= selection <= 4):
                break
            else:
                print(UNKNOWN_SELECTION)
                continue
        except ValueError:
            print(UNKNOWN_SELECTION)
            continue
        except Exception as error:
            print(UNKNOWN_ERROR.format(error))
            sys.exit(-5)
    return(selection)


def addItem(items):
    print(SPACER0)
    print("Tuotteiden lisäys:")
    item = ITEM()
    item.setName()
    item.setPrice()
    item.setCount()
    item.setDiscountPercent()
    items.append(item)
    return None


def modifyItem(items):
    while (True):
        # Vahvistetaan jatkaminen.        
        ID_MAX = len(items)-1
        print(SPACER0)
        print("Tuotteiden muokkaus:")
        printList(items, 1)
        print()

        while (True):
            error = BAD_VALUE.format("ID")
            try:
                print("Anna muutettavan tuotteen ID")
                id = int(input("(0 palaa takaisin): "))
                if (id == 0):
                    return None
                elif (1 <= id <= ID_MAX+1):
                    break
                else:
                    print(error)
                    continue
            except ValueError:
                print(error)
            except Exception as error:
                print(UNKNOWN_ERROR.format(error))
                sys.exit(-4)
        
        item = items[id-1]
        items1 = [item]
        
        while (True):
            print()
            printList(items1, id)
            selection = modifyMenu()
            if (selection == 1):
                item.setName()
            elif (selection == 2):
                item.setPrice()
            elif (selection == 3):
                item.setCount()
            elif (selection == 4):
                item.setDiscount()
            elif (selection == 0):
                break
            else:
                print(UNKNOWN_SELECTION)


def removeItem(items):
    while (True):
        ID_MAX = len(items)-1
        print(SPACER0)
        print("Tuotteiden poisto:")
        printList(items)
        print()

        while (True):
            error = BAD_VALUE.format("ID")
            try:
                print("Anna poistettavan tuotteen ID")
                id = int(input("(0 palaa takaisin): "))
                if (id == 0):
                    return None
                elif (1 <= id <= ID_MAX+1):
                    break
                else:
                    print(error)
                    continue
            except ValueError:
                print(error)
            except Exception as error:
                print(UNKNOWN_ERROR.format(error))
                sys.exit(-4)
        
        while (True):
            print("Haluatko varmasti poistaa tuotteen seuraavan tuotteen?")
            item = items[id-1]
            items1 = [item]
            printList(items1, id)
            selection = input("Poista tuote (k/e): ")
            if (selection == "k"):
                items.pop(id-1)
                print("Tuote '{0}' poistettiin listalta.".format(id))
                break
            elif (selection == "e"):
                print("Tuotteen poistaminen peruutettiin.")
                break
            else:
                print(UNKNOWN_SELECTION)


def menu():
    print("Päävalikko:")
    print("1) Lisää tuote")
    print("2) Muokkaa tuotetta")
    print("3) Poista tuote")
    print("4) Esikatsele kuittia")
    print("5) Vie kuitti tekstitiedostoon")
    print("6) Tallenna tiedosto")
    print("7) Avaa tiedosto")
    print("0) Lopeta")
    print()
    selection = input("Valintasi: ")
    try:
        selection = int(selection)
    except ValueError:
        pass
    except Exception as error:
        print(UNKNOWN_ERROR.format(error))
        sys.exit(-1)
    return(selection)


def main():
    items = []
    while (True):
        length = len(items)
        print(SPACER0)
        selection = menu()
        if (selection == 0):
            print("Kiitos ohjelman käytöstä.")
            break
        elif (selection == 1):
            addItem(items)
        elif (selection == 2):
            if (length == 0):
                print(NO_ITEMS)
            else:
                modifyItem(items)
        elif (selection == 3):
            if (length == 0):
                print(NO_ITEMS)
            else:
                removeItem(items)
        elif (selection == 4):
            if (length == 0):
                print(NO_ITEMS)
            else:
                print("4")
        elif (selection == 5):
            if (length == 0):
                print(NO_ITEMS)
            else:
                print("5")
        elif (selection == 6):
            if (length == 0):
                print(NO_ITEMS)
            else:
                print("6")
        elif (selection == 7):
            print("7")
        else:
            print(UNKNOWN_SELECTION)
    return None


main()
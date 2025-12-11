from datetime import date
import numpy as np

# --------------------------------------------------------
# 1) VSTUPNÍ DATA
# --------------------------------------------------------
# Cashflow (vklady záporně, výběry/aktuální hodnota kladně)
cashflows = [-3000, -1800, -2300, 8000]

# Odpovídající data jednotlivých pohybů
dates = [
    date(2025, 1, 1),
    date(2025, 2, 2),
    date(2025, 3, 5),
    date(2025, 4, 1)
]

# --------------------------------------------------------
# 2) JEDNODUCHÉ ZHODNOCENÍ
# --------------------------------------------------------
def simple_return(cashflows):
    total_invested = -sum(cf for cf in cashflows if cf < 0)
    final_value = cashflows[-1]
    gain = final_value - total_invested
    return gain / total_invested

simple = simple_return(cashflows)
print("Jednoduché zhodnocení:", round(simple * 100, 2), "%")


# --------------------------------------------------------
# 3) XIRR (IRR, MWR) – SKUTEČNÉ ZHODNOCENÍ PENĚZ
# --------------------------------------------------------
def xirr(cashflows, dates, guess=0.1):
    # přepočet dat na roky od prvního data
    t0 = dates[0]
    times = [(d - t0).days / 365 for d in dates]

    # definice NPV
    def npv(r):
        return sum(cf / ((1 + r) ** t) for cf, t in zip(cashflows, times))

    # derivace
    def d_npv(r):
        return sum(-t * cf / ((1 + r) ** (t + 1)) for cf, t in zip(cashflows, times))

    r = guess
    for _ in range(1000):  # Newtonova metoda
        r_new = r - npv(r) / d_npv(r)
        if abs(r - r_new) < 1e-10:
            break
        r = r_new

    return r

irr = xirr(cashflows, dates)
print("XIRR / IRR / MWR:", round(irr * 100, 2), "% p.a.")


# --------------------------------------------------------
# 4) TWR – TIME WEIGHTED RETURN
# --------------------------------------------------------
def time_weighted_return(values):
    """
    values = seznam hodnot portfolia po každém období,
    vždy BEZ vlivů vkladů/výběrů (tj. před a po úpravě).
    Tady si to budeme počítat podle cashflow.
    """

    # Pro výpočet TWR musíme znát hodnotu portfolia těsně před každým vkladem.
    # Proto si uděláme simulaci hodnot.
    # V tomto jednoduchém příkladu vezmeme změny relativně:

    twr_factors = []

    # Simulace průběhu hodnot
    # Zjednodušeně: mezi cashflow bereme čistý růst hodnoty
    for i in range(len(cashflows) - 1):
        # hodnota portfolia těsně před vkladem
        # předpokládáme, že změna je způsobena růstem
        start = -sum(cf for cf in cashflows[:i+1] if cf < 0)
        end = -sum(cf for cf in cashflows[:i+2] if cf < 0)

        if start != 0:
            twr_factors.append(end / start)

    # TWR = součin (1 + výnos v období) - 1
    twr = np.prod(twr_factors) - 1
    return twr

# Toto je jednoduchý TWR pro základní princip
twr = time_weighted_return(cashflows)
print("TWR (Time Weighted Return):", round(twr * 100, 2), "%")

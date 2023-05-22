# HeroesOfCatch

# Bekannte Bugs:

# 1) Wenn das Fenster länger verschoben wird, kann die Verbindung zum Server verloren gehen. (Während einer Runde ist die Wahrscheinlichkeit höher, da die Datenrate deutlich erhöht ist)
# Grund: Beim Verschieben, wird der Prozess oft pausiert. Das führt zu einem Datenstau, der fehlerhafte Pakete erzeugt.
# In diesem Fall wird die Serververbindung vom Client unterbrochen, um Abweichungen im Spielverlauf zu vermeiden.

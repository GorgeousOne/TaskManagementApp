# Task Management App
![So sieht es auf meinem PC aus](res/screenshots/example.png)

Task Management App ist ein Python-Projekt zum 
Dies ist das Abschlussprojekt von  für das Modul "Einführung in die Programmierung".

## Installation
Das Programm wurde mit [Python3](https://www.python.org/downloads/) entwickelt und benutzt die 
die Bibliothek "PySide2".

Sie kann mit [pip](https://pip.pypa.io/en/stable/) direkt installiert werden: `pip install PySide2`.  
(Oder es geht auch mit der requirements.rxt: `pip install -r requirements.txt`)

Mit dem Befehl `python3 main.py` kann die App dann ausgeführt werden.

## Bedienung

Mit dem Programm kann man Aufgaben und Erinnerungen als kleine Notizen anlegen, die dann in einer Zeitleiste aufgelistet werden.
Wird eine Notiz nicht mehr gebraucht, dann kann sie als erledigt markiert werden oder gelöscht werden.

#### Aufgaben anlegen
Mit dem "+" Knopf in der oberen blauen Leiste öffnet sich ein Formular, um eine neue Aufgabe zu erstellen.  

Eine Aufgabe braucht immer einen Titel und ein Datum.
Es kann auch eine Beschreibung hinzugefügt werden und ausgewählt werden, ob sie ganztags oder zu einer bestimmten Uhrzeit stattfindet.
Außerdem kann jede Aufgabe einem Projekt zugeordnet werden (siehe Optionale Features).

![](res/screenshots/editor.png)

Sobald die Notiz mit "Save" gespeichert wird sie mit in der Zeitleiste zu sehen. 
Die Beschreibung klappt sich unter dem Titel aus und ein, wenn man auf die Notiz klickt.

#### Aufgaben bearbeiten, erledigen, löschen
Wenn man mit der Maus über eine Aufgabe fährt, werden die Knöpfe zum Bearbeiten der Aufgabe sichtbar.

* Der Knopf mir dem Stift-Icon öffnet wieder das Formular, damit Änderungen gemacht werden können.
* Der "Completed"-Knopf markiert eine Aufgabe als erledigt und graut sie aus. Mit einem zweiten Klick auf den Knopf kann dies wieder rückgängig gemacht werden.
Erledigte Aufgaben können auch temporär ausgeblendet werden mit dem "Hide completed"-Kontrollkästchen in der oberen Leiste.

* Der Mülleimer-Knopf löscht eine Aufgabe permanent, was nicht rückgängig gemacht werden kann.

#### Aufgaben speichern und laden
Aufgaben und Projekte werden immer automatisch in einem Ordner "TaskManagementApp" im Benutzer Home-Verzeichnis abgespeichert.


## Optionale Features
Aus dem Pool der optionalen Features habe ich mir
* die Zuordnung von Aufgaben zu Projekten und
* die Bedienung des Programms über ein Command-Line-Interface

ausgesucht.

#### Projekte

Projekte können ähnlich wie Notizen in der linken Seitenleiste erstellt werden.
Der "+" Knopf mit dem Kreis herum, öffnet das Formular zum Erstellen eines Projektes.   Jedes Projekt braucht einen eindeutigen Namen und kann eine Farbe haben.

Genauso wie Aufgaben können Projekte mit Knöpfen, die beim hinüberfahren erscheinen, bearbeitet oder gelöscht werden.

![](res/screenshots/editor2.png)


Im Bearbeitungsformular kann eine Aufgabe dann einem Projekt zugeordnet werden, 
was dann an dem Projekticon in der Zeitleiste erkennbar ist.

Um sich nur die Aufgaben eines Projektes anzeigen zu lassen kann man auf den Namen eines Projektes klicken,
dann werden alle anderen Aufgaben ausgeblendet. 
Mit den "Show all tasks" Knopf werden wieder alle Aufgaben angezeigt.

#### CLI

Befehle des Command-Line-Interfaces können mit `python3 main.py` und dem Namen eines Unterbefehls dahinter ausgeführt werden.

Hier ist eine Übersicht aller Befehle:
```
task                    
    list                Lists all tasks with an index, optionally filters tasks of a project or uncompleted tasks
    create              Creates a new task
    edit                Edits the passed properties of a task
    complete            Sets the completion state of a task
    delete              Deletes a task
    
project                 
    list                Lists all projects
    create              Creates a new project
    rename              Renames a project
    delete              Deletes a project
```
Viele der untersten Befehle besitzen feste oder optionale Argumente. 
Die genaue Verwendung jedes Befehls kann mit `[command] -h` eingesehen werden.

##### Beispiele:
Der Befehl `python3 main.py task list` z.B. listet alle Aufgaben in der Konsole auf: 
```
-------------------- Samstag, 13. März --------------------
1  11:00
   &#2713; Gemüse einkaufen
      Paprika, Lauch, Zwiebeln, Kartoffeln
-------------------- Mittwoch, 17. März --------------------
2  14:00
   Opa Fridolin anrufen   (Familie&Freunde)
-------------------- Freitag, 2. April --------------------
3  Bib Buch zurückgeben   (Uni)
      Mathematik für Ingenieure und Naturwissenschaftler Band 1

```
Der Index einer Aufgabe in dieser Liste kann in anderen Befehlen verwendet werden, 
beispielsweise um den Einkauf an einen anderen Tag zu verschieben: `python3 main.py task edit 1 --date 23.3.`

Daraufhin steht diese Aufgabe an einer anderen Stelle in der Liste:
```
-------------------- Dienstag, 23. März --------------------
2  11:00
   &#2713; Gemüse einkaufen
      Paprika, Lauch, Zwiebeln, Kartoffeln
```

## Sonstiges


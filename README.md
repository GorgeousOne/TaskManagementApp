# Task Management App
Dieses Projekt wurde im Rahmen des Abschlussprojektes des Moduls "Einführung in die Programmierung" im Studiengang Informatik B.Sc. an der Bauhaus-Universität Weimar angefertigt.

Die Aufgabe bestand darin eine grafische Python-Anwendung zu entwickeln, mit der sich Aufgaben verwalten lassen.

## Installation
Um das Programm auszuführen muss [Python3](https://www.python.org/downloads/) installiert sein.  
Das Projekt benutzt die Bibliotheken:
* PySide2

Sie sind auch in der requirements.rxt aufgelistet und können mit `pip install -r requirements.txt` installiert werden.

Um das Programm mit GUI auszuführen, muss der Befehl `python3 main.py` ausgeführt werden.

## Features

### Aufgaben anlegen
Mit dem "+" Knopf in der oberen blauen Leiste öffnet sich ein Formular, in dem eine Aufgabe neu erstellt werden kann.  
*IMG*  

Eine Aufgabe hat immer einen Titel und ein Datum, zu dem sie gehört.
Es kann auch eine Beschreibung hinzugefügt und eine Uhrzeit und Projekt (siehe Optionale Features) ausgewählt werden.

Mit einem Klick auf "Save" wird die Aufgabe nun im Hauptfenster angezeigt.

### Darstellung der Aufgaben
Alle Aufgaben werden als zeitlich geordnete Liste im Hauptbereich der GUI angezeigt.
Tage sind durch beschriftete Trennlinien getrennt und Uhrzeiten werden in den Aufgabenkästchen angezeigt.
Haben Aufgaben keine Uhrzeit werden sie alphabetisch am Anfang des Tages angezeigt.

Wenn man mit der Maus über eine Aufgabe fährt werden all Knöpfe sichtbar, die zur Bearbeitung der Aufgabe vorhanden sind.

### Aufgaben bearbeiten, erledigen, löschen
* Der Knopf mir dem Stift-Icon öffnet wieder das Aufgaben-Formular und Änderungen können vorgenommen und gespeichert werden.
* Der "Completed"-Knopf markiert eine Aufgabe als erledigt und graut sie aus. Durch erneutes Klicken kann dies jederzeit wieder rückgängig gemacht werden.  
Erledigte Aufgaben können auch ganz ausgeblendet werden mit dem "Hide completed"-Kontrollkästchen in der oberen Leiste.

* Der Mülleimer-Knopf löscht eine Aufgabe permanent, was nicht rückgängig gemacht werden kann.

### Aufgaben speichern und laden
Aufgaben und Projekte werden immer automatisch in einem Ordner "TaskManagementApp" im Benutzer Home-Verzeichnis abgespeichert.


## Optionale Features
Aus dem Pool der optionalen Features habe ich mir
* die Zuordnung von Aufgaben zu Projekten und
* die Bedienung des Programms über ein Command-Line-Interface

ausgesucht.
  
### Projekte


### CLI


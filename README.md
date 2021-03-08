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

*IMG*


### Aufgaben bearbeiten, erledigen, löschen
Wenn man mit der Maus über eine Aufgabe fährt werden all Knöpfe sichtbar, die zur Bearbeitung der Aufgabe vorhanden sind.

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

Projekte können in der linken Seitenleiste erstellt werden. 
Mit einem Klick auf den "+" Knopf dort öffnet sich ein Formular zum Erstellen eines Projektes mit einem Namen und einer Farbe.
Genauso wie eine Aufgabe kann ein Projekt bearbeitet oder gelöscht werden mit den Knöpfen, die auftauchen,
wenn man mit der Maus über das Projekt fährt.

Eine Aufgabe kann dann einem Projekt zugeordnet werden, in dem dieses im Formular zum Bearbeiten der Aufgabe ausgewählt wird. Die Zuordnung einer Aufgabe zu einem Projekt wird durch das Anzeigen Projekticons in Timeline sichtbar gemacht.

Klickt man auf den Namen eines Projektes in der Seitenleiste, so werden all Aufgaben,
die nicht zu diesem Projekt gehören, ausgeblendet. 
Mit einem Klick auf "All tasks" werden wieder all Aufgaben angezeigt.

### CLI

Befehle des Command-Line-Interfaces können mit `python3 main.py` und dem Namen eines Unterbefehls dahinter ausgeführt werden.

Hier ist eine Übersicht aller Befehle:
```
task                    
    list                Lists all tasks with an index, optionally filters tasks of a project and/or all uncompleted tasks
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
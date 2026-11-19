# Home Assistant – FAQ für Einsteiger

Nov 19, 2026 · @Martin

Diese FAQ beantwortet die Fragen, die Einsteiger in den Facebook-Gruppen „Home Assistant DE“ und „Home Assistant Gruppe – Dashboard, Automationen und vieles mehr“ immer wieder stellen. Grundlage sind rund 180 Beiträge vom November 2026. Die Antworten beziehen sich auf **Home Assistant 2026.11**.

Wichtig vorab: 2026 haben sich zwei Begriffe geändert, über die viele Anleitungen im Netz noch stolpern. Aus **Add-ons** wurden **Apps**, und **HACS** heißt jetzt **Marketplace**. Wer eine ältere Anleitung liest, sollte die Begriffe gedanklich übersetzen.

## 1. Hardware und Installation

### Was brauche ich, um anzufangen?

Ein Gerät, das rund um die Uhr läuft, mit **Home Assistant OS (HAOS)**. Laut offizieller Installationsseite ist HAOS die empfohlene Installationsart für die meisten Nutzer ([Quelle](https://www.home-assistant.io/installation/)). Dazu kommen je nach Geräten ein Zigbee- oder Thread-Funkstick. WLAN-Geräte wie Shelly brauchen keinen Stick.

### Home Assistant Green, Raspberry Pi 5 oder Mini-PC?

| Option | Für wen | Hinweis |
| --- | --- | --- |
| Home Assistant Green | Wer ohne Basteln starten will | HAOS ist vorinstalliert; offiziell „der einfachste Einstieg“ |
| Raspberry Pi 4/5 | Wer schon einen hat | HAOS braucht mindestens 2 GB RAM; SSD statt SD-Karte ist robuster |
| Gebrauchter Mini-PC / Thin Client (x86-64) | Mehr Leistung, z. B. für lokale Sprachsteuerung | Fujitsu Futro, HP EliteDesk u. Ä. werden in den Gruppen oft genutzt |
| Virtuelle Maschine (Proxmox, Synology, Windows) | Wer schon einen Server betreibt | HAOS läuft als VM; Funksticks müssen durchgereicht werden |

Quelle für die Varianten und die 2-GB-Angabe: [home-assistant.io/installation](https://www.home-assistant.io/installation/).

*Einschätzung:* Für typische Haushalte mit Licht, Heizung und PV reicht ein Green oder ein Thin Client mit 4 GB RAM. Mehr Leistung braucht man vor allem für lokale Spracherkennung, Kameras mit Objekterkennung oder viele Apps.

### Ich will Windows auf dem Mini-PC loswerden. Wie installiere ich HAOS direkt?

HAOS ersetzt das Betriebssystem komplett. Man schreibt das Image für „Generic x86-64“ auf die interne SSD, dabei wird Windows gelöscht. Die Schritt-für-Schritt-Anleitung steht auf der [Installationsseite](https://www.home-assistant.io/installation/) unter „Generic x86-64“.

### Die VM unter Windows startet nicht. Woran liegt das?

*Einschätzung:* Meist ist im BIOS die Virtualisierung (Intel VT-x bzw. AMD-V) ausgeschaltet, oder die VM ist nicht auf UEFI gestellt. Bei schwachen Notebooks ist eine VM unter Windows außerdem keine gute Dauerlösung, weil der Rechner dann immer laufen muss.

### Der Green ist überall ausverkauft. Was tun?

Die Verfügbarkeit schwankt, aktuelle Händler lassen sich hier nicht seriös nennen. Ein gebrauchter Thin Client oder Mini-PC ist eine vollwertige Alternative mit derselben Software.

## 2. Erste Schritte und Begriffe

### Integration, App, Marketplace – was ist was?

| Begriff | Was es ist | Wo man es findet |
| --- | --- | --- |
| Integration | Verbindet HA mit einem Gerät oder Dienst (Shelly, Hue, Wechselrichter) | Einstellungen → Geräte & Dienste |
| App (früher „Add-on“) | Eigenes Programm neben HA, z. B. Zigbee2MQTT, Mosquitto, File Editor | Einstellungen → Apps (nur bei HAOS) |
| Marketplace (früher „HACS“) | Community-Erweiterungen: Integrationen, Dashboard-Karten, Themes | Einstellungen → Marketplace |

Add-ons heißen seit Version 2026.2 Apps ([Release-Notes 2026.2](https://www.home-assistant.io/blog/2026/02/04/release-20262/)). HACS ist seit 2026.11 als Marketplace fest eingebaut ([Release-Notes 2026.11](https://www.home-assistant.io/blog/2026/11/04/release-202611/)).

### Überall steht „installiere HACS“. Wie geht das?

Gar nicht mehr, und das ist auch nicht nötig. Ab 2026.11 lässt sich HACS nicht mehr separat installieren, der Marketplace ersetzt es ([Release-Notes 2026.11](https://www.home-assistant.io/blog/2026/11/04/release-202611/)). Wer HACS schon hatte, wird beim Update automatisch umgezogen. Installierte Erweiterungen bleiben erhalten ([raspberry.tips](https://raspberry.tips/en/smart-home/home-assistant-2026-11-whats-new)).

### Eine Erweiterung (z. B. Floorplan) ist nicht im Marketplace. Was tun?

Im Marketplace gibt es „Über Link hinzufügen“. Dort trägt man die GitHub-Adresse des Projekts ein. Das Repository muss öffentlich sein, und Home Assistant braucht dazu eine GitHub-Verbindung ([raspberry.tips](https://raspberry.tips/en/smart-home/home-assistant-2026-11-whats-new)).

### HA ist unter IP:8123 nicht erreichbar, nur ohne Port. Ist das kaputt?

Nein. Seit 2026.8 nutzen **neue** HAOS-Installationen standardmäßig eine normale Webadresse ohne Portnummer. Bestehende Installationen behalten ihren Port ([Release-Notes 2026.8](https://home-assistant.io/blog/2026/08/05/release-20268)). Viele ältere Anleitungen und Links mit „:8123“ passen deshalb nicht mehr. In der App und in Lesezeichen muss man die Adresse dann anpassen.

### HA findet nur einen Teil meiner Shellys. Muss ich alle per IP anlegen?

*Einschätzung:* Die automatische Erkennung läuft über mDNS und klappt meist nur, wenn HA und Geräte im selben Netz (Subnetz/VLAN) sind. Liegen die Geräte in einem anderen VLAN oder blockiert der Router Multicast, bleibt nur das manuelle Anlegen per IP. Feste IP-Adressen im Router zu vergeben, lohnt sich ohnehin. **Ich bin mir hier nicht sicher**, ob es bei Shelly noch weitere Ursachen gibt, etwa die Gerätegeneration.

### Kann ich in der Handy-App mehrere HA-Instanzen nutzen (Zuhause, Wohnwagen, Firma)?

Ja. Die Android-App kann seit 2023 mehrere Server verwalten ([Blog Android 2023.3](https://www.home-assistant.io/blog/2023/03/30/android-20233/)), die iOS-App schon länger. Einen weiteren Server fügt man unter Einstellungen → Companion App hinzu.

## 3. Fernzugriff

### Wie komme ich von unterwegs auf mein HA?

| Weg | Aufwand | Kosten | Hinweis |
| --- | --- | --- | --- |
| Home Assistant Cloud / Link (Nabu Casa) | Sehr gering | Abo | Finanziert die HA-Entwicklung; enthält auch Alexa/Google-Anbindung |
| VPN über den Router (z. B. WireGuard in der FRITZ!Box) | Mittel | Keine | VPN muss auf dem Handy aktiv sein |
| Tailscale o. Ä. | Gering bis mittel | Kostenlose Stufe vorhanden | Funktioniert auch ohne öffentliche IPv4 |
| Portfreigabe + Reverse Proxy | Hoch | Keine | Nur mit Erfahrung in Netzwerksicherheit |

### Heißt es jetzt „Nabu Casa“, „Home Assistant Cloud“ oder „Home Assistant Link“?

Nabu Casa ist die Firma. Ihr Abo hieß bisher Home Assistant Cloud und wird in **Home Assistant Link** umbenannt, am Dienst ändert sich nichts ([HA-Blog](https://home-assistant.io/blog/2026/10/02/big-tech-ruined-the-cloud-so-were-renaming-ours/)). Die Umbenennung soll mit Version 2026.12 im Dezember umgesetzt werden ([housecontrollers.de](https://www.housecontrollers.de/?p=228685)). Wichtig für Einsteiger: HA selbst läuft immer lokal, das Abo ist optional.

### Fernzugriff funktioniert nicht. Woran liegt das?

*Einschätzung, häufigste Ursachen:*

- Der Anschluss hat keine eigene öffentliche IPv4 (DS-Lite, oft bei Kabel- und Glasfaseranschlüssen). Dann funktioniert eine Portfreigabe nicht. Abhilfe: Cloud/Link oder Tailscale.
- In HA ist unter Einstellungen → System → Netzwerk keine externe URL eingetragen.
- Die Handy-App nutzt noch die alte Adresse mit „:8123“ (siehe Abschnitt 2).

### Ich vergesse ständig, den WireGuard-Tunnel einzuschalten. Lösung ohne Abo?

*Einschätzung:* Android bietet in den Systemeinstellungen ein „dauerhaftes VPN“ (Always-on). Das hält den Tunnel aber auch zu Hause offen. Alternativ macht Tailscale das automatisch. Wer es ganz bequem haben will, landet bei Cloud/Link.

## 4. Geräte einbinden

### Ich will weg von Alexa. Was brauche ich für Steckdosen, Lampen und Shellys?

Shelly und viele WLAN-Geräte bindet HA direkt über das Netzwerk ein, ganz ohne zusätzliche Hardware. Hinzu kommt je nach Funkstandard:

| Geräte funken mit … | Man braucht | Hinweis |
| --- | --- | --- |
| WLAN (Shelly, Tasmota, ESPHome) | nichts | lokal, ohne Cloud |
| Zigbee (IKEA, innr, Aqara, Sonoff) | Zigbee-Stick oder Netzwerk-Koordinator | Software: ZHA (eingebaut) oder Zigbee2MQTT (App) |
| Matter über Thread | Thread-Funkstick bzw. Border Router | Matter-Server-App in HA |
| Matter über WLAN | nichts außer der Matter-Server-App | Einrichtung per Handy-App |
| Herstellersystem (Hue, Homematic IP) | die Bridge/Zentrale des Herstellers | HA spricht mit der Bridge |

Alexa kann man parallel weiterverwenden. Sprachsteuerung ist in Abschnitt 8 beschrieben.

### Eine Zigbee-Lampe funktioniert nur in einer bestimmten Fassung. Warum?

*Einschätzung:* Fast immer ein Reichweitenproblem. Zigbee ist ein Mesh-Netz, Geräte mit Dauerstrom (Lampen, Steckdosen) leiten Signale weiter. Stehen zwischen Stick und Lampe zu wenige solcher Router, bricht die Verbindung ab. Abhilfe: eine Zigbee-Steckdose dazwischen, den Stick mit USB-Verlängerung weg vom Rechner, oder ein Netzwerk-Koordinator an zentraler Stelle.

### Kann ich den Zigbee-Koordinator wechseln, ohne alle Geräte neu anzulernen?

Meist ja, solange der Chip-Typ gleich bleibt (Z-Stack zu Z-Stack oder Ember zu Ember). Zwischen den Familien ist eine Migration nur mit mehr Aufwand möglich ([SMLIGHT-Anleitung](https://smlight.tech/de/youtube/49f4b31a-5725-4581-bd8f-edce2891a517)). Laut Nutzerberichten kommen die meisten Geräte danach von selbst zurück, einzelne müssen neu angelernt werden ([Zigbee2MQTT-Diskussion](https://github.com/Koenkk/zigbee2mqtt/discussions/26716)). Vorher unbedingt ein Backup machen.

### Nach einer Neuinstallation von HA lassen sich meine Matter-Geräte nicht mehr hinzufügen.

Das Gerät ist noch im alten Matter-Netz („Fabric“) gespeichert, und sein ursprünglicher QR-Code gilt nicht mehr. Lösungen: das Gerät auf Werkseinstellungen zurücksetzen, oder es aus einem anderen System (Apple, Google, Hersteller-App) mit einem neuen Kopplungscode an HA teilen ([HA-Community](https://community.home-assistant.io/t/cant-re-add-deleted-device-trying-to-add-a-noc-for-a-fabric-that-already-exists/889114)). Grundlagen: [Matter-Integration](https://www.home-assistant.io/integrations/matter/).

### Matter-Geräte fallen immer wieder aus, alles andere läuft stabil.

*Einschätzung:* Häufige Ursache sind mehrere Thread-Netze nebeneinander, z. B. eines von Apple-HomePods und eines von HA. Die Geräte sollten in einem gemeinsamen Thread-Netz hängen. **Ich bin mir nicht sicher**, ob das im Einzelfall die Ursache ist. Matter/Thread ist zurzeit die häufigste Quelle schwer zu erklärender Probleme.

### Homematic IP: Reicht der Access Point, oder brauche ich die neue HCU?

Beides geht, es gibt drei Wege ([Doku Homematic(IP) Local](https://sukramj.github.io/aiohomematic/user/homeassistant_integration)):

| Zentrale | Integration in HA | Verbindung |
| --- | --- | --- |
| Access Point (HAP) | Homematic IP Cloud (eingebaut) | über die Herstellercloud |
| CCU3 / OpenCCU | Homematic(IP) Local for OpenCCU (Marketplace) | lokal |
| Home Control Unit (HCU) | Homematic IP Local (HCU) (Marketplace, ggf. über „Über Link hinzufügen“) | lokal |

Matter wird für die Einbindung nicht gebraucht.

## 5. Energie, PV und Speicher

PV ist in den Gruppen das häufigste einzelne Thema. Die Fragen drehen sich fast immer um drei Dinge: Gerät einbinden, Daten auswerten, Überschuss nutzen.

### Wie bekomme ich Wechselrichter, Speicher oder Smart Meter in HA?

Zuerst unter Einstellungen → Geräte & Dienste → „Integration hinzufügen“ nach dem Hersteller suchen, danach im Marketplace. Für viele gängige Marken gibt es eine fertige Integration. Ob ein bestimmtes Modell lokal oder nur über die Herstellercloud angebunden wird, steht auf der jeweiligen Integrationsseite.

*Tipp aus den Gruppen:* Vor dem Fragen den genauen Modellnamen und die Firmware nennen. „Hat jemand X eingebunden?“ bekommt sonst kaum brauchbare Antworten.

### Fehlermeldung: „Der Wechselrichter unterstützt nur eine Modbus-Verbindung“

Viele Wechselrichter erlauben nur eine oder wenige gleichzeitige Modbus-Verbindungen. Läuft schon ein anderes Programm (Hersteller-App im lokalen Modus, evcc, eine zweite Integration), wird HA abgewiesen. Seit 2026.9 können Integrationen eine Modbus-Verbindung teilen. Laut Release-Notes betrifft das bisher aber nur einzelne Integrationen wie Fronius ([Release-Notes 2026.9](https://home-assistant.io/blog/2026/09/02/release-20269)). **Ich bin mir nicht sicher**, ob das für Huawei oder SMA schon hilft.

### Wie kann ich diesen Winter mit dem letzten vergleichen?

Dafür gibt es das **Energie-Dashboard** unter Einstellungen → Dashboards → Energie. Es zeigt Netzbezug, PV, Speicher und einzelne Verbraucher. Hat man nur einen Leistungssensor (W) und keinen Energiezähler (kWh), rechnet die Integration „Riemann-Summe“ die Energie aus ([Doku Energie](https://www.home-assistant.io/docs/energy/)).

Der normale Verlauf wird standardmäßig nach 10 Tagen gelöscht ([Doku Recorder](https://www.home-assistant.io/integrations/recorder/)). Für Jahresvergleiche nutzt HA die Langzeitstatistik, die stündliche Werte speichert. *Nach meinem Kenntnisstand* wird sie nicht automatisch gelöscht. Das habe ich in der aktuellen Doku nicht ausdrücklich gefunden.

### Wie lade ich mein Auto mit PV-Überschuss?

Die verbreitetste Lösung ist **evcc**, entweder separat oder als App in HA. evcc übernimmt die Ladelogik, HA die übrige Hausautomation ([v2charge.com](https://v2charge.com/de/wallbox-smart-home-integration/)). Bei manchen Wallboxen geht es auch ohne evcc über die Wallbox-Integration in HA, etwa beim go-e Charger ([ha-evcc](https://github.com/marq24/ha-evcc)).

### Kann ich die Klimaanlage nach PV-Überschuss steuern?

Wenn die Klimaanlage in HA eingebunden ist, ja, über eine Automation: Überschuss über X Watt für Y Minuten → einschalten. Ob sich die Leistung stufenlos an den Überschuss anpassen lässt, hängt davon ab, was die Integration des Herstellers anbietet.

## 6. Dashboards und Wandtablets

### Welches Tablet oder Display für die Wand?

Das ist die mit Abstand häufigste Frage. Eine allgemeingültige Empfehlung gibt es nicht, aber eine Entscheidungshilfe (*Einschätzung*):

| Variante | Vorteil | Nachteil |
| --- | --- | --- |
| Günstiges Android-Tablet (z. B. Amazon Fire) + Fully Kiosk Browser | billig, viel Software-Unterstützung | Akku bläht sich im Dauerbetrieb mit der Zeit auf |
| Wandpanel für die Unterputzdose (z. B. Shelly Wall Display) | sauber eingebaut, 230 V direkt | kleinerer Bildschirm, teurer |
| Touch-Monitor 15–27 Zoll + Mini-PC oder Raspberry Pi | groß | zwei Geräte, mehr Stromverbrauch |
| Kleines ESP32-Display | sehr billig, sparsam | nur einfache Anzeigen |

Für Tablets im Dauerbetrieb lohnt sich eine schaltbare Steckdose. Eine Automation lädt den Akku dann nur zwischen etwa 20 und 80 %.

### Kann ich ein altes iPad (iPad 2, iPad Air 1) nutzen?

**Ich bin mir nicht sicher.** Diese Geräte bekommen keine aktuellen iOS-Versionen mehr, und die HA-Oberfläche braucht einen aktuellen Browser. Bei sehr alten iPads ist damit zu rechnen, dass das Dashboard gar nicht oder nur teilweise lädt. Ausprobieren kostet nichts: Safari öffnen, HA-Adresse eingeben.

### Wie schaltet das Tablet bei Bewegung ein, und wie wechsle ich per Automation die Ansicht?

Mit **Fully Kiosk Browser** auf Android. Die Fully-Kiosk-Integration kann den Bildschirm und die Bewegungserkennung schalten und mit der Aktion `fully_kiosk.load_url` eine andere Seite laden, z. B. eine andere Dashboard-Ansicht. Dafür braucht man die kostenpflichtige Fully-Plus-Lizenz ([Doku Fully Kiosk](https://www.home-assistant.io/integrations/fully_kiosk/)).

### Wie bekommen andere so schöne Dashboards hin?

Meist mit Community-Karten aus dem Marketplace (z. B. Mushroom, Bubble Card, Power-Flow-Karten), und inzwischen oft mit KI-Hilfe (siehe Abschnitt 8). Ein guter Start ist das eingebaute Dashboard. Dann eine Karte nach der anderen anpassen, statt ein fremdes Design komplett nachzubauen.

## 7. Automationen

### Licht per Bewegungsmelder, aber nur wenn es dunkel ist

Der Bewegungsmelder ist der **Auslöser**, die Helligkeit die **Bedingung**. Ein häufiger Fehler ist, die Helligkeit als zweiten Auslöser einzutragen. Beispiel (Entitätsnamen anpassen):

```yaml
id: aussenlicht_bewegung_dunkel
alias: Außenlicht bei Bewegung im Dunkeln
description: Schaltet das Außenlicht bei Bewegung ein, wenn es dunkler als 20 lx ist, und nach 3 Minuten ohne Bewegung wieder aus.
mode: restart
triggers:
  - trigger: state
    entity_id: binary_sensor.bewegung_eingang
    to: "on"
conditions:
  - condition: numeric_state
    entity_id: sensor.helligkeit_eingang
    below: 20
actions:
  - action: light.turn_on
    target:
      entity_id: light.aussenlicht
  - wait_for_trigger:
      - trigger: state
        entity_id: binary_sensor.bewegung_eingang
        to: "off"
        for: "00:03:00"
  - action: light.turn_off
    target:
      entity_id: light.aussenlicht
```

`mode: restart` sorgt dafür, dass neue Bewegung die Wartezeit neu startet.

### Meine Abwesenheits-Automation löst nicht aus

*Einschätzung, die häufigsten Ursachen:*

- Die Handys sind nicht der jeweiligen **Person** zugeordnet (Einstellungen → Personen → „Geräte verfolgen“).
- Die Companion-App darf den Standort nicht „immer“ abrufen, oder der Energiesparmodus des Handys blockiert sie.
- Ohne Fernzugriff kann das Handy unterwegs keine Position melden (siehe Abschnitt 3).

Am einfachsten ist ein Auslöser auf `zone.home`. Ihr Wert ist die Anzahl der Personen zu Hause, also Auslöser „Zustand wird 0“.

### Wie finde ich heraus, warum eine Automation nicht läuft?

In der Automation oben rechts → **Traces**. Dort sieht man jeden Lauf Schritt für Schritt und an welcher Bedingung er abgebrochen ist. Wurde die Automation gar nicht ausgelöst, stimmt meist der Auslöser nicht.

## 8. KI und Sprachsteuerung

### Kann Claude oder ChatGPT mein HA einrichten?

Teilweise. KI-Assistenten schreiben inzwischen brauchbare Automationen, Dashboard-Karten und Templates. Viele in den Gruppen gezeigte Dashboards sind so entstanden. *Einschätzung:* Geräte einbinden, Netzwerk und Funk muss man trotzdem selbst verstehen. Und man sollte nachvollziehen können, was die KI gebaut hat, bevor man ihr Schreibzugriff gibt.

### Wie verbinde ich Claude mit HA (MCP-Server)?

HA bringt die Integration **Model Context Protocol Server** mit. Damit kann ein KI-Assistent Geräte steuern und den Zustand des Hauses sehen ([Doku MCP Server](https://home-assistant.io/integrations/mcp_server/)). Ablauf in Kurzform:

1. In HA unter Einstellungen → Geräte & Dienste die Integration „Model Context Protocol Server“ hinzufügen.
2. Unter Einstellungen → System → KI die MCP-Adresse kopieren.
3. In Claude unter Einstellungen → Konnektoren einen eigenen Konnektor mit dieser Adresse anlegen.

Der häufigste Stolperstein: Claude verbindet sich **von Anthropics Servern aus**, nicht vom eigenen PC. HA muss also aus dem Internet erreichbar sein, ein VPN reicht nicht. Außerdem akzeptiert Claude keine Adresse mit Portnummer wie `:8123` ([Claude-Hilfe](https://support.claude.com/en/articles/11175166)). Eine ausführliche deutsche Anleitung gibt es bei [SSD Nodes](https://www.ssdnodes.com/learn/lang/de/connect-claude-to-home-assistant-with-mcp).

### Brauche ich dafür ein Claude-Abo?

Nein. Eigene Konnektoren gibt es auch im kostenlosen Tarif, dort ist es aber genau einer ([Claude-Hilfe](https://support.claude.com/en/articles/11175166)). Wer nach drei Tagen zur Kasse gebeten wird, hat vermutlich eine Testphase eines Bezahltarifs gestartet statt den Free-Tarif. **Ich bin mir nicht sicher**, was im Einzelfall angezeigt wurde.

### Welchen Sprachassistenten nehmen? Alexa versteht so wenig.

*Einschätzung:* HA hat mit **Assist** einen eigenen Sprachassistenten. Als „Gehirn“ kann man ein Sprachmodell wie ChatGPT, Claude oder ein lokales Modell einbinden. Als Mikrofon dienen die Handy-App oder eigene Sprach-Hardware. Alexa und Google lassen sich weiter nutzen, am bequemsten über Cloud/Link.

## 9. Backup und Sicherheit

### Was muss ich beim Backup unbedingt beachten?

HA-Backups sind verschlüsselt. Ohne den Schlüssel aus dem **Notfall-Kit** („Backup emergency kit“) lässt sich ein Backup nicht wiederherstellen ([Doku Notfall-Kit](https://home-assistant.io/more-info/backup-emergency-kit)). Das Kit lädt man unter Einstellungen → System → Backups herunter und bewahrt es **außerhalb** von HA auf, z. B. im Passwortmanager ([Doku Backups](https://www.home-assistant.io/common-tasks/general/backups/)). Nabu Casa speichert den Schlüssel ebenfalls nicht und kann bei Verlust nicht helfen ([Nabu-Casa-Support](https://support.nabucasa.com/hc/en-us/articles/26323093151901)).

In der Gruppe gab es den typischen Fall: Umzug auf Proxmox, Schlüssel vergessen, HA komplett neu aufsetzen.

### Wohin sollen die Backups?

Nicht nur auf das HA-Gerät selbst. Unter Einstellungen → System → Backups lässt sich ein zweiter Speicherort einrichten, etwa ein NAS oder Cloud/Link.

### Darf ich einer KI vollen Zugriff auf HA geben?

*Einschätzung:* Nur mit Bedacht. Der MCP-Server läuft standardmäßig mit einem Administratorkonto ([Doku MCP Server](https://home-assistant.io/integrations/mcp_server/)). Wer ausprobiert, sollte vorher ein Backup machen, nur die nötigen Entitäten freigeben und Änderungen der KI prüfen, bevor sie live gehen.

## Quellen

Geprüft am 19. November 2026. Release-Notes und Doku: [2026.2](https://www.home-assistant.io/blog/2026/02/04/release-20262/) · [2026.8](https://home-assistant.io/blog/2026/08/05/release-20268) · [2026.9](https://home-assistant.io/blog/2026/09/02/release-20269) · [2026.11](https://www.home-assistant.io/blog/2026/11/04/release-202611/) · [Installation](https://www.home-assistant.io/installation/) · [Cloud wird Link](https://home-assistant.io/blog/2026/10/02/big-tech-ruined-the-cloud-so-were-renaming-ours/) · [Matter](https://www.home-assistant.io/integrations/matter/) · [Fully Kiosk](https://www.home-assistant.io/integrations/fully_kiosk/) · [Energie](https://www.home-assistant.io/docs/energy/) · [Recorder](https://www.home-assistant.io/integrations/recorder/) · [MCP Server](https://home-assistant.io/integrations/mcp_server/) · [Claude-Konnektoren](https://support.claude.com/en/articles/11175166). Weitere Quellen stehen direkt bei der jeweiligen Antwort.

Antworten mit „Einschätzung“ sind Erfahrungswerte und nicht durch eine Quelle belegt.

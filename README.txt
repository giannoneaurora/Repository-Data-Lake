# README per Redis Chat App

# DESCRIZIONE

Questa è una applicazione pc per poter chattare usando un server di Redis. L'app usa le funzionalità di
GUI della libraria tkinter per rendere la user experience migliore, inoltre usa il pubsub di Redis 
per la condivisione dei messaggi. 

# FUNZIONI

L'app consente all'utente di registrarsi con un username e una password. Lo username è univoco. 
Una volta fatta la registrazione, l'utente può effettuare il login con le sue credenziali e può accedere
alla chat. Nella pagina di chat, l'utente ha a disposizione alcune funzionalità:
- ricercare e aggiungere altri utenti alla propria lista contatti per poter chattare: la ricerca funziona per
  nome parziale, ovvero quando un utente scrive un username, deve sempre confermare l'inserimento dello username
  per poterlo aggiungere alla propria lista contatti. 
- attivazione della modalità Do Not Disturb: l'utente ha la possibilità cliccando un tasto di attivare/disattivare
  la possibilità di ricevere messaggi. Quando il DND è ON, l'utente non riceve alcun messaggio. Se un utente tenta
  di inviare un messaggio ad un altro con la modalità DND attiva, riceve una notifica che l'utente non può 
  ricevere messaggi al momento.
- funzionalità di chat: l'utente può scegliere di chattare con un altro utente tramite due features, una cella
  per poter inserire e inviare il proprio messaggio. L'utente deve scegliere, tramite un menu a tendina, a chi
  inviare il messaggio, dopodiché questo viene mostrato nel display. L'ordine dei messaggi è invertito, i messaggi
  più recenti sono più in alto nel display. 
  La formattazione dei messaggi è:
	> <scrittore_messaggio> <messaggio> [<data_invio> <orario_invio>]
  es. > Paolo 'Hello World!' [2024-07-01 16:00:00]
- ricevimento di notifiche push: quando un utente riceve un messaggio, a schermo compare una notifica all'utente
  che ha ricevuto il messaggio
- creazione di chat temporanea: l'utente può creare una chat a tempo con un suo contatto, la chat ha un timer di
  60 secondi dalla creazione. il timer viene aggiornato ogni volta che un utente invia un messaggio.

# APPLICAZIONI USATE

- Redis Server
- Python:
	- libreria time
	- libreria bcrypt
	- libreria tkinter
	- libreria redis

N.B. Le librerie da installare sono inserite nel file requirements.txt

# INSTALLAZIONE

Per poter usare l'applicazione è necessario disporre di Python 3.

Per installare l'app è necessario scaricare la repo di GitHub al link
https://github.com/giannoneaurora/Repository-Data-Lake.git

Bisogna aprire la cartella 'Repository Data Lake' e aprire con un qualunque IDE il file GUI.py
Dopo essersi assicurati dell'installazione delle librerie necessarie, è sufficiente far partire il codice
di GUI.py per poter far partire la chat. 

N.B. Una connessione ad internet è necessaria per poter usare la chat, dato che l'utente deve poter accedere al
server Redis. Risulta possibile far partire la chat in locale apportando delle modifiche al codice.

# COME USARE L'APPLICAZIONE

Dopo aver fatto partire il file GUI.py, comparirà la finestra di login. L'utente può accedere all'applicazione dispone già di un account, oppure può creare un nuovo account cliccando sul tasto Create New Account. 
In questo caso l'utente la UI cambierà e darà la possibilità di creare il proprio account all'utente. Una volta creato l'account, l'utente viene rimandato alla pagina di login, se l'account è stato creato. 
Dopo aver fatto il login, l'utente si trova nella pagina principale dell'applicazione, ovvero la chat.
La chat presenta tutte le funzionalità disponibili: in centro è presente il display della chat che di default è vuoto e sotto sono presenti tutti i tasti per le funzionalità e un menu a tendina e uno spazio per poter scrivere i messaggi. Nella barra è sempre visibile il DND status dell'utente.
Il tasto Send permette di inviare il messaggio nella chat, tuttavia l'utente deve prima selezionare l'utente a cui inviare il messaggio tramite il menu a tendina. Una volta selezionato col menu a tendina, il display mostra tutti vecchi messaggi e permette all'utente di inviarne di nuovi.
Il tasto Do Not Disturb permette di cambiare la modalità DND. 
Il tasto Add Contact permette di aggiungere un utente tramite ricerca parziale del nome: l'utente inserisce dei caratteri, poi vengono mostrati tutti gli utenti che hanno quei caratteri nel nome. Viene poi richiesto di confermare il contatto da aggiungere reinserendo lo username corretto. 
Il tasto View Contact mostra la propria lista contatti.
Il tasto Create Temp Chat crea una chat a tempo con utente della propria lista contatti: la chat ha un timer di 60 secondi che viene riaggiornato ogni volta che viene mandato un messaggio da uno degli utenti. 

# NOTE

--- disclaimer 
L'app è stata creata come progetto scolastico per l'ITS Angelo Rizzoli di Milano, corso Big Data Specialist classe 2023-25. L'app è stata creata col contributo degli studenti Amato Giacomo, Durante Pierluigi, Giannone Aurora e Goldin Roberto. 


--- svolgimento del progetto
Le funzioni sono state prima create in maniera approssimativa per poter testare le funzioni di redis e il collegamento con il server. Il file codice_di_prova.py è quindi la bozza iniziale con le funzioni. 
Dopodiché abbiamo preso ogni funzione e abbiamo diviso per funzionalità creando diversi file .py. Ogni funzione è stata testata e funziona, sebbene non siano state tutte implementate nella funzione main del programma. 
Una volta creata la UI usando la libreria tkinter, abbiamo deciso di non continuare a programma il main.py e abbiamo riadattato e inserito tutte le funzioni in GUI.py. Le funzionalità di GUI sono quelle più aggiornate e presentano varie modifiche e bug fixes, inoltre sono state aggiunte alcune funzioni per la gestione della GUI. 
Il file program_test.py è stato utilizzato per poter testare le funzionalità dell'app con l'inserimento di utenti di prova. 


--- funzionalità non implementate
Nel file password_hashing.py sono presenti le funzioni per l'hashing della password per poter salvare le password nel server in sicurezza. Con l'implementazione della GUI, abbiamo deciso di non implementare la funzione di hashing dato che presentava errori. La funzione check_password_limitations, che permette di rendere la password più sicura, è stata solo abbozzata e non è stata implementata nel progetto. 
La funzione per poter vedere tutti gli utenti sul server è presente nel main.py, ma non è stata data la possibilità all'utente di usarla. Stessa cosa per la funzione che mostra tutti i contatti, la funzione che mostra tutte le informazioni di un utente e altri funzioni del main. Abbiamo deciso di implementarle, ma solo come funzionalità di controllo e test del sistema.
L'app non ha funzioni per poter cambiare linguaggio e tutti i messaggi di sistema sono in lingua inglese. 


--- modificare il server di connessione
Di default, l'utente si collega al server creato da noi. Risulta possibile cambiare tale server andando a modificarlo cambiando il codice del file client_server_connection.py. 
Il file presenta una classe Client e una funzione get_client che viene richiamato negli altri file .py.
Cambiare il server richiede di cambiare:
	HOST_NAME 
	PORT_NUMBER
	PASSWORD
	DB_NUMBER (se necessario)
Sostituendo tali valori coi propri dati è possibile cambiare il server di connessione.


--- bug conosciuti
- L'app non mostra errori nel caso non possa accedere al server di Redis
- L'app potrebbe risultare lenta nella connessione al server
- La funzionalità di chat temporanea mostra a display la chat all'utente che ha creato la chat, ma mostra i messaggi nella chat normale all'altro utente. 
- Se l'app viene spenta mentre una chat temporanea è stata attivata, quando l'utente rientra ritrova la chat temporanea tra i propri contatti.















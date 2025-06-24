# E-commerce di Gioielli (full web site)
![Logo FREYA JEWELS](static/images/logo.png)

## Descrizione

Questo progetto è un sito e-commerce per la vendita di gioielli, sviluppato con Django e Bootstrap.  
Il progetto include tutte le funzionalità fondamentali di un negozio online, con un'interfaccia utente intuitiva e un pannello di gestione per gli amministratori: 
permette agli utenti di navigare tra i prodotti, aggiungerli al carrello o alla wishlist, completare ordini e visualizzare lo storico degli ordini effettuati. 
Gli store manager hanno accesso a un pannello di controllo dedicato per gestire i prodotti e monitorare gli ordini in sospeso.

## Tecnologie utilizzate
- **Backend**: Django 5.0
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Database**: SQLite (sviluppo), PostgreSQL (produzione)
- **Autenticazione**: Custom User Model con estensione per gestori
- **Hosting**: Railway

## Live Deployment
Il progetto è attualmente deployato su **Railway** ed è accessibile all'indirizzo:  
👉 [https://web-production-f7e6.up.railway.app/](https://web-production-f7e6.up.railway.app/)

Il deployment include un mini-dataset dimostrativo con: 
1 solo prodotto e una sola categoria e il superuser (stesso username e password di quello nel database locale)

*Per il dataset completo, vedere il database locale pre-popolato ('db.sqlite3').*


## 📝 Requisiti soddisfatti
- 2 diverse app Django (shop e users)
- 2 relazioni tra modelli (es. Product-Category, Order-OrderItem)
- Viste class-based generiche (ProductListView, ProductDetailView)
- 2 gruppi di utenti con permessi diversi (utenti normali e store manager)
- Estensione della classe User (CustomUser con campi aggiuntivi)
- Database locale (db.sqlite3)
- Deployment su Railway


## Funzionalità principali
### Per tutti gli utenti
-  Registrazione e profilo personalizzato con foto
-  Catalogo prodotti con filtri avanzati (categoria, prezzo, materiali)
-  Carrello della spesa con gestione quantità
-  Checkout con diversi metodi di pagamento
-  Storico ordini
-  Wishlist personale
-  Ricerca prodotti

### Solo per i gestori
-  Pannello di controllo dedicato
-  Gestione completa prodotti (CRUD)
-  Gestione ordini
-  Statistiche di vendita
-  Creazione automatica di materiali e taglie standard



## 👥 Account di test
### Admin/Store manager:

username: carmen
Password: passworddelcreatore

### Utente normale:

Email: utente2
Password: #L#7sQR#QT3Jyc!








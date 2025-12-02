# 🚀 Relancement du Projet Kafka Mini Uber

Guide rapide pour relancer le projet après l'installation initiale.

> 💡 **Note** : Ce guide suppose que vous avez déjà effectué l'installation complète.  
> Si ce n'est pas le cas, consultez d'abord [INSTALL.md](INSTALL.md).

---

## ⚡ Commandes de relancement

### 1️⃣ Démarrer Zookeeper

Ouvrez un **terminal PowerShell** :

```powershell
cd C:\kafka
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```

Laissez ce terminal ouvert.

---

### 2️⃣ Démarrer le broker Kafka

Ouvrez un **nouveau terminal PowerShell** :

```powershell
cd C:\kafka
.\bin\windows\kafka-server-start.bat .\config\server.properties
```

> **Note** : Si vous utilisez Kafka en mode KRaft (sans Zookeeper), démarrez uniquement le broker KRaft :
> ```powershell
> cd C:\kafka
> .\bin\windows\kafka-server-start.bat .\config\kraft\server.properties
> ```

Laissez ce terminal ouvert.

---

### 3️⃣ Lancer le Producer

Ouvrez un **nouveau terminal PowerShell** :

```powershell
cd C:\Users\Quent\OneDrive\Bureau\kafka-uber
venv\Scripts\Activate.ps1
python producer/producer.py
```

Le producer commence à envoyer les positions GPS du taxi toutes les secondes.

---

### 4️⃣ Lancer le Consumer Streamlit

Ouvrez un **nouveau terminal PowerShell** :

```powershell
cd C:\Users\Quent\OneDrive\Bureau\kafka-uber
venv\Scripts\Activate.ps1
streamlit run consumer/streamlit_consumer.py
```

Votre navigateur s'ouvrira automatiquement sur l'application Streamlit.

---

## ✅ Vérification

Vous devriez avoir **4 terminaux ouverts** :

1. ✅ Zookeeper (si mode classique)
2. ✅ Broker Kafka
3. ✅ Producer (envoie des positions)
4. ✅ Consumer Streamlit (affiche la carte)

---

## 🛑 Arrêt

Pour arrêter proprement :

1. **Producer** : `Ctrl+C` dans son terminal
2. **Streamlit** : `Ctrl+C` dans son terminal
3. **Kafka** : `Ctrl+C` dans le terminal du broker
4. **Zookeeper** : `Ctrl+C` dans son terminal (si utilisé)

---

## 📝 Notes

- **Chemin du projet** : Adaptez `C:\Users\Quent\OneDrive\Bureau\kafka-uber` à votre propre chemin si nécessaire.
- **Chemin Kafka** : Adaptez `C:\kafka` à votre propre chemin d'installation de Kafka si nécessaire.



Absolument. Voici un compte rendu structuré que vous pouvez présenter directement à vos développeurs. Il est rédigé pour être clair, technique et actionnable.

---

### **Plan d'Action : Remplacement de l'API OpenAI par l'API Perplexity**

**Date :** 29 août 2025

**Projet :** Graphiti pour Agents IA

#### **1. Objectif**

Migrer la dépendance de notre service Graphiti de l'API OpenAI vers l'API Perplexity pour l'extraction d'entités et de relations à partir des messages.

#### **2. Contexte Technique et Faisabilité**

L'API de Perplexity est annoncée comme étant **"compatible OpenAI"**. Ce standard de compatibilité implique que Perplexity a répliqué la structure des endpoints, les formats de requêtes (JSON) et les formats de réponses de l'API OpenAI.

Grâce à cette compatibilité, notre application Graphiti, qui utilise la bibliothèque cliente standard d'OpenAI, peut être redirigée vers Perplexity par une simple modification de configuration, sans nécessiter de changement dans le code source. L'application continuera de "penser" qu'elle communique avec OpenAI, alors que les appels seront traités par Perplexity.

#### **3. Prérequis**

*   Accès administrateur à l'interface de déploiement Coolify.
*   Une clé API valide pour le service Perplexity.
*   Le nom du modèle Perplexity à utiliser (par ex. `llama-3-sonar-large-32k-online`).

#### **4. Procédure de Mise en Œuvre**

La modification s'effectue entièrement via la configuration des variables d'environnement du service **Graphiti** dans Coolify.

**Action :** Naviguer vers `Projets > Graphit > Configuration > Environment Variables`.

1.  **Modification de la Clé API :**
    *   **Variable :** `OPENAI_API_KEY`
    *   **Action :** Remplacer la valeur actuelle par la **clé API fournie par Perplexity**.

2.  **Redirection de l'URL de Base de l'API (Étape la plus critique) :**
    *   **Variable :** `OPENAI_API_BASE`
    *   **Action :** Ajouter (ou modifier si elle existe) cette variable pour qu'elle pointe vers l'endpoint de Perplexity.
    *   **Valeur :** `https://api.perplexity.ai`

3.  **(Optionnel mais recommandé) Spécification du Modèle :**
    *   **Variable :** `OPENAI_MODEL_NAME` (ou un nom similaire, à vérifier dans la configuration existante).
    *   **Action :** Si une variable définit le modèle à utiliser (par ex. `gpt-4-turbo`), la modifier pour utiliser un modèle Perplexity compatible.
    *   **Valeur d'exemple :** `llama-3-sonar-large-32k-online`

4.  **Déploiement :**
    *   **Action :** Sauvegarder les modifications des variables d'environnement, puis redéployer le service Graphiti.

#### **5. Plan de Validation et de Test**

1.  **Vérification du Démarrage :**
    *   **Action :** Consulter les logs du service Graphiti après le redéploiement.
    *   **Résultat Attendu :** Le service doit démarrer sans erreur d'authentification ou de connexion. L'absence d'erreur validera que la nouvelle configuration est acceptée.

2.  **Test Fonctionnel End-to-End :**
    *   **Action :** Reproduire le test de création de relation effectué précédemment.
        *   a. S'assurer que les nœuds "Alice" et "Bob" existent.
        *   b. Exécuter un appel `POST /messages` avec le contenu `"Alice knows Bob."`.
    *   **Résultat Attendu :** L'appel API doit retourner un code de succès (`202`).

3.  **Validation dans la Base de Données :**
    *   **Action :** Se connecter au Neo4j Browser et exécuter la requête Cypher : `MATCH (n)-[r]->(m) WHERE n.name = 'Alice' AND m.name = 'Bob' RETURN n, r, m`.
    *   **Résultat Attendu :** Le graphe doit afficher une relation (par ex. `RELATES_TO`) entre les nœuds "Alice" et "Bob", prouvant que l'extraction par Perplexity a fonctionné.

#### **6. En Cas d'Échec (Plan de Contingence)**

*   **Scénario 1 : Le service ne démarre pas.**
    *   **Cause probable :** Erreur dans la clé API ou l'URL de base.
    *   **Action :** Vérifier minutieusement les valeurs des variables d'environnement.

*   **Scénario 2 : Le service démarre mais l'extraction échoue.**
    *   **Cause probable :** L'URL de base de l'API est codée "en dur" dans le code source de Graphiti.
    *   **Action :** Une intervention sur le code sera nécessaire pour externaliser l'URL de base dans une variable d'environnement, afin de la rendre configurable.

---
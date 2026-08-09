![Freddy — Bot journalier sur X](assets/freddy-banner.png)

# Freddy

Freddy est un bot Python simple qui publie automatiquement un message daté sur X. Il peut être testé localement sans publier, puis exécuté chaque jour avec GitHub Actions, même lorsque l'ordinateur de son propriétaire est éteint.

Le projet utilise :

- Python ;
- [Tweepy](https://www.tweepy.org/) pour communiquer avec l'API X ;
- `python-dotenv` pour charger les variables locales ;
- GitHub Actions pour la publication automatique.

## Fonctionnement

À chaque exécution, le programme :

1. récupère la date actuelle ;
2. traduit le mois en français ;
3. construit le message ;
4. vérifie qu'il ne dépasse pas 280 caractères ;
5. affiche le message en mode simulation ou le publie sur X en mode réel.

Le workflow fourni est programmé chaque jour à **04 h 20**, dans le fuseau `Europe/Brussels`.

## Prérequis

- Python 3.13 recommandé ;
- Git ;
- un compte X ;
- un accès à la [Developer Console de X](https://console.x.com/) ;
- une application X autorisée à lire et publier des messages ;
- un compte GitHub pour utiliser l'automatisation.

L'accès à l'API X et la publication peuvent dépendre de l'offre et des crédits disponibles sur le compte développeur.

## 1. Récupérer le projet

Cloner directement le dépôt :

```bash
git clone https://github.com/p3sko/Freddy_v1.0.1.git
cd Freddy_v1.0.1
```

Pour créer sa propre version sur GitHub, il est préférable de cliquer sur **Fork** depuis la page du dépôt, puis de cloner ce fork.

## 2. Créer un environnement Python

Créer l'environnement virtuel :

```bash
python -m venv .venv
```

Sous Windows PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

Sous macOS ou Linux :

```bash
source .venv/bin/activate
```

Installer les dépendances :

```bash
python -m pip install -r requirements.txt
```

## 3. Configurer l'application X

Dans la [Developer Console de X](https://console.x.com/) :

1. créer une application ;
2. activer l'authentification utilisateur OAuth 1.0a ;
3. accorder à l'application les droits de lecture et d'écriture ;
4. générer l'API Key et son Secret ;
5. générer l'Access Token et son Secret après avoir configuré les permissions.

Le bot utilise quatre informations :

| Variable | Identifiant X correspondant |
| --- | --- |
| `X_API_KEY` | API Key, aussi appelée Consumer Key |
| `X_API_SECRET` | API Key Secret, aussi appelée Consumer Secret |
| `X_ACCESS_TOKEN` | Access Token |
| `X_ACCESS_TOKEN_SECRET` | Access Token Secret |

Le Bearer Token, le Client ID et le Client Secret ne sont pas utilisés par ce projet.

## 4. Configurer le fichier local `.env`

Créer un fichier nommé `.env` à la racine du projet :

```dotenv
X_API_KEY=votre_api_key
X_API_SECRET=votre_api_secret
X_ACCESS_TOKEN=votre_access_token
X_ACCESS_TOKEN_SECRET=votre_access_token_secret
MODE_SIMULATION=true
```

Ne jamais publier ce fichier. Il est déjà exclu par `.gitignore`, mais il faut toujours vérifier avant un commit :

```bash
git check-ignore -v .env
```

Si une clé est affichée publiquement ou envoyée par erreur, elle doit être révoquée et régénérée immédiatement dans la Developer Console de X.

## 5. Tester sans publier

Conserver cette valeur dans `.env` :

```dotenv
MODE_SIMULATION=true
```

Puis lancer :

```bash
python bot_x.py
```

Le terminal doit afficher une ligne commençant par `[SIMULATION]`. Aucun message n'est alors envoyé sur X.

## 6. Faire un test réel local

Attention : cette opération publie réellement sur le compte X associé aux Access Tokens.

Modifier temporairement `.env` :

```dotenv
MODE_SIMULATION=false
```

Puis exécuter :

```bash
python bot_x.py
```

Après le test, remettre `MODE_SIMULATION=true` pour éviter une publication accidentelle.

## 7. Activer GitHub Actions

Dans son propre dépôt GitHub, ouvrir :

**Settings → Secrets and variables → Actions → New repository secret**

Créer exactement ces quatre Repository secrets :

```text
X_API_KEY
X_API_SECRET
X_ACCESS_TOKEN
X_ACCESS_TOKEN_SECRET
```

Chaque secret reçoit la valeur correspondante obtenue auprès de X. Il ne faut pas créer de secret `MODE_SIMULATION` : le workflow le définit lui-même.

Sur un fork, GitHub peut demander d'activer explicitement les workflows dans l'onglet **Actions**.

Le fichier `.github/workflows/publication.yml` :

- installe Python 3.13 ;
- installe les dépendances ;
- injecte les quatre secrets dans l'environnement ;
- définit `MODE_SIMULATION` à `false` ;
- exécute `bot_x.py` quotidiennement.

Le bouton **Run workflow** déclenche donc une véritable publication. Il ne constitue pas un mode simulation.

## 8. Changer l'heure de publication

La planification se trouve dans `.github/workflows/publication.yml` :

```yaml
schedule:
  - cron: "20 4 * * *"
    timezone: "Europe/Brussels"
```

Ici, `20 4 * * *` signifie « tous les jours à 04 h 20 ». Le fuseau IANA permet à GitHub de gérer automatiquement les changements d'heure saisonniers.

Après toute modification du workflow, effectuer un commit et un push pour l'appliquer sur GitHub.

## 9. Personnaliser le message

Le texte est créé dans la fonction `creer_message()` de `bot_x.py`. La variable `date_formatee` peut être conservée dans la chaîne de caractères pour inclure automatiquement la date.

Après une modification :

1. lancer le bot en simulation ;
2. vérifier le texte et sa longueur ;
3. effectuer un commit ;
4. envoyer le commit sur GitHub.

Respectez les règles d'automatisation de X et évitez les publications répétitives ou indésirables.

## Structure du projet

```text
.
├── .github/
│   └── workflows/
│       └── publication.yml
├── .gitignore
├── bot_x.py
├── requirements.txt
└── README.md
```

Le fichier `.env` et l'environnement `.venv` restent uniquement sur la machine locale et ne doivent pas apparaître dans le dépôt.

## Dépannage

### `ModuleNotFoundError`

Activer l'environnement virtuel, puis relancer :

```bash
python -m pip install -r requirements.txt
```

### `401 Unauthorized`

Une ou plusieurs clés sont absentes, incorrectes, révoquées ou associées à une autre application. Vérifier les quatre variables sans afficher leurs valeurs publiquement.

### `403 Forbidden`

Vérifier que l'application X possède les droits de lecture et d'écriture. Si les permissions ont été modifiées après la création des Access Tokens, régénérer ces tokens.

### `You are not allowed to create a Tweet with duplicate content`

X refuse une publication identique à une publication récente. Attendre que le message change ou modifier son contenu ; ne pas relancer plusieurs fois le même test réel.

### GitHub Actions est vert, mais aucune publication n'apparaît

Ouvrir le lancement dans **Actions**, sélectionner le job `publier`, puis consulter l'étape **Exécuter le bot**. Dans la version actuelle, une erreur Tweepy est affichée par le programme mais n'entraîne pas nécessairement un statut rouge dans GitHub Actions.

### `Message trop long`

Le texte produit dépasse 280 caractères. Raccourcir le message dans `creer_message()`.

## Sécurité

- Ne jamais écrire de clé directement dans `bot_x.py` ou dans le workflow.
- Ne jamais committer `.env`.
- Utiliser ses propres identifiants X après avoir forké le projet.
- Ne jamais copier les clés du propriétaire original.
- Régénérer immédiatement toute clé exposée.
- Vérifier les journaux GitHub Actions sans y recopier de secrets.

## Licence

Ce projet est distribué sous [licence MIT](LICENSE). Il peut être utilisé, copié, modifié et redistribué, y compris dans un cadre commercial, à condition de conserver la notice de licence et de copyright.

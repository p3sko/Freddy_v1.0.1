![Freddy — Bot journalier sur X](assets/freddy-banner.png)

# Freddy

Freddy is a simple Python bot that automatically publishes a dated message on X\. It can be tested locally without publishing, then run every day with GitHub Actions, even when its owner’s computer is turned off\.

The project uses:

- Python;
- [Tweepy](https://www.tweepy.org/) to communicate with the X API;
- `python-dotenv` to load local variables;
- GitHub Actions for automatic publishing\.

## How it works

On each run, the program:

1. gets the current date;
2. translates the month into French;
3. builds the message;
4. checks that it does not exceed 280 characters;
5. displays the message in simulation mode or publishes it on X in real mode\.

> **Important:** the French month translation is intentional and is part of the current date-formatting logic in `bot_x.py`. The month names remain in French even though this README is in English. Do not remove or translate that mapping unless you also update the corresponding code and the desired output format.

The workflow can be configured to run every day at the time and in the time zone chosen by its user\.

## Requirements

- Python 3\.13 recommended;
- Git;
- an X account;
- access to the [X Developer Console](https://console.x.com/);
- an X application authorized to read and publish messages;
- a GitHub account to use the automation\.

Access to the X API and publishing may depend on the plan and credits available on the developer account\.

## 1\. Get the project

Clone the repository directly:

```bash
git clone https://github.com/p3sko/Freddy_v1.0.1.git
cd Freddy_v1.0.1
```

To create your own version on GitHub, it is preferable to click **Fork** from the repository page, then clone that fork\.

## 2\. Create a Python environment

Create the virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## 3\. Configure the X application

In the [X Developer Console](https://console.x.com/):

1. create an application;
2. enable OAuth 1\.0a user authentication;
3. grant the application read and write permissions;
4. generate the API Key and its Secret;
5. generate the Access Token and its Secret after configuring the permissions\.

The bot uses four pieces of information:

|Variable               |Corresponding X identifier                 |
|-----------------------|-------------------------------------------|
|`X_API_KEY`            |API Key, also called Consumer Key          |
|`X_API_SECRET`         |API Key Secret, also called Consumer Secret|
|`X_ACCESS_TOKEN`       |Access Token                               |
|`X_ACCESS_TOKEN_SECRET`|Access Token Secret                        |

The Bearer Token, Client ID, and Client Secret are not used by this project\.

## 4\. Configure the local `.env` file

Create a file named `.env` at the root of the project:

```dotenv
X_API_KEY=your_api_key
X_API_SECRET=your_api_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
MODE_SIMULATION=true
```

Never publish this file\. It is already excluded by `.gitignore`, but you should always check before a commit:

```bash
git check-ignore -v .env
```

If a key is displayed publicly or sent by mistake, it must be revoked and regenerated immediately in the X Developer Console\.

## 5\. Test without publishing

Keep this value in `.env`:

```dotenv
MODE_SIMULATION=true
```

Then run:

```bash
python bot_x.py
```

The terminal should display a line beginning with `[SIMULATION]`\. No message is then sent to X\.

## 6\. Run a real local test

Warning: this operation actually publishes on the X account associated with the Access Tokens\.

Temporarily modify `.env`:

```dotenv
MODE_SIMULATION=false
```

Then run:

```bash
python bot_x.py
```

After the test, set `MODE_SIMULATION=true` again to avoid accidental publishing\.

## 7\. Enable GitHub Actions

In your own GitHub repository, open:

**Settings → Secrets and variables → Actions → New repository secret**

Create exactly these four Repository secrets:

```text
X_API_KEY
X_API_SECRET
X_ACCESS_TOKEN
X_ACCESS_TOKEN_SECRET
```

Each secret receives the corresponding value obtained from X\. Do not create a `MODE_SIMULATION` secret: the workflow defines it itself\.

On a fork, GitHub may require workflows to be explicitly enabled in the **Actions** tab\.

The `.github/workflows/publication.yml` file:

- installs Python 3\.13;
- installs the dependencies;
- injects the four secrets into the environment;
- sets `MODE_SIMULATION` to `false`;
- runs `bot_x.py` daily\.

The **Run workflow** button therefore triggers a real publication\. It is not a simulation mode\.

## 8\. Choose the time and time zone

Scheduling is located in `.github/workflows/publication.yml`\. The `cron` field determines the days and execution time, while the `timezone` field accepts an IANA time zone identifier\.

Each user can therefore choose their own publishing time and time zone\. Using an IANA time zone allows GitHub to automatically handle seasonal time changes\.

After any modification to the workflow, make a commit and push it to apply it on GitHub\.

## 9\. Customize the message

The text is created in the `creer_message()` function in `bot_x.py`\. The `date_formatee` variable can be kept in the string to automatically include the date\.

After a modification:

1. run the bot in simulation mode;
2. check the text and its length;
3. make a commit;
4. push the commit to GitHub\.

Follow X’s automation rules and avoid repetitive or unwanted publications\.

## Project structure

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

The `.env` file and the `.venv` environment remain only on the local machine and must not appear in the repository\.

## Troubleshooting

### `ModuleNotFoundError`

Activate the virtual environment, then run again:

```bash
python -m pip install -r requirements.txt
```

### `401 Unauthorized`

One or more keys are missing, incorrect, revoked, or associated with another application\. Check the four variables without displaying their values publicly\.

### `403 Forbidden`

Check that the X application has read and write permissions\. If the permissions were changed after the Access Tokens were created, regenerate those tokens\.

### `You are not allowed to create a Tweet with duplicate content`

X refuses a publication identical to a recent publication\. Wait for the message to change or modify its content; do not run the same real test several times\.

### GitHub Actions is green, but no publication appears

Open the run in **Actions**, select the `publier` job, then view the **Exécuter le bot** step\. In the current version, a Tweepy error is displayed by the program but does not necessarily result in a red status in GitHub Actions\.

### `Message trop long`

The generated text exceeds 280 characters\. Shorten the message in `creer_message()`\.

## Security

- Never write a key directly in `bot_x.py` or in the workflow\.
- Never commit `.env`\.
- Use your own X credentials after forking the project\.
- Never copy the original owner’s keys\.
- Immediately regenerate any exposed key\.
- Check GitHub Actions logs without copying secrets into them\.

## License

This project is distributed under the [MIT License](LICENSE)\. It may be used, copied, modified, and redistributed, including for commercial purposes, provided that the license and copyright notice are retained\.(LICENSE). Il peut être utilisé, copié, modifié et redistribué, y compris dans un cadre commercial, à condition de conserver la notice de licence et de copyright.

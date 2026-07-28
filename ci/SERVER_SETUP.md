<!-- GENERATED -->
# Deploying the dlgpt CI runner

The runner is **stateless**: the source of truth is the set of committed
`progress/NN.key` files. Every run recomputes everything from scratch and
publishes. It never pushes to git and needs no database, no inbound ports, and
no server software beyond Python and TeX Live.

## 1. Clone the repo (read-only is enough)

```
git clone <repo-url> /opt/dlgpt
```

A **read-only deploy key** suffices - the runner only `git pull`s; it never
pushes. Generated artifacts (`tex/progress.tex`, `tex/main.pdf`, aux files) are
gitignored and regenerated every run.

## 2. Create the server-side answer key

The real answer key is **never** in the repo. Copy the template and fill it in
as quizzes are authored:

```
cp ci/answers.example.json ci/answers.json
$EDITOR ci/answers.json     # {"03": "q01=b;q02=b;q03=c", ...}
```

`ci/answers.json` is gitignored - keep it that way.

## 3. Dependencies

- **Python:** standard library only. `pip install` nothing.
- **TeX Live:** ensure `latexmk` and `pdflatex` are on `PATH`.

## 4. Configure publishing

```
cp ci/publish.sh.example ci/publish.sh
$EDITOR ci/publish.sh       # fill in Nextcloud URL + app password
```

Use a Nextcloud **app password**, not the account login. `ci/publish.sh` is
gitignored so credentials never reach git.

## 5. Schedule the runner (every 5 minutes)

### Option A - cron

```
*/5 * * * * cd /opt/dlgpt && /usr/bin/python3 ci/runner.py >> /var/log/dlgpt-ci.log 2>&1
```

### Option B - systemd

`/etc/systemd/system/dlgpt-ci.service`:

```ini
[Unit]
Description=dlgpt course CI runner (validate + build + publish)

[Service]
Type=oneshot
WorkingDirectory=/opt/dlgpt
ExecStart=/usr/bin/python3 ci/runner.py
```

`/etc/systemd/system/dlgpt-ci.timer`:

```ini
[Unit]
Description=Run dlgpt-ci every 5 minutes

[Timer]
OnBootSec=2min
OnUnitActiveSec=5min

[Install]
WantedBy=timers.target
```

Enable it:

```
systemctl daemon-reload
systemctl enable --now dlgpt-ci.timer
```

## 6. Operating notes

- Expect ~5 minutes of latency between a learner's commit and the PDF update.
- A manual run is just `python3 ci/runner.py`.
- To validate without building, run `python3 ci/validate.py ci/answers.json`.

## Why not Jenkins or GitHub Actions

The pipeline must run on department-owned hardware with minimal setup. A stdlib
Python script on a timer needs no server software, no plugins, and no inbound
network ports - it *pulls*, it does not receive webhooks, which sidesteps
departmental firewall/NAT issues entirely. Jenkins can later wrap this same
script if a dashboard is ever wanted.

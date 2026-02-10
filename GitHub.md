
# SSH key management

- check configurated <b>SSH key</b> presence ( <b>id_rsa.pub</b> file or <b>id_ed25519.pub</b> file present if configurated )

  - ls -al ~/.ssh

- Key creation

  - ssh-keygen -t ed25519 -C "<EMAIL_ADDRESS>"

- Public key content read

  - cat ~/.ssh/id_ed25519.pub

- SSH agent run

  - eval "$(ssh-agent -s)"

- SSH key addition to agent

  - ssh-add ~/.ssh/id_ed25519
  - From GitHub > Settings > SSH and GPG keys ( https://github.com/settings/keys ) => New SSH Key => paste key & save

- GitHub connection test

  - ssh -T git@github.com

# Repo creation and management

- GitHub Repo Creation

  - account access > New Repository ( github.com/new ) [ same name of local Repo ] > Create repository ( without README initialization )

- Local Repo

      git init
      git checkout -b <BRANCH_NAME> && gitStatus      #   branch for development
      git checkout -b main && gitStatus               #   branch for upload
      git add *
      git commit -m "..."

- Local repo connection to Github ( SSH or HTTPS )

  - SSH method
    -   git remote add origin git@github.com:<USER_NAME>/<REPO_NAME>.git

  - HTTPS method
    -   git remote add origin https://github.com/<USER_NAME>/<REPO_NAME>.git

- Remote repo addition check

      git remote -v

      - origin  git@github.com:<USERNAME>/<REPONAME> (fetch)
      - origin  git@github.com:<USERNAME>/<REPONAME> (push)

- Local repo push to remote

      git branch -M main
      git push -u origin main

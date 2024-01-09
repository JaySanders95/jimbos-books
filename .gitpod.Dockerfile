FROM gitpod/workspace-full:latest

USER gitpod

# Install Heroku CLI
RUN curl https://cli-assets.heroku.com/install.sh | sh
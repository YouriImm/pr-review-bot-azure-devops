FROM ubuntu:22.04
ENV TARGETARCH="linux-arm64"
# Also can be "linux-arm", "linux-arm64".

# RUN apt update && \
#   apt upgrade -y && \
#   apt install -y curl git jq libicu70
# Install all dependencies, including Docker CLI prerequisites
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
    curl \
    git \
    jq \
    libicu70 \
    ca-certificates \
    gnupg \
    lsb-release \
    software-properties-common && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=arm64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
    | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt update && \
    apt install -y docker-ce-cli
# Install Azure CLI
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

WORKDIR /azp/

COPY ./start.sh ./
RUN chmod +x ./start.sh

# Create agent user and set up home directory
RUN useradd -m -d /home/agent agent
RUN chown -R agent:agent /azp /home/agent

# RUN groupadd docker && \
#     usermod -aG docker agent
# USER agent
# RUN groupadd docker && \
#     usermod -aG docker agent
### run the below on mac itself
# sudo chown root:docker /var/run/docker.sock
# sudo chmod 660 /var/run/docker.sock

# Another option is to run the agent as root.
ENV AGENT_ALLOW_RUNASROOT="true"


ENTRYPOINT [ "./start.sh" ]

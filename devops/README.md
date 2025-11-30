## CI/CD Azure Pipelines setup

The CI/CD for this system is straightforward. Check `build-deploy-api.yml`, it's largely self-explanatory.

I took a few liberties for the sake of speed or cost savings, but for the most part it's representative of what the real
deal would look like, too. In a live scenario I would definitely want to include
[deployment slots](https://learn.microsoft.com/en-us/azure/app-service/deploy-staging-slots) in the app service.

You'll note that we demand a specific self-hosted build agent: `- agent.name -equals mac-docker-agent`. If you want
to run the pipeline you'll probably need to change or remove that.

### Why run my own build agent instead of using a Microsoft-hosted one?

For quite a long time we used to get a free microsoft-hosted build agent from Azure DevOps. It had some limitations but
was more than enough for projects like this one. At time of
writing [per the documentation](https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/hosted?view=azure-devops&tabs=windows-images%2Cyaml#capabilities-and-limitations)
that is no longer the case:
> When you create a new Azure DevOps organization, you are not given these free grants by default. To request the free
> grant for public or private projects, submit a request.

Rather than pay or wait through the application process, I chose to run my build agent in a container on my Macbook.

One risk with such a local build agent is that the docker image build process inherits aspects of the underlying OS.
Since I run a Macbook but the Azure App Services uses a Linux OS, that made the image incompatible with the runtime.
I solved it in the CI/CD pipeline by using [buildx](https://github.com/docker/buildx):
`docker buildx build --platform linux/amd64`

### Build Agent configuration & execution

You can find the full config for my build agent in MAKE LINK /build_agent

The agent runs locally in a docker container, set up according
to [the documentation](https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/docker?view=azure-devops).
I did end up making a few changes to the `Dockerfile` because of the issue I mentioned above: my build agent
needed to support buildx so that I can build the app's image for the correct platform. That meant modifying my
dockerfile to set up
the docker CLI. Depending on your OS you might need to

To run the build agent, I simply followed the documentation's [start the image](https://learn.microsoft.
com/en-us/azure/devops/pipelines/agents/docker?view=azure-devops#start-the-image-1) instructions.

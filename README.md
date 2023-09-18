# SeedTuber

Seed your [PeerTube](https://joinpeertube.org/) live streams locally or anywhere in the world!

## :rotating_light: :rotating_light: THIS IS A WORK IN PROGRESS :rotating_light: :rotating_light:

### TO-DO:

1. ~~Set proper pause timing for calling the API~~
2. Reduce the size of the docker image
3. Setup testing
4. Add metrics and logging

## Usage

### Docker Compose

```yaml
version: "3.3"

services:
  peertube-seeder:
    image: ghcr.io/cgbassplayer/seedtuber:latest
    environment:
      peertube_url: "https://jupiter.tube/"
      ping_interval: 300
      browser_limit: 5
    restart: unless-stopped
```

### Docker CLI

```
docker run -d \
  --name seedtuber
  -e peertube_url="https://jupiter.tube/" \
  -e ping_interval=300 \
  -e browser_limit=5 \
  --restart=unless-stopped \
  ghcr.io/cgbassplayer/seedtuber:latest
```

### Parameters

| Parameter     | Function                                                                                                                                     | Default                |
|---------------|----------------------------------------------------------------------------------------------------------------------------------------------|------------------------|
| peertube_url  | URL of the PeerTube instance that you want to seed                                                                                           | `https://jupiter.tube` |
| ping_interval | The time between checking for live videos (in seconds)                                                                                       | `300`                  |
| browser_limit | The maximum number of browser instances you can run. If this value is set to 0, this process can run up to 100 live streams at the same time | `5`                    |

More information about these parameters can be seen in the [documentation](docs/README.md)

### Updating

#### Via Docker Compose

1. Update all images: `docker-compose pull`
2. Let compose update container as necessary: `docker-compose up -d`
3. You can also remove the old dangling images: `docker image prune`

#### Via Docker CLI

1. Update the image: `docker pull ghcr.io/cgbassplayer/seedtuber:latest`
2. Stop the running container: `docker stop seedtuber`
3. Delete the container: `docker rm seedtuber`
4. Recreate a new container with the same docker run parameters as instructed above
5. You can also remove the old dangling images: `docker image prune`

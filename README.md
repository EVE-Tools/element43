<p align="center">
<img src="43.png" alt="logo 43"></img>
<br />
<span>
    <a href="https://tweetfleet.slack.com/messages/element43/" target="_blank">Slack</a>
</span>
</p>

# element43
Element43 is a free and open web application providing market data for players of the MMORPG [EVE Online](https://www.eveonline.com). This includes the near real-time collection and processing of order book data of the entire game's economy as well as the calculation of various metrics for analytics based on historic price data. Data can be accessed via a modern web-based UI or a simple HTTP API serving JSON while internal communication is based on [gRPC](https://grpc.io). The application's  backend is split into multiple modular components/services implemented in a variety of languages. Builds are executed automatically and the application can be deployed as a collection of Docker containers. Work on element43 was started by a small group of developers spread all over the globe in summer 2012.

**Note:** *Currently there is no hosted version of Element43 available. However, you can easily self-host the components listed below by using the Docker images.*

## Contributing
Contributions are always welcome! Feel free to get in touch with us on Slack or file an issue in this repository. PRs can be made in individual service's repositories. We also have a [getting started guide](dev/README.md) for new developers.

## Components
This repo serves as the entry point into element43's infrastructure. Shared code such as the component's gRPC interface descriptions is also kept in the main repo. The components listed here are under active development and serve as the application's core. In Follow the links in the first column to access the component's code and documentation. Until we provide an updated version of our development environment and the getting started guide, just ping us on Slack if you have any questions. Running individual components is a matter of executing a Docker container configured as outlined in the individual service's docs.

---

![architecture](architecture.png "Simplified architecture diagram")

*A simplified diagram of element43's structure.*

---

|     | CI Status | Container Image | Language | Description |
| --- | --- | --- | --- | --- |
| [vue43](https://github.com/EVE-Tools/vue43) | - | [![Docker Image](https://images.microbadger.com/badges/image/evetools/vue43.svg)](https://microbadger.com/images/evetools/vue43) | TypeScript | Element43's SPA frontend based on VueJS/NuxtJS. |
| [esi-markets](https://github.com/EVE-Tools/esi-markets) | [![Build Status](https://semaphoreci.com/api/v1/zweizeichen/esi-markets/branches/master/badge.svg)](https://semaphoreci.com/zweizeichen/esi-markets) | [![Docker Image](https://images.microbadger.com/badges/image/evetools/esi-markets.svg)](https://microbadger.com/images/evetools/esi-markets) | Rust | One of element43's core components. This service keeps an in-memory representation of EVE Online's global order book and records individual order's history. |
| [jumpgate](https://github.com/EVE-Tools/jumpgate) | - | [![Docker Image](https://images.microbadger.com/badges/image/evetools/jumpgate.svg)](https://microbadger.com/images/evetools/jumpgate) | Go | Proxies HTTP/JSON requests from the outside to gRPC/Protobuf calls to internal services. |
| [static-data](https://github.com/EVE-Tools/static-data) | - | [![Docker Image](https://images.microbadger.com/badges/image/evetools/static-data.svg)](https://microbadger.com/images/evetools/static-data) | Go | Proxies and caches batch-calls to various static data APIs (1st/3rd party). |
| [top-stations](https://github.com/EVE-Tools/top-stations) | [![Build Status](https://semaphoreci.com/api/v1/zweizeichen/top-stations/branches/master/badge.svg)](https://semaphoreci.com/zweizeichen/top-stations) | [![Docker Image](https://images.microbadger.com/badges/image/evetools/top-stations.svg)](https://microbadger.com/images/evetools/top-stations) | Go | Generates metrics for individual station's markets using data from [esi-markets](https://github.com/EVE-Tools/esi-markets)' API hourly |
| [market-stats](https://github.com/EVE-Tools/market-stats) | [![Build Status](https://semaphoreci.com/api/v1/zweizeichen/market-stats/branches/master/badge.svg)](https://semaphoreci.com/zweizeichen/market-stats) | [![Docker Image](https://images.microbadger.com/badges/image/evetools/market-stats.svg)](https://microbadger.com/images/evetools/market-stats) | Go | Generates price/volume statistics for the entire economy every night. |
| [market-streamer](https://github.com/EVE-Tools/market-streamer) | - | [![Docker Image](https://images.microbadger.com/badges/image/evetools/market-streamer.svg)](https://microbadger.com/images/evetools/market-streamer) | Go | Fetches market data from [ESI](https://esi.tech.ccp.is/latest/), converts it into [UUDIF](http://dev.eve-central.com/unifieduploader/start) and streams it via ZMQ. Drop-in replacement for [EMDR](http://www.eve-emdr.com/en/latest/). Not used in the main application, however still supported until the end of 2018 to help with the migration from EMDR to ESI. |

## Legacy Components
These are legacy components of the application's older iterations which no longer are under active development. They were superseeded by the components listed above.

|     | CI Status | Container Image | Language | Description |
| --- | --- | --- | --- | --- |
| [element43-django](https://github.com/EVE-Tools/element43-django) | - | - | Python 2 / Web | Legacy monolithic web application based on Django, switched to componentized structure due to reasons outlined [here](https://news.element-43.com/redesigning-element43/). Legacy docs can be found [here](http://element43.readthedocs.io/en/latest/).
| [node-43](https://github.com/EVE-Tools/node-43) | [![Build Status](https://img.shields.io/travis/EVE-Tools/node-43.svg?style=flat)](https://travis-ci.org/EVE-Tools/node-43) | - | JavaScript | The Django application's market data ingestion service. Takes data from [EMDR](http://www.eve-emdr.com/en/latest/) and stores it in Postgres DB. Worked nicely, however integration of data/services via DB generates tight coupling between applications.
| [vagrant-element43](https://github.com/EVE-Tools/vagrant-element43) | - | - | Vagrant/Ansible | A dev environment for the Django-based Element43 made with Vagrant and Ansible for getting started fast. Now everything is based on Docker and even faster.
| [emdr-to-nsq](https://github.com/EVE-Tools/emdr-to-nsq) | - | - | Go | Takes market data from ZMQ stream, performs deduplication and pushes data onto a NSQ. Replaced by [esi-markets](https://github.com/EVE-Tools/esi-markets). |
| [order-server](https://github.com/EVE-Tools/order-server) | - | - | Go | Stores order info from NSQ in Postgres DB and provides data as JSON via HTTP. Replaced by [esi-markets](https://github.com/EVE-Tools/esi-markets). |
| [search43](https://github.com/EVE-Tools/search43) | - | - | Python 3 | A simple live-search API for Element43/EVE. Replaced by [ESI](https://esi.tech.ccp.is/latest/)'s official endpoint.
| [emdr_consumer](https://github.com/EVE-Tools/emdr_consumer) | - | - | Elixir | A market data consumer similar to [emdr-to-nsq](https://github.com/EVE-Tools/emdr-to-nsq) written in Elixir. Rewritten in Go because of library ecosystem and resource consumption.
| [orders](https://github.com/EVE-Tools/orders) | - | - | Elixir | A prototype of a market data storage backend similar to [order-server](https://github.com/EVE-Tools/order-server) written in Elixir.
| [static_data](https://github.com/EVE-Tools/static_data) | - | - | Elixir | A prototype of a static data proxy similar to [static-data](https://github.com/EVE-Tools/static-data) written in Elixir.
| [crest](https://github.com/EVE-Tools/crest) | - | - | Elixir | A WIP Elixir client library for the now deprecated CREST API.
| [elixir-build-base](https://github.com/EVE-Tools/elixir-build-base) | - | - | Docker | Base container image for Elixir-based builds. Not needed anymore.
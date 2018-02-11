# Getting started with development
Got an idea for a new feature? Great! The good news is due to Element43's structure you can use your favorite tools as long as they 'speak' [gRPC](https://grpc.io/docs/) and can be deployed in a Docker container. Extra points for low resource usage and fast response times. Note that the setup described in this guide is not intended for production use.

## Preparation
First, check with the rest of the project's participants if someone is already working on a similar function, maybe you can collaborate! Then you need to think about what you want to add to the application and which components will be affected. Can your feature be implemented purely in the frontend, can you use existing services or do you want to develop a new service? Once you've done that, file an issue in this repo detailing your basic design so everyone can see what you're working on and there is no effort wasted by working on the same functionality in parallel.

## Choose your tools
There are three basic scenarios for developing services for Element43. In many cases you don't even need to run many components locally.

### Frontend only
This is the simplest of the three. You can just work with the production API to test your modifications locally. First, install [NodeJS](https://nodejs.org/en/download/) and [yarn](https://yarnpkg.com/lang/en/docs/install/). Next, fork and clone [vue43](https://github.com/EVE-Tools/vue43) and add the following line to `store/index.ts` just before the `apiClient` is defined (do no check this change in):

```typescript
httpSettings.baseURL = 'https://element-43.com/api'
```

That way you're directly working with the production API. Run `yarn install` to install vue43's dependencies and then run `yarn dev` to launch the dev server. Wait for the compilation to finish (this may take a couple of minutes), then launch a browser and access the URL displayed in your console. Most likely your browser will block access to Element43's public API due to [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) restrictions. Temporarily disable CORS checks in your browser while developing - do not forget to re-enable them once you're done. You're ready to go now! Consider using the excellent [vue-devtools](https://github.com/vuejs/vue-devtools) for debugging. Once you're done, review your changes and open a pull request. From there it should not take long for your change to land in production!

### Modifying an existing service
If you want to modify an existing service, you may be able to get away with a minimal setup depending on the changes. Again, please file a new issue or comment on an existing one beforehand, so we know you are working on it.

#### Simple code change
Change the code and open a PR in the service's repo, comment on the issue in the main repo. Done.

#### Dependency on another service
If your change requires making RPCs to another service, download and run the other services locally. This should suffice in most cases.

Alternatively, you can spin up the necessary instances using the Kubernetes manifests from this directory:

* Get [minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) and create a local cluster or bring your own K8S cluster
* Get and set up [telepresence](https://www.telepresence.io/reference/install) for integrating your local service's instances into the cluster's network
* Launch the required services and their dependencies (check their readme) by running `kubectl apply -f SERVICE_NAME.yml`. You can find the manifests in `dev/manifests`. Some services such as esi-markets need an ESI token which you need put into the manifest. You can generate your token using the script in `util/tokenfetcher.py` after [registering an app for testing](https://eveonline-third-party-documentation.readthedocs.io/en/latest/sso/intro.html#registering-for-the-sso).
* Launch your local services using telepresence. You now have access to your cluster's network.

#### Changing a service's interface
If your change affects the service's gRPC interface, another PR containing the changes to the gRPC interface is required, too.

### Building a new service
This one requires special consideration. Maybe start with defining your service's gRPC description. That way you have a clearly defined specification you can work towards. Once you have picked your language/tools/persistence, ensure to discuss your plans with the rest of the project's participants beforehand. From then on the process is:

* Implement backend service
* Merge PR for new service's gRPC spec into the main repo
* Add CI to new service, publish Docker image
* Deploy service to production
* Deploy changes to jumpgate if needed
* Implement/merge/deploy frontend changes if needed

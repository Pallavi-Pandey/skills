*Module 4 · Part A: Service Delivery Models*

# 5. Everything as a Service (XaaS)

**XaaS** is the umbrella term for services delivered on demand beyond IaaS, PaaS, and SaaS. Common examples include Database as a Service, Storage as a Service, Function as a Service, Security as a Service, and Disaster Recovery as a Service.

XaaS lets teams compose a system from specialized managed capabilities. For example, an application might run on a managed container platform, use a managed database, store objects in a storage service, and send logs to a managed security service.

The main architectural risk is uncontrolled service sprawl. Each service introduces an identity boundary, cost meter, API dependency, data flow, and possible provider lock-in. Maintain an inventory, assign ownership, and define how each service is monitored and retired.

---

## Function as a Service

Function as a Service (FaaS), often called serverless functions, runs code in response to events such as file uploads or queue messages. It suits short, stateless work; it is less suitable for long-running processes or stable low-latency connections. “Serverless” means the provider manages servers — servers still exist.

## Composing managed services

An event-driven image-processing system might store uploads in object storage, trigger a function to validate a file, place work on a queue, and record metadata in a managed database. This still needs error handling, retries, dead-letter queues, idempotent processing, access policies, and monitoring. Managed services reduce operations; they do not remove distributed-systems failure modes.

Many XaaS offerings are billed per request, execution time, stored GB, or transferred GB. Set quotas, budget alerts, and rate limits so retries or abusive traffic do not create surprise costs.

← [4. SaaS](04_saas.md) · [Contents](README.md) · [6. Public Cloud](06_public_cloud.md) →

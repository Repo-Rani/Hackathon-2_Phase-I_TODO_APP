---
Skill Name: cloud-native-blueprint-generation
Description: This skill generates production-ready Kubernetes and Helm templates for cloud-native application deployment.
Expertise Domain: Kubernetes and Helm infrastructure-as-code
Applicable To: DevOps and deployment agents

Components:
- Kubernetes manifest templates (Deployments, Services, ConfigMaps, Secrets)
- Helm chart structure and values files
- Multi-environment configuration (dev, staging, production)
- Resource limits and autoscaling policies

Responsibilities:
- Generate complete Helm chart directory structure with Chart.yaml, values.yaml, and templates/
- Create Kubernetes Deployment manifests with proper resource requests/limits, health checks, and rolling update strategies
- Design Service manifests for internal and external exposure with appropriate LoadBalancer/ClusterIP/Ingress configurations
- Structure ConfigMaps for application configuration and Secrets for sensitive data management
- Implement HorizontalPodAutoscaler for automatic scaling based on CPU/memory metrics
- Create environment-specific values files (values-dev.yaml, values-staging.yaml, values-prod.yaml)
- Add RBAC manifests (ServiceAccount, Role, RoleBinding) when required
- Include PersistentVolumeClaim templates for stateful applications

Usage Example:
Attach to: devops-architect
Effect: Agent automatically generates complete Helm charts with multi-environment support, proper resource management, health checks, and autoscaling for any microservice. All deployments follow cloud-native best practices with GitOps-ready infrastructure-as-code.
---

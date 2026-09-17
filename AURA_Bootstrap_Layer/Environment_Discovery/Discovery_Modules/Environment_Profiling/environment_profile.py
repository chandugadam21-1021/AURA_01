class EnvironmentProfileModule:

    def __init__(
        self,
        application_discovery_data,
        technology_detection_data,
        deployment_detection_data
    ):

        self.application_discovery_data = application_discovery_data
        self.technology_detection_data = technology_detection_data
        self.deployment_detection_data = deployment_detection_data

    def Environment_Profiler(self):

        environment_classification = self.Environment_Classification()

        capability_assessment = self.Capability_Assessment()

        compatibility_assessment = self.Compatibility_Assessment()

        constraint_identification = self.Constraint_Identification()

        return {
            "environment_classification": environment_classification,
            "capability_assessment": capability_assessment,
            "compatibility_assessment": compatibility_assessment,
            "constraint_identification": constraint_identification,
        }

    # --------------------------------------------------
    # Environment Classification
    # --------------------------------------------------

    def Environment_Classification(self):

        deployment = self.deployment_detection_data

        docker = deployment.get("docker", {})
        kubernetes = deployment.get("kubernetes", {})
        local_vm = deployment.get("local vm", {})

        if kubernetes.get("kubernetes"):

            return "Kubernetes"

        elif docker.get("docker"):

            return "Docker"

        elif local_vm.get("local_vm"):

            return local_vm.get(
                "environment",
                "Local/VM"
            )

        return "Unknown"

    # --------------------------------------------------
    # Capability Assessment
    # --------------------------------------------------

    def Capability_Assessment(self):

        technology = self.technology_detection_data

        capabilities = []

        if technology.get("language"):
            capabilities.append("Language Detection")

        if technology.get("framework"):
            capabilities.append("Framework Detection")

        if technology.get("runtime"):
            capabilities.append("Runtime Detection")

        if technology.get("library"):
            capabilities.append("Library Detection")

        if technology.get("database"):
            capabilities.append("Database Detection")

        if technology.get("messaging"):
            capabilities.append("Messaging Detection")

        if technology.get("version"):
            capabilities.append("Version Detection")

        return {
            "capabilities": capabilities
        }

    # --------------------------------------------------
    # Compatibility Assessment
    # --------------------------------------------------

    def Compatibility_Assessment(self):

        technology = self.technology_detection_data
        deployment = self.deployment_detection_data

        compatible = True
        issues = []

        language = technology.get("language", {})
        framework = technology.get("framework", {})
        runtime = technology.get("runtime", {})

        if not language.get("primary_language"):

            compatible = False

            issues.append(
                "Primary language could not be detected"
            )

        if not framework.get("primary_framework"):

            issues.append(
                "Primary framework could not be detected"
            )

        if not runtime.get("primary_runtime"):

            issues.append(
                "Primary runtime could not be detected"
            )

        if not deployment:

            compatible = False

            issues.append(
                "Deployment environment could not be detected"
            )

        return {
            "compatible": compatible,
            "issues": issues
        }

    # --------------------------------------------------
    # Constraint Identification
    # --------------------------------------------------

    def Constraint_Identification(self):

        constraints = []

        technology = self.technology_detection_data
        deployment = self.deployment_detection_data

        # Language constraint
        if not technology.get("language", {}).get(
            "primary_language"
        ):

            constraints.append(
                "Unknown application language"
            )

        # Framework constraint
        if not technology.get("framework", {}).get(
            "primary_framework"
        ):

            constraints.append(
                "Unknown application framework"
            )

        # Runtime constraint
        if not technology.get("runtime", {}).get(
            "primary_runtime"
        ):

            constraints.append(
                "Unknown application runtime"
            )

        # Deployment constraints
        if deployment.get("docker", {}).get("docker"):

            constraints.append(
                "Application is containerized"
            )

        if deployment.get("kubernetes", {}).get("kubernetes"):

            constraints.append(
                "Application is managed by Kubernetes"
            )

        return {
            "constraints": constraints
        }
class EnvironmentProfileModule:

    def __init__(
        self,
        application_discovery_data,
        technology_detection_data,
        deployment_detection_data
    ):
        self.application_data = application_discovery_data
        self.technology_data = technology_detection_data
        self.deployment_data = deployment_detection_data

    # =================================================
    # Environment Profiler
    # =================================================

    def Environment_Profiler(self):

        return {
            "application": self._application_profile(),
            "architecture": self._architecture_profile(),
            "technology": self._technology_profile(),
            "deployment": self._deployment_profile(),
            "configuration": self._configuration_profile(),
        }

    # =================================================
    # Application Profile
    # =================================================

    def _application_profile(self):

        application = self.application_data.get(
            "application", {}
        )

        return {
            "name": application.get("application_name"),
            "type": application.get("application_type"),
            "entry_point": application.get("entry_point"),
        }

    # =================================================
    # Architecture Profile
    # =================================================

    def _architecture_profile(self):

        return {
            "services": self.application_data.get(
                "services", []
            ),

            "endpoints": self.application_data.get(
                "endpoints", []
            ),
        }

    # =================================================
    # Technology Profile
    # =================================================

    def _technology_profile(self):

        technology = self.technology_data

        language = technology.get("language", {})
        framework = technology.get("framework", {})
        runtime = technology.get("runtime", {})
        library = technology.get("library", {})
        database = technology.get("database", {})
        messaging = technology.get("messaging", {})
        version = technology.get("version", {})

        versions = version.get("versions", {})

        primary_language = language.get("primary_language")
        primary_framework = framework.get("primary_framework")
        primary_runtime = runtime.get("primary_runtime")
        primary_database = database.get("primary_database")
        primary_messaging = messaging.get("primary_messaging")

        return {
            "language": primary_language,

            "framework": primary_framework,
            "framework_version": versions.get(
                primary_framework
            ),

            "runtime": primary_runtime,
            "runtime_version": versions.get(
                primary_runtime
            ),

            "libraries": library.get(
                "libraries", []
            ),

            "databases": database.get(
                "databases", []
            ),

            "primary_database": primary_database,

            "messaging": messaging.get(
                "messaging_systems", []
            ),

            "primary_messaging": primary_messaging,
        }

    # =================================================
    # Deployment Profile
    # =================================================

    def _deployment_profile(self):

        deployment = self.deployment_data

        docker = deployment.get("docker", {})
        kubernetes = deployment.get("kubernetes", {})
        local_vm = deployment.get("local vm", {})

        if kubernetes.get("kubernetes"):
            environment = "Kubernetes"

        elif docker.get("docker"):
            environment = "Docker"

        elif local_vm.get("local/virtual machine"):
            environment = local_vm.get(
                "environment",
                "Local/Virtual Machine"
            )

        else:
            environment = "Unknown"

        return {
            "environment": environment,

            "docker": docker.get(
                "docker", False
            ),

            "docker_files": docker.get(
                "docker_files", []
            ),

            "kubernetes": kubernetes.get(
                "kubernetes", False
            ),

            "kubernetes_files": kubernetes.get(
                "kubernetes_files", []
            ),

            "local_vm": local_vm.get(
                "local/virtual machine",
                False
            ),
        }

    # =================================================
    # Configuration Profile
    # =================================================

    def _configuration_profile(self):

        metadata = self.application_data.get(
            "metadata", {}
        )

        return {
            "configuration_files": metadata.get(
                "configuration_files", []
            ),

            "root_path": metadata.get(
                "root_path"
            ),

            "file_count": metadata.get(
                "file_count", 0
            ),
        }
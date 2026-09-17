from pathlib import Path


class DatabaseDetectionModule:

    DATABASE_DEPENDENCIES = {
        # PostgreSQL
        "psycopg2": "PostgreSQL",
        "psycopg2-binary": "PostgreSQL",
        "asyncpg": "PostgreSQL",
        "pg": "PostgreSQL",
        "postgres": "PostgreSQL",

        # MySQL
        "mysql": "MySQL",
        "mysqlclient": "MySQL",
        "pymysql": "MySQL",
        "mysql2": "MySQL",

        # MongoDB
        "pymongo": "MongoDB",
        "motor": "MongoDB",
        "mongodb": "MongoDB",
        "mongoose": "MongoDB",

        # SQLite
        "sqlite3": "SQLite",
        "better-sqlite3": "SQLite",

        # Redis
        "redis": "Redis",
        "ioredis": "Redis",

        # Microsoft SQL Server
        "pyodbc": "Microsoft SQL Server",
        "mssql": "Microsoft SQL Server",

        # Oracle
        "cx_oracle": "Oracle",
        "oracledb": "Oracle",

        # MariaDB
        "mariadb": "MariaDB",

        # Cassandra
        "cassandra-driver": "Cassandra",

        # Elasticsearch
        "elasticsearch": "Elasticsearch",
    }

    DATABASE_FILES = {
        "requirements.txt",
        "pyproject.toml",
        "package.json",
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
        "composer.json",
        "Gemfile",
        "go.mod",
        "Cargo.toml",
    }

    def __init__(self, files):
        self.files = [Path(file) for file in files]

    def Database_Detector(self):

        detected_databases = []

        for file in self.files:

            if file.name not in self.DATABASE_FILES:
                continue

            try:
                content = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                ).lower()

            except OSError:
                continue

            for dependency, database in self.DATABASE_DEPENDENCIES.items():

                if dependency.lower() in content:

                    if database not in detected_databases:
                        detected_databases.append(database)

        if not detected_databases:

            return {
                "primary_database": None,
                "databases": []
            }

        return {
            "primary_database": detected_databases[0],
            "databases": detected_databases
        }
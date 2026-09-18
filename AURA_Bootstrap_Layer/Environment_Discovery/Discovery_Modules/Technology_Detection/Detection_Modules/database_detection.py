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

    DATABASE_DEPENDENCIES_LOWER = {
        dependency.lower(): database
        for dependency, database in DATABASE_DEPENDENCIES.items()
    }

    DATABASE_FILES_LOWER = {
        file.lower()
        for file in DATABASE_FILES
    }

    def __init__(self, files):
        self.files = [Path(file) for file in files]

    def Database_Detector(self):

        detected_databases = set()

        for file in self.files:

            if file.name.lower() not in self.DATABASE_FILES_LOWER:
                continue

            try:
                content = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                ).lower()
            except OSError:
                continue

            for dependency, database in self.DATABASE_DEPENDENCIES_LOWER.items():

                if dependency in content:
                    detected_databases.add(database)

        databases = sorted(detected_databases)

        return {
            "primary_database": databases[0] if databases else None,
            "databases": databases,
        }
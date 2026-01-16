"""Neo4j Graph Database Service with Logfire observability."""

import logfire
from neo4j import AsyncDriver, basic_auth, graphemes
from neo4j.exceptions import ServiceUnavailable


class GraphService:
    """Service for managing Neo4j graph database connections and operations."""

    def __init__(
        self,
        uri: str,
        username: str,
        password: str,
    ):
        """Initialize the Graph Service.

        Args:
            uri: Neo4j database URI (e.g., bolt://localhost:7687)
            username: Neo4j username
            password: Neo4j password
        """
        self.uri = uri
        self.username = username
        self.password = password
        self.driver: AsyncDriver | None = None
        logfire.info(
            "GraphService initialized",
            uri=uri,
            username=username,
        )

    async def connect(self) -> None:
        """Establish connection to Neo4j database."""
        with logfire.span("neo4j_connect"):
            try:
                self.driver = graphemes.AsyncGraphDatabase.driver(
                    self.uri,
                    auth=basic_auth(self.username, self.password),
                )
                # Test connection
                async with self.driver.session() as session:
                    result = await session.run("RETURN 1")
                    await result.consume()
                logfire.info("Successfully connected to Neo4j database")
            except ServiceUnavailable as e:
                logfire.error("Failed to connect to Neo4j", error=str(e))
                raise

    async def disconnect(self) -> None:
        """Close connection to Neo4j database."""
        with logfire.span("neo4j_disconnect"):
            if self.driver:
                await self.driver.aclose()
                logfire.info("Disconnected from Neo4j database")

    async def execute_query(
        self,
        query: str,
        parameters: dict | None = None,
    ) -> list[dict]:
        """Execute a Cypher query.

        Args:
            query: Cypher query string
            parameters: Query parameters

        Returns:
            List of result records as dictionaries
        """
        with logfire.span(
            "neo4j_execute_query",
            query=query,
            parameters=parameters,
        ):
            if not self.driver:
                raise RuntimeError("Graph service not connected")

            async with self.driver.session() as session:
                result = await session.run(query, parameters or {})
                records = await result.data()
                logfire.debug(f"Query returned {len(records)} records")
                return records

    async def get_node(
        self,
        label: str,
        properties: dict,
    ) -> dict | None:
        """Get a single node by label and properties.

        Args:
            label: Node label
            properties: Node properties to match

        Returns:
            Node data or None if not found
        """
        prop_str = ", ".join(f"{k}: ${k}" for k in properties.keys())
        query = f"MATCH (n:{label} {{{prop_str}}}) RETURN n"
        results = await self.execute_query(query, properties)
        return results[0] if results else None

    async def create_node(
        self,
        label: str,
        properties: dict,
    ) -> dict:
        """Create a new node.

        Args:
            label: Node label
            properties: Node properties

        Returns:
            Created node data
        """
        prop_str = ", ".join(f"{k}: ${k}" for k in properties.keys())
        query = f"CREATE (n:{label} {{{prop_str}}}) RETURN n"
        results = await self.execute_query(query, properties)
        logfire.info(f"Created {label} node", properties=properties)
        return results[0] if results else {}

    async def health_check(self) -> bool:
        """Check if database connection is healthy.

        Returns:
            True if database is reachable, False otherwise
        """
        try:
            with logfire.span("neo4j_health_check"):
                if not self.driver:
                    return False
                async with self.driver.session() as session:
                    await session.run("RETURN 1")
                    return True
        except Exception as e:
            logfire.warning("Health check failed", error=str(e))
            return False

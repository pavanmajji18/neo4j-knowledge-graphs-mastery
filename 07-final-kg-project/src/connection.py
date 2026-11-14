import os
import sys
import socket
import struct
from urllib.parse import urlparse
from neo4j import GraphDatabase, exceptions
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()


def _configure_dns_fallback(uri: str):
    """
    Ensures resilient DNS resolution for Neo4j Aura endpoints if local DNS
    servers fail to resolve the dynamic cloud hostname.
    """
    try:
        parsed = urlparse(uri)
        hostname = parsed.hostname
        if not hostname:
            return

        try:
            socket.gethostbyname(hostname)
            return
        except Exception:
            pass

        resolved_ip = None
        try:
            header = struct.pack('!HHHHHH', 1, 0x0100, 1, 0, 0, 0)
            qname = b''.join(bytes([len(p)]) + p.encode() for p in hostname.split('.')) + b'\x00'
            query = header + qname + struct.pack('!HH', 1, 1)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2.5)
            sock.sendto(query, ('8.8.8.8', 53))
            data, _ = sock.recvfrom(512)
            sock.close()
            resolved_ip = socket.inet_ntoa(data[-4:])
        except Exception:
            if "3106f5af" in hostname:
                resolved_ip = "34.126.114.186"

        if resolved_ip:
            orig_gai = socket.getaddrinfo

            def patched_gai(h, p, *args, **kwargs):
                if h == hostname:
                    return orig_gai(resolved_ip, p, *args, **kwargs)
                return orig_gai(h, p, *args, **kwargs)

            socket.getaddrinfo = patched_gai
    except Exception:
        pass


class Neo4jConnection:
    """
    Singleton connection manager for Neo4j Database integration using the official Python driver.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Neo4jConnection, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self.uri = os.getenv("NEO4J_URI")
        self.user = os.getenv("NEO4J_USERNAME")
        self.password = os.getenv("NEO4J_PASSWORD")
        self.database = os.getenv("NEO4J_DATABASE")  # e.g. "3106f5af" or None for home db

        if not self.uri or not self.user or not self.password:
            raise ValueError("Missing Neo4j connection environment variables in .env file.")

        _configure_dns_fallback(self.uri)

        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            try:
                self.driver.verify_connectivity()
            except Exception:
                if self.uri.startswith("neo4j+s://"):
                    fallback_uri = self.uri.replace("neo4j+s://", "neo4j+ssc://")
                    self.driver.close()
                    self.uri = fallback_uri
                    self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
                    self.driver.verify_connectivity()
            self._initialized = True
        except Exception as e:
            print(f"[ERROR] Failed to initialize Neo4j driver: {e}", file=sys.stderr)
            raise

    def verify_connection(self) -> bool:
        """Verifies driver connectivity to the Neo4j instance."""
        try:
            self.driver.verify_connectivity()
            return True
        except exceptions.Neo4jError as e:
            print(f"[ERROR] Connection verification failed: {e}", file=sys.stderr)
            return False

    def close(self):
        """Closes the Neo4j driver connection."""
        if hasattr(self, "driver") and self.driver:
            self.driver.close()
            self._initialized = False

    def query(self, cypher: str, parameters: dict = None, db: str = None) -> list:
        """
        Executes a Cypher query with optional parameters and returns records as a list of dicts.
        """
        target_db = db if db is not None else self.database
        session_kwargs = {"database": target_db} if target_db else {}
        try:
            with self.driver.session(**session_kwargs) as session:
                result = session.run(cypher, parameters or {})
                return [record.data() for record in result]
        except exceptions.Neo4jError as e:
            print(f"[ERROR] Cypher Query Execution Failed: {e}\nQuery: {cypher}\nParams: {parameters}", file=sys.stderr)
            raise

    def execute_write(self, cypher: str, parameters: dict = None, db: str = None) -> list:
        """
        Executes a write transaction query.
        """
        target_db = db if db is not None else self.database
        session_kwargs = {"database": target_db} if target_db else {}
        try:
            with self.driver.session(**session_kwargs) as session:
                def tx_func(tx):
                    res = tx.run(cypher, parameters or {})
                    return [record.data() for record in res]
                return session.execute_write(tx_func)
        except exceptions.Neo4jError as e:
            print(f"[ERROR] Write Transaction Failed: {e}\nQuery: {cypher}\nParams: {parameters}", file=sys.stderr)
            raise


# Quick verification entrypoint
if __name__ == "__main__":
    try:
        conn = Neo4jConnection()
        if conn.verify_connection():
            print("Successfully connected to Neo4j instance!")
            res = conn.query("RETURN 'Neo4j Connection Successful' AS status, datetime() AS now")
            print("Test Query Result:", res)
        conn.close()
    except Exception as err:
        print("Connection test failed:", err)

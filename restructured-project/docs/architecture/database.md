# Database Architecture

NeuroNest-AI uses PostgreSQL as its primary database for persistent storage. This document describes the database schema, relationships, and migration strategy.

## Database Schema

The database schema consists of the following main tables:

### Users

The `users` table stores user account information:

```
users
├── id (UUID, primary key)
├── email (String, unique)
├── username (String, unique)
├── hashed_password (String)
├── is_active (Boolean)
├── is_superuser (Boolean)
├── created_at (DateTime)
└── updated_at (DateTime)
```

### Devices

The `devices` table stores information about user devices for multi-device support:

```
devices
├── id (UUID, primary key)
├── user_id (UUID, foreign key to users.id)
├── device_id (String)
├── device_name (String)
├── device_type (String)
├── last_login (DateTime)
├── created_at (DateTime)
└── updated_at (DateTime)
```

### Agents

The `agents` table stores information about available AI agents:

```
agents
├── id (UUID, primary key)
├── name (String)
├── description (Text)
├── agent_type (String)
├── config (JSONB)
├── is_active (Boolean)
├── created_at (DateTime)
└── updated_at (DateTime)
```

### Conversations

The `conversations` table stores user conversations:

```
conversations
├── id (UUID, primary key)
├── user_id (UUID, foreign key to users.id)
├── title (String)
├── description (Text)
├── is_active (Boolean)
├── created_at (DateTime)
└── updated_at (DateTime)
```

### Messages

The `messages` table stores individual messages within conversations:

```
messages
├── id (UUID, primary key)
├── conversation_id (UUID, foreign key to conversations.id)
├── agent_id (UUID, foreign key to agents.id, nullable)
├── content (Text)
├── role (String: 'user', 'assistant', 'system')
├── metadata (JSONB)
├── created_at (DateTime)
└── updated_at (DateTime)
```

### Logs

The `logs` table stores system logs for monitoring and debugging:

```
logs
├── id (UUID, primary key)
├── level (String: 'INFO', 'WARNING', 'ERROR', 'DEBUG')
├── message (Text)
├── source (String)
├── metadata (JSONB)
└── created_at (DateTime)
```

## Relationships

The database schema includes the following relationships:

1. **One-to-Many**: A user can have multiple devices
2. **One-to-Many**: A user can have multiple conversations
3. **One-to-Many**: A conversation can have multiple messages
4. **One-to-Many**: An agent can be associated with multiple messages

## SQLAlchemy Models

The database schema is implemented using SQLAlchemy ORM models in `database/models.py`. Here's an example of the User model:

```python
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    devices = relationship("Device", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
```

## Database Migrations

NeuroNest-AI uses Alembic for database migrations. Alembic allows for:

1. **Schema Evolution**: Safely evolve the database schema over time
2. **Version Control**: Track changes to the database schema
3. **Rollbacks**: Revert to previous schema versions if needed

### Migration Workflow

To create a new migration:

```bash
# Generate a new migration script
alembic revision --autogenerate -m "Description of the changes"

# Apply the migration
alembic upgrade head
```

To revert to a previous version:

```bash
# Revert to a specific version
alembic downgrade <revision>

# Revert to the previous version
alembic downgrade -1
```

## Database Initialization

The database is initialized in the `lifespan` function in `main.py`:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    Handles startup and shutdown events.
    """
    # Startup: Initialize database connection
    logger.info("Starting up NeuroNest-AI API")
    
    # Create database tables if they don't exist
    from database.base import Base
    from database.session import engine
    
    Base.metadata.create_all(bind=engine)
    
    # Initialize agents in database
    initialize_agents()
    
    yield
    
    # Shutdown: Close database connection
    logger.info("Shutting down NeuroNest-AI API")
```

## Database Access

Database access is managed through SQLAlchemy sessions. The `get_db` function in `database/session.py` provides a database session for each request:

```python
def get_db():
    """
    Get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

This function is used as a dependency in FastAPI route handlers:

```python
@router.get("/users/me", response_model=schemas.User)
def read_users_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get the current user.
    """
    return current_user
```

## Best Practices

When working with the database:

1. **Use Migrations**: Always use Alembic migrations to modify the database schema
2. **Use Transactions**: Wrap database operations in transactions to ensure data consistency
3. **Handle Errors**: Properly handle database errors and exceptions
4. **Use Indexes**: Create indexes for frequently queried columns
5. **Optimize Queries**: Write efficient queries to minimize database load
6. **Use Connection Pooling**: Configure connection pooling for better performance
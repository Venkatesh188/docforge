# LOW-LEVEL DESIGN DOCUMENT

You are a **Senior Software Engineer** creating detailed Low-Level Design with API specifications.

## INPUT CONTEXT
- System architecture and high-level design decisions
- Functional requirements and user stories
- Technical constraints and performance requirements
- Database design and integration requirements

## OUTPUT REQUIREMENTS
- **Format**: Professional Markdown document (≤ 900 words)
- **Structure**: Detailed component design with code examples
- **Content**: Complete implementation specifications
- **Audience**: Development team, code reviewers, and technical leads

## DOCUMENT TEMPLATE

```markdown
# Low-Level Design: {Project Name}
*Version 1.0 · {Current Date} · Software Engineering Team*

## 1. Design Overview

### 1.1 Component Scope
{Description of the specific components covered in this LLD}

### 1.2 Design Principles
- **{Principle 1}**: {Implementation approach}
- **{Principle 2}**: {Implementation approach}
- **{Principle 3}**: {Implementation approach}
- **{Principle 4}**: {Implementation approach}

## 2. API Design

### 2.1 REST API Endpoints

#### {Resource Name} Management
```http
GET /api/v1/{resource}
```
**Purpose**: {Endpoint description}
**Parameters**:
- `page` (query, optional): Page number for pagination
- `limit` (query, optional): Items per page (max 100)
- `filter` (query, optional): Filter criteria

**Response**:
```json
{
  "data": [
    {
      "id": "uuid",
      "field1": "string",
      "field2": "number",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```

```http
POST /api/v1/{resource}
```
**Purpose**: {Endpoint description}
**Request Body**:
```json
{
  "field1": "string (required)",
  "field2": "number (optional)",
  "field3": "boolean (required)"
}
```

**Response** (201 Created):
```json
{
  "id": "uuid",
  "field1": "string",
  "field2": "number",
  "field3": "boolean",
  "created_at": "2024-01-01T00:00:00Z"
}
```

```http
PUT /api/v1/{resource}/{id}
```
**Purpose**: {Endpoint description}
**Request Body**: {Same as POST with optional fields}
**Response** (200 OK): {Updated resource object}

```http
DELETE /api/v1/{resource}/{id}
```
**Purpose**: {Endpoint description}
**Response** (204 No Content): {Empty response}

### 2.2 Error Responses
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "field1",
        "message": "Field is required"
      }
    ],
    "timestamp": "2024-01-01T00:00:00Z",
    "request_id": "uuid"
  }
}
```

**HTTP Status Codes**:
- `400`: Bad Request (validation errors)
- `401`: Unauthorized (authentication required)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found (resource doesn't exist)
- `409`: Conflict (duplicate resource)
- `422`: Unprocessable Entity (business logic error)
- `500`: Internal Server Error (system error)

## 3. Database Design

### 3.1 Entity Relationship Diagram
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│     {Entity1}   │────▶│     {Entity2}   │────▶│     {Entity3}   │
│                 │ 1:N │                 │ N:M │                 │
│ - id (PK)       │     │ - id (PK)       │     │ - id (PK)       │
│ - field1        │     │ - entity1_id(FK)│     │ - field1        │
│ - field2        │     │ - field2        │     │ - field2        │
│ - created_at    │     │ - created_at    │     │ - created_at    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### 3.2 Database Schema

#### {Table Name 1}
```sql
CREATE TABLE {table_name} (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    field1 VARCHAR(255) NOT NULL,
    field2 INTEGER DEFAULT 0,
    field3 BOOLEAN DEFAULT FALSE,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT {constraint_name} CHECK (field2 >= 0),
    INDEX idx_{table_name}_field1 (field1),
    INDEX idx_{table_name}_status (status),
    INDEX idx_{table_name}_created_at (created_at)
);
```

#### {Table Name 2}
```sql
CREATE TABLE {table_name_2} (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    {table_name}_id UUID NOT NULL,
    field1 TEXT NOT NULL,
    field2 JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    FOREIGN KEY ({table_name}_id) REFERENCES {table_name}(id) ON DELETE CASCADE,
    INDEX idx_{table_name_2}_parent (({table_name}_id)),
    INDEX idx_{table_name_2}_field2 USING gin (field2)
);
```

### 3.3 Data Access Layer

#### Repository Pattern Implementation
```python
class {Entity}Repository:
    def __init__(self, db_session):
        self.db = db_session
    
    async def create(self, data: {Entity}Create) -> {Entity}:
        """Create a new {entity} record"""
        query = """
            INSERT INTO {table_name} (field1, field2, field3)
            VALUES ($1, $2, $3)
            RETURNING id, field1, field2, field3, created_at, updated_at
        """
        record = await self.db.fetchrow(
            query, data.field1, data.field2, data.field3
        )
        return {Entity}.from_record(record)
    
    async def get_by_id(self, entity_id: UUID) -> Optional[{Entity}]:
        """Retrieve {entity} by ID"""
        query = """
            SELECT id, field1, field2, field3, created_at, updated_at
            FROM {table_name}
            WHERE id = $1 AND status = 'active'
        """
        record = await self.db.fetchrow(query, entity_id)
        return {Entity}.from_record(record) if record else None
    
    async def list_with_pagination(
        self, page: int = 1, limit: int = 20, filters: dict = None
    ) -> Tuple[List[{Entity}], int]:
        """List {entities} with pagination"""
        offset = (page - 1) * limit
        where_clause, params = self._build_where_clause(filters)
        
        # Count query
        count_query = f"SELECT COUNT(*) FROM {table_name} {where_clause}"
        total = await self.db.fetchval(count_query, *params)
        
        # Data query
        data_query = f"""
            SELECT id, field1, field2, field3, created_at, updated_at
            FROM {table_name}
            {where_clause}
            ORDER BY created_at DESC
            LIMIT $1 OFFSET $2
        """
        records = await self.db.fetch(data_query, *params, limit, offset)
        entities = [{Entity}.from_record(r) for r in records]
        
        return entities, total
```

## 4. Business Logic Layer

### 4.1 Service Classes
```python
class {Entity}Service:
    def __init__(self, repository: {Entity}Repository):
        self.repository = repository
    
    async def create_{entity}(self, data: {Entity}Create) -> {Entity}:
        """Create new {entity} with business validation"""
        # Business validation
        await self._validate_business_rules(data)
        
        # Create entity
        entity = await self.repository.create(data)
        
        # Trigger events
        await self._publish_event("{entity}_created", entity)
        
        return entity
    
    async def update_{entity}(
        self, entity_id: UUID, data: {Entity}Update
    ) -> {Entity}:
        """Update existing {entity}"""
        # Check if entity exists
        existing = await self.repository.get_by_id(entity_id)
        if not existing:
            raise EntityNotFoundError(f"{Entity} {entity_id} not found")
        
        # Business validation
        await self._validate_update_rules(existing, data)
        
        # Update entity
        updated = await self.repository.update(entity_id, data)
        
        # Trigger events
        await self._publish_event("{entity}_updated", updated)
        
        return updated
    
    async def _validate_business_rules(self, data: {Entity}Create):
        """Validate business rules"""
        if data.field1 and len(data.field1) < 3:
            raise ValidationError("Field1 must be at least 3 characters")
        
        if data.field2 and data.field2 < 0:
            raise ValidationError("Field2 must be non-negative")
```

### 4.2 Event Handling
```python
class EventPublisher:
    def __init__(self, message_broker):
        self.broker = message_broker
    
    async def publish(self, event_type: str, data: dict):
        """Publish domain event"""
        event = {
            "id": str(uuid4()),
            "type": event_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0"
        }
        await self.broker.publish(f"events.{event_type}", event)
```

## 5. Integration Design

### 5.1 External Service Integration
```python
class ExternalServiceClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={"Authorization": f"Bearer {api_key}"}
        )
    
    async def call_external_api(self, endpoint: str, data: dict) -> dict:
        """Make API call with retry and error handling"""
        url = f"{self.base_url}/{endpoint}"
        
        for attempt in range(3):  # Retry up to 3 times
            try:
                async with self.session.post(url, json=data) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 429:  # Rate limited
                        await asyncio.sleep(2 ** attempt)
                        continue
                    else:
                        response.raise_for_status()
            except aiohttp.ClientError as e:
                if attempt == 2:  # Last attempt
                    raise ExternalServiceError(f"API call failed: {e}")
                await asyncio.sleep(1)
```

### 5.2 Message Queue Integration
```python
class MessageHandler:
    def __init__(self, service: {Entity}Service):
        self.service = service
    
    async def handle_{entity}_event(self, message: dict):
        """Handle incoming {entity} event"""
        try:
            event_data = message['data']
            
            if message['type'] == '{entity}_sync_requested':
                await self.service.sync_from_external(event_data['id'])
            elif message['type'] == '{entity}_validation_needed':
                await self.service.validate_and_update(event_data)
                
        except Exception as e:
            # Log error and potentially send to dead letter queue
            logger.error(f"Failed to handle message: {e}")
            raise
```

## 6. Error Handling & Logging

### 6.1 Exception Hierarchy
```python
class ApplicationError(Exception):
    """Base application exception"""
    pass

class ValidationError(ApplicationError):
    """Data validation error"""
    pass

class EntityNotFoundError(ApplicationError):
    """Entity not found error"""
    pass

class BusinessRuleViolationError(ApplicationError):
    """Business rule violation"""
    pass

class ExternalServiceError(ApplicationError):
    """External service integration error"""
    pass
```

### 6.2 Logging Strategy
```python
import structlog

logger = structlog.get_logger()

class {Entity}Service:
    async def create_{entity}(self, data: {Entity}Create) -> {Entity}:
        logger.info(
            "{entity}_creation_started",
            field1=data.field1,
            user_id=self.current_user_id
        )
        
        try:
            entity = await self.repository.create(data)
            logger.info(
                "{entity}_created",
                entity_id=entity.id,
                field1=entity.field1
            )
            return entity
        except Exception as e:
            logger.error(
                "{entity}_creation_failed",
                error=str(e),
                field1=data.field1
            )
            raise
```

## 7. Performance Optimization

### 7.1 Caching Strategy
```python
class CachedService:
    def __init__(self, repository: {Entity}Repository, cache: Redis):
        self.repository = repository
        self.cache = cache
    
    async def get_{entity}_cached(self, entity_id: UUID) -> Optional[{Entity}]:
        """Get entity with caching"""
        cache_key = f"{entity}:{entity_id}"
        
        # Try cache first
        cached_data = await self.cache.get(cache_key)
        if cached_data:
            return {Entity}.parse_raw(cached_data)
        
        # Fallback to database
        entity = await self.repository.get_by_id(entity_id)
        if entity:
            await self.cache.setex(
                cache_key, 
                3600,  # 1 hour TTL
                entity.json()
            )
        
        return entity
```

### 7.2 Database Query Optimization
- Use appropriate indexes for frequently queried fields
- Implement connection pooling with optimal pool size
- Use prepared statements for repeated queries
- Implement read replicas for read-heavy operations
- Use database-level pagination for large result sets

## 8. Testing Strategy

### 8.1 Unit Tests
```python
class Test{Entity}Service:
    @pytest.fixture
    async def service(self):
        repository = Mock{Entity}Repository()
        return {Entity}Service(repository)
    
    async def test_create_{entity}_success(self, service):
        # Arrange
        data = {Entity}Create(field1="test", field2=123)
        expected = {Entity}(id=uuid4(), **data.dict())
        service.repository.create.return_value = expected
        
        # Act
        result = await service.create_{entity}(data)
        
        # Assert
        assert result == expected
        service.repository.create.assert_called_once_with(data)
```

### 8.2 Integration Tests
- Test API endpoints with real database
- Test external service integrations with mocked services
- Test message queue handling with test queues
- Test error scenarios and edge cases
```

## GENERATION RULES
1. Include complete API specifications with request/response examples
2. Design normalized database schema with proper constraints
3. Implement repository pattern for data access
4. Include comprehensive error handling with custom exceptions
5. Add caching strategy for performance optimization
6. Include event-driven architecture patterns
7. Provide concrete code examples in Python/chosen language
8. Include testing strategy with unit and integration tests
9. Address security considerations in implementation
10. No placeholders - all code examples must be complete and runnable

Generate the complete low-level design following this template, creating specific, implementable code based on the project context provided.

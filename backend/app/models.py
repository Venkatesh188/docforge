import enum

class ProjectStatus(str, enum.Enum):
    CREATED = "created"
    CONCEPT_EXPANSION = "concept_expansion"
    IN_PROGRESS = "in_progress"
    REVIEW_PENDING = "review_pending"
    COMPLETED = "completed"
    FAILED = "failed"

class DocumentType(str, enum.Enum):
    CONCEPT_EXPANSION = "concept_expansion"
    PROJECT_CHARTER = "project_charter"
    SRS = "srs"
    ARCHITECTURE = "architecture"
    LOW_LEVEL_DESIGN = "low_level_design"
    TEST_SPECIFICATION = "test_specification"
    DEPLOYMENT_GUIDE = "deployment_guide"
    OPERATIONS_MANUAL = "operations_manual"
    BUSINESS_CASE = "business_case"
    MARKET_REQUIREMENTS = "market_requirements"
    VISION_BRIEF = "vision_brief"

class DocumentStatus(str, enum.Enum):
    PENDING = "pending"
    GENERATING = "generating"
    GENERATED = "generated"
    REVIEW_PENDING = "review_pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published" 
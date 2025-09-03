import openai
from typing import Optional, Dict, Any
import tiktoken
from langchain_openai import ChatOpenAI
from ..core.simple_config import settings

class OpenAIService:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenAI service with optional user-specific API key"""
        self.api_key = api_key or settings.openai_api_key
        self.model = settings.openai_model
        self.tokenizer = tiktoken.encoding_for_model(self.model)
        
        # Initialize client with the provided API key
        if self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def get_llm(self):
        """Get LLM instance for CrewAI agents"""
        if not self.api_key:
            raise ValueError("OpenAI API key is required for LLM operations")
            
        return ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            temperature=0.7,
            max_tokens=4000
        )
    
    def is_configured(self) -> bool:
        """Check if OpenAI API key is configured"""
        return bool(self.api_key)
    
    async def validate_api_key(self, api_key: str) -> Dict[str, Any]:
        """Validate an OpenAI API key"""
        try:
            # Basic format validation first
            if not api_key or not api_key.startswith('sk-'):
                return {
                    "valid": False,
                    "message": "API key must start with 'sk-'"
                }
            
            # Use a minimal, free metadata call to validate credentials
            test_client = openai.OpenAI(api_key=api_key)

            # Listing models is a lightweight way to validate auth without incurring usage
            # Some accounts may not have access to all models; we only care that the call authenticates.
            try:
                _ = test_client.models.list(timeout=10)
            except Exception as inner:
                # If the inner exception is not auth-related, re-raise to outer handlers
                raise inner
            
            return {
                "valid": True,
                "message": "API key is valid"
            }
            
        except openai.AuthenticationError:
            return {
                "valid": False,
                "message": "Invalid API key - Authentication failed"
            }
        except openai.RateLimitError:
            return {
                "valid": False,
                "message": "API key is valid but rate limit exceeded"
            }
        except openai.APITimeoutError:
            return {
                "valid": False,
                "message": "API key validation timed out - network issue"
            }
        except openai.APIConnectionError:
            return {
                "valid": False,
                "message": "Cannot connect to OpenAI API - network issue"
            }
        except Exception as e:
            return {
                "valid": False,
                "message": f"Validation error: {str(e)}"
            }
    
    async def generate_completion(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        max_tokens: int = 4000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Generate completion using OpenAI API"""
        if not self.client:
            return {
                "content": "",
                "tokens_used": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "success": False,
                "error": "OpenAI API key not configured"
            }
            
        try:
            messages = []
            
            if system_message:
                messages.append({"role": "system", "content": system_message})
            
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return {
                "content": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens,
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "success": True
            }
            
        except Exception as e:
            return {
                "content": "",
                "tokens_used": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "success": False,
                "error": str(e)
            }
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        try:
            return len(self.tokenizer.encode(text))
        except Exception:
            # Fallback estimation
            return len(text) // 4
    
    def truncate_to_token_limit(self, text: str, max_tokens: int) -> str:
        """Truncate text to fit within token limit"""
        try:
            tokens = self.tokenizer.encode(text)
            if len(tokens) <= max_tokens:
                return text
            
            truncated_tokens = tokens[:max_tokens]
            return self.tokenizer.decode(truncated_tokens)
        except Exception:
            # Fallback: truncate by character count
            estimated_chars = max_tokens * 4
            return text[:estimated_chars] 
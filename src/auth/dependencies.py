from fastapi import Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from fastapi.exceptions import HTTPException

class TokenBearer(HTTPBearer):
    
    def __init__(self, auto_error = True):
        super().__init__(auto_error = auto_error)
        
    async def __call__(self, request: Request) -> dict:
        
        creds = await super().__call__(request)
        token = creds.credentials
        
        
        token_data = decode_token(token)
        
        
        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid or expired token"
            )
            
        self.verify_token_data(token_data)
        
        return token_data
    
    def token_valid(self,token:str) -> bool:
        token_data = decode_token(token)
        
        return True if token_data is not None else False
    
    def verify_token_data(self, token_data):
        raise NotImplementedError('Please Override this method in child classes')
    
class AccessTokenBearer(TokenBearer):
    
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data.get('refresh') is True:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Please provide an access token"
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data.get('refresh') is not True:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Please provide a refresh token"
            )
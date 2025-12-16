from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import Request, status
from fastapi.exceptions import HTTPException
from .utils import decode_token

class TokenBearer(HTTPBearer):
    async def __call__(self, request: Request) -> dict:
        creds: HTTPAuthorizationCredentials = await super().__call__(request)

        if not creds:
            raise HTTPException(status_code=403, detail="Token missing")

        token = creds.credentials
        token_data = decode_token(token)

        if not self.token_valid(token):
            raise HTTPException(status_code=403, detail="Invalid or expired token")

        self.verify_token_data(token_data)
        return token_data

    def token_valid(self, token: str) -> bool:
        return decode_token(token) is not None

    def verify_token_data(self, token_data: dict):
        raise NotImplementedError("Override in child class")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict):
        if token_data.get("refresh"):
            raise HTTPException(403, "Please provide access token")


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict):
        if not token_data.get("refresh"):
            raise HTTPException(403, "Please provide refresh token")

from fastapi import HTTPException
from simplepam import authenticate


def isAuthenticated(username: str, password: str) -> bool:

  if authenticate(username=username, password=password):
    return True

  raise HTTPException(status_code=401, detail={"error": username, "reason": "authentication failure"})


# def isAuthenticated(username: str, password: str):  # BYPASS AUTH FOR DEV AND TESTING: PAM ERRORS WILL FAIL TESTS
#   return True

from fastapi import HTTPException


def isAuthenticated(isTrue: bool):

  def testAuth(username: str, password: str):

    if isTrue:

      return True

    raise HTTPException(status_code=401, detail={"error": username, "reason": "authentication failure"})

  return testAuth

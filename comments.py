from fastapi import FastAPI, Body, status, HTTPException

app = FastAPI(title="Comments app")
comments_db = {0: "First comment in FastAPI"}


@app.get("/comments", status_code=status.HTTP_200_OK)
async def comments() -> dict[int, str]:
    return comments_db


@app.get("/comments/{comment_id}")
async def get_comment(comment_id: int) -> str:
    if comment_id not in comments_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comments_db[comment_id]


@app.post("/comments", status_code=status.HTTP_201_CREATED)
async def create_comment(comment: str = Body(...)) -> str:
    current_index = max(comments_db) + 1 if comments_db else 0
    comments_db[current_index] = comment
    return "Commend created"


@app.put("/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def update_comment(comment_id: int, comment: str = Body(...)) -> str:
    if comment_id not in comments_db:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Comment not found")
    comments_db[comment_id] = comment
    return "Commend updated!"


@app.delete("/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment(comment_id: int) -> str:
    if comment_id not in comments_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    comments_db.pop(comment_id)
    return "Comment deleted!"

# print(__file__)
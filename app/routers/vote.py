from fastapi import APIRouter, Response, status, HTTPException, Depends
from .. import schemas,database,models,oauth2
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/",status_code = status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.id_post).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with id. {vote.id_post} was not found")
    
    vote_query = db.query(models.Vote).filter(models.Vote.id_post == vote.id_post, models.Vote.id_user == current_user.id)
    vote_found = vote_query.first()
        
    if vote.dir == 1:
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"The user {current_user.id} has already voted on the post {vote.id_post}")
        
        new_vote = models.Vote(id_post = vote.id_post, id_user = current_user.id)
        db.add(new_vote)
        db.commit()
        
        return {"message":"Successfully added vote"}
    
    else:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The vote is not found")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        
        return {"message": "Successfully deleted vote"}
        
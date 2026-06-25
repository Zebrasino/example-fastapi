from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database, models, oauth2, schemas

router = APIRouter(prefix="/retweet", tags=["Retweet"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def retweet(
    retweet: schemas.Retweet,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == retweet.id_post).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id: {retweet.id_post} was not found",
        )

    retweet_query = db.query(models.Retweet).filter(
        models.Retweet.id_post == retweet.id_post,
        models.Retweet.id_user == current_user.id,
    )
    retweet_found = retweet_query.first()

    if retweet.dir == 1:
        if retweet_found:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"The user {current_user.id} has already retweeted post {retweet.id_post}",
            )

        new_retweet = models.Retweet(id_post=retweet.id_post, id_user=current_user.id)
        db.add(new_retweet)
        db.commit()

        return {"message": "Successfully added retweet"}

    if not retweet_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The retweet was not found",
        )

    retweet_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Successfully removed retweet"}

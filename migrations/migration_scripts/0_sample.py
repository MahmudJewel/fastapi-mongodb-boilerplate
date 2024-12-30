import logging
from enum import Enum

# Enum for UserCreationMethod
class UserCreationMethod(str, Enum):
    SYSTEM = "system"
    GOOGLE = "google"

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def upgrade(db):
    updated_count = 0
    not_updated_count = 0

    # Default value for the new field
    default_creation_method = UserCreationMethod.SYSTEM.value

    # Fetch all users in FAPIUser collection using async for
    async for user in db.users.find({}):  # Use async for here
        if "creation_method" not in user:
            # Update the user with the default value for `creation_method`
            await db.users.update_one(
                {"_id": user["_id"]},
                {"$set": {"creation_method": default_creation_method}}
            )
            updated_count += 1
            logger.info(
                f"Updated creation_method for user {user['_id']} to {default_creation_method}"
            )
        else:
            not_updated_count += 1

    # Log the results
    logger.info(
        f"=====> User update completed.\n=====> Total documents updated: {updated_count}\n=====> Total documents not updated: {not_updated_count}"
    )

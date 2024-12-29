import argparse
import importlib
import os
import sys
import logging
from datetime import datetime, timezone
import asyncio

from motor.motor_asyncio import AsyncIOMotorClient
from env import MONGODB_URL, ClUSTER_NAME

# Set up logging
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_directory, 'migration.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add a stream handler to also log to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)

# Adding the parent directory of the migrations folder to sys.path
migration_scripts_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(migration_scripts_path)
logger.info(f"Sys.path updated with: {migration_scripts_path}")


def get_db_client():
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        database = client.get_database(ClUSTER_NAME)
        
        return database

    except Exception as e:
        logger.error(f"Failed to connect to database: {str(e)}")
        raise

async def is_migration_applied(db, script_name):
    try:
        migration = await db.migrations.find_one({'script': script_name, 'applied': True})
        return migration is not None
    except Exception as e:
        logger.error(f"Error checking migration status for {script_name}: {str(e)}")
        raise

async def apply_migration(db, script_name):
    try:
        if await is_migration_applied(db, script_name):
            logger.info(f"Migration {script_name} has already been applied. Skipping.")
            return

        module_path = f"migrations.migration_scripts.{script_name}"
        module = importlib.import_module(module_path)

        start_time = datetime.now(timezone.utc)
        await module.upgrade(db)  # Ensure `upgrade` is asynchronous
        end_time = datetime.now(timezone.utc)

        await db.migrations.update_one(
            {'script': script_name},
            {'$set': {
                'applied': True,
                'applied_at': end_time,
                'duration': (end_time - start_time).total_seconds()
            }},
            upsert=True
        )
        logger.info(f"Successfully applied migration {script_name} in {end_time - start_time}")
    except Exception as e:
        logger.error(f"Error applying migration {script_name}: {str(e)}")
        raise

async def revert_migration(db, script_name):
    try:
        if not await is_migration_applied(db, script_name):
            logger.info(f"Migration {script_name} has not been applied. Cannot revert.")
            return

        module_path = f"migrations.migration_scripts.{script_name}"
        module = importlib.import_module(module_path)

        start_time = datetime.now(timezone.utc)
        await module.downgrade(db)  # Ensure `downgrade` is asynchronous
        end_time = datetime.now(timezone.utc)

        await db.migrations.update_one(
            {'script': script_name},
            {'$set': {
                'applied': False,
                'reverted_at': end_time,
                'revert_duration': (end_time - start_time).total_seconds()
            }}
        )
        logger.info(f"Successfully reverted migration {script_name} in {end_time - start_time}")
    except Exception as e:
        logger.error(f"Error reverting migration {script_name}: {str(e)}")
        raise

def get_migration_files():
    migration_dir = os.path.join(
        migration_scripts_path, 'migrations', 'migration_scripts')
    files = [f[:-3] for f in os.listdir(migration_dir) if f.endswith('.py')]
    # logger.info(f"file list =====> {files}")
    return sorted(files)

async def main():
    parser = argparse.ArgumentParser(description="Run database migrations.")
    parser.add_argument('script_name', nargs='?', help="The name of the migration script to run")
    parser.add_argument('--revert', action='store_true', help="Revert the specified migration instead of applying it")
    parser.add_argument('--all', action='store_true', help="Apply all pending migrations")
    args = parser.parse_args()

    try:
        db = get_db_client()
        # logger.info(f"Connected to MongoDB ==========> {db}")
        if args.all:
            logger.info("Applying all pending migrations")
            for script_name in get_migration_files():
                if not await is_migration_applied(db, script_name):
                    await apply_migration(db, script_name)
        elif args.script_name:
            if args.revert:
                logger.info(f"Reverting migration: {args.script_name}")
                await revert_migration(db, args.script_name)
            else:
                logger.info(f"Applying migration: {args.script_name}")
                await apply_migration(db, args.script_name)
        else:
            parser.print_help()
    except Exception as e:
        logger.error(f"Migration process failed: {str(e)}")
        sys.exit(1)

    logger.info("Migration process completed")

if __name__ == "__main__":
    asyncio.run(main())

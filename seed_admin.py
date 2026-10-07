"""
SKINALYTIX — One-time script to create the first admin account.

Run this from the root of your skinalytix_backend folder (same place
as seed_products.py), with your venv activated:

    python seed_admin.py

Change ADMIN_USERNAME / ADMIN_PASSWORD below before running, or just
run it with the defaults and change the password later via pgAdmin
(update password_hash with a fresh bcrypt hash) if you forget it.
"""

from passlib.context import CryptContext
from app.database import SessionLocal
from app.models import AdminUser

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "SkinalytixAdmin123"  # change this before running


def seed():
    db = SessionLocal()
    try:
        existing = db.query(AdminUser).filter(AdminUser.username == ADMIN_USERNAME).first()
        if existing:
            print("Admin account already exists — nothing to do.")
            return

        admin = AdminUser(
            username=ADMIN_USERNAME,
            password_hash=pwd_context.hash(ADMIN_PASSWORD),
            role="admin",
        )
        db.add(admin)
        db.commit()
        print(f"✅ Admin account created — username: '{ADMIN_USERNAME}'")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
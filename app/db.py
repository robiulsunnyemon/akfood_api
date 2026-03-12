from prisma import Prisma

db = Prisma()

def get_db():
    return db


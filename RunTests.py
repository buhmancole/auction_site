import os
from subprocess import run
migrationFolderPath = "./alphaAuction/auction/migrations"
managePath = './alphaAuction/manage.py'
dbPath = './alphaAuction/db.sqlite3'
imagesFolderPath = "./alphaAuction/media"


def deleteFiles(dirObject , dirPath):
    if dirObject.is_dir(follow_symlinks=False):
        name = os.fsdecode(dirObject.name)
        newDir = dirPath+"/"+name
        moreFiles = os.scandir(newDir)
        for file in moreFiles:
            if file.is_dir(follow_symlinks=False):
                deleteFiles(file, newDir)
                os.rmdir(newDir+"/"+os.fsdecode(file.name))
            else:
                os.remove(newDir+"/"+os.fsdecode(file.name))
        os.rmdir(newDir)
    else:
        os.remove(dirPath+"/"+os.fsdecode(dirObject.name))

def startDeletingMigrations(directory):
    try:
        files = os.scandir(directory)
        for file in files:
            deleteFiles(file, directory)
        os.rmdir(directory)
    except:
        print("migrations folder was already deleted")

def clearImages(imagesDir):
    if os.path.exists(imagesDir):
        for file in os.scandir(imagesDir):
            deleteFiles(file, imagesDir)
    else:
        os.makedirs(imagesDir)

def deleteDatabase():
    if os.path.exists(dbPath):
        os.remove(dbPath)
    else:
        print('you do not have a database that needs deleting')

def makeMigrations():
    run(["python", managePath, "makemigrations"])

def migrate():
    run(["python", managePath, "migrate"])

def runTests():
    run(["python", managePath, "test", "auction"])

def syncDatabase():
    run(["python", managePath, "migrate", "--run-syncdb"])

def init():
    run(["python", managePath, "init", "3", "16"])

def main():
    startDeletingMigrations(migrationFolderPath)
    deleteDatabase()
    makeMigrations()
    migrate()
    syncDatabase()
    clearImages(imagesFolderPath)
    runTests()
    init()

main()






import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        
        MIGRATION_FILES_PATH = "HR/migrations"
        SQL_SCRIPTS_FILES_PATH = "HR/SQLScripts" 

        if not os.path.exists(MIGRATION_FILES_PATH):
            self.stdout.write(self.style.WARNING("MIGRATION_FILES_PATH is wrong"))
            
        if not os.path.exists(SQL_SCRIPTS_FILES_PATH):
            self.stdout.write(self.style.WARNING("SQL_SCRIPTS_FILES_PATH is wrong"))

        for filename in os.listdir(SQL_SCRIPTS_FILES_PATH):
            file_path = os.path.join(SQL_SCRIPTS_FILES_PATH, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                self.stdout.write(self.style.SUCCESS(f"{filename.rjust(100, " ")}          ..REMOVED"))
        
        for filename in os.listdir(MIGRATION_FILES_PATH):
            file_path = os.path.join(MIGRATION_FILES_PATH, filename)
            if os.path.isfile(file_path) and "_GIS_SCRIPT" in filename:
                os.remove(file_path)
                self.stdout.write(self.style.SUCCESS(f"{filename.rjust(100, " ")}          ..REMOVED"))

    
        
        



                

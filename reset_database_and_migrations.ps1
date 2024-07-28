# Save this as reset_database_and_migrations.ps1

# Function to run PostgreSQL commands
function Run-PostgresCommand {
    param([string]$command)
    wsl sudo -u postgres psql -c "$command"
}

# Drop and recreate the database
Write-Host "Dropping and recreating the database..."
Run-PostgresCommand "DROP DATABASE IF EXISTS beetogther_db;"
Run-PostgresCommand "CREATE DATABASE beetogther_db;"

# Remove all migration files except __init__.py
Write-Host "Removing migration files..."
Get-ChildItem -Recurse -Filter migrations |
    Get-ChildItem -Filter *.py |
    Where-Object { $_.Name -ne "__init__.py" } |
    Remove-Item

# Recreate initial migrations
Write-Host "Creating new initial migrations..."
python manage.py makemigrations

# Apply new migrations
Write-Host "Applying new migrations..."
python manage.py migrate

Write-Host "Reset process completed!"